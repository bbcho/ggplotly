# geoms/geom_text.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_text(Geom):
    """
    Geom for adding text labels to a plot.

    Automatically handles categorical variables for color and text.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        textposition (str, optional): Position of the text relative to the data points ('top center', 'middle right', etc.).
        color (str, optional): Color of the text labels.
        alpha (float, optional): Transparency level for the text labels. Default is 1.
        group (str, optional): Grouping variable for the text labels.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text()
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text(textposition='top right')
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw text labels on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Create aesthetic mapper for this geom
        from ..aesthetic_mapper import AestheticMapper
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        label = data[self.mapping["label"]]  # Use 'label' mapping instead of 'text'

        textposition = self.params.get("textposition", "top center")
        alpha = style_props['alpha']
        group_values = style_props['group_series']

        color_targets = dict(color="textfont_color")

        # Draw text traces
        if group_values is not None:
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
                        mode="text",
                        text=label[group_mask],
                        textposition=textposition,
                        opacity=alpha,
                        showlegend=False,
                        name=str(group),
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )
        elif style_props['color_series'] is not None:
            # Case 2: Colored by categorical variable
            cat_series = style_props['color_series']
            cat_map = style_props['color_map']
            cat_col = style_props['color']

            for cat_value in cat_map.keys():
                cat_mask = data[cat_col] == cat_value
                trace_props = self._apply_color_targets(color_targets, style_props, value_key=cat_value)

                fig.add_trace(
                    go.Scatter(
                        x=x[cat_mask],
                        y=y[cat_mask],
                        mode="text",
                        text=label[cat_mask],
                        textposition=textposition,
                        opacity=alpha,
                        showlegend=False,
                        name=str(cat_value),
                        **trace_props,
                    ),
                    row=row,
                    col=col,
                )
        else:
            trace_props = self._apply_color_targets(color_targets, style_props)

            fig.add_trace(
                go.Scatter(
                    x=x,
                    y=y,
                    mode="text",
                    text=label,
                    textposition=textposition,
                    opacity=alpha,
                    showlegend=False,
                    name=self.params.get("name", "Text"),
                    **trace_props,
                ),
                row=row,
                col=col,
            )
