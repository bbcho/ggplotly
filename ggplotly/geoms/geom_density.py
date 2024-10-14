# geoms/geom_density.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import plotly.express as px
import pandas as pd


# geoms/geom_density.py

import plotly.graph_objects as go
import plotly.express as px


class geom_density(Geom):
    """
    Geom for drawing density plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the density plot.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        linetype (str, optional): Line style of the density plot ('solid', 'dash', etc.).
        group (str, optional): Grouping variable for the density plots.
    """

    def draw(self, fig, data=None, row=1, col=1):
        payload = dict()
        data = data if data is not None else self.data

        # transform data into inputs to produce a density plot
        # using go.Scatter
        x = data[self.mapping["x"]]
        kde = gaussian_kde(x)
        x_grid = np.linspace(x.min(), x.max(), 1000)
        y = kde(x_grid)

        self.mapping["y"] = "density"

        data = pd.DataFrame({self.mapping["x"]: x_grid, self.mapping["y"]: y})

        plot = go.Scatter

        payload["name"] = self.params.get("name", "Density")

        line_dash = self.params.get("linetype", "solid")
        self.params.pop("linetype", None)
        name = self.params.get("name", "Line")
        self.params.pop("name", None)
        fill = self.params.get("fill", None)
        self.params.pop("fill", None)

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=fill,
        )

        color_targets = dict(
            fill="line_fill",
            color="line_color",
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
        )
        payload = {}

        # payload["name"] = self.params.get("name", "Histogram")
        # payload["nbinsx"] = self.bin

        color_targets = dict(
            # fill="marker_fill",
            # fill="fillcolor",
            color="marker_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        data = pd.DataFrame({self.mapping["x"]: y})
        plot = go.Histogram
        self._transform_fig(
            plot,
            fig,
            data,
            payload,
            color_targets,
            row,
            col,
        )
