# geoms/geom_segment.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_segment(Geom):
    """
    Geom for drawing line segments.

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        xend (float): End x-coordinate of the line segment.
        yend (float): End y-coordinate of the line segment.
        color (str, optional): Color of the segment lines.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the segments. Default is 1.
        group (str, optional): Grouping variable for the segments.
    """

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 2
        data = data if data is not None else self.data

        # Create aesthetic mapper for this geom
        from ..aesthetic_mapper import AestheticMapper
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        xend = data[self.mapping["xend"]]
        yend = data[self.mapping["yend"]]

        linetype = self.params.get("linetype", "solid")
        alpha = style_props['alpha']
        group_values = style_props['group_series']

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
                    fig.add_trace(
                        go.Scatter(
                            x=[x[idx], xend[idx]],
                            y=[y[idx], yend[idx]],
                            mode="lines",
                            line_dash=linetype,
                            opacity=alpha,
                            name=str(group),
                            legendgroup=str(group),
                            showlegend=(i == 0),  # Only show legend for first segment
                            **trace_props,
                        ),
                        row=row,
                        col=col,
                    )
        elif style_props['color_series'] is not None:
            # Case 2: Colored by categorical variable
            cat_series = style_props['color_series']
            cat_map = style_props['color_map']
            cat_col = style_props['color']

            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value
                trace_props = self._apply_color_targets(color_targets, style_props, value_key=cat_value)

                # Create separate segments for each data point in the category
                for i, idx in enumerate(data[cat_mask].index):
                    fig.add_trace(
                        go.Scatter(
                            x=[x[idx], xend[idx]],
                            y=[y[idx], yend[idx]],
                            mode="lines",
                            line_dash=linetype,
                            opacity=alpha,
                            name=str(cat_value),
                            legendgroup=str(cat_value),
                            showlegend=(i == 0),  # Only show legend for first segment
                            **trace_props,
                        ),
                        row=row,
                        col=col,
                    )
        else:
            # Case 3: No grouping or categorical coloring - single trace per segment
            trace_props = self._apply_color_targets(color_targets, style_props)

            for i, idx in enumerate(data.index):
                fig.add_trace(
                    go.Scatter(
                        x=[x[idx], xend[idx]],
                        y=[y[idx], yend[idx]],
                        mode="lines",
                        line_dash=linetype,
                        opacity=alpha,
                        name=self.params.get("name", "Segment"),
                        legendgroup="segment",
                        showlegend=(i == 0),  # Only show legend for first segment
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )
