"""
Geom for force-directed edge bundling visualization.

Creates bundled graph visualizations where edges are attracted to each other
based on compatibility, reducing visual clutter in dense graphs.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom
from ggplotly.stats.stat_edgebundle import stat_edgebundle


class geom_edgebundle(Geom):
    """
    Bundled edges for graph visualization.

    This geom applies force-directed edge bundling to create smooth, bundled
    paths between nodes, reducing visual clutter in dense graphs.

    Parameters
    ----------
    mapping : aes, optional
        Aesthetic mappings. Required aesthetics:
        - x, y: start coordinates
        - xend, yend: end coordinates
        Optional aesthetics:
        - color: edge color (can be mapped to a variable)
        - alpha: transparency
        - size/width: line width

    K : float, default=0.1
        Spring constant controlling bundling strength.
        Higher values = tighter bundling.
        Typical range: 0.05 - 0.15

    cycles : int, default=6
        Number of refinement cycles.
        More cycles = more subdivision points = smoother curves.
        Each cycle doubles the number of points.

    compatibility_threshold : float, default=0.1
        Minimum compatibility for edges to interact.
        Higher values = more selective bundling.
        Range: 0.0 - 1.0

    color : str, default='steelblue'
        Edge color (literal value)

    alpha : float, default=0.6
        Edge transparency (0-1)

    width : float, default=1.5
        Edge line width

    Examples
    --------
    Basic usage with edge list:

    >>> edges_df = pd.DataFrame({
    ...     'x': [0, 1, 2],
    ...     'y': [0, 1, 0],
    ...     'xend': [2, 3, 3],
    ...     'yend': [2, 2, 1]
    ... })
    >>> p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    >>> p = p + geom_edgebundle()

    With colored edges:

    >>> edges_df['flow'] = [100, 200, 150]
    >>> p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
    >>> p = p + geom_edgebundle()

    Adjust bundling parameters:

    >>> p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    >>> p = p + geom_edgebundle(K=0.15, cycles=8, compatibility_threshold=0.2)
    """

    def __init__(
        self,
        mapping=None,
        K: float = 0.1,
        cycles: int = 6,
        compatibility_threshold: float = 0.6,
        color: str = 'steelblue',
        alpha: float = 0.6,
        width: float = 1.5,
        **kwargs
    ):
        super().__init__(mapping=mapping, **kwargs)
        self.K = K
        self.cycles = cycles
        self.compatibility_threshold = compatibility_threshold
        self.params['color'] = color
        self.params['alpha'] = alpha
        self.params['width'] = width

        # Initialize stat transformer
        self.stat = stat_edgebundle(
            K=K,
            cycles=cycles,
            compatibility_threshold=compatibility_threshold
        )

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw bundled edges on the figure.

        Parameters
        ----------
        fig : go.Figure
            Plotly figure to add traces to

        data : pd.DataFrame, optional
            Must contain columns for x, y, xend, yend

        row : int
            Row position in subplot (for faceting)

        col : int
            Column position in subplot (for faceting)

        Returns
        -------
        go.Figure
            Updated figure with bundled edges
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

        # Prepare edge data
        edges_df = pd.DataFrame({
            'x': data[x],
            'y': data[y],
            'xend': data[xend],
            'yend': data[yend]
        })

        # Add edge_id to track individual edges
        edges_df['edge_id'] = range(len(edges_df))

        # Apply edge bundling transformation
        bundled = self.stat.compute_bundling(edges_df)

        # Check if color is mapped to a column
        color_col = self.mapping.get('color')
        if color_col and color_col in data.columns:
            # Create mapping from edge_id to color value
            # edge_id corresponds to the original row index
            color_values_map = {i: data[color_col].iloc[i] for i in range(len(data))}
            self._draw_colored_bundles(fig, bundled, color_values_map, color_col)
        else:
            # Single color for all edges
            self._draw_uniform_bundles(fig, bundled)

        return fig

    def _draw_uniform_bundles(self, fig: go.Figure, bundled: pd.DataFrame):
        """Draw all bundled edges with uniform styling."""
        color = self.params.get('color', 'steelblue')
        alpha = self.params.get('alpha', 0.6)
        width = self.params.get('width', 1.5)

        # Convert alpha to RGBA
        rgba_color = self._color_to_rgba(color, alpha)

        # Draw each bundled edge as a separate trace
        for edge_id in bundled['edge_id'].unique():
            edge_data = bundled[bundled['edge_id'] == edge_id].sort_values('segment')

            fig.add_trace(
                go.Scatter(
                    x=edge_data['x'].values,
                    y=edge_data['y'].values,
                    mode='lines',
                    line=dict(
                        color=rgba_color,
                        width=width,
                        shape='spline',  # Smooth spline interpolation
                        smoothing=0.8
                    ),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )

    def _draw_colored_bundles(
        self,
        fig: go.Figure,
        bundled: pd.DataFrame,
        color_values_map: dict,
        color_col: str
    ):
        """Draw bundled edges with color mapped to a variable."""
        alpha = self.params.get('alpha', 0.6)
        width = self.params.get('width', 1.5)

        # Get all color values
        color_vals = list(color_values_map.values())

        # Create color scale
        # For continuous values, use a gradient; for categorical, use discrete colors
        sample_val = color_vals[0] if color_vals else None
        if sample_val is not None and pd.api.types.is_numeric_dtype(type(sample_val)):
            # Continuous color scale
            vmin, vmax = min(color_vals), max(color_vals)
            colorscale = 'Blues'  # Default colorscale

            for edge_id in bundled['edge_id'].unique():
                edge_data = bundled[bundled['edge_id'] == edge_id].sort_values('segment')
                color_val = color_values_map[edge_id]

                # Normalize color value to [0, 1]
                normalized_val = (color_val - vmin) / (vmax - vmin) if vmax > vmin else 0.5

                # Get color from colorscale
                edge_color = self._get_color_from_scale(normalized_val, colorscale)
                rgba_color = self._color_to_rgba(edge_color, alpha)

                fig.add_trace(
                    go.Scatter(
                        x=edge_data['x'].values,
                        y=edge_data['y'].values,
                        mode='lines',
                        line=dict(
                            color=rgba_color,
                            width=width,
                            shape='spline',
                            smoothing=0.8
                        ),
                        showlegend=False,
                        hoverinfo='skip'
                    )
                )
        else:
            # Categorical color mapping
            unique_vals = list(set(color_vals))
            palette = self._get_categorical_palette(len(unique_vals))
            color_map = dict(zip(unique_vals, palette))

            for edge_id in bundled['edge_id'].unique():
                edge_data = bundled[bundled['edge_id'] == edge_id].sort_values('segment')
                color_val = color_values_map[edge_id]
                edge_color = color_map[color_val]
                rgba_color = self._color_to_rgba(edge_color, alpha)

                fig.add_trace(
                    go.Scatter(
                        x=edge_data['x'].values,
                        y=edge_data['y'].values,
                        mode='lines',
                        line=dict(
                            color=rgba_color,
                            width=width,
                            shape='spline',
                            smoothing=0.8
                        ),
                        name=str(color_val),
                        showlegend=False,
                        legendgroup=str(color_val),
                        hoverinfo='skip'
                    )
                )

    def _color_to_rgba(self, color: str, alpha: float) -> str:
        """Convert color name/hex to RGBA string with alpha."""
        # Simple conversion for common colors
        # For production, use a proper color library
        color_map = {
            'steelblue': (70, 130, 180),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
        }

        if color.startswith('#'):
            # Hex color
            color = color.lstrip('#')
            r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
        elif color in color_map:
            r, g, b = color_map[color]
        else:
            # Default to steelblue
            r, g, b = color_map['steelblue']

        return f'rgba({r},{g},{b},{alpha})'

    def _get_color_from_scale(self, value: float, colorscale: str) -> str:
        """Get color from a named colorscale at normalized position [0, 1]."""
        # Simplified: return blue shades based on value
        # For production, use plotly.colors
        intensity = int(255 * value)
        return f'#{intensity:02x}{intensity:02x}ff'

    def _get_categorical_palette(self, n: int) -> list:
        """Get a categorical color palette with n colors."""
        # Default palette
        base_colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        # Repeat if needed
        return (base_colors * (n // len(base_colors) + 1))[:n]
