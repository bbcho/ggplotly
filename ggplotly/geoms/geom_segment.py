# geoms/geom_segment.py

import plotly.graph_objects as go

from .geom_base import Geom


class geom_segment(Geom):
    """
    Geom for drawing line segments.

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        xend (float): End x-coordinate of the line segment.
        yend (float): End y-coordinate of the line segment.
        color (str, optional): Color of the segment lines.
        colour (str, optional): Alias for color (British spelling).
        size (float, optional): Line width. Default is 2.
        linewidth (float, optional): Alias for size (ggplot2 3.4+ compatibility).
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the segments. Default is 1.
        group (str, optional): Grouping variable for the segments.
        arrow (bool, optional): If True, adds an arrowhead at the end of the segment.
            Default is False.
        arrow_size (int, optional): Size of the arrowhead. Default is 15.
        na_rm (bool, optional): If True, remove missing values. Default is False.
        show_legend (bool, optional): Whether to show in legend. Default is True.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment()
        >>> ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment(arrow=True)
    """

    required_aes = ['x', 'y', 'xend', 'yend']
    default_params = {"size": 2, "arrow": False, "arrow_size": 15}

    def _draw_impl(self, fig, data, row, col):
        style_props = self._get_style_props(data)

        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        xend = data[self.mapping["xend"]]
        yend = data[self.mapping["yend"]]

        linetype = self.params.get("linetype", "solid")
        alpha = style_props['alpha']
        group_values = style_props['group_series']

        # Arrow configuration
        arrow = self.params.get("arrow", False)
        arrow_size = self.params.get("arrow_size", 15)
        if arrow:
            mode = "lines+markers"
            marker_config = dict(
                symbol=["circle", "arrow"],
                size=[0, arrow_size],
                angleref="previous",
            )
        else:
            mode = "lines"
            marker_config = None

        color_targets = dict(color="line_color")

        # Handle grouped or colored segments
        if group_values is not None:
            # Case 1: Grouped by 'group' aesthetic
            for group in group_values.unique():
                group_mask = group_values == group
                # If color is also mapped to a column, use the group value as the key for color lookup
                if style_props['color_series'] is not None:
                    trace_props = self._apply_color_targets(color_targets, style_props, value_key=group)
                else:
                    trace_props = self._apply_color_targets(color_targets, style_props)

                # Create separate segments for each data point in the group
                for i, idx in enumerate(data[group_mask].index):
                    scatter_kwargs = dict(
                        x=[x[idx], xend[idx]],
                        y=[y[idx], yend[idx]],
                        mode=mode,
                        line_dash=linetype,
                        opacity=alpha,
                        name=str(group),
                        legendgroup=str(group),
                        showlegend=(i == 0),  # Only show legend for first segment
                        **trace_props,
                    )
                    if marker_config:
                        scatter_kwargs["marker"] = marker_config
                    fig.add_trace(go.Scatter(**scatter_kwargs), row=row, col=col)
        elif style_props['color_series'] is not None:
            # Case 2: Colored by categorical variable
            cat_map = style_props['color_map']
            cat_col = style_props['color']

            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value
                trace_props = self._apply_color_targets(color_targets, style_props, value_key=cat_value)

                # Create separate segments for each data point in the category
                for i, idx in enumerate(data[cat_mask].index):
                    scatter_kwargs = dict(
                        x=[x[idx], xend[idx]],
                        y=[y[idx], yend[idx]],
                        mode=mode,
                        line_dash=linetype,
                        opacity=alpha,
                        name=str(cat_value),
                        legendgroup=str(cat_value),
                        showlegend=(i == 0),  # Only show legend for first segment
                        **trace_props,
                    )
                    if marker_config:
                        scatter_kwargs["marker"] = marker_config
                    fig.add_trace(go.Scatter(**scatter_kwargs), row=row, col=col)
        else:
            # Case 3: No grouping or categorical coloring - single trace per segment
            trace_props = self._apply_color_targets(color_targets, style_props)

            for i, idx in enumerate(data.index):
                scatter_kwargs = dict(
                    x=[x[idx], xend[idx]],
                    y=[y[idx], yend[idx]],
                    mode=mode,
                    line_dash=linetype,
                    opacity=alpha,
                    name=self.params.get("name", "Segment"),
                    legendgroup="segment",
                    showlegend=(i == 0),  # Only show legend for first segment
                    **trace_props,
                )
                if marker_config:
                    scatter_kwargs["marker"] = marker_config
                fig.add_trace(go.Scatter(**scatter_kwargs), row=row, col=col)
