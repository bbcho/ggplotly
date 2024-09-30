# geoms/geom_boxplot.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_boxplot(Geom):
    """
    Geom for drawing boxplots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        color (str, optional): Outline color of the boxplot.
        fill (str, optional): Fill color for the boxplots.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["fill"]] if "fill" in self.mapping else None
        fill_color = self.params.get("fill", "lightblue")  # Default fill color
        alpha = self.params.get("alpha", 1)

        # Handle fill and color mapping if fill is categorical
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

        # Draw boxplot traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Box(
                        x=x[group_mask],
                        y=y[group_mask],
                        marker_color=(
                            color_values[group_mask].iloc[0]
                            if color_values is not None
                            else fill_color
                        ),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Box(
                    x=x,
                    y=y,
                    marker_color=fill_color,
                    opacity=alpha,
                    name=self.params.get("name", "Boxplot"),
                ),
                row=row,
                col=col,
            )
