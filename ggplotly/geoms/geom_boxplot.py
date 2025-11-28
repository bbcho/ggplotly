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

        plot = go.Box

        payload = dict(
            name=self.params.get("name", "Boxplot"),
        )

        color_targets = dict(
            fill="fillcolor",
            color="marker_color",
            size="marker_size",
        )
        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
