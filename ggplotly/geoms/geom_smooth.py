# geoms/geom_smooth.py

import plotly.graph_objects as go
import plotly.express as px
from ..stats.stat_smooth import stat_smooth
import numpy as np
from .geom_base import Geom
import pandas as pd


class geom_smooth(Geom):
    """
    Geom for drawing smooth lines (regression/LOESS/etc.).

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        method (str, optional): The smoothing method ('loess', 'lm', etc.). Default is 'loess'.
        color (str, optional): Color of the smooth lines. If a categorical variable is mapped to color, different colors will be assigned.
        linetype (str, optional): Line type ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the smooth lines. Default is 1.
        group (str, optional): Grouping variable for the smooth lines.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = (
            data.copy() if data is not None else self.data.copy()
        )  # Ensuring we are working on a copy
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["color"]] if "color" in self.mapping else None
        method = self.params.get("method", "loess")  # Default to 'loess'
        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)

        # Initialize stat_smooth for statistical smoothing
        smoother = stat_smooth(method=method)

        # Handle color mapping if color is categorical
        if color_values is not None:
            if not pd.api.types.is_categorical_dtype(color_values):
                data.loc[:, self.mapping["color"]] = pd.Categorical(
                    color_values
                )  # Fixing SettingWithCopyWarning
                color_values = data[self.mapping["color"]]

            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            color_values = color_values.map(color_map)

        # Compute smoothed values using stat_smooth
        data = smoother.compute_stat(data)

        # Generate smooth traces based on groups
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=data["y"][
                            group_mask
                        ],  # Use smoothed y-values from stat_smooth
                        mode="lines",
                        line=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else "blue"
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
                    y=data["y"],  # Use smoothed y-values from stat_smooth
                    mode="lines",
                    line=dict(color="blue", dash=linetype),
                    opacity=alpha,
                    name=self.params.get("name", "Smooth"),
                ),
                row=row,
                col=col,
            )
