# geoms/geom_contour.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import numpy as np
from scipy.stats import gaussian_kde


class geom_contour(Geom):
    """Geom for drawing contour lines from 2D data."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw contour lines from 2D data.

        Can be used in two ways:
        1. With x and y aesthetics: Computes 2D kernel density estimation
        2. With x, y, and z aesthetics: Draws contours from gridded z values

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x, y. Optional: z.
        bins : int, default=10
            Number of contour levels.
        color : str, optional
            Color of contour lines. Default uses theme colors.
        size : float, default=1
            Line width of contours.
        alpha : float, default=1
            Transparency (0-1).
        linetype : str, default='solid'
            Line style: 'solid', 'dash', 'dot'.
        gridsize : int, default=100
            Grid resolution for KDE computation.
        label : bool, default=False
            Whether to show contour labels.

        Examples
        --------
        >>> geom_contour()  # 2D density contours
        >>> geom_contour(bins=5, color='blue')
        """
        super().__init__(data, mapping, **params)
        self.bins = params.get('bins', 10)
        self.gridsize = params.get('gridsize', 100)

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if "size" not in self.params:
            self.params["size"] = 1

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        z_col = self.mapping.get("z")

        x = data[x_col].values if x_col and x_col in data.columns else None
        y = data[y_col].values if y_col and y_col in data.columns else None

        if x is None or y is None:
            raise ValueError("geom_contour requires both x and y aesthetics")

        alpha = style_props['alpha']
        color = style_props.get('color') or style_props['default_color']
        line_width = style_props['size']
        linetype = self.params.get('linetype', 'solid')

        # Check if z is provided (gridded data) or need to compute KDE
        if z_col and z_col in data.columns:
            # Use provided z values - assume data is in long format
            # Need to pivot to grid format
            z = data[z_col].values

            # Try to reshape if data appears to be gridded
            x_unique = np.unique(x)
            y_unique = np.unique(y)

            if len(x_unique) * len(y_unique) == len(z):
                # Data is gridded, reshape
                z_grid = z.reshape(len(y_unique), len(x_unique))
                x_grid = x_unique
                y_grid = y_unique
            else:
                # Irregular data, interpolate to grid
                from scipy.interpolate import griddata
                x_grid = np.linspace(x.min(), x.max(), self.gridsize)
                y_grid = np.linspace(y.min(), y.max(), self.gridsize)
                X, Y = np.meshgrid(x_grid, y_grid)
                z_grid = griddata((x, y), z, (X, Y), method='linear')
        else:
            # Compute 2D KDE
            x_grid = np.linspace(x.min(), x.max(), self.gridsize)
            y_grid = np.linspace(y.min(), y.max(), self.gridsize)
            X, Y = np.meshgrid(x_grid, y_grid)
            positions = np.vstack([X.ravel(), Y.ravel()])

            # Handle case where all points are identical or nearly so
            try:
                kernel = gaussian_kde(np.vstack([x, y]))
                z_grid = kernel(positions).reshape(X.shape)
            except np.linalg.LinAlgError:
                # Singular matrix - points are too clustered
                z_grid = np.zeros(X.shape)

        # Create contour trace
        fig.add_trace(
            go.Contour(
                x=x_grid,
                y=y_grid,
                z=z_grid,
                ncontours=self.bins,
                contours=dict(
                    coloring='lines',
                    showlabels=self.params.get('label', False),
                ),
                line=dict(
                    color=color,
                    width=line_width,
                    dash=linetype,
                ),
                opacity=alpha,
                showscale=self.params.get('showscale', False),
                name=self.params.get('name', 'Contour'),
                showlegend=self.params.get('showlegend', False),
            ),
            row=row,
            col=col,
        )
