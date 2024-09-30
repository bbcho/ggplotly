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
        color_values = data[self.mapping["fill"]] if "fill" in self.mapping else None
        fill_color = self.params.get("fill", "lightblue")
        alpha = self.params.get("alpha", 0.5)
        linetype = self.params.get("linetype", "solid")

        # Handle fill mapping if fill is categorical
        if color_values is not None:
            if not pd.api.types.is_categorical_dtype(color_values):
                data[self.mapping["fill"]] = pd.Categorical(color_values)
                color_values = data[self.mapping["fill"]]

            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            color_values = color_values.map(color_map)

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
                                color_values[group_mask].iloc[0]
                                if color_values is not None
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
