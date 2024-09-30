# geoms/geom_point.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
import pandas as pd


class geom_point(Geom):
    """
    Geom for drawing scatter (point) plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the points.
        alpha (float, optional): Transparency level for the points. Default is 1.
        group (str, optional): Grouping variable for the points.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = (
            data.copy() if data is not None else self.data.copy()
        )  # Ensuring we are working on a copy
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["color"]] if "color" in self.mapping else None
        point_color = self.params.get("color", "blue")
        alpha = self.params.get("alpha", 1)

        # Handle color mapping if color is categorical
        if color_values is not None:
            if not pd.api.types.is_categorical_dtype(color_values):
                data.loc[:, self.mapping["color"]] = pd.Categorical(
                    color_values
                )  # Avoiding SettingWithCopyWarning
                color_values = data[self.mapping["color"]]

            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            color_values = color_values.map(color_map)

        # Draw point traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        mode="markers",
                        marker=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else point_color
                            )
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
                    mode="markers",
                    marker=dict(color=point_color),
                    opacity=alpha,
                    name=self.params.get("name", "Point"),
                ),
                row=row,
                col=col,
            )
