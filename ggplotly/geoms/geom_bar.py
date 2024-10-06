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
        payload = dict()
        data = data if data is not None else self.data
        data = pd.DataFrame(data).copy()

        grouping = list(set([v for k, v in self.mapping.items()]))
        grouping = [g for g in grouping if g in data.columns]

        if len(data.columns) == 1:
            tf = data.value_counts()
        else:
            tf = data.groupby(grouping).count().iloc[:, [0]]
            tf.columns = ["count"]
            tf = tf.reset_index()

        tf = tf.reset_index()

        if ("x" in self.mapping) & ("y" not in self.mapping):
            dcol = "x"
            x = list(tf[self.mapping[dcol]])
            y = list(tf["count"])
            self.mapping["x"] = self.mapping[dcol]
            self.mapping["y"] = "count"
            payload["orientation"] = "v"
        elif ("y" in self.mapping) & ("x" not in self.mapping):
            dcol = "y"
            y = list(tf[self.mapping[dcol]])
            x = list(tf["count"])
            self.mapping["y"] = self.mapping[dcol]
            self.mapping["x"] = "count"
            payload["orientation"] = "h"

        data = tf

        payload["name"] = self.params.get("name", "Bar")

        plot = go.Bar

        color_targets = dict(
            # fill="marker_fill",
            # fill="fillcolor",
            color="marker_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)

        # data = data if data is not None else self.data
        # x = data[self.mapping["x"]] if "x" in self.mapping else None
        # y = data[self.mapping["y"]] if "y" in self.mapping else None

        # if y is None:
        #     y = pd.Series(x).value_counts()
        #     x = None

        # if x is None:
        #     x = pd.Series(y).value_counts()
        #     y = None

        # # Handle grouping if a 'group' mapping is provided
        # group_values = data[self.mapping["group"]] if "group" in self.mapping else None

        # # Get shared color logic from the parent Geom class
        # color_info = self.handle_colors(data, self.mapping, self.params)
        # color_values = color_info["color_values"]
        # default_color = color_info["default_color"]
        # alpha = self.params.get("alpha", 1)

        # # Generate bars based on groups and categories
        # if group_values is not None:
        #     fig.add_trace(
        #         go.Bar(
        #             x=x,
        #             y=y,
        #             marker=dict(
        #                 color=color_values,  # Pass the color series
        #             ),
        #             opacity=alpha,
        #             showlegend=self.params.get("showlegend", True),
        #             name=self.params.get("name", "Bar"),
        #         ),
        #         row=row,
        #         col=col,
        #     )
        # else:
        #     fig.add_trace(
        #         go.Bar(
        #             x=x,
        #             y=y,
        #             marker_color=(
        #                 color_values.iloc[0]
        #                 if color_values is not None
        #                 else default_color
        #             ),
        #             opacity=alpha,
        #             showlegend=self.params.get("showlegend", True),
        #             name=self.params.get("name", "Bar"),
        #         ),
        #         row=row,
        #         col=col,
        #     )
