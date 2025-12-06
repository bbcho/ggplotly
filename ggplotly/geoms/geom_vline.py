from .geom_base import Geom
import pandas as pd


class geom_vline(Geom):
    """Geom for drawing vertical reference lines."""

    __name__ = "geom_vline"

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw vertical lines at specified x-intercepts.

        Parameters
        ----------
        data : float or list of float
            X-coordinate(s) for vertical line(s). Same as xintercept.
        mapping : aes, optional
            Aesthetic mappings (typically not used for vline).
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
        >>> geom_vline(data=5)
        >>> geom_vline(data=[1, 2, 3], color='red', linetype='dash')
        """
        # data parameter is the xintercept value (matching ggplot2's data parameter)
        if data is not None:
            params['xintercept'] = data
        super().__init__(None, mapping, **params)

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 2

        # Get xintercept from params (ggplot2 convention)
        x = self.params.get("xintercept", None)

        # Fallback to x param if xintercept not provided
        if x is None:
            x = self.params.get("x", None)

        if x is None:
            raise ValueError("Parameter 'xintercept' must be provided for geom_vline")

        if not isinstance(x, list):
            x = [x]

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
        name = self.params.get("name", "vline")

        for x_coord in x:
            fig.add_vline(
                x=x_coord,
                line=dict(color=color, dash=linetype, width=2),
                opacity=alpha,
                row=row,
                col=col,
                name=name,
            )
