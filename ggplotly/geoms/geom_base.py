import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from itertools import product
from ..aes import aes
from ..stats.stat_base import Stat
from ..aesthetic_mapper import AestheticMapper
import copy


class Geom:
    """
    Base class for all geoms.
    """

    def __init__(self, data=None, mapping=None, **params):
        # check to see if data was passed first or if aes was passed first
        if isinstance(data, aes):
            self.mapping = data.mapping
            self.data = None
        else:
            self.data = data
            self.mapping = mapping.mapping if mapping else {}

        self.params = params
        self.stats = []
        self.layers = []
        # Track whether this geom has explicit data or inherited from plot
        self._has_explicit_data = data is not None and not isinstance(data, aes)

    # def __add__(self, other):
    #     if isinstance(other, Geom):
    #         self.layers.append(other)

    #     return self.copy()
    # else:
    # raise ValueError("Only Geom and Stat objects can be added to Geom objects.")

    def copy(self):
        new = copy.deepcopy(self)
        new.stats = [*self.stats.copy()]
        return new

    def setup_data(self, data, plot_mapping):
        """
        Combine plot mapping with geom-specific mapping and set data.

        Parameters:
            data (DataFrame): The dataset to use.
            plot_mapping (dict): The global aesthetic mappings from the plot.
        """
        # Merge plot mapping and geom mapping, with geom mapping taking precedence
        combined_mapping = {**plot_mapping, **self.mapping}
        self.mapping = combined_mapping
        self.data = data.copy()

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the geometry on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Optional data subset for faceting.
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).
        """
        raise NotImplementedError("The draw method must be implemented by subclasses.")

    def _apply_color_targets(self, target_props: dict, style_props: dict, value_key=None, data_mask=None, shape_key=None) -> dict:
        """
        Apply color/fill/size/shape to trace properties based on target mapping.

        Parameters:
            target_props: Dict mapping aesthetics to trace property names
                         e.g., {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'}
            style_props: Style properties from AestheticMapper
            value_key: Optional key for looking up color from color_map
            data_mask: Optional boolean mask to filter size series data
            shape_key: Optional key for looking up shape from shape_map

        Returns:
            Dict of trace properties to apply
        """
        result = {}

        # Determine the color to use
        if value_key is not None:
            # Looking up color for a specific category
            if style_props['color_series'] is not None:
                color_value = style_props['color_map'].get(value_key)
            elif style_props['fill_series'] is not None:
                color_value = style_props['fill_map'].get(value_key)
            else:
                # Handle None explicitly for literal values
                color_value = style_props.get('color') if style_props.get('color') is not None else \
                             style_props.get('fill') if style_props.get('fill') is not None else \
                             style_props['default_color']
        else:
            # Use literal value or default (handle None explicitly)
            color_value = style_props.get('color') if style_props.get('color') is not None else \
                         style_props.get('fill') if style_props.get('fill') is not None else \
                         style_props['default_color']

        # Apply to appropriate trace properties
        for aesthetic, trace_prop in target_props.items():
            if aesthetic == 'color' or aesthetic == 'fill':
                result[trace_prop] = color_value
            elif aesthetic == 'size':
                # Check if size is mapped to a column (series) or is a literal value
                if style_props['size_series'] is not None:
                    # Size is mapped to a column - use the series data
                    if data_mask is not None:
                        result[trace_prop] = style_props['size_series'][data_mask]
                    else:
                        result[trace_prop] = style_props['size_series']
                else:
                    # Size is a literal value
                    result[trace_prop] = style_props['size']
            elif aesthetic == 'shape':
                # Determine shape to use
                if shape_key is not None and style_props.get('shape_map'):
                    result[trace_prop] = style_props['shape_map'].get(shape_key, 'circle')
                elif style_props.get('shape') is not None and style_props.get('shape_series') is None:
                    # Literal shape value
                    result[trace_prop] = style_props['shape']
                else:
                    # Default shape
                    result[trace_prop] = 'circle'

        return result

    def _transform_fig(
        self, plot, fig, data, payload, color_targets, row, col, **layout
    ):
        # Create aesthetic mapper for this geom
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        # Extract commonly used values
        group_values = style_props['group_series']
        alpha = style_props['alpha']
        shape_series = style_props.get('shape_series')
        shape_map = style_props.get('shape_map')

        # Get x and y data
        x = data[self.mapping["x"]] if "x" in self.mapping else None
        y = data[self.mapping["y"]] if "y" in self.mapping else None

        # Determine the grouping strategy
        # Priority: explicit group > color/fill mapping > shape mapping
        # If multiple aesthetics are mapped, we need to create traces for each combination

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

        # Remove 'name' from payload if it exists (we set it explicitly)
        payload_copy = {k: v for k, v in payload.items() if k != 'name'}

        # Case 1: Grouped by explicit 'group' aesthetic
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group

                # Determine color and shape keys
                color_key = group if has_color_grouping else None
                shape_key = group if has_shape_grouping else None

                trace_props = self._apply_color_targets(
                    color_targets, style_props,
                    value_key=color_key, data_mask=group_mask, shape_key=shape_key
                )

                fig.add_trace(
                    plot(
                        x=x[group_mask],
                        y=y[group_mask],
                        showlegend=self.params.get("showlegend", True),
                        opacity=alpha,
                        name=str(group),
                        **payload_copy,
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )

        # Case 2: Both color/fill AND shape are mapped to columns
        # Need to create traces for each combination
        elif has_color_grouping and has_shape_grouping:
            # Check if color and shape are mapped to the same column
            same_column = cat_col == shape_col

            color_values = list(cat_map.keys())
            shape_values = list(shape_map.keys())

            for color_val in color_values:
                for shape_val in shape_values:
                    # Filter data for this combination
                    combo_mask = (data[cat_col] == color_val) & (data[shape_col] == shape_val)

                    # Skip if no data for this combination
                    if not combo_mask.any():
                        continue

                    x_subset = x[combo_mask] if x is not None else None
                    y_subset = y[combo_mask] if y is not None else None

                    trace_props = self._apply_color_targets(
                        color_targets, style_props,
                        value_key=color_val, data_mask=combo_mask, shape_key=shape_val
                    )

                    # Create legend name - use single value if same column, otherwise combine
                    if same_column:
                        legend_name = str(color_val)
                    else:
                        legend_name = f"{color_val}, {shape_val}"

                    fig.add_trace(
                        plot(
                            x=x_subset,
                            y=y_subset,
                            opacity=alpha,
                            name=legend_name,
                            showlegend=self.params.get("showlegend", True),
                            **payload_copy,
                            **trace_props,
                        ),
                        row=row,
                        col=col,
                    )

        # Case 3: Only color/fill mapped (no shape grouping)
        elif has_color_grouping:
            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value
                x_subset = x[cat_mask] if x is not None else None
                y_subset = y[cat_mask] if y is not None else None

                trace_props = self._apply_color_targets(
                    color_targets, style_props,
                    value_key=cat_value, data_mask=cat_mask, shape_key=None
                )

                fig.add_trace(
                    plot(
                        x=x_subset,
                        y=y_subset,
                        opacity=alpha,
                        name=str(cat_value),
                        showlegend=self.params.get("showlegend", True),
                        **payload_copy,
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )

        # Case 4: Only shape mapped (no color grouping)
        elif has_shape_grouping:
            for shape_val in shape_map.keys():
                shape_mask = data[shape_col] == shape_val
                x_subset = x[shape_mask] if x is not None else None
                y_subset = y[shape_mask] if y is not None else None

                trace_props = self._apply_color_targets(
                    color_targets, style_props,
                    value_key=None, data_mask=shape_mask, shape_key=shape_val
                )

                fig.add_trace(
                    plot(
                        x=x_subset,
                        y=y_subset,
                        opacity=alpha,
                        name=str(shape_val),
                        showlegend=self.params.get("showlegend", True),
                        **payload_copy,
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )

        # Case 5: No grouping - single trace
        else:
            trace_props = self._apply_color_targets(
                color_targets, style_props,
                data_mask=None, shape_key=None
            )

            fig.add_trace(
                plot(
                    x=x,
                    y=y,
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    **payload,
                    **trace_props,
                ),
                row=row,
                col=col,
            )

        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(**layout)
