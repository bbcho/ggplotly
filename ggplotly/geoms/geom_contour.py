# geoms/geom_contour.py

import plotly.graph_objects as go

from ..stats.stat_contour import stat_contour
from .geom_base import Geom


class geom_contour(Geom):
    """Geom for drawing contour lines from 2D data."""

    required_aes = ['x', 'y']  # z is optional (computed from KDE if not provided)
    default_params = {"size": 1}

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
            raise ValueError("geom_contour requires both x and y aesthetics")

        alpha = style_props['alpha']
        color = style_props.get('color') or style_props['default_color']
        line_width = style_props['size']
        linetype = self.params.get('linetype', 'solid')

        # Compute grid using stat_contour
        grid_data = self._compute_contour_grid(data)
        x_grid = grid_data['x']
        y_grid = grid_data['y']
        z_grid = grid_data['z']

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
