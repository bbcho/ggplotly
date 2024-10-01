# geoms/geom_col.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_col(Geom):
    """
    Geom for drawing column plots (similar to bar plots).

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the columns.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        group (str, optional): Grouping variable for the columns.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data.copy() if data is not None else self.data.copy()  # Ensuring a copy
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 1)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        color_values = color_info["color_values"]
        fill_color = color_info["fill_colors"]

        # Draw column traces
        if group_values is not None:
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    marker=dict(
                        color=color_values if color_values is not None else fill_color
                    ),
                    opacity=alpha,
                    name=self.params.get("name", "Column"),
                ),
                row=row,
                col=col,
            )
        else:
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    marker_color=fill_color,
                    opacity=alpha,
                    name=self.params.get("name", "Column"),
                ),
                row=row,
                col=col,
            )
