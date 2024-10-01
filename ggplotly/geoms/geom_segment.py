# geoms/geom_segment.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


# geoms/geom_segment.py

import plotly.graph_objects as go
import plotly.express as px


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
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        xend = data[self.mapping["xend"]]
        yend = data[self.mapping["yend"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        color_values = color_info["color_values"]
        segment_color = color_info["fill_colors"]

        # Draw segment traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=[x[group_mask], xend[group_mask]],
                        y=[y[group_mask], yend[group_mask]],
                        mode="lines",
                        line=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else segment_color
                            ),
                            dash=linetype,
                        ),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=[x, xend],
                    y=[y, yend],
                    mode="lines",
                    line=dict(color=segment_color, dash=linetype),
                    opacity=alpha,
                    name=self.params.get("name", "Segment"),
                ),
                row=row,
                col=col,
            )
