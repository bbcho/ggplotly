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
        if "linewidth" not in self.params:
            self.params["linewidth"] = 1
        data = data if data is not None else self.data

        plot = go.Violin

        payload = dict(
            name=self.params.get("name", "Violin"),
            box_visible=True,
        )

        # Note: opacity/alpha is handled by _transform_fig via AestheticMapper
        # Don't add it to payload to avoid duplicate keyword argument

        if "linewidth" in self.params:
            payload["line_width"] = self.params["linewidth"]

        color_targets = dict(
            fill="fillcolor",
            color="line_color",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
