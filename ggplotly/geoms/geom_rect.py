# geoms/geom_rect.py

import plotly.graph_objects as go

from .geom_base import Geom


class geom_rect(Geom):
    """
    Geom for drawing rectangles.

    Rectangles are defined by their corner coordinates (xmin, xmax, ymin, ymax).
    Useful for highlighting regions, drawing backgrounds, or creating custom shapes.

    Parameters:
        fill (str, optional): Fill color for the rectangles. Default is theme color.
        color (str, optional): Border color for the rectangles. Default is None (no border).
        alpha (float, optional): Transparency level (0-1). Default is 0.5.
        linetype (str, optional): Border line style ('solid', 'dash', 'dot', 'dashdot').
            Default is 'solid'.
        size (float, optional): Border line width. Default is 1.
        linewidth (float, optional): Alias for size (ggplot2 3.4+ compatibility).

    Aesthetics:
        - xmin: Left edge of rectangle (required)
        - xmax: Right edge of rectangle (required)
        - ymin: Bottom edge of rectangle (required)
        - ymax: Top edge of rectangle (required)
        - fill: Fill color (optional, can be mapped to variable)
        - color: Border color (optional)
        - group: Grouping variable (optional)

    Examples:
        >>> # Highlight a region
        >>> df = pd.DataFrame({'xmin': [2], 'xmax': [4], 'ymin': [1], 'ymax': [3]})
        >>> ggplot(df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax')) + geom_rect()

        >>> # Multiple rectangles with fill mapping
        >>> df = pd.DataFrame({
        ...     'xmin': [1, 3], 'xmax': [2, 4],
        ...     'ymin': [1, 2], 'ymax': [3, 4],
        ...     'category': ['A', 'B']
        ... })
        >>> ggplot(df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax', fill='category')) + geom_rect()

        >>> # Rectangle with border
        >>> ggplot(df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax')) + geom_rect(
        ...     fill='lightblue', color='navy', size=2
        ... )

        >>> # Highlight region on existing plot
        >>> highlight = pd.DataFrame({'xmin': [2], 'xmax': [4], 'ymin': [0], 'ymax': [10]})
        >>> (ggplot(data, aes(x='x', y='y'))
        ...  + geom_rect(data=highlight, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
        ...              fill='yellow', alpha=0.3)
        ...  + geom_point())
    """

    required_aes = ['xmin', 'xmax', 'ymin', 'ymax']
    default_params = {"alpha": 0.5, "size": 1, "linetype": "solid"}

    def _draw_impl(self, fig, data, row, col):
        style_props = self._get_style_props(data)

        xmin = data[self.mapping["xmin"]]
        xmax = data[self.mapping["xmax"]]
        ymin = data[self.mapping["ymin"]]
        ymax = data[self.mapping["ymax"]]

        linetype = self.params.get("linetype", "solid")
        linewidth = style_props.get("size", 1)
        alpha = style_props["alpha"]
        group_values = style_props["group_series"]

        # Border color - use 'color' param or None for no border
        border_color = self.params.get("color", None)

        color_targets = dict(fill="fillcolor")

        def add_rect_trace(x_min, x_max, y_min, y_max, fill_color, name, showlegend=True, legendgroup=None):
            """Helper to add a single rectangle as a filled scatter trace."""
            # Create rectangle path (clockwise from bottom-left)
            x_path = [x_min, x_min, x_max, x_max, x_min]
            y_path = [y_min, y_max, y_max, y_min, y_min]

            line_config = None
            if border_color:
                line_config = dict(color=border_color, width=linewidth, dash=linetype)

            fig.add_trace(
                go.Scatter(
                    x=x_path,
                    y=y_path,
                    mode="lines",
                    fill="toself",
                    fillcolor=fill_color,
                    line=line_config if line_config else dict(width=0),
                    opacity=alpha,
                    name=name,
                    legendgroup=legendgroup or name,
                    showlegend=showlegend,
                    hoverinfo="name",
                ),
                row=row,
                col=col,
            )

        # Handle grouped or colored rectangles
        if group_values is not None:
            # Case 1: Grouped by 'group' aesthetic
            for group in group_values.unique():
                group_mask = group_values == group
                if style_props["fill_series"] is not None:
                    trace_props = self._apply_color_targets(color_targets, style_props, value_key=group)
                else:
                    trace_props = self._apply_color_targets(color_targets, style_props)

                fill_color = trace_props.get("fillcolor", style_props["default_color"])

                for i, idx in enumerate(data[group_mask].index):
                    add_rect_trace(
                        xmin[idx], xmax[idx], ymin[idx], ymax[idx],
                        fill_color, str(group),
                        showlegend=(i == 0),
                        legendgroup=str(group)
                    )

        elif style_props["fill_series"] is not None:
            # Case 2: Fill mapped to categorical variable
            fill_map = style_props["fill_map"]
            fill_col = style_props["fill"]

            for cat_value in fill_map.keys():
                cat_mask = data[fill_col] == cat_value
                trace_props = self._apply_color_targets(color_targets, style_props, value_key=cat_value)
                fill_color = trace_props.get("fillcolor", style_props["default_color"])

                for i, idx in enumerate(data[cat_mask].index):
                    add_rect_trace(
                        xmin[idx], xmax[idx], ymin[idx], ymax[idx],
                        fill_color, str(cat_value),
                        showlegend=(i == 0),
                        legendgroup=str(cat_value)
                    )

        elif style_props["color_series"] is not None:
            # Case 3: Color mapped to categorical variable (use for fill)
            color_map = style_props["color_map"]
            color_col = style_props["color"]

            for cat_value in color_map.keys():
                cat_mask = data[color_col] == cat_value
                fill_color = color_map.get(cat_value, style_props["default_color"])

                for i, idx in enumerate(data[cat_mask].index):
                    add_rect_trace(
                        xmin[idx], xmax[idx], ymin[idx], ymax[idx],
                        fill_color, str(cat_value),
                        showlegend=(i == 0),
                        legendgroup=str(cat_value)
                    )

        else:
            # Case 4: No grouping - single color for all rectangles
            # Check for explicit fill param first (literal color value)
            fill_color = self.params.get("fill")
            if fill_color is None:
                trace_props = self._apply_color_targets(color_targets, style_props)
                fill_color = trace_props.get("fillcolor", style_props["default_color"])

            name = self.params.get("name", "Rectangle")
            for i, idx in enumerate(data.index):
                add_rect_trace(
                    xmin[idx], xmax[idx], ymin[idx], ymax[idx],
                    fill_color, name,
                    showlegend=(i == 0),
                    legendgroup="rect"
                )
