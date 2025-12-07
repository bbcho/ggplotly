# geoms/geom_bar.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from ..stats.stat_count import stat_count


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
        stat: ['count', 'identity', None]
            The statistical transformation to use on the data for this layer. Default is 'count'.
        width (float, optional): Bar width as a fraction of the distance between bars.
            Default is 0.9 (90% of available space). Use values between 0 and 1.
        position (str, optional): Position adjustment. Options are 'stack' (default),
            'dodge', 'fill', or 'identity'.
        na_rm (bool, optional): If True, silently remove missing values. Default is False.

    Examples:
        >>> ggplot(df, aes(x='category')) + geom_bar()
        >>> ggplot(df, aes(x='category', fill='group')) + geom_bar(position='dodge')
        >>> ggplot(df, aes(x='category')) + geom_bar(width=0.5)  # narrower bars
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

        # need this in case data is passed directly to the geom
        data = data if data is not None else self.data
        data = pd.DataFrame(data)

        if self.stats == []:
            stat = self.params.get("stat", "count")

            if stat == "count":
                self = self + stat_count()

        if ("x" in self.mapping) & ("y" not in self.mapping):
            payload["orientation"] = "v"
        elif ("y" in self.mapping) & ("x" not in self.mapping):
            payload["orientation"] = "h"

        plot = go.Bar

        for comp in self.stats:
            # stack all stats on the data
            data, self.mapping = comp.compute(data)

        payload["name"] = self.params.get("name", "Bar")

        # Apply width parameter (default 0.9 to match ggplot2)
        width = self.params.get("width", 0.9)
        payload["width"] = width

        color_targets = dict(
            # fill="marker_fill",
            # fill="fillcolor",
            color="marker_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        if "position" in self.params:
            if self.params["position"] == "dodge":
                fig.update_layout(barmode="group")
        else:
            fig.update_layout(barmode="relative")

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
