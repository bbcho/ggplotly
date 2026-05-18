# geoms/geom_bar.py

import pandas as pd
import plotly.graph_objects as go

from ..stats.stat_count import stat_count
from ._bar_positioning import compute_bar_trace_specs
from .geom_base import Geom


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

    required_aes = ['x']  # y is computed by stat_count

    def _apply_stats(self, data):
        """Add default stat_count if no stats and stat='count'."""
        if self.stats == []:
            stat = self.params.get("stat", "count")
            if stat == "count":
                self.stats.append(stat_count(mapping=self.mapping))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        """
        Draws a bar plot on the given figure.

        Automatically converts columns to categorical if necessary and
        maps categorical variables to colors.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Data (already transformed by stats).
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).
        """
        data = pd.DataFrame(data)

        style_props = self._get_style_props(data)
        result = compute_bar_trace_specs(data, self.mapping, self.params, style_props, "Bar")

        if not hasattr(fig, '_ggplotly_shown_legendgroups'):
            fig._ggplotly_shown_legendgroups = set()

        line_width = self.params.get("linewidth", self.params.get("size", None))
        for spec in result.traces:
            show_legend = self._show_legend_once(fig, spec.legendgroup)
            outline_width = line_width if line_width is not None else (1 if spec.outline is not None else 0)
            fig.add_trace(
                go.Bar(
                    x=spec.x,
                    y=spec.y,
                    width=spec.width,
                    marker_color=spec.fill,
                    marker_line_color=spec.outline,
                    marker_line_width=outline_width,
                    opacity=style_props["alpha"],
                    name=spec.name,
                    showlegend=show_legend,
                    legendgroup=spec.legendgroup,
                    offsetgroup=spec.offsetgroup,
                ),
                row=row,
                col=col,
            )

        fig.update_yaxes(rangemode="tozero")
        if result.yaxis_range is not None:
            fig.update_yaxes(range=result.yaxis_range, row=row, col=col)
        fig.update_layout(barmode=result.barmode)

    def _show_legend_once(self, fig, legendgroup):
        if not self.params.get("showlegend", True):
            return False
        if legendgroup in fig._ggplotly_shown_legendgroups:
            return False
        fig._ggplotly_shown_legendgroups.add(legendgroup)
        return True
