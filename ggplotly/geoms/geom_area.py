# geoms/geom_area.py

from .geom_base import Geom
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from itertools import permutations


class geom_area(Geom):
    """
    Geom for drawing area plots.

    Automatically handles continuous and categorical variables for fill.
    Automatically converts 'group' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        color (str, optional): Color of the area. If a categorical variable is mapped to color, different colors will be assigned.
        linetype (str, optional): Line type ('solid', 'dash', etc.). Default is 'solid'.
        group (str, optional): Grouping variable for the areas.
        fill (str, optional): Fill color for the area. Default is 'lightblue'.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        showlegend (bool, optional): Whether to show legend entries. Default is True.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        plot = go.Scatter
        payload = dict(
            mode="lines",
            fill="tozeroy",
            line_dash=self.params.get("linetype", "solid"),
            name=self.params.get("name", "Area"),
        )

        color_targets = dict(
            # fill="line",
            fill="fillcolor",
            color="line_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
