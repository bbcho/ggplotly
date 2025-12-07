# geoms/geom_density.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import plotly.express as px
import pandas as pd


class geom_density(Geom):
    """
    Geom for drawing density plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        bw (str or float, optional): Bandwidth method or value. Options:
            - 'nrd0': Scott's rule (default, matches R's default)
            - 'nrd': Silverman's rule
            - 'scott': Scott's rule (alias for nrd0)
            - 'silverman': Silverman's rule (alias for nrd)
            - A numeric value for a fixed bandwidth
        adjust (float, optional): Bandwidth adjustment multiplier. Default is 1.
            Values > 1 produce smoother curves, < 1 produce more detail.
        kernel (str, optional): Kernel to use. Default is 'gaussian'.
            Note: scipy's gaussian_kde only supports gaussian kernel.
        n (int, optional): Number of evaluation points. Default is 512 to match R.
        trim (bool, optional): If True, trim density to range of data. Default is False.
        fill (str, optional): Fill color for the density plot.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        linetype (str, optional): Line style of the density plot ('solid', 'dash', etc.).
        group (str, optional): Grouping variable for the density plots.
        na_rm (bool, optional): If True, silently remove missing values. Default is False.

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_density()
        >>> ggplot(df, aes(x='value')) + geom_density(adjust=0.5)  # less smoothing
        >>> ggplot(df, aes(x='value')) + geom_density(bw=0.5)  # fixed bandwidth
        >>> ggplot(df, aes(x='value', fill='group')) + geom_density(alpha=0.3)
    """

    def __init__(self, data=None, mapping=None, bw='nrd0', adjust=1, kernel='gaussian',
                 n=512, trim=False, **params):
        """
        Initialize the density geom.

        Parameters:
            data (DataFrame, optional): Data for this geom.
            mapping (aes, optional): Aesthetic mappings.
            bw (str or float): Bandwidth method or fixed value. Default is 'nrd0'.
            adjust (float): Bandwidth adjustment multiplier. Default is 1.
            kernel (str): Kernel function (only 'gaussian' supported). Default is 'gaussian'.
            n (int): Number of evaluation points. Default is 512.
            trim (bool): Whether to trim density to data range. Default is False.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)
        self.bw = bw
        self.adjust = adjust
        self.kernel = kernel
        self.n = n
        self.trim = trim

    def _compute_bandwidth(self, x, bw, adjust):
        """Compute bandwidth using specified method."""
        n = len(x)
        std = np.std(x, ddof=1)
        iqr = np.percentile(x, 75) - np.percentile(x, 25)

        if isinstance(bw, (int, float)):
            return bw * adjust

        # Scott's rule (nrd0) - R's default
        if bw in ('nrd0', 'scott'):
            # R's bw.nrd0: 0.9 * min(sd, IQR/1.34) * n^(-1/5)
            bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)
        # Silverman's rule (nrd)
        elif bw in ('nrd', 'silverman'):
            # R's bw.nrd: 1.06 * min(sd, IQR/1.34) * n^(-1/5)
            bandwidth = 1.06 * min(std, iqr / 1.34) * n ** (-0.2)
        else:
            # Fall back to scipy's default (Scott's rule)
            bandwidth = std * n ** (-0.2)

        return bandwidth * adjust

    def _compute_density_for_group(self, x_data, na_rm=False):
        """
        Compute KDE for a single group of data.

        Parameters:
            x_data: Series or array of x values
            na_rm: Whether to remove NA values

        Returns:
            tuple: (x_grid, y_density) arrays
        """
        if na_rm:
            x_data = x_data.dropna()

        # Need at least 2 points for KDE
        if len(x_data) < 2:
            return None, None

        # Compute bandwidth
        bandwidth = self._compute_bandwidth(x_data, self.bw, self.adjust)

        # Handle edge case where std is 0
        std = np.std(x_data, ddof=1)
        if std == 0:
            return None, None

        # Create KDE with custom bandwidth
        kde = gaussian_kde(x_data, bw_method=bandwidth / std)

        # Generate evaluation points
        if self.trim:
            x_grid = np.linspace(x_data.min(), x_data.max(), self.n)
        else:
            # Extend beyond data range like R does (by 3 bandwidths)
            x_min = x_data.min() - 3 * bandwidth
            x_max = x_data.max() + 3 * bandwidth
            x_grid = np.linspace(x_min, x_max, self.n)

        y = kde(x_grid)
        return x_grid, y

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 2
        data = data if data is not None else self.data

        # Remove size from mapping if present - density lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        # Handle na_rm parameter
        na_rm = self.params.get("na_rm", False)

        # Determine grouping column from fill, color, or group mapping
        group_col = None
        for aesthetic in ['fill', 'color', 'group']:
            if aesthetic in self.mapping:
                potential_col = self.mapping[aesthetic]
                if potential_col in data.columns:
                    group_col = potential_col
                    break

        x_col = self.mapping["x"]

        # Compute densities - either grouped or ungrouped
        if group_col is not None:
            # Grouped density: compute separate KDE for each group
            density_frames = []
            for group_value in data[group_col].unique():
                group_data = data[data[group_col] == group_value]
                x_data = group_data[x_col]

                x_grid, y_density = self._compute_density_for_group(x_data, na_rm)

                if x_grid is not None:
                    group_df = pd.DataFrame({
                        x_col: x_grid,
                        'density': y_density,
                        group_col: group_value
                    })
                    density_frames.append(group_df)

            if density_frames:
                computed_data = pd.concat(density_frames, ignore_index=True)
            else:
                # No valid groups, fall back to empty
                computed_data = pd.DataFrame({x_col: [], 'density': [], group_col: []})
        else:
            # Ungrouped density: single KDE for all data
            x_data = data[x_col]
            x_grid, y_density = self._compute_density_for_group(x_data, na_rm)

            if x_grid is not None:
                computed_data = pd.DataFrame({x_col: x_grid, 'density': y_density})
            else:
                computed_data = pd.DataFrame({x_col: [], 'density': []})

        self.mapping["y"] = "density"

        # Handle Plotly's fill parameter (tonexty, tozeroy, etc.) separately from fill aesthetic
        fill_param = self.params.get("fill", None)
        plotly_fill = None
        if fill_param in ['tonexty', 'tozeroy', 'tonextx', 'tozerox', 'toself', 'tonext']:
            # This is a Plotly fill mode, not a color aesthetic
            plotly_fill = fill_param
            # Temporarily remove from params so AestheticMapper doesn't treat it as a fill aesthetic
            self.params.pop("fill", None)

        line_dash = self.params.get("linetype", "solid")
        name = self.params.get("name", "Density")

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=plotly_fill,
        )

        # Restore fill parameter if it was removed
        if plotly_fill is not None:
            self.params["fill"] = plotly_fill

        color_targets = dict(
            fill="fillcolor",
            color="line_color",
        )

        self._transform_fig(
            plot,
            fig,
            computed_data,
            payload,
            color_targets,
            row,
            col,
        )
