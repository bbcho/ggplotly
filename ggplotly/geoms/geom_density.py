# geoms/geom_density.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import plotly.express as px
import pandas as pd


# geoms/geom_density.py

import plotly.graph_objects as go
import plotly.express as px


class geom_density(Geom):
    """
    Geom for drawing density plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the density plot.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        linetype (str, optional): Line style of the density plot ('solid', 'dash', etc.).
        group (str, optional): Grouping variable for the density plots.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 0.5)
        linetype = self.params.get("linetype", "solid")

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        fill_colors = color_info["fill_colors"]

        # Draw density traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        mode="lines",
                        line=dict(
                            color=(
                                color_map[group]
                                if color_map is not None
                                else fill_color
                            ),
                            dash=linetype,
                        ),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=x,
                    mode="lines",
                    line=dict(color=fill_color, dash=linetype),
                    opacity=alpha,
                    name=self.params.get("name", "Density"),
                ),
                row=row,
                col=col,
            )
