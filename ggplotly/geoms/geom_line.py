# geoms/geom_line.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
import pandas as pd


class geom_line(Geom):
    """
    Geom for drawing line plots, sorted by x-axis values.

    Connects points in order of x-axis values (sorted). For connecting points
    in data order (unsorted), use geom_path instead.

    Parameters:
        color (str, optional): Color of the lines. If not provided, will use the theme's color palette.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        size (float, optional): Line width. Default is 2.
        group (str, optional): Grouping variable for the lines.

    Aesthetics:
        - x: x-axis values (data will be sorted by this)
        - y: y-axis values
        - color: Grouping variable for colored lines
        - group: Grouping variable for separate lines

    See Also:
        geom_path: Connect points in data order (no sorting)
    """

    __name__ = "geom_line"

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw line(s) on the figure, sorted by x-axis values.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Sort data by x-axis (key difference from geom_path)
        x_col = self.mapping.get("x")
        if x_col and x_col in data.columns:
            data = data.sort_values(by=x_col).reset_index(drop=True)

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
