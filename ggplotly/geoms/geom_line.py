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

        # Set default line width to 2 if not specified
        if "size" not in self.params:
            self.params["size"] = 2

        # Remove size from mapping if present - lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        line_dash = self.params.get("linetype", "solid")
        name = self.params.get("name", "Line")

        # Handle Plotly's fill parameter (tonexty, tozeroy, etc.) separately from fill aesthetic
        # Check if fill is a Plotly fill mode string (not a color aesthetic)
        fill_param = self.params.get("fill", None)
        plotly_fill = None
        if fill_param in ['tonexty', 'tozeroy', 'tonextx', 'tozerox', 'toself', 'tonext']:
            # This is a Plotly fill mode, not a color aesthetic
            plotly_fill = fill_param
            # Temporarily remove from params so AestheticMapper doesn't treat it as a fill aesthetic
            original_fill = self.params.pop("fill", None)

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=plotly_fill,
        )

        color_targets = dict(
            fill="line_color",  # Both fill and color map to line_color for lines
            color="line_color",
            size="line_width",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)

        # Restore fill parameter if it was removed
        if plotly_fill is not None:
            self.params["fill"] = original_fill
