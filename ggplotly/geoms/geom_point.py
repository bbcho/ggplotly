# geoms/geom_point.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
import pandas as pd


class geom_point(Geom):
    """
    Geom for drawing point plots.

    Automatically handles categorical variables for color and group.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the points. If not provided, will use the theme's color palette.
        size (int, optional): Size of the points. Default is 10.
        alpha (float, optional): Transparency level for the points. Default is 1.
        group (str, optional): Grouping variable for the points.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        plot = go.Scatter
        payload = dict(
            mode="markers",
            name=self.params.get("name", "Point"),
        )

        color_targets = dict(
            # fill="marker",
            color="marker_color",
            size="marker_size",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
