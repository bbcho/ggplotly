# geoms/geom_errorbar.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_errorbar(Geom):
    """
    Geom for drawing error bars.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        ymin (float): Minimum y value for the error bar.
        ymax (float): Maximum y value for the error bar.
        color (str, optional): Color of the error bars.
        alpha (float, optional): Transparency level for the error bars. Default is 1.
        linetype (str, optional): Line style of the error bars ('solid', 'dash', etc.).
        group (str, optional): Grouping variable for the error bars.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]

        # Check for 'yerr' and calculate 'ymin' and 'ymax' if not provided
        if "yerr" in self.mapping:
            yerr = data[self.mapping["yerr"]]
            ymin = y - yerr
            ymax = y + yerr
        else:
            ymin = data[self.mapping["ymin"]]
            ymax = data[self.mapping["ymax"]]

        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["fill"]] if "fill" in self.mapping else None
        fill_color = self.params.get("fill", "lightblue")
        alpha = self.params.get("alpha", 1)
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

        # Draw error bar traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        error_y=dict(
                            type="data",
                            array=ymax[group_mask] - y[group_mask],
                            arrayminus=y[group_mask] - ymin[group_mask],
                        ),
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
                    y=y,
                    error_y=dict(type="data", array=ymax - y, arrayminus=y - ymin),
                    mode="lines",
                    line=dict(color=fill_color, dash=linetype),
                    opacity=alpha,
                    name=self.params.get("name", "Errorbar"),
                ),
                row=row,
                col=col,
            )
