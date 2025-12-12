# geoms/geom_step.py

from .geom_base import Geom
import plotly.graph_objects as go
from ..stats.stat_ecdf import stat_ecdf


class geom_step(Geom):
    """
    Geom for drawing step plots.

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the steps.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the steps. Default is 1.
        group (str, optional): Grouping variable for the steps.
        stat (str, optional): The statistical transformation to use. Default is 'identity'.
    """

    def draw(self, fig, data=None, row=1, col=1):
        if "size" not in self.params:
            self.params["size"] = 2
        data = data if data is not None else self.data

        # Remove size from mapping if present - step lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        # Handle ECDF transformation using stat_ecdf
        stat = self.params.get("stat", "identity")
        if stat == "ecdf":
            ecdf_stat = stat_ecdf(mapping=self.mapping)
            data, self.mapping = ecdf_stat.compute(data)

        plot = go.Scatter
        line_dash = self.params.get("linetype", "solid")

        payload = dict(
            mode="lines",
            line_shape="hv",
            line_dash=line_dash,
            name=self.params.get("name", "Step"),
        )

        color_targets = dict(
            color="line_color",
            size="line_width",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
