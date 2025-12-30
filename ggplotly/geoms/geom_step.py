# geoms/geom_step.py

import plotly.graph_objects as go

from ..stats.stat_ecdf import stat_ecdf
from .geom_base import Geom


class geom_step(Geom):
    """
    Geom for drawing step plots.

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        color (str, optional): Color of the steps.
        colour (str, optional): Alias for color (British spelling).
        size (float, optional): Line width. Default is 2.
        linewidth (float, optional): Alias for size (ggplot2 3.4+ compatibility).
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the steps. Default is 1.
        group (str, optional): Grouping variable for the steps.
        stat (str, optional): The statistical transformation to use. Default is 'identity'.
            Use 'ecdf' for empirical cumulative distribution function.
        na_rm (bool, optional): If True, remove missing values. Default is False.
        show_legend (bool, optional): Whether to show in legend. Default is True.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_step()
        >>> ggplot(df, aes(x='x')) + geom_step(stat='ecdf')
    """

    required_aes = ['x']  # y is optional when stat='ecdf'
    default_params = {"size": 2}

    def _apply_stats(self, data):
        """Add stat_ecdf if stat='ecdf'."""
        if self.stats == []:
            stat = self.params.get("stat", "identity")
            if stat == "ecdf":
                self.stats.append(stat_ecdf(mapping=self.mapping))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):

        # Remove size from mapping if present - step lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

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
