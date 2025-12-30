# geoms/geom_contour_filled.py

import plotly.graph_objects as go

from ..stats.stat_contour import stat_contour
from .geom_base import Geom


class geom_contour_filled(Geom):
    """Geom for drawing filled contours from 2D data."""

    required_aes = ['x', 'y']  # z is optional (computed from KDE if not provided)
    default_params = {"alpha": 0.8}

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

    def _compute_contour_grid(self, data):
        """
        Compute 2D grid using stat_contour.

        Parameters
        ----------
        data : DataFrame
            Data with x, y, and optionally z columns.

        Returns
        -------
        dict
            Contains x, y, z grid arrays.
        """
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        z_col = self.mapping.get("z")

        mapping = {'x': x_col, 'y': y_col}
        if z_col and z_col in data.columns:
            mapping['z'] = z_col

        contour_stat = stat_contour(
            mapping=mapping,
            gridsize=self.gridsize,
            na_rm=self.params.get('na_rm', False)
        )

        result, _ = contour_stat.compute(data)
        return result

    def _draw_impl(self, fig, data, row, col):
        style_props = self._get_style_props(data)

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")

        if not x_col or not y_col:
            raise ValueError("geom_contour_filled requires both x and y aesthetics")

        alpha = style_props['alpha']

        # Compute grid using stat_contour
        grid_data = self._compute_contour_grid(data)
        x_grid = grid_data['x']
        y_grid = grid_data['y']
        z_grid = grid_data['z']

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
