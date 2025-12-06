from .geom_base import Geom
import pandas as pd


class geom_hline(Geom):
    """Geom for drawing horizontal reference lines."""

    __name__ = "geom_hline"

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw horizontal lines at specified y-intercepts.

        Parameters
        ----------
        data : float or list of float
            Y-coordinate(s) for horizontal line(s). Same as yintercept.
        mapping : aes, optional
            Aesthetic mappings (typically not used for hline).
        color : str, default='black'
            Line color.
        linetype : str, default='solid'
            Line style: 'solid', 'dash', 'dot', 'dashdot'.
        alpha : float, default=1
            Transparency (0-1).
        size : float, default=2
            Line width.
        name : str, optional
            Legend name.

        Examples
        --------
        >>> geom_hline(data=100)
        >>> geom_hline(data=[50, 100, 150], color='red', linetype='dash')
        """
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
