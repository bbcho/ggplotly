# geoms/geom_errorbar.py

import plotly.graph_objects as go

from .geom_base import Geom


class geom_errorbar(Geom):
    """
    Geom for drawing error bars.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        ymin (float): Minimum y value for the error bar.
        ymax (float): Maximum y value for the error bar.
        color (str, optional): Color of the error bars.
        alpha (float, optional): Transparency level for the error bars. Default is 1.
        linetype (str, optional): Line style of the error bars ('solid', 'dash', etc.).
        width (float, optional): Width of the error bar caps in pixels. Default is 4.
        group (str, optional): Grouping variable for the error bars.
    """

    required_aes = ['x', 'y']  # ymin/ymax or yerr are also needed but handled in _draw_impl
    default_params = {"size": 2, "width": 4}

    def _draw_impl(self, fig, data, row, col):
        style_props = self._get_style_props(data)

        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]

        # Check for 'yerr' and calculate 'ymin' and 'ymax' if not provided
        if "yerr" in self.mapping:
            yerr = data[self.mapping["yerr"]]
            ymin = y - yerr
            ymax = y + yerr
        else:
            ymin = data[self.mapping["ymin"]]
            ymax = data[self.mapping["ymax"]]

        linetype = self.params.get("linetype", "solid")
        width = self.params.get("width", 4)
        alpha = style_props['alpha']
        group_values = style_props['group_series']

        color_targets = dict(color="marker_color")

        # Handle grouped or colored error bars
        if group_values is not None:
            # Case 1: Grouped by 'group' aesthetic
            for group in group_values.unique():
                group_mask = group_values == group
                # If color is also mapped to a column, use the group value as the key for color lookup
                if style_props['color_series'] is not None:
                    trace_props = self._apply_color_targets(color_targets, style_props, value_key=group)
                else:
                    trace_props = self._apply_color_targets(color_targets, style_props)

                fig.add_trace(
                    go.Scatter(
                        x=x[group_mask],
                        y=y[group_mask],
                        error_y=dict(
                            type="data",
                            array=ymax[group_mask] - y[group_mask],
                            arrayminus=y[group_mask] - ymin[group_mask],
                            width=width,
                        ),
                        mode="markers",
                        line_dash=linetype,
                        opacity=alpha,
                        name=str(group),
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )
        elif style_props['color_series'] is not None:
            # Case 2: Colored by categorical variable
            style_props['color_series']
            cat_map = style_props['color_map']
            cat_col = style_props['color']

            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value
                trace_props = self._apply_color_targets(color_targets, style_props, value_key=cat_value)

                fig.add_trace(
                    go.Scatter(
                        x=x[cat_mask],
                        y=y[cat_mask],
                        error_y=dict(
                            type="data",
                            array=ymax[cat_mask] - y[cat_mask],
                            arrayminus=y[cat_mask] - ymin[cat_mask],
                            width=width,
                        ),
                        mode="markers",
                        line_dash=linetype,
                        opacity=alpha,
                        name=str(cat_value),
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )
        else:
            # Case 3: No grouping or categorical coloring
            trace_props = self._apply_color_targets(color_targets, style_props)

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    error_y=dict(
                        type="data",
                        array=ymax - y,
                        arrayminus=y - ymin,
                        width=width,
                    ),
                    mode="markers",
                    line_dash=linetype,
                    opacity=alpha,
                    name=self.params.get("name", "Errorbar"),
                    **trace_props,
                ),
                row=row,
                col=col,
            )
