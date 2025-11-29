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

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_boxplot()
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + geom_boxplot()
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw boxplot(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        plot = go.Box

        payload = dict(
            name=self.params.get("name", "Boxplot"),
        )

        color_targets = dict(
            fill="fillcolor",
            color="marker_color",
            size="marker_size",
        )
        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
