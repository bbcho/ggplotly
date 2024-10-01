# geoms/geom_violin.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_violin(Geom):
    """
    Geom for drawing violin plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the violins.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        color (str, optional): Outline color of the violin plots.
        linewidth (float, optional): Line width of the violin outline.
        group (str, optional): Grouping variable for the violin plots.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 0.5)
        linewidth = self.params.get("linewidth", 1)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        outline_color = self.params.get("color", "black")
        fill_color = color_info["fill_colors"]

        # Draw violin traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Violin(
                        x=x[group_mask],
                        y=y[group_mask],
                        fillcolor=(
                            group_values[group_mask].iloc[0]
                            if group_values is not None
                            else fill_color
                        ),
                        line=dict(color=outline_color, width=linewidth),
                        opacity=alpha,
                        name=str(group),
                        box_visible=True,  # Optional: to show inner box plot
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Violin(
                    x=x,
                    y=y,
                    fillcolor=fill_color,
                    line=dict(color=outline_color, width=linewidth),
                    opacity=alpha,
                    name=self.params.get("name", "Violin"),
                    box_visible=True,  # Optional: to show inner box plot
                ),
                row=row,
                col=col,
            )
