"""
Geom for force-directed edge bundling visualization.

Creates bundled graph visualizations where edges are attracted to each other
based on compatibility, reducing visual clutter in dense graphs.

Automatically detects geo context and uses Scattergeo when a map is present.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom
from ..stats.stat_edgebundle import stat_edgebundle


class geom_edgebundle(Geom):
    """
    Bundled edges for graph visualization.

    This geom applies force-directed edge bundling to create smooth, bundled
    paths between nodes, reducing visual clutter in dense graphs.

    Automatically detects if a map context exists (geom_map or geom_point_map)
    and switches to Scattergeo for geographic rendering.

    Parameters
    ----------
    mapping : aes, optional
        Aesthetic mappings. Required aesthetics:
        - x, y: start coordinates (or longitude/latitude for maps)
        - xend, yend: end coordinates

    K : float, default=1.0
        Spring constant controlling bundling strength.
        Higher values = tighter bundling.

    C : int, default=6
        Number of refinement cycles.
        More cycles = more subdivision points = smoother curves.

    P : int, default=1
        Initial number of edge subdivisions.

    S : float, default=0.04
        Initial step size for force simulation.

    P_rate : int, default=2
        Rate of subdivision increase per cycle.

    I : int, default=50
        Initial iterations per cycle.

    I_rate : float, default=2/3
        Rate of iteration decrease per cycle.

    compatibility_threshold : float, default=0.6
        Minimum compatibility for edges to interact (0-1).
        Higher values = more selective bundling.

    color : str, default='#9d0191'
        Edge color (magenta by default, matching R edgebundle style).

    alpha : float, default=0.8
        Edge transparency (0-1).

    linewidth : float, default=0.5
        Edge line width.

    show_highlight : bool, default=True
        Add thin highlight lines on top of edges.

    highlight_color : str, default='white'
        Color of highlight lines.

    highlight_alpha : float, default=0.3
        Transparency of highlight lines (0-1).

    highlight_width : float, default=0.1
        Width of highlight lines.

    verbose : bool, default=True
        Print progress messages during bundling.

    Examples
    --------
    Basic usage with edge data:

    >>> edges_df = pd.DataFrame({
    ...     'x': [0, 1, 2],
    ...     'y': [0, 1, 0],
    ...     'xend': [2, 3, 3],
    ...     'yend': [2, 2, 1]
    ... })
    >>> (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    ...  + geom_edgebundle())

    With geographic data (auto-detects map context):

    >>> (ggplot(flights_df, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
    ...  + geom_point_map(data=airports_df, mapping=aes(x='lon', y='lat'), map='usa')
    ...  + geom_edgebundle(compatibility_threshold=0.6)
    ...  + theme_dark())

    Adjust bundling parameters:

    >>> (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    ...  + geom_edgebundle(K=1.0, C=6, compatibility_threshold=0.5))
    """

    def __init__(
        self,
        mapping=None,
        data=None,
        K: float = 1.0,
        C: int = 6,
        P: int = 1,
        S: float = 0.04,
        P_rate: int = 2,
        I: int = 50,
        I_rate: float = 2/3,
        compatibility_threshold: float = 0.6,
        color: str = '#9d0191',
        alpha: float = 0.8,
        linewidth: float = 0.5,
        show_highlight: bool = True,
        highlight_color: str = 'white',
        highlight_alpha: float = 0.3,
        highlight_width: float = 0.1,
        verbose: bool = True,
        **kwargs
    ):
        super().__init__(data=data, mapping=mapping, **kwargs)

        # Bundling parameters
        self.K = K
        self.C = C
        self.P = P
        self.S = S
        self.P_rate = P_rate
        self.I = I
        self.I_rate = I_rate
        self.compatibility_threshold = compatibility_threshold
        self.verbose = verbose

        # Visual parameters
        self.params['color'] = color
        self.params['alpha'] = alpha
        self.params['linewidth'] = linewidth
        self.params['show_highlight'] = show_highlight
        self.params['highlight_color'] = highlight_color
        self.params['highlight_alpha'] = highlight_alpha
        self.params['highlight_width'] = highlight_width

        # Initialize stat transformer
        self.stat = stat_edgebundle(
            K=K,
            C=C,
            P=P,
            S=S,
            P_rate=P_rate,
            I=I,
            I_rate=I_rate,
            compatibility_threshold=compatibility_threshold,
            verbose=verbose
        )

    def _is_geo_figure(self, fig) -> bool:
        """
        Check if figure has geo context (map traces present).

        Returns True if any Scattergeo or Choropleth traces exist,
        indicating we should render edges as Scattergeo too.
        """
        if not fig.data:
            return False

        geo_types = ('scattergeo', 'choropleth', 'scattermapbox', 'choroplethmapbox')
        return any(
            hasattr(trace, 'type') and trace.type in geo_types
            for trace in fig.data
        )

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw bundled edges on the figure.

        Automatically detects geo context and uses appropriate trace type.
        """
        data = data if data is not None else self.data

        if data is None or data.empty:
            return fig

        # Get aesthetic mappings
        x = self.mapping.get('x', 'x')
        y = self.mapping.get('y', 'y')
        xend = self.mapping.get('xend', 'xend')
        yend = self.mapping.get('yend', 'yend')

        # Validate required columns
        required = [x, y, xend, yend]
        missing = [col for col in required if col not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Prepare edge data for stat transformation
        edges_df = pd.DataFrame({
            'x': data[x],
            'y': data[y],
            'xend': data[xend],
            'yend': data[yend]
        })

        # Apply edge bundling transformation
        bundled = self.stat.compute(edges_df)

        # Check if we're in geo context
        is_geo = self._is_geo_figure(fig)

        # Get visual parameters
        color = self.params.get('color', '#9d0191')
        alpha = self.params.get('alpha', 0.8)
        linewidth = self.params.get('linewidth', 0.5)
        show_highlight = self.params.get('show_highlight', True)
        highlight_color = self.params.get('highlight_color', 'white')
        highlight_alpha = self.params.get('highlight_alpha', 0.3)
        highlight_width = self.params.get('highlight_width', 0.1)

        # Convert colors to rgba
        rgba_color = self._color_to_rgba(color, alpha)
        rgba_highlight = self._color_to_rgba(highlight_color, highlight_alpha)

        # Draw bundled edges
        if is_geo:
            self._draw_geo_bundles(fig, bundled, rgba_color, linewidth)
            if show_highlight:
                self._draw_geo_bundles(fig, bundled, rgba_highlight, highlight_width)
        else:
            self._draw_cartesian_bundles(fig, bundled, rgba_color, linewidth, row, col)
            if show_highlight:
                self._draw_cartesian_bundles(fig, bundled, rgba_highlight, highlight_width, row, col)

        return fig

    def _draw_cartesian_bundles(self, fig, bundled, color, width, row, col):
        """Draw bundled edges as Scatter traces (Cartesian coordinates)."""
        for group_id in bundled['group'].unique():
            group_data = bundled[bundled['group'] == group_id]

            fig.add_trace(
                go.Scatter(
                    x=group_data['x'].values,
                    y=group_data['y'].values,
                    mode='lines',
                    line=dict(color=color, width=width),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=row,
                col=col
            )

    def _draw_geo_bundles(self, fig, bundled, color, width):
        """Draw bundled edges as Scattergeo traces (geographic coordinates)."""
        for group_id in bundled['group'].unique():
            group_data = bundled[bundled['group'] == group_id]

            # For geo traces: x is longitude, y is latitude
            fig.add_trace(
                go.Scattergeo(
                    lon=group_data['x'].values,
                    lat=group_data['y'].values,
                    mode='lines',
                    line=dict(color=color, width=width),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )

    def _color_to_rgba(self, color: str, alpha: float) -> str:
        """Convert color name/hex to RGBA string with alpha."""
        color_map = {
            'steelblue': (70, 130, 180),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'magenta': (157, 1, 145),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
        }

        if color.startswith('rgba'):
            return color
        elif color.startswith('#'):
            color = color.lstrip('#')
            if len(color) == 6:
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            elif len(color) == 3:
                r, g, b = int(color[0]*2, 16), int(color[1]*2, 16), int(color[2]*2, 16)
            else:
                r, g, b = 157, 1, 145  # Default magenta
        elif color.lower() in color_map:
            r, g, b = color_map[color.lower()]
        else:
            r, g, b = 157, 1, 145  # Default magenta

        return f'rgba({r},{g},{b},{alpha})'
