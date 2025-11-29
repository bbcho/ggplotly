# geoms/geom_density.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde
import plotly.express as px
import pandas as pd


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
        if "size" not in self.params:
            self.params["size"] = 2
        data = data if data is not None else self.data

        # Remove size from mapping if present - density lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        # Transform data into inputs to produce a density plot using go.Scatter
        x = data[self.mapping["x"]]
        kde = gaussian_kde(x)
        x_grid = np.linspace(x.min(), x.max(), 1000)
        y = kde(x_grid)

        self.mapping["y"] = "density"
        data = pd.DataFrame({self.mapping["x"]: x_grid, self.mapping["y"]: y})

        # Handle Plotly's fill parameter (tonexty, tozeroy, etc.) separately from fill aesthetic
        fill_param = self.params.get("fill", None)
        plotly_fill = None
        if fill_param in ['tonexty', 'tozeroy', 'tonextx', 'tozerox', 'toself', 'tonext']:
            # This is a Plotly fill mode, not a color aesthetic
            plotly_fill = fill_param
            # Temporarily remove from params so AestheticMapper doesn't treat it as a fill aesthetic
            self.params.pop("fill", None)

        line_dash = self.params.get("linetype", "solid")
        name = self.params.get("name", "Density")

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=plotly_fill,
        )

        # Restore fill parameter if it was removed
        if plotly_fill is not None:
            self.params["fill"] = plotly_fill

        color_targets = dict(
            fill="fillcolor",
            color="line_color",
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
