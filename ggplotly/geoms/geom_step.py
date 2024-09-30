# geoms/geom_step.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd


class geom_step(Geom):
    """
    Geom for drawing step plots.

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the steps.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the steps. Default is 1.
        group (str, optional): Grouping variable for the steps.
        stat (str, optional): The statistical transformation to use. Default is 'identity'.
    """

    def compute_ecdf(self, x):
        """Compute the ECDF values for a given array of x values."""
        x_sorted = np.sort(x)
        y_values = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
        return x_sorted, y_values

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        stat = self.params.get("stat", "identity")
        step_color = self.params.get("color", "blue")
        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["color"]] if "color" in self.mapping else None

        # Handle ECDF calculation if stat='ecdf'
        if stat == "ecdf":
            x, y = self.compute_ecdf(x)
        else:
            y = data[self.mapping["y"]]  # Default behavior expects 'y' mapping

        # Handle color mapping if color is categorical
        if color_values is not None:
            if not pd.api.types.is_categorical_dtype(color_values):
                data[self.mapping["color"]] = pd.Categorical(color_values)
                color_values = data[self.mapping["color"]]

            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            color_values = color_values.map(color_map)

        # Draw step traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        mode="lines",
                        line_shape="hv",
                        line=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else step_color
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
                    y=y,
                    mode="lines",
                    line_shape="hv",
                    line=dict(color=step_color, dash=linetype),
                    opacity=alpha,
                    name=self.params.get("name", "Step"),
                ),
                row=row,
                col=col,
            )
