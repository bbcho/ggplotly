# geoms/geom_point_3d.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd


# Valid 3D marker symbols in Plotly
# See: https://plotly.com/python/reference/scatter3d/#scatter3d-marker-symbol
VALID_3D_SYMBOLS = ['circle', 'circle-open', 'cross', 'diamond', 'diamond-open', 'square', 'square-open', 'x']

# 3D-compatible shape palette for categorical mapping
SHAPE_PALETTE_3D = [
    'circle',
    'square',
    'diamond',
    'cross',
    'x',
    'circle-open',
    'square-open',
    'diamond-open',
]

# Map 2D symbols to 3D equivalents
SYMBOL_2D_TO_3D = {
    'circle': 'circle',
    'triangle-up': 'diamond',  # No triangle in 3D, use diamond
    'square': 'square',
    'cross': 'cross',
    'diamond': 'diamond',
    'triangle-down': 'diamond',  # No triangle in 3D, use diamond
    'star': 'cross',  # No star in 3D, use cross
    'hexagon': 'circle',  # No hexagon in 3D, use circle
    'circle-open': 'circle-open',
    'triangle-up-open': 'diamond-open',
    'square-open': 'square-open',
    'diamond-open': 'diamond-open',
    'x': 'x',
    'star-open': 'cross',
    'hexagon-open': 'circle-open',
}


class geom_point_3d(Geom):
    """
    Geom for drawing 3D scatter plots.

    Creates interactive 3D scatter plots using Plotly's Scatter3d trace.
    Supports color, size, and shape aesthetics for categorical grouping.

    Parameters:
        x (str): Column name for x-axis (via aes mapping).
        y (str): Column name for y-axis (via aes mapping).
        z (str): Column name for z-axis (via aes mapping).
        color (str, optional): Color of the points. If a column name, maps categories to colors.
        size (int, optional): Size of the points. Default is 6.
        alpha (float, optional): Transparency level for the points. Default is 1.
        shape (str, optional): Shape of the points. If a column name, maps categories to shapes.
            Literal values can be any Plotly 3D marker symbol (e.g., 'circle', 'square',
            'diamond', 'cross', 'x', 'circle-open', 'square-open', etc.)
        group (str, optional): Grouping variable for the points.

    Examples:
        >>> # Basic 3D scatter plot
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()

        >>> # 3D scatter with color grouping
        >>> ggplot(df, aes(x='x', y='y', z='z', color='category')) + geom_point_3d()

        >>> # 3D scatter with custom size and alpha
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d(size=10, alpha=0.7)
    """

    def _convert_symbol_to_3d(self, symbol):
        """Convert a 2D symbol to its 3D equivalent."""
        if symbol is None:
            return 'circle'
        if symbol in VALID_3D_SYMBOLS:
            return symbol
        return SYMBOL_2D_TO_3D.get(symbol, 'circle')

    def _create_shape_map_3d(self, series):
        """Create a shape map using only 3D-compatible symbols."""
        unique_values = series.dropna().unique()
        shape_map = {}
        for i, val in enumerate(unique_values):
            shape_map[val] = SHAPE_PALETTE_3D[i % len(SHAPE_PALETTE_3D)]
        return shape_map

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        # Set default point size to 6 if not specified (smaller default for 3D)
        if "size" not in self.params:
            self.params["size"] = 6

        # Create aesthetic mapper
        mapper = AestheticMapper(
            data, self.mapping, self.params, self.theme,
            global_color_map=self._global_color_map,
            global_shape_map=self._global_shape_map
        )
        style_props = mapper.get_style_properties()

        # Override shape_map with 3D-compatible symbols
        if style_props.get('shape_series') is not None:
            style_props['shape_map'] = self._create_shape_map_3d(style_props['shape_series'])

        # Extract axis data
        x = data[self.mapping["x"]] if "x" in self.mapping else None
        y = data[self.mapping["y"]] if "y" in self.mapping else None
        z = data[self.mapping["z"]] if "z" in self.mapping else None

        if x is None or y is None or z is None:
            raise ValueError("geom_point_3d requires 'x', 'y', and 'z' aesthetics")

        # Extract style properties
        alpha = style_props['alpha']
        group_values = style_props['group_series']
        shape_series = style_props.get('shape_series')
        shape_map = style_props.get('shape_map')

        # For faceted plots, track which legend groups have been shown
        base_showlegend = self.params.get("showlegend", True)

        if not hasattr(fig, '_shown_legendgroups'):
            fig._shown_legendgroups = set()

        def should_show_legend(legendgroup):
            """Show legend only the first time this group appears."""
            if not base_showlegend:
                return False
            if legendgroup in fig._shown_legendgroups:
                return False
            fig._shown_legendgroups.add(legendgroup)
            return True

        # Determine grouping strategy
        has_color_grouping = style_props['color_series'] is not None or style_props['fill_series'] is not None
        has_shape_grouping = shape_series is not None

        # Get categorical aesthetic info
        if style_props['color_series'] is not None:
            cat_col = style_props['color']
            cat_map = style_props['color_map']
        elif style_props['fill_series'] is not None:
            cat_col = style_props['fill']
            cat_map = style_props['fill_map']
        else:
            cat_col = None
            cat_map = None

        shape_col = style_props.get('shape') if has_shape_grouping else None

        # Case 1: Grouped by explicit 'group' aesthetic
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group

                color_key = group if has_color_grouping else None
                shape_key = group if has_shape_grouping else None

                trace_props = self._apply_color_targets(
                    {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'},
                    style_props,
                    value_key=color_key, data_mask=group_mask, shape_key=shape_key
                )

                legend_name = str(group)
                self._add_trace_3d(
                    fig, x[group_mask], y[group_mask], z[group_mask],
                    trace_props, alpha, legend_name, should_show_legend, row, col
                )

        # Case 2: Both color/fill AND shape are mapped
        elif has_color_grouping and has_shape_grouping:
            same_column = cat_col == shape_col
            color_values = list(cat_map.keys())
            shape_values = list(shape_map.keys())

            for color_val in color_values:
                for shape_val in shape_values:
                    combo_mask = (data[cat_col] == color_val) & (data[shape_col] == shape_val)

                    if not combo_mask.any():
                        continue

                    trace_props = self._apply_color_targets(
                        {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'},
                        style_props,
                        value_key=color_val, data_mask=combo_mask, shape_key=shape_val
                    )

                    legend_name = str(color_val) if same_column else f"{color_val}, {shape_val}"
                    self._add_trace_3d(
                        fig, x[combo_mask], y[combo_mask], z[combo_mask],
                        trace_props, alpha, legend_name, should_show_legend, row, col
                    )

        # Case 3: Only color/fill mapped
        elif has_color_grouping:
            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value

                if not cat_mask.any():
                    continue

                trace_props = self._apply_color_targets(
                    {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'},
                    style_props,
                    value_key=cat_value, data_mask=cat_mask, shape_key=None
                )

                legend_name = str(cat_value)
                self._add_trace_3d(
                    fig, x[cat_mask], y[cat_mask], z[cat_mask],
                    trace_props, alpha, legend_name, should_show_legend, row, col
                )

        # Case 4: Only shape mapped
        elif has_shape_grouping:
            for shape_val in shape_map.keys():
                shape_mask = data[shape_col] == shape_val

                if not shape_mask.any():
                    continue

                trace_props = self._apply_color_targets(
                    {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'},
                    style_props,
                    value_key=None, data_mask=shape_mask, shape_key=shape_val
                )

                legend_name = str(shape_val)
                self._add_trace_3d(
                    fig, x[shape_mask], y[shape_mask], z[shape_mask],
                    trace_props, alpha, legend_name, should_show_legend, row, col
                )

        # Case 5: No grouping - single trace
        else:
            trace_props = self._apply_color_targets(
                {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'},
                style_props,
                data_mask=None, shape_key=None
            )

            trace_name = self.params.get('name', '3D Scatter')
            self._add_trace_3d(
                fig, x, y, z,
                trace_props, alpha, trace_name, should_show_legend, row, col
            )

        # Update 3D scene layout
        scene_dict = {}
        if 'x' in self.mapping:
            scene_dict['xaxis_title'] = self.mapping['x']
        if 'y' in self.mapping:
            scene_dict['yaxis_title'] = self.mapping['y']
        if 'z' in self.mapping:
            scene_dict['zaxis_title'] = self.mapping['z']

        if scene_dict:
            # Use the scene key from faceting if available, otherwise default to 'scene'
            scene_key = self.params.get('_scene_key', 'scene')
            fig.update_layout(**{scene_key: scene_dict})

    def _add_trace_3d(self, fig, x, y, z, trace_props, alpha, legend_name, should_show_legend, row, col):
        """Helper to add a 3D scatter trace."""
        marker_dict = dict(
            size=trace_props.get('marker_size', self.params.get('size', 6)),
            opacity=alpha,
        )

        if 'marker_color' in trace_props:
            marker_dict['color'] = trace_props['marker_color']

        if 'marker_symbol' in trace_props:
            # Convert to 3D-compatible symbol
            marker_dict['symbol'] = self._convert_symbol_to_3d(trace_props['marker_symbol'])

        # Get scene key for faceting support
        scene_key = self.params.get('_scene_key', 'scene')

        trace = go.Scatter3d(
            x=x,
            y=y,
            z=z,
            mode='markers',
            marker=marker_dict,
            name=legend_name,
            showlegend=should_show_legend(legend_name),
            legendgroup=legend_name,
            scene=scene_key,
        )

        # Add trace directly (3D traces use scene parameter, not row/col)
        fig.add_trace(trace)
