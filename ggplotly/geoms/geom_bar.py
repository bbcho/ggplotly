# geoms/geom_bar.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_bar(Geom):
    """
    Geom for drawing bar plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        color (str, optional): Color of the bars. If a categorical variable is mapped to color, different colors will be assigned.
        group (str, optional): Grouping variable for the bars.
        fill (str, optional): Fill color for the bars.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        showlegend (bool, optional): Whether to show legend entries. Default is True.
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draws a bar plot on the given figure.

        Automatically converts columns to categorical if necessary and
        maps categorical variables to colors.

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
        color_values = (
            data[self.mapping["fill"]] if "fill" in self.mapping else None
        )  # Use 'fill' for color mapping
        fill_color = self.params.get("fill", "lightblue")
        alpha = self.params.get("alpha", 1)

        # Automatically convert 'group' and 'fill' columns to categorical if necessary
        if group_values is not None and not pd.api.types.is_categorical_dtype(
            group_values
        ):
            data[self.mapping["group"]] = pd.Categorical(group_values)
            group_values = data[self.mapping["group"]]

        if color_values is not None and not pd.api.types.is_categorical_dtype(
            color_values
        ):
            data[self.mapping["fill"]] = pd.Categorical(color_values)
            color_values = data[self.mapping["fill"]]

        # If 'fill' is categorical, map to colors automatically
        if color_values is not None:
            unique_colors = color_values.unique()
            color_map = {
                val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
                for i, val in enumerate(unique_colors)
            }
            color_values = color_values.map(
                color_map
            )  # Apply color map to the fill aesthetic

        # Generate bars based on groups and categories
        if group_values is not None:
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    marker=dict(
                        color=color_values,  # Pass the color series
                    ),
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    name=self.params.get("name", "Bar"),
                ),
                row=row,
                col=col,
            )
        else:
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    marker_color=(
                        color_values.iloc[0] if color_values is not None else fill_color
                    ),
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    name=self.params.get("name", "Bar"),
                ),
                row=row,
                col=col,
            )
