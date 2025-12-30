# geoms/geom_sankey.py

import pandas as pd
import plotly.graph_objects as go

from .geom_base import Geom


class geom_sankey(Geom):
    """
    Geom for creating Sankey diagrams.

    Sankey diagrams visualize flows between nodes, where the width of each
    link is proportional to the flow quantity. This is useful for showing
    how values flow from one set of categories to another.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. Required: source, target, value.
        Optional: node_label (for custom node labels).
    node_pad : float, default=15
        Padding between nodes.
    node_thickness : float, default=20
        Thickness of nodes.
    node_color : str or list, optional
        Color(s) for nodes. Can be a single color or list of colors.
    link_color : str, optional
        Color for links. If not specified, uses source node color with alpha.
    link_alpha : float, default=0.4
        Transparency of links (0-1).
    arrangement : str, default='snap'
        Node arrangement: 'snap', 'perpendicular', 'freeform', 'fixed'.
    orientation : str, default='h'
        Orientation: 'h' (horizontal) or 'v' (vertical).
    valueformat : str, default='.0f'
        Format string for values in hover.
    name : str, default='Sankey'
        Name for the diagram.

    Aesthetics
    ----------
    source : str (required)
        Column containing source node names/IDs.
    target : str (required)
        Column containing target node names/IDs.
    value : str (required)
        Column containing flow values/weights.
    node_label : str, optional
        Column containing custom node labels.

    Examples
    --------
    >>> import pandas as pd
    >>> from ggplotly import ggplot, aes, geom_sankey
    >>>
    >>> # Basic Sankey diagram
    >>> df = pd.DataFrame({
    ...     'source': ['A', 'A', 'B', 'B'],
    ...     'target': ['X', 'Y', 'X', 'Y'],
    ...     'value': [10, 20, 15, 25]
    ... })
    >>> (ggplot(df, aes(source='source', target='target', value='value'))
    ...  + geom_sankey())
    >>>
    >>> # With custom colors
    >>> (ggplot(df, aes(source='source', target='target', value='value'))
    ...  + geom_sankey(node_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']))
    >>>
    >>> # Multi-stage Sankey (long format)
    >>> df = pd.DataFrame({
    ...     'source': ['Budget', 'Budget', 'Sales', 'Sales', 'Marketing', 'Marketing'],
    ...     'target': ['Sales', 'Marketing', 'Revenue', 'Costs', 'Revenue', 'Costs'],
    ...     'value': [100, 50, 80, 20, 40, 10]
    ... })
    >>> (ggplot(df, aes(source='source', target='target', value='value'))
    ...  + geom_sankey())

    See Also
    --------
    geom_edgebundle : For circular flow visualizations.

    Notes
    -----
    Data should be in "edge list" format with source, target, and value columns.
    Each row represents a flow from source to target with the given value.
    """

    required_aes = ['source', 'target', 'value']

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)

    def _draw_impl(self, fig, data, row, col):
        """
        Draw Sankey diagram on the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        data : DataFrame
            Data for the Sankey diagram.
        row : int
            Row position in subplot.
        col : int
            Column position in subplot.
        """
        # Validate required aesthetics
        required = ['source', 'target', 'value']
        missing = [aes for aes in required if aes not in self.mapping]
        if missing:
            raise ValueError(
                f"geom_sankey requires aesthetics: {', '.join(required)}. "
                f"Missing: {', '.join(missing)}"
            )

        # Get column names from mapping
        source_col = self.mapping['source']
        target_col = self.mapping['target']
        value_col = self.mapping['value']
        node_label_col = self.mapping.get('node_label')

        # Validate columns exist
        for col_name, aes_name in [(source_col, 'source'), (target_col, 'target'), (value_col, 'value')]:
            if col_name not in data.columns:
                raise ValueError(f"Column '{col_name}' for '{aes_name}' not found in data")

        # Get parameters
        node_pad = self.params.get('node_pad', 15)
        node_thickness = self.params.get('node_thickness', 20)
        node_color = self.params.get('node_color', None)
        link_color = self.params.get('link_color', None)
        link_alpha = self.params.get('link_alpha', 0.4)
        arrangement = self.params.get('arrangement', 'snap')
        orientation = self.params.get('orientation', 'h')
        valueformat = self.params.get('valueformat', '.0f')
        name = self.params.get('name', 'Sankey')

        # Build unique node list
        all_nodes = pd.concat([data[source_col], data[target_col]]).unique()
        node_to_idx = {node: idx for idx, node in enumerate(all_nodes)}

        # Get node labels
        if node_label_col and node_label_col in data.columns:
            # Build label mapping from data
            label_map = {}
            for _, row_data in data.iterrows():
                if row_data[source_col] not in label_map:
                    label_map[row_data[source_col]] = str(row_data.get(node_label_col, row_data[source_col]))
            node_labels = [label_map.get(node, str(node)) for node in all_nodes]
        else:
            node_labels = [str(node) for node in all_nodes]

        # Convert source/target to indices
        source_indices = [node_to_idx[s] for s in data[source_col]]
        target_indices = [node_to_idx[t] for t in data[target_col]]
        values = data[value_col].tolist()

        # Set up node colors
        if node_color is None:
            # Use default plotly colors
            default_colors = [
                '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
                '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
            ]
            node_colors = [default_colors[i % len(default_colors)] for i in range(len(all_nodes))]
        elif isinstance(node_color, str):
            node_colors = [node_color] * len(all_nodes)
        else:
            # Assume it's a list
            node_colors = list(node_color)
            # Extend if needed
            while len(node_colors) < len(all_nodes):
                node_colors.extend(node_color)
            node_colors = node_colors[:len(all_nodes)]

        # Set up link colors
        if link_color is None:
            # Use source node color with alpha
            link_colors = []
            for src_idx in source_indices:
                color = node_colors[src_idx]
                # Convert to rgba
                rgba_color = self._color_to_rgba(color, link_alpha)
                link_colors.append(rgba_color)
        else:
            rgba_link = self._color_to_rgba(link_color, link_alpha)
            link_colors = [rgba_link] * len(source_indices)

        # Create Sankey trace
        trace = go.Sankey(
            arrangement=arrangement,
            orientation=orientation,
            valueformat=valueformat,
            node=dict(
                pad=node_pad,
                thickness=node_thickness,
                label=node_labels,
                color=node_colors,
            ),
            link=dict(
                source=source_indices,
                target=target_indices,
                value=values,
                color=link_colors,
            ),
            name=name,
        )

        # Sankey is not compatible with subplots, add directly
        fig.add_trace(trace)

    def _color_to_rgba(self, color, alpha):
        """Convert a color to rgba format with specified alpha."""
        if color.startswith('rgba'):
            return color
        elif color.startswith('rgb'):
            # rgb(r, g, b) -> rgba(r, g, b, alpha)
            return color.replace('rgb', 'rgba').replace(')', f', {alpha})')
        elif color.startswith('#'):
            # Hex to rgba
            hex_color = color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c*2 for c in hex_color])
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            return f'rgba({r}, {g}, {b}, {alpha})'
        else:
            # Named color - return with alpha as separate parameter
            # Plotly handles named colors, so we'll wrap in rgba approximation
            # This is a simplification; for perfect results, use hex or rgb
            return color
