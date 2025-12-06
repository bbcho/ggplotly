# geoms/geom_contour_filled.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import numpy as np
from scipy.stats import gaussian_kde


class geom_contour_filled(Geom):
    """Geom for drawing filled contours from 2D data."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw filled contours from 2D data.

        Can be used in two ways:
        1. With x and y aesthetics: Computes 2D kernel density estimation
        2. With x, y, and z aesthetics: Draws filled contours from gridded z values

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x, y. Optional: z.
        bins : int, default=10
            Number of contour levels.
        palette : str, default='Viridis'
            Color palette name. Options: 'Viridis', 'Plasma', 'Inferno',
            'Magma', 'Blues', 'Greens', 'Reds', etc.
        alpha : float, default=0.8
            Transparency (0-1).
        gridsize : int, default=100
            Grid resolution for KDE computation.
        label : bool, default=False
            Whether to show contour labels.
        show_colorbar : bool, default=True
            Whether to show the colorbar.

        Examples
        --------
        >>> geom_contour_filled()  # 2D density filled contours
        >>> geom_contour_filled(bins=15, palette='Plasma')
        """
        super().__init__(data, mapping, **params)
        self.bins = params.get('bins', 10)
        self.gridsize = params.get('gridsize', 100)
        self.palette = params.get('palette', 'Viridis')

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if "alpha" not in self.params:
            self.params["alpha"] = 0.8

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        z_col = self.mapping.get("z")

        x = data[x_col].values if x_col and x_col in data.columns else None
        y = data[y_col].values if y_col and y_col in data.columns else None

        if x is None or y is None:
            raise ValueError("geom_contour_filled requires both x and y aesthetics")

        alpha = style_props['alpha']

        # Check if z is provided (gridded data) or need to compute KDE
        if z_col and z_col in data.columns:
            # Use provided z values
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

        # Create filled contour trace
        fig.add_trace(
            go.Contour(
                x=x_grid,
                y=y_grid,
                z=z_grid,
                ncontours=self.bins,
                contours=dict(
                    coloring='heatmap',  # 'heatmap' gives smooth filled contours
                    showlabels=self.params.get('label', False),
                ),
                colorscale=self.palette,
                opacity=alpha,
                showscale=self.params.get('show_colorbar', True),
                name=self.params.get('name', 'Contour'),
                showlegend=self.params.get('showlegend', False),
                colorbar=dict(
                    title=self.params.get('colorbar_title', ''),
                ) if self.params.get('show_colorbar', True) else None,
            ),
            row=row,
            col=col,
        )
