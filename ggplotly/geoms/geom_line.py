# geoms/geom_line.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
import pandas as pd


class geom_line(Geom):
    """
    Geom for drawing line plots.

    Automatically handles categorical variables for color and group.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the lines. If not provided, will use the theme's color palette.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        group (str, optional): Grouping variable for the lines.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=self.params.get("linetype", "solid"),
            name=self.params.get("name", "Line"),
        )

        color_targets = dict(
            fill="line",
            color="line",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)


# class geom_line(Geom):
#     """
#     Geom for drawing line plots.

#     Automatically handles categorical variables for color.
#     Automatically converts 'group' and 'color' columns to categorical if necessary.

#     Parameters:
#         color (str, optional): Color of the lines.
#         linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
#         alpha (float, optional): Transparency level for the lines. Default is 1.
#         group (str, optional): Grouping variable for the lines.
#     """

#     def draw(self, fig, data=None, row=1, col=1):
#         data = data if data is not None else self.data
#         x = data[self.mapping["x"]]
#         y = data[self.mapping["y"]]
#         group_values = data[self.mapping["group"]] if "group" in self.mapping else None
#         color_values = data[self.mapping["color"]] if "color" in self.mapping else None
#         line_color = self.params.get("color", "blue")
#         linetype = self.params.get("linetype", "solid")
#         alpha = self.params.get("alpha", 1)

#         # Handle color mapping if color is categorical
#         if color_values is not None:
#             if not pd.api.types.is_categorical_dtype(color_values):
#                 data.loc[:, self.mapping["color"]] = pd.Categorical(
#                     color_values
#                 )  # Fixing SettingWithCopyWarning
#                 color_values = data[self.mapping["color"]]

#             unique_colors = color_values.unique()
#             color_map = {
#                 val: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)]
#                 for i, val in enumerate(unique_colors)
#             }
#             color_values = color_values.map(color_map)

#         # Draw line traces
#         if group_values is not None:
#             for group in group_values.unique():
#                 group_mask = group_values == group
#                 fig.add_trace(
#                     go.Scatter(
#                         x=x[group_mask],
#                         y=y[group_mask],
#                         mode="lines",
#                         line=dict(
#                             color=(
#                                 color_values[group_mask].iloc[0]
#                                 if color_values is not None
#                                 else line_color
#                             ),
#                             dash=linetype,
#                         ),
#                         opacity=alpha,
#                         name=str(group),
#                     ),
#                     row=row,
#                     col=col,
#                 )
#         else:
#             fig.add_trace(
#                 go.Scatter(
#                     x=x,
#                     y=y,
#                     mode="lines",
#                     line=dict(color=line_color, dash=linetype),
#                     opacity=alpha,
#                     name=self.params.get("name", "Line"),
#                 ),
#                 row=row,
#                 col=col,
#             )
