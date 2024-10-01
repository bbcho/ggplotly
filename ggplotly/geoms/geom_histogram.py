# geoms/geom_histogram.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_histogram(Geom):
    """
    Geom for drawing histograms.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        color (str, optional): Color of the histogram bars. If a categorical variable is mapped to color, different colors will be assigned.
        group (str, optional): Grouping variable for the histogram bars.
        fill (str, optional): Fill color for the bars.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        showlegend (bool, optional): Whether to show legend entries. Default is True.
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draws a histogram on the given figure.

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

        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 1)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        color_values = color_info["color_values"]
        fill_color = color_info["fill_colors"]

        # Generate histograms based on groups and categories
        if group_values is not None:
            fig.add_trace(
                go.Histogram(
                    x=x,
                    marker=dict(
                        color=color_values,  # Pass the color series
                    ),
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    name=self.params.get("name", "Histogram"),
                ),
                row=row,
                col=col,
            )
        else:
            fig.add_trace(
                go.Histogram(
                    x=x,
                    marker_color=(
                        color_values.iloc[0] if color_values is not None else fill_color
                    ),
                    opacity=alpha,
                    showlegend=self.params.get("showlegend", True),
                    name=self.params.get("name", "Histogram"),
                ),
                row=row,
                col=col,
            )
