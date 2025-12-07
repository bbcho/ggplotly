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
        hjust (float, optional): Horizontal justification (0=left, 0.5=center, 1=right).
            Default is 0.5 (centered). Maps to Plotly textposition.
        vjust (float, optional): Vertical justification (0=bottom, 0.5=middle, 1=top).
            Default is 0.5 (middle). Maps to Plotly textposition.
        angle (float, optional): Rotation angle in degrees (counter-clockwise). Default is 0.
        nudge_x (float, optional): Horizontal offset to apply to text position. Default is 0.
        nudge_y (float, optional): Vertical offset to apply to text position. Default is 0.
        check_overlap (bool, optional): If True, text that overlaps previous text will not
            be plotted. Default is False. Note: Limited support in Plotly.
        size (float, optional): Text size in points. Default is 11.
        family (str, optional): Font family. Default is None (use Plotly default).
        fontface (str, optional): Font face ('plain', 'bold', 'italic', 'bold.italic').
            Default is 'plain'.
        na_rm (bool, optional): If True, silently remove missing values. Default is False.
        textposition (str, optional): Direct Plotly textposition override
            ('top center', 'middle right', etc.). If provided, overrides hjust/vjust.
        color (str, optional): Color of the text labels.
        alpha (float, optional): Transparency level for the text labels. Default is 1.
        group (str, optional): Grouping variable for the text labels.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text()
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text(hjust=0, vjust=1)  # top-left
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text(angle=45)
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_text(nudge_y=0.5)
    """

    def _hjust_vjust_to_textposition(self, hjust, vjust):
        """
        Convert hjust/vjust values to Plotly textposition string.

        Parameters:
            hjust (float): Horizontal justification (0=left, 0.5=center, 1=right)
            vjust (float): Vertical justification (0=bottom, 0.5=middle, 1=top)

        Returns:
            str: Plotly textposition string like 'top left', 'middle center', etc.
        """
        # Determine vertical position
        if vjust <= 0.25:
            v_pos = "bottom"
        elif vjust >= 0.75:
            v_pos = "top"
        else:
            v_pos = "middle"

        # Determine horizontal position
        if hjust <= 0.25:
            h_pos = "left"
        elif hjust >= 0.75:
            h_pos = "right"
        else:
            h_pos = "center"

        return f"{v_pos} {h_pos}"

    def _fontface_to_plotly(self, fontface):
        """Convert R-style fontface to Plotly font properties."""
        if fontface == "bold":
            return {"weight": "bold"}
        elif fontface == "italic":
            return {"style": "italic"}
        elif fontface == "bold.italic":
            return {"weight": "bold", "style": "italic"}
        return {}  # plain

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

        # Handle na_rm parameter
        na_rm = self.params.get("na_rm", False)
        if na_rm:
            # Remove rows with NA in x, y, or label columns
            cols_to_check = [self.mapping["x"], self.mapping["y"], self.mapping["label"]]
            data = data.dropna(subset=cols_to_check)

        # Create aesthetic mapper for this geom
        from ..aesthetic_mapper import AestheticMapper
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x = data[self.mapping["x"]].copy()
        y = data[self.mapping["y"]].copy()
        label = data[self.mapping["label"]]  # Use 'label' mapping instead of 'text'

        # Apply nudge offsets
        nudge_x = self.params.get("nudge_x", 0)
        nudge_y = self.params.get("nudge_y", 0)
        if nudge_x != 0:
            x = x + nudge_x
        if nudge_y != 0:
            y = y + nudge_y

        # Determine text position from hjust/vjust or direct textposition
        if "textposition" in self.params:
            textposition = self.params["textposition"]
        else:
            hjust = self.params.get("hjust", 0.5)
            vjust = self.params.get("vjust", 0.5)
            textposition = self._hjust_vjust_to_textposition(hjust, vjust)

        # Get angle parameter (note: Plotly uses clockwise, R uses counter-clockwise)
        angle = self.params.get("angle", 0)
        textangle = -angle if angle != 0 else None  # Convert to Plotly convention

        # Get text styling parameters
        text_size = self.params.get("size", 11)
        font_family = self.params.get("family", None)
        fontface = self.params.get("fontface", "plain")
        font_props = self._fontface_to_plotly(fontface)

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
