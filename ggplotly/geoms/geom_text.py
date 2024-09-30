# geoms/geom_text.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_text(Geom):
    """
    Geom for adding text labels to a plot.

    Automatically handles categorical variables for color and text.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        textposition (str, optional): Position of the text relative to the data points ('top center', 'middle right', etc.).
        color (str, optional): Color of the text labels.
        alpha (float, optional): Transparency level for the text labels. Default is 1.
        group (str, optional): Grouping variable for the text labels.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        label = data[self.mapping["label"]]  # Use 'label' mapping instead of 'text'
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        color_values = data[self.mapping["color"]] if "color" in self.mapping else None
        textposition = self.params.get("textposition", "top center")
        alpha = self.params.get("alpha", 1)
        text_color = self.params.get("color", "black")

        # Handle color mapping if color is categorical
        if color_values is not None:
            if not pd.api.types.is_categorical_dtype(color_values):
                # Use .loc to avoid SettingWithCopyWarning
                data.loc[:, self.mapping["color"]] = pd.Categorical(color_values)
                color_values = data[self.mapping["color"]]

            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            # Use .loc to avoid SettingWithCopyWarning when mapping colors
            color_values = color_values.map(color_map)

        # Draw text traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        mode="text",
                        text=label[group_mask],
                        textposition=textposition,
                        textfont=dict(
                            color=(
                                color_values[group_mask].iloc[0]
                                if color_values is not None
                                else text_color
                            )
                        ),
                        opacity=alpha,
                        showlegend=False,
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
                    mode="text",
                    text=label,
                    textposition=textposition,
                    textfont=dict(color=text_color),
                    opacity=alpha,
                    showlegend=False,
                    name=self.params.get("name", "Text"),
                ),
                row=row,
                col=col,
            )
