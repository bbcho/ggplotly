# stats/stat_contour.py
"""
2D density estimation and grid interpolation stat for contour plots.

This stat supports two modes of operation:

1. **2D Kernel Density Estimation (KDE)**
   When only x and y aesthetics are provided, computes 2D probability density.
   Uses scipy.stats.gaussian_kde for the computation.

   Example:
       ggplot(df, aes(x='x', y='y')) + geom_contour()

2. **Grid Interpolation from z values**
   When x, y, and z aesthetics are provided, interpolates z values to a
   regular grid for contour plotting.

   Example:
       ggplot(df, aes(x='x', y='y', z='elevation')) + geom_contour()

The stat outputs:
- x: 1D array of grid x coordinates
- y: 1D array of grid y coordinates
- z: 2D array of density/interpolated values
- density: Alias for z (for compatibility)

These outputs are used by geom_contour and geom_contour_filled to render
contour lines or filled contours.
"""

import numpy as np
from scipy.interpolate import griddata
from scipy.stats import gaussian_kde

from .stat_base import Stat


class stat_contour(Stat):
    """
    Compute 2D density or interpolate gridded data for contour plots.

    This stat performs either 2D kernel density estimation (when only x, y
    are provided) or interpolation of irregular z data to a regular grid
    (when x, y, z are provided).

    Attributes:
        gridsize (int): Resolution of the output grid (number of points per axis)
        bw_method: Bandwidth method for KDE ('scott', 'silverman', or scalar)
        na_rm (bool): Whether to remove NA values before computation

    Computed Variables:
        x: Grid x coordinates (1D array of length gridsize)
        y: Grid y coordinates (1D array of length gridsize)
        z: 2D density/interpolated values (2D array of shape gridsize x gridsize)
        density: Alias for z

    Examples:
        >>> # 2D density estimation from scatter points
        >>> ggplot(df, aes(x='x', y='y')) + geom_contour()

        >>> # Contours from explicit z values (e.g., elevation data)
        >>> ggplot(df, aes(x='lon', y='lat', z='elevation')) + geom_contour()

        >>> # With custom grid resolution and bandwidth
        >>> stat = stat_contour(gridsize=50, bw_method='silverman')
    """

    # Name identifier for this stat (used in error messages, etc.)
    __name__ = "contour"

    def __init__(self, data=None, mapping=None, gridsize=100, bw_method=None,
                 na_rm=False, **params):
        """
        Initialize the contour stat.

        Parameters:
            data (DataFrame, optional): Data to use for this stat.
                If None, data will be provided by the geom or plot.

            mapping (dict, optional): Aesthetic mappings.
                Required: 'x', 'y'
                Optional: 'z' (if provided, interpolates instead of computing KDE)

            gridsize (int): Resolution of the output grid.
                Higher values give smoother contours but take longer to compute.
                Default is 100 (produces 100x100 grid = 10,000 points).

            bw_method (str or float, optional): Bandwidth method for KDE.
                - 'scott': Scott's rule of thumb (default if None)
                - 'silverman': Silverman's rule of thumb
                - float: Manual bandwidth factor
                Only used when computing KDE (when z is not provided).

            na_rm (bool): If True, remove NA values before computation.
                Default is False (NA values will cause errors).

            **params: Additional parameters passed to the Stat base class.
        """
        super().__init__(data, mapping, **params)

        # Grid resolution - number of points along each axis
        # Total grid size is gridsize x gridsize
        self.gridsize = gridsize

        # Bandwidth method for KDE
        # Only used when z is not provided (2D density mode)
        self.bw_method = bw_method

        # Whether to remove NA values before computation
        self.na_rm = na_rm

    def compute(self, data):
        """
        Compute 2D density or interpolate z values to a grid.

        This is the main computation method. It:
        1. Extracts x, y (and optionally z) from the data
        2. Optionally removes NA values
        3. Calls either _compute_kde or _compute_from_z
        4. Returns the grid data and updated mapping

        Parameters:
            data (DataFrame): Data containing the columns specified in mapping.
                Must have x and y columns. May optionally have z column.

        Returns:
            tuple: (result_dict, new_mapping)
                - result_dict: Contains 'x', 'y', 'z', 'density' arrays
                - new_mapping: Updated mapping pointing to result columns

        Raises:
            ValueError: If x or y aesthetics are not specified in mapping.
        """
        # Get column names from mapping
        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')
        z_col = self.mapping.get('z')

        # Validate required aesthetics
        if x_col is None or y_col is None:
            raise ValueError("stat_contour requires both 'x' and 'y' aesthetics")

        # Extract data arrays (copy to avoid modifying original)
        x = data[x_col].values.copy()
        y = data[y_col].values.copy()

        # Handle NA values
        if self.na_rm:
            # Create mask for valid (non-NA) values
            mask = ~(np.isnan(x) | np.isnan(y))
            x = x[mask]
            y = y[mask]
            # Also filter z if provided
            if z_col and z_col in data.columns:
                z = data[z_col].values.copy()[mask]
            else:
                z = None
        else:
            # Get z values if provided (without NA filtering)
            z = data[z_col].values.copy() if z_col and z_col in data.columns else None

        # Handle empty data case
        if len(x) == 0 or len(y) == 0:
            # Return empty arrays with correct structure
            result = {
                'x': np.array([]),
                'y': np.array([]),
                'z': np.array([[]]),
                'density': np.array([[]]),
            }
            return result, self.mapping.copy()

        # Choose computation method based on whether z is provided
        if z is not None:
            # z values provided - interpolate to grid
            x_grid, y_grid, z_grid = self._compute_from_z(x, y, z)
        else:
            # No z values - compute 2D KDE
            x_grid, y_grid, z_grid = self._compute_kde(x, y)

        # Package results
        result = {
            'x': x_grid,      # 1D array of grid x coordinates
            'y': y_grid,      # 1D array of grid y coordinates
            'z': z_grid,      # 2D array of computed values
            'density': z_grid,  # Alias for compatibility
        }

        # Update mapping to point to result column names
        new_mapping = self.mapping.copy()
        new_mapping['x'] = 'x'
        new_mapping['y'] = 'y'
        new_mapping['z'] = 'z'

        return result, new_mapping

    def _compute_kde(self, x, y):
        """
        Compute 2D kernel density estimation.

        Uses scipy.stats.gaussian_kde to estimate the probability density
        function of the 2D data. The result is evaluated on a regular grid.

        Parameters:
            x (ndarray): 1D array of x values (data points).
            y (ndarray): 1D array of y values (data points).

        Returns:
            tuple: (x_grid, y_grid, z_grid)
                - x_grid: 1D array of grid x coordinates
                - y_grid: 1D array of grid y coordinates
                - z_grid: 2D array of density values

        Note:
            If the data points are too clustered (singular covariance matrix),
            returns a grid of zeros to avoid errors.
        """
        # Create 1D grid coordinates spanning the data range
        x_grid = np.linspace(x.min(), x.max(), self.gridsize)
        y_grid = np.linspace(y.min(), y.max(), self.gridsize)

        # Create 2D mesh grid for evaluation
        X, Y = np.meshgrid(x_grid, y_grid)

        # Flatten mesh to get evaluation positions
        # Shape: (2, gridsize*gridsize)
        positions = np.vstack([X.ravel(), Y.ravel()])

        # Compute KDE
        try:
            # Stack x and y as 2D data for KDE
            # Shape: (2, n_points)
            if self.bw_method is not None:
                kernel = gaussian_kde(np.vstack([x, y]), bw_method=self.bw_method)
            else:
                kernel = gaussian_kde(np.vstack([x, y]))

            # Evaluate KDE at all grid positions
            # Result shape: (gridsize*gridsize,) -> reshape to (gridsize, gridsize)
            z_grid = kernel(positions).reshape(X.shape)

        except np.linalg.LinAlgError:
            # Singular covariance matrix - data points are too clustered
            # or collinear. Return zeros to avoid crashing.
            z_grid = np.zeros(X.shape)

        return x_grid, y_grid, z_grid

    def _compute_from_z(self, x, y, z):
        """
        Compute grid from provided z values.

        Handles two cases:
        1. Data is already on a regular grid - reshape it
        2. Data is irregular - interpolate to a regular grid

        Parameters:
            x (ndarray): 1D array of x coordinates.
            y (ndarray): 1D array of y coordinates.
            z (ndarray): 1D array of z values at each (x, y) point.

        Returns:
            tuple: (x_grid, y_grid, z_grid)
                - x_grid: 1D array of grid x coordinates
                - y_grid: 1D array of grid y coordinates
                - z_grid: 2D array of z values on the grid
        """
        # Find unique x and y values
        x_unique = np.unique(x)
        y_unique = np.unique(y)

        # Check if data is already gridded
        # (number of points equals product of unique x and y values)
        if len(x_unique) * len(y_unique) == len(z):
            # Data is on a regular grid - just reshape it

            # Sort by y then x to ensure correct ordering
            sort_idx = np.lexsort((x, y))
            z_sorted = z[sort_idx]

            # Reshape to 2D grid
            z_grid = z_sorted.reshape(len(y_unique), len(x_unique))
            x_grid = x_unique
            y_grid = y_unique

        else:
            # Irregular data - interpolate to regular grid

            # Create regular grid
            x_grid = np.linspace(x.min(), x.max(), self.gridsize)
            y_grid = np.linspace(y.min(), y.max(), self.gridsize)
            X, Y = np.meshgrid(x_grid, y_grid)

            # Interpolate z values to grid using scipy's griddata
            # Uses linear interpolation by default
            z_grid = griddata((x, y), z, (X, Y), method='linear')

        return x_grid, y_grid, z_grid

    def compute_grid(self, data, x_col='x', y_col='y', z_col=None):
        """
        Convenience method to compute grid directly from column names.

        This is a simpler interface when you want to call stat_contour
        directly without setting up mapping first.

        Parameters:
            data (DataFrame): Input data containing the specified columns.
            x_col (str): Name of x column. Default is 'x'.
            y_col (str): Name of y column. Default is 'y'.
            z_col (str, optional): Name of z column. If None, computes KDE.

        Returns:
            dict: Contains 'x', 'y', 'z' grid arrays.

        Example:
            >>> stat = stat_contour(gridsize=50)
            >>> grid = stat.compute_grid(df, x_col='longitude', y_col='latitude')
            >>> # grid['z'] contains the 2D KDE values
        """
        # Set up mapping from column names
        self.mapping = {'x': x_col, 'y': y_col}
        if z_col:
            self.mapping['z'] = z_col

        # Compute and return result (discard the new_mapping)
        result, _ = self.compute(data)
        return result
