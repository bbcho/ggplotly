# geoms/geom_violin.py

import plotly.graph_objects as go

from .geom_base import Geom


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

    required_aes = ['x', 'y']

    def _draw_impl(self, fig, data, row, col):
        if "linewidth" not in self.params:
            self.params["linewidth"] = 1

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
