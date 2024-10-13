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

    def __init__(self, data=None, mapping=None, bin=30, barmode="stack", **params):

        super().__init__(data, mapping, **params)
        self.bin = bin
        self.barmode = barmode

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
        payload = dict()
        data = data if data is not None else self.data

        plot = go.Histogram

        payload["name"] = self.params.get("name", "Histogram")
        payload["nbinsx"] = self.bin

        color_targets = dict(
            # fill="marker_fill",
            # fill="fillcolor",
            color="marker_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(
            plot,
            fig,
            data,
            payload,
            color_targets,
            row,
            col,
            barmode=self.barmode,
        )
