from .geom_base import Geom
import pandas as pd


class geom_hline(Geom):
    """
    Geom for drawing horizontal lines.

    Parameters:
        data (float or list of floats): The y-coordinate(s) where the horizontal line(s) should be drawn.
            Same as yintercept in ggplot2.
        color (str, optional): Color of the lines. Default is 'black'.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        name (str, optional): Name of the line(s) for the legend.

    Examples:
        geom_hline(data=100)
        geom_hline(data=[50, 100, 150], color='red')
    """

    __name__ = "geom_hline"

    def __init__(self, data=None, mapping=None, **params):
        # data parameter is the yintercept value (matching ggplot2's data parameter)
        if data is not None:
            params['yintercept'] = data
        super().__init__(None, mapping, **params)

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 2

        # Get yintercept from params (ggplot2 convention)
        y = self.params.get("yintercept", None)

        # Fallback to y param if yintercept not provided
        if y is None:
            y = self.params.get("y", None)

        if y is None:
            raise ValueError("Parameter 'yintercept' must be provided for geom_hline")

        if not isinstance(y, list):
            y = [y]

        # Get color from params, or use theme default
        color = self.params.get("color", None)
        if color is None and hasattr(self, 'theme') and self.theme:
            # Use first color from theme palette
            import plotly.express as px
            palette = self.theme.color_map if hasattr(self.theme, 'color_map') and self.theme.color_map else px.colors.qualitative.Plotly
            color = palette[0]
        elif color is None:
            # Default to theme's default color
            color = '#1f77b4'

        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)
        name = self.params.get("name", "hline")

        for y_coord in y:
            fig.add_hline(
                y=y_coord,
                line=dict(color=color, dash=linetype, width=2),
                opacity=alpha,
                row=row,
                col=col,
                name=name,
            )
