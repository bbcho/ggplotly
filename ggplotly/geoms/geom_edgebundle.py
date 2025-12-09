"""
Geom for force-directed edge bundling visualization.

Creates bundled graph visualizations where edges are attracted to each other
based on compatibility, reducing visual clutter in dense graphs.

Automatically detects geo context and uses Scattergeo when a map is present.
Supports igraph Graph objects for convenient graph visualization.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom
from ..stats.stat_edgebundle import stat_edgebundle


def _extract_graph_data(graph, weight_attr=None):
    """
    Extract edge and node data from an igraph Graph object.

    Parameters
    ----------
    graph : igraph.Graph
        Graph object with vertex attributes for coordinates.
        Expected attributes: 'longitude'/'lon'/'x' and 'latitude'/'lat'/'y'.
    weight_attr : str, optional
        Name of edge attribute to use as weight. If None, will auto-detect
        'weight' attribute if present.

    Returns
    -------
    tuple : (edges_df, nodes_df)
        DataFrames containing edge coordinates and node attributes.
        edges_df includes 'weight' column if weights are available.
    """
    # Get coordinate attribute names
    lon_attr = None
    lat_attr = None
    for attr in ['longitude', 'lon', 'x']:
        if attr in graph.vs.attributes():
            lon_attr = attr
            break
    for attr in ['latitude', 'lat', 'y']:
        if attr in graph.vs.attributes():
            lat_attr = attr
            break

    if lon_attr is None or lat_attr is None:
        raise ValueError(
            "Graph vertices must have coordinate attributes. "
            "Expected 'longitude'/'lon'/'x' and 'latitude'/'lat'/'y'."
        )

    # Determine weight attribute
    if weight_attr is None and 'weight' in graph.es.attributes():
        weight_attr = 'weight'

    # Extract node data
    nodes_data = {'x': graph.vs[lon_attr], 'y': graph.vs[lat_attr]}
    for attr in graph.vs.attributes():
        nodes_data[attr] = graph.vs[attr]
    nodes_df = pd.DataFrame(nodes_data)

    # Extract edge data
    edges = []
    for edge in graph.es:
        source, target = edge.source, edge.target
        edge_data = {
            'x': graph.vs[source][lon_attr],
            'y': graph.vs[source][lat_attr],
            'xend': graph.vs[target][lon_attr],
            'yend': graph.vs[target][lat_attr]
        }
        if weight_attr is not None:
            edge_data['weight'] = edge[weight_attr]
        edges.append(edge_data)
    edges_df = pd.DataFrame(edges)

    return edges_df, nodes_df


class geom_edgebundle(Geom):
    """Bundled edges for graph visualization using force-directed edge bundling."""

    def __init__(
        self,
        mapping=None,
        data=None,
        graph=None,
        weight=None,
        K: float = 1.0,
        E: float = 1.0,
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
        show_nodes: bool = True,
        node_color: str = 'white',
        node_size: float = 3,
        node_alpha: float = 1.0,
        verbose: bool = True,
        **kwargs
    ):
        """
        Create bundled edges for graph visualization.

        Applies force-directed edge bundling to create smooth, bundled paths
        between nodes, reducing visual clutter in dense graphs. Automatically
        detects map context and uses Scattergeo for geographic rendering.

        Parameters
        ----------
        mapping : aes, optional
            Aesthetic mappings. Required: x, y (start), xend, yend (end).
            Optional: weight (edge weight for bundling attraction).
            Not needed when using graph parameter.
        data : DataFrame, optional
            Data to use for this geom (overrides plot data).
        graph : igraph.Graph, optional
            An igraph Graph object with vertex coordinate attributes.
            When provided, edges and nodes are extracted automatically.
            Vertices must have 'longitude'/'lon'/'x' and 'latitude'/'lat'/'y'.
            Edge 'weight' attribute is used automatically if present.
        weight : str, optional
            Column name or igraph edge attribute for edge weights.
            Heavier edges attract compatible edges more strongly during
            bundling, causing lighter edges to bundle toward heavy routes.
            Weights are normalized to [0.5, 1.5] range internally.
        K : float, default=1.0
            Spring constant controlling edge stiffness (resists bundling).
        E : float, default=1.0
            Electrostatic constant controlling bundling attraction strength.
            Higher values increase bundling, lower values decrease it.
        C : int, default=6
            Number of cycles. More = smoother curves.
        P : int, default=1
            Initial edge subdivisions.
        S : float, default=0.04
            Initial step size for force simulation.
        P_rate : int, default=2
            Subdivision increase rate per cycle.
        I : int, default=50
            Initial iterations per cycle.
        I_rate : float, default=2/3
            Iteration decrease rate per cycle.
        compatibility_threshold : float, default=0.6
            Min compatibility (0-1). Higher = more selective bundling.
        color : str, default='#9d0191'
            Edge color.
        alpha : float, default=0.8
            Edge transparency (0-1).
        linewidth : float, default=0.5
            Edge line width.
        show_highlight : bool, default=True
            Add highlight lines on top of edges.
        highlight_color : str, default='white'
            Highlight line color.
        highlight_alpha : float, default=0.3
            Highlight transparency (0-1).
        highlight_width : float, default=0.1
            Highlight line width.
        show_nodes : bool, default=True
            Show nodes when using igraph input.
        node_color : str, default='white'
            Node marker color.
        node_size : float, default=3
            Node marker size.
        node_alpha : float, default=1.0
            Node transparency (0-1).
        verbose : bool, default=True
            Print progress messages.

        Examples
        --------
        >>> # From DataFrame
        >>> (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
        ...  + geom_edgebundle(compatibility_threshold=0.6))

        >>> # From DataFrame with weights
        >>> (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', weight='traffic'))
        ...  + geom_edgebundle())

        >>> # From igraph (auto-detects 'weight' edge attribute)
        >>> g = data('us_flights')
        >>> ggplot() + geom_edgebundle(graph=g)

        >>> # From igraph with explicit weight attribute
        >>> ggplot() + geom_edgebundle(graph=g, weight='passengers')
        """
        super().__init__(data=data, mapping=mapping, **kwargs)

        # Store weight column/attribute name
        self.weight_attr = weight

        # Store graph and extracted data
        self.graph = graph
        self.nodes = None
        if graph is not None:
            edges_df, nodes_df = _extract_graph_data(graph, weight_attr=weight)
            self.data = edges_df
            self.nodes = nodes_df

        # Bundling parameters
        self.K = K
        self.E = E
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
        self.params['show_nodes'] = show_nodes
        self.params['node_color'] = node_color
        self.params['node_size'] = node_size
        self.params['node_alpha'] = node_alpha

        # Initialize stat transformer
        self.stat = stat_edgebundle(
            K=K,
            E=E,
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

        if data is None or (hasattr(data, 'empty') and data.empty):
            return fig

        # Get aesthetic mappings
        x = self.mapping.get('x', 'x')
        y = self.mapping.get('y', 'y')
        xend = self.mapping.get('xend', 'xend')
        yend = self.mapping.get('yend', 'yend')

        # Validate required columns
        required = [x, y, xend, yend]
        missing = [c for c in required if c not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Prepare edge data for stat transformation
        edges_df = pd.DataFrame({
            'x': data[x],
            'y': data[y],
            'xend': data[xend],
            'yend': data[yend]
        })

        # Extract weights if available
        weights = None
        weight_col = self.mapping.get('weight', self.weight_attr)
        if weight_col is None and 'weight' in data.columns:
            # Auto-detect weight column (e.g., from igraph extraction)
            weight_col = 'weight'
        if weight_col is not None and weight_col in data.columns:
            weights = data[weight_col].values

        # Apply edge bundling transformation
        bundled = self.stat.compute(edges_df, weights=weights)

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

        # Draw nodes if we have them (from igraph input)
        if self.nodes is not None and self.params.get('show_nodes', True):
            self._draw_nodes(fig, is_geo, row, col)

        return fig

    def _draw_nodes(self, fig, is_geo, row, col):
        """Draw nodes from igraph data."""
        node_color = self.params.get('node_color', 'white')
        node_size = self.params.get('node_size', 3)
        node_alpha = self.params.get('node_alpha', 1.0)

        rgba_node = self._color_to_rgba(node_color, node_alpha)

        # Get hover text if 'name' attribute exists
        hover_text = self.nodes.get('name', None)

        if is_geo:
            fig.add_trace(
                go.Scattergeo(
                    lon=self.nodes['x'].values,
                    lat=self.nodes['y'].values,
                    mode='markers',
                    marker=dict(color=rgba_node, size=node_size),
                    text=hover_text,
                    hoverinfo='text' if hover_text is not None else 'skip',
                    showlegend=False
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=self.nodes['x'].values,
                    y=self.nodes['y'].values,
                    mode='markers',
                    marker=dict(color=rgba_node, size=node_size),
                    text=hover_text,
                    hoverinfo='text' if hover_text is not None else 'skip',
                    showlegend=False
                ),
                row=row,
                col=col
            )

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
