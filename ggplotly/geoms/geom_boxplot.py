# geoms/geom_boxplot.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_boxplot(Geom):
    """
    Geom for drawing boxplots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        color (str, optional): Outline color of the boxplot.
        fill (str, optional): Fill color for the boxplots.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None

        alpha = self.params.get("alpha", 1)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        color_values = color_info["color_values"]
        fill_color = color_info["fill_colors"]

        # Draw boxplot traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Box(
                        x=x[group_mask],
                        y=y[group_mask],
                        marker_color=(
                            color_values[group_mask].iloc[0]
                            if color_values is not None
                            else fill_color
                        ),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Box(
                    x=x,
                    y=y,
                    marker_color=fill_color,
                    opacity=alpha,
                    name=self.params.get("name", "Boxplot"),
                ),
                row=row,
                col=col,
            )
