# geoms/geom_abline.py

import plotly.graph_objects as go
from .geom_base import Geom
import numpy as np


class geom_abline(Geom):
    """Geom for drawing lines with specified slope and intercept."""

    __name__ = "geom_abline"

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw lines defined by slope and intercept (y = intercept + slope * x).

        Useful for adding regression lines, reference lines, or theoretical
        relationships to plots.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings (typically not used for abline).
        slope : float or list, default=1
            Slope(s) of the line(s).
        intercept : float or list, default=0
            Y-intercept(s) of the line(s).
        color : str, default='black'
            Line color.
        linetype : str, default='solid'
            Line style: 'solid', 'dash', 'dot', 'dashdot'.
        size : float, default=1
            Line width.
        alpha : float, default=1
            Transparency (0-1).
        name : str, optional
            Name for the legend.

        Examples
        --------
        >>> geom_abline(slope=1, intercept=0)  # y = x line
        >>> geom_abline(slope=0.5, intercept=2, color='red', linetype='dash')
        >>> geom_abline(slope=[1, 2], intercept=[0, -1])  # multiple lines
        """
        super().__init__(data, mapping, **params)
        self.slope = params.get('slope', 1)
        self.intercept = params.get('intercept', 0)

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 1

        # Get color from params, or use theme default
        color = self.params.get("color", None)
        if color is None and hasattr(self, 'theme') and self.theme:
            import plotly.express as px
            palette = self.theme.color_map if hasattr(self.theme, 'color_map') and self.theme.color_map else px.colors.qualitative.Plotly
            color = palette[0]
        elif color is None:
            color = 'black'

        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)
        line_width = self.params.get("size", 1)
        name = self.params.get("name", "abline")

        # Handle single values or lists
        slopes = self.slope if isinstance(self.slope, (list, tuple)) else [self.slope]
        intercepts = self.intercept if isinstance(self.intercept, (list, tuple)) else [self.intercept]

        # If one is shorter, extend it
        max_len = max(len(slopes), len(intercepts))
        if len(slopes) < max_len:
            slopes = slopes * max_len
        if len(intercepts) < max_len:
            intercepts = intercepts * max_len

        # Get current axis ranges to determine line extent
        # We'll use a wide range and let Plotly clip it
        x_range = [-1e10, 1e10]

        for i, (slope, intercept) in enumerate(zip(slopes, intercepts)):
            # Calculate y values at the x range boundaries
            y_start = intercept + slope * x_range[0]
            y_end = intercept + slope * x_range[1]

            # Create the line trace
            trace_name = name if len(slopes) == 1 else f"{name}_{i+1}"

            fig.add_trace(
                go.Scatter(
                    x=x_range,
                    y=[y_start, y_end],
                    mode="lines",
                    line=dict(color=color, dash=linetype, width=line_width),
                    opacity=alpha,
                    name=trace_name,
                    showlegend=self.params.get("showlegend", False),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
