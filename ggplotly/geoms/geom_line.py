# geoms/geom_line.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
import pandas as pd


class geom_line(Geom):
    """
    Geom for drawing line plots.

    Automatically handles categorical variables for color and group.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the lines. If not provided, will use the theme's color palette.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        group (str, optional): Grouping variable for the lines.
    """

    __name__ = "geom_line"

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        line_dash = self.params.get("linetype", "solid")
        self.params.pop("linetype", None)
        name = self.params.get("name", "Line")
        self.params.pop("name", None)
        fill = self.params.get("fill", None)
        self.params.pop("fill", None)

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=fill,
        )

        color_targets = dict(
            fill="line_fill",
            color="line_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
