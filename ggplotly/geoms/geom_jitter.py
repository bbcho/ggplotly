# geoms/geom_jitter.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import numpy as np
import pandas as pd


class geom_jitter(Geom):
    """
    Geom for drawing jittered point plots.

    Jittering adds a small amount of random noise to the position of each point,
    which is useful for visualizing overlapping points in categorical data.

    Parameters:
        width (float, optional): Amount of horizontal jitter. Default is 0.2.
            The jitter is added in both directions, so the total spread is 2*width.
        height (float, optional): Amount of vertical jitter. Default is 0.
            The jitter is added in both directions, so the total spread is 2*height.
        color (str, optional): Color of the points. If a column name, maps categories to colors.
        size (int, optional): Size of the points. Default is 8.
        alpha (float, optional): Transparency level for the points. Default is 1.
        shape (str, optional): Shape of the points. If a column name, maps categories to shapes.
        seed (int, optional): Random seed for reproducibility. Default is None.
        group (str, optional): Grouping variable for the points.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_jitter()
        >>> ggplot(df, aes(x='category', y='value', color='group')) + geom_jitter(width=0.3)
    """

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the jitter geom.

        Parameters:
            data (DataFrame, optional): Data for this geom.
            mapping (aes, optional): Aesthetic mappings.
            **params: Additional parameters (width, height, seed, etc.).
        """
        super().__init__(data, mapping, **params)
        self.width = params.get('width', 0.2)
        self.height = params.get('height', 0)
        self.seed = params.get('seed', None)

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw jittered points on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Set default point size to 8 if not specified
        if "size" not in self.params:
            self.params["size"] = 8

        # Create a copy of data to add jitter
        data = data.copy()

        # Set random seed if provided
        rng = np.random.RandomState(self.seed)

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")

        # Check if x is categorical
        x_is_categorical = False
        if x_col and x_col in data.columns:
            x_is_categorical = data[x_col].dtype == 'object' or str(data[x_col].dtype) == 'category'

        # Check if y is categorical
        y_is_categorical = False
        if y_col and y_col in data.columns:
            y_is_categorical = data[y_col].dtype == 'object' or str(data[y_col].dtype) == 'category'

        # Now draw using custom logic to handle categorical axes
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        alpha = style_props['alpha']
        group_values = style_props['group_series']

        # Determine grouping
        has_color_grouping = style_props['color_series'] is not None or style_props['fill_series'] is not None
        has_shape_grouping = style_props.get('shape_series') is not None

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
        shape_map = style_props.get('shape_map')

        def get_trace_props(value_key=None, shape_key=None):
            """Get marker properties for a trace."""
            props = {}
            # Color
            if value_key is not None and cat_map:
                props['marker_color'] = cat_map.get(value_key, style_props['default_color'])
            else:
                props['marker_color'] = style_props.get('color') or style_props['default_color']
            # Size
            props['marker_size'] = style_props['size']
            # Shape
            if shape_key is not None and shape_map:
                props['marker_symbol'] = shape_map.get(shape_key, 'circle')
            elif style_props.get('shape') and not has_shape_grouping:
                props['marker_symbol'] = style_props['shape']
            else:
                props['marker_symbol'] = 'circle'
            return props

        def add_jitter_trace(x_data, y_data, name, trace_props, indices=None):
            """Add a jittered trace. Uses go.Box with invisible box for categorical axes."""

            if x_is_categorical and not y_is_categorical:
                # Categorical x, numeric y - use go.Box with jitter for proper alignment
                fig.add_trace(
                    go.Box(
                        x=x_data,
                        y=y_data,
                        name=name,
                        opacity=alpha,
                        showlegend=self.params.get("showlegend", True),
                        marker=dict(
                            color=trace_props['marker_color'],
                            size=trace_props['marker_size'],
                            symbol=trace_props['marker_symbol'],
                        ),
                        boxpoints='all',
                        jitter=min(self.width * 2, 1.0),  # Plotly jitter is 0-1 scale
                        pointpos=0,
                        line=dict(color='rgba(0,0,0,0)', width=0),
                        fillcolor='rgba(0,0,0,0)',
                        hoveron='points',
                    ),
                    row=row,
                    col=col,
                )
            elif y_is_categorical and not x_is_categorical:
                # Categorical y, numeric x - use horizontal box
                fig.add_trace(
                    go.Box(
                        x=x_data,
                        y=y_data,
                        name=name,
                        opacity=alpha,
                        showlegend=self.params.get("showlegend", True),
                        marker=dict(
                            color=trace_props['marker_color'],
                            size=trace_props['marker_size'],
                            symbol=trace_props['marker_symbol'],
                        ),
                        boxpoints='all',
                        jitter=min(self.height * 2, 1.0),
                        pointpos=0,
                        orientation='h',
                        line=dict(color='rgba(0,0,0,0)', width=0),
                        fillcolor='rgba(0,0,0,0)',
                        hoveron='points',
                    ),
                    row=row,
                    col=col,
                )
            else:
                # Both numeric - use scatter with manual jitter
                if indices is not None:
                    x_jitter = rng.uniform(-self.width, self.width, len(indices))
                    y_jitter_vals = rng.uniform(-self.height, self.height, len(indices))
                else:
                    x_jitter = rng.uniform(-self.width, self.width, len(x_data))
                    y_jitter_vals = rng.uniform(-self.height, self.height, len(y_data) if y_data is not None else len(x_data))

                x_plot = np.array(x_data) + x_jitter if x_data is not None else None
                y_plot = np.array(y_data) + y_jitter_vals if y_data is not None else None

                fig.add_trace(
                    go.Scatter(
                        x=x_plot,
                        y=y_plot,
                        mode="markers",
                        name=name,
                        opacity=alpha,
                        showlegend=self.params.get("showlegend", True),
                        marker_color=trace_props['marker_color'],
                        marker_size=trace_props['marker_size'],
                        marker_symbol=trace_props['marker_symbol'],
                    ),
                    row=row,
                    col=col,
                )

        # Get base x and y data
        x_base = data[x_col] if x_col and x_col in data.columns else None
        y_base = data[y_col] if y_col and y_col in data.columns else None

        # Case 1: Grouped by explicit 'group' aesthetic
        if group_values is not None:
            for group in group_values.unique():
                mask = group_values == group
                trace_props = get_trace_props(
                    value_key=group if has_color_grouping else None,
                    shape_key=group if has_shape_grouping else None
                )
                add_jitter_trace(
                    x_base[mask] if x_base is not None else None,
                    y_base[mask] if y_base is not None else None,
                    str(group), trace_props,
                    indices=np.where(mask)[0]
                )

        # Case 2: Both color and shape mapped
        elif has_color_grouping and has_shape_grouping:
            same_column = cat_col == shape_col
            for color_val in cat_map.keys():
                for shape_val in shape_map.keys():
                    mask = (data[cat_col] == color_val) & (data[shape_col] == shape_val)
                    if not mask.any():
                        continue
                    trace_props = get_trace_props(value_key=color_val, shape_key=shape_val)
                    legend_name = str(color_val) if same_column else f"{color_val}, {shape_val}"
                    add_jitter_trace(
                        x_base[mask] if x_base is not None else None,
                        y_base[mask] if y_base is not None else None,
                        legend_name, trace_props,
                        indices=np.where(mask)[0]
                    )

        # Case 3: Only color mapped
        elif has_color_grouping:
            for cat_value in cat_map.keys():
                mask = data[cat_col] == cat_value
                trace_props = get_trace_props(value_key=cat_value)
                add_jitter_trace(
                    x_base[mask] if x_base is not None else None,
                    y_base[mask] if y_base is not None else None,
                    str(cat_value), trace_props,
                    indices=np.where(mask)[0]
                )

        # Case 4: Only shape mapped
        elif has_shape_grouping:
            for shape_val in shape_map.keys():
                mask = data[shape_col] == shape_val
                trace_props = get_trace_props(shape_key=shape_val)
                add_jitter_trace(
                    x_base[mask] if x_base is not None else None,
                    y_base[mask] if y_base is not None else None,
                    str(shape_val), trace_props,
                    indices=np.where(mask)[0]
                )

        # Case 5: No grouping
        else:
            trace_props = get_trace_props()
            add_jitter_trace(x_base, y_base, self.params.get("name", "Jitter"), trace_props)
