# geoms/geom_col.py

import plotly.graph_objects as go

from ._bar_positioning import compute_bar_trace_specs
from .geom_base import Geom


class geom_col(Geom):
    """
    Geom for drawing column plots (similar to bar plots).

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        fill (str, optional): Fill color for the columns.
        color (str, optional): Border color for the columns.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        width (float, optional): Width of the bars as fraction of available space.
            Default is 0.9. Values should be between 0 and 1.
        group (str, optional): Grouping variable for the columns.
        na_rm (bool, optional): If True, remove missing values. Default is False.
        show_legend (bool, optional): Whether to show in legend. Default is True.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_col()
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + geom_col()
        >>> ggplot(df, aes(x='category', y='value')) + geom_col(width=0.5)
    """

    required_aes = ['x', 'y']
    default_params = {"alpha": 1, "width": 0.9}

    def _draw_impl(self, fig, data, row, col):
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

        style_props = self._get_style_props(data)
        result = compute_bar_trace_specs(data, self.mapping, self.params, style_props, "Column")

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
