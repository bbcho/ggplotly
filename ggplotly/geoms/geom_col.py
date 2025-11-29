# geoms/geom_col.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_col(Geom):
    """
    Geom for drawing column plots (similar to bar plots).

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the columns.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        group (str, optional): Grouping variable for the columns.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_col()
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + geom_col()
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw column(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        payload = dict()
        payload["name"] = self.params.get("name", "Column")

        # Note: opacity/alpha is handled by _transform_fig via AestheticMapper
        # Don't add it to payload to avoid duplicate keyword argument

        plot = go.Bar

        color_targets = dict(
            fill="marker_color",
            color="marker_color",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
