# geoms/geom_area.py

from .geom_base import Geom
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px


class geom_area(Geom):
    """
    Geom for drawing area plots.

    Automatically handles continuous and categorical variables for fill.
    Automatically converts 'group' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        color (str, optional): Color of the area. If a categorical variable is mapped to color, different colors will be assigned.
        linetype (str, optional): Line type ('solid', 'dash', etc.). Default is 'solid'.
        group (str, optional): Grouping variable for the areas.
        fill (str, optional): Fill color for the area. Default is 'lightblue'.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        showlegend (bool, optional): Whether to show legend entries. Default is True.
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draws an area plot on the given figure.

        Automatically converts columns to categorical if necessary and
        maps continuous or categorical variables to colors.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Optional data subset for faceting.
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).
        """
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]

        # Handle grouping if a 'group' mapping is provided
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        fill_values = data[self.mapping["fill"]] if "fill" in self.mapping else None
        fill_color = self.params.get("fill", "lightblue")
        alpha = self.params.get("alpha", 0.5)

        # Automatically convert 'group' to categorical if necessary
        if group_values is not None and not pd.api.types.is_categorical_dtype(
            group_values
        ):
            data.loc[:, self.mapping["group"]] = pd.Categorical(group_values)
            group_values = data[self.mapping["group"]]

        # Handle fill values - map continuous data to a gradient color scale
        if fill_values is not None:
            if pd.api.types.is_numeric_dtype(fill_values):
                # Use continuous color scale for continuous data
                color_map = (
                    px.colors.sequential.Viridis
                )  # Choose any continuous color scale
                fill_values_normalized = (fill_values - fill_values.min()) / (
                    fill_values.max() - fill_values.min()
                )
                fill_colors = [
                    color_map[int(v * (len(color_map) - 1))]
                    for v in fill_values_normalized
                ]
            else:
                # Handle categorical fill as usual
                unique_colors = fill_values.unique()
                color_map = {
                    val: px.colors.qualitative.Plotly[
                        i % len(px.colors.qualitative.Plotly)
                    ]
                    for i, val in enumerate(unique_colors)
                }
                fill_colors = fill_values.map(color_map)

        # Generate areas based on groups and categories
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        fill="tozeroy",
                        line=dict(
                            color=fill_colors[group_mask].iloc[
                                0
                            ],  # Apply the fill color
                            dash=self.params.get("linetype", "solid"),
                        ),
                        fillcolor=fill_colors[group_mask].iloc[0],
                        opacity=alpha,
                        showlegend=self.params.get("showlegend", True),
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
                    fill="tozeroy",
                    line=dict(
                        color=(fill_colors[0] if fill_values is not None else "blue")
                    ),
                    fillcolor=fill_color,
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    name=self.params.get("name", "Area"),
                ),
                row=row,
                col=col,
            )
