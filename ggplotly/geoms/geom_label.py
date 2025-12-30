# geoms/geom_label.py

import plotly.graph_objects as go

from ..aesthetic_mapper import AestheticMapper
from .geom_base import Geom


class geom_label(Geom):
    """
    Geom for adding text labels with a background box.

    Similar to geom_text but draws a rectangle behind the text for better
    readability, especially when labels overlap with data.

    Parameters:
        hjust (float, optional): Horizontal justification (0=left, 0.5=center, 1=right).
            Default is 0.5 (centered).
        vjust (float, optional): Vertical justification (0=bottom, 0.5=middle, 1=top).
            Default is 0.5 (middle).
        nudge_x (float, optional): Horizontal offset to apply to label position. Default is 0.
        nudge_y (float, optional): Vertical offset to apply to label position. Default is 0.
        size (float, optional): Text size in points. Default is 11.
        family (str, optional): Font family. Default is None (use Plotly default).
        fontface (str, optional): Font face ('plain', 'bold', 'italic', 'bold.italic').
            Default is 'plain'.
        color (str, optional): Text color. Default is 'black'.
        fill (str, optional): Background fill color. Default is 'white'.
        alpha (float, optional): Background transparency (0-1). Default is 0.8.
        label_padding (float, optional): Padding around text in pixels. Default is 4.
        label_r (float, optional): Border radius in pixels. Default is 2.
        label_size (float, optional): Border line width. Default is 0.5.
        parse (bool, optional): If True, parse text labels as LaTeX math expressions.
            Default is False.
        na_rm (bool, optional): If True, silently remove missing values. Default is False.

    Aesthetics:
        - x: x-axis position (required)
        - y: y-axis position (required)
        - label: Text to display (required)
        - color: Text color (optional)
        - fill: Background color (optional)
        - group: Grouping variable (optional)

    Examples:
        >>> # Basic label
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_label()

        >>> # Styled label
        >>> ggplot(df, aes(x='x', y='y', label='name')) + geom_label(
        ...     fill='lightblue', color='navy', size=12
        ... )

        >>> # Labels with nudge to avoid overlapping points
        >>> (ggplot(df, aes(x='x', y='y', label='name'))
        ...  + geom_point()
        ...  + geom_label(nudge_y=0.5))

        >>> # Labels colored by category
        >>> ggplot(df, aes(x='x', y='y', label='name', fill='category')) + geom_label()

    See Also:
        geom_text: Text labels without background
    """

    required_aes = ['x', 'y', 'label']

    default_params = {
        "size": 11,
        "alpha": 0.8,
        "label_padding": 4,
        "label_r": 2,
        "label_size": 0.5,
        "hjust": 0.5,
        "vjust": 0.5,
        "fill": "white",
        "color": "black",
    }

    def _hjust_vjust_to_anchor(self, hjust, vjust):
        """
        Convert hjust/vjust values to Plotly xanchor/yanchor strings.

        Parameters:
            hjust (float): Horizontal justification (0=left, 0.5=center, 1=right)
            vjust (float): Vertical justification (0=bottom, 0.5=middle, 1=top)

        Returns:
            tuple: (xanchor, yanchor) strings for Plotly annotation
        """
        # Determine horizontal anchor
        if hjust <= 0.25:
            xanchor = "left"
        elif hjust >= 0.75:
            xanchor = "right"
        else:
            xanchor = "center"

        # Determine vertical anchor
        if vjust <= 0.25:
            yanchor = "bottom"
        elif vjust >= 0.75:
            yanchor = "top"
        else:
            yanchor = "middle"

        return xanchor, yanchor

    def _fontface_to_plotly(self, fontface):
        """Convert R-style fontface to Plotly font properties."""
        if fontface == "bold":
            return {"weight": "bold"}
        elif fontface == "italic":
            return {"style": "italic"}
        elif fontface == "bold.italic":
            return {"weight": "bold", "style": "italic"}
        return {}  # plain

    def _draw_impl(self, fig, data, row, col):
        """
        Draw text labels with background boxes on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Data (already transformed by stats).
            row (int): Row position in subplot.
            col (int): Column position in subplot.

        Returns:
            None: Modifies the figure in place.
        """
        # Handle na_rm parameter
        na_rm = self.params.get("na_rm", False)
        if na_rm:
            cols_to_check = [self.mapping["x"], self.mapping["y"], self.mapping["label"]]
            data = data.dropna(subset=cols_to_check)

        if len(data) == 0:
            return

        # Create aesthetic mapper for this geom
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x = data[self.mapping["x"]].copy()
        y = data[self.mapping["y"]].copy()
        label = data[self.mapping["label"]]

        # Handle parse parameter - wrap labels in $...$ for MathJax rendering
        parse = self.params.get("parse", False)
        if parse:
            label = label.apply(lambda t: f"${t}$" if not str(t).startswith("$") else t)

        # Apply nudge offsets
        nudge_x = self.params.get("nudge_x", 0)
        nudge_y = self.params.get("nudge_y", 0)
        if nudge_x != 0:
            x = x + nudge_x
        if nudge_y != 0:
            y = y + nudge_y

        # Get justification
        hjust = self.params.get("hjust", 0.5)
        vjust = self.params.get("vjust", 0.5)
        xanchor, yanchor = self._hjust_vjust_to_anchor(hjust, vjust)

        # Get text styling parameters
        font_size = self.params.get("size", 11)
        font_family = self.params.get("family", None)
        fontface = self.params.get("fontface", "plain")
        font_props = self._fontface_to_plotly(fontface)

        # Get label box styling
        label_padding = self.params.get("label_padding", 4)
        label_r = self.params.get("label_r", 2)
        label_size = self.params.get("label_size", 0.5)
        alpha = style_props["alpha"]

        # Default colors
        default_text_color = self.params.get("color", "black")
        default_fill_color = self.params.get("fill", "white")

        # Determine axis references for subplots
        # For faceted plots, we need the correct axis reference
        xref = f"x{col}" if col > 1 else "x"
        yref = f"y{row}" if row > 1 else "y"
        # Adjust for subplot layout
        if row > 1 or col > 1:
            subplot_idx = (row - 1) * fig._grid_ref[0].__len__() + col if hasattr(fig, '_grid_ref') else 1
            if subplot_idx > 1:
                xref = f"x{subplot_idx}"
                yref = f"y{subplot_idx}"

        # Handle fill mapping for background colors
        fill_series = style_props.get("fill_series")
        fill_map = style_props.get("fill_map", {})
        fill_col = style_props.get("fill")

        # Handle color mapping for text colors
        color_series = style_props.get("color_series")
        color_map = style_props.get("color_map", {})
        color_col = style_props.get("color")

        # Add annotations for each label
        for idx in data.index:
            # Determine fill color for this label
            if fill_series is not None and fill_col in data.columns:
                cat_value = data.loc[idx, fill_col]
                fill_color = fill_map.get(cat_value, default_fill_color)
            else:
                fill_color = default_fill_color

            # Determine text color for this label
            if color_series is not None and color_col in data.columns:
                cat_value = data.loc[idx, color_col]
                text_color = color_map.get(cat_value, default_text_color)
            else:
                text_color = default_text_color

            # Build font dict
            font_dict = {"size": font_size, "color": text_color}
            if font_family:
                font_dict["family"] = font_family
            font_dict.update(font_props)

            # Add annotation with background
            fig.add_annotation(
                x=x[idx],
                y=y[idx],
                text=str(label[idx]),
                showarrow=False,
                font=font_dict,
                xanchor=xanchor,
                yanchor=yanchor,
                bgcolor=fill_color,
                opacity=alpha,
                bordercolor=text_color,
                borderwidth=label_size,
                borderpad=label_padding,
                xref=xref,
                yref=yref,
            )

        # Add invisible scatter trace for legend if fill is mapped
        if fill_series is not None:
            for cat_value, color in fill_map.items():
                fig.add_trace(
                    go.Scatter(
                        x=[None],
                        y=[None],
                        mode="markers",
                        marker=dict(size=10, color=color, symbol="square"),
                        name=str(cat_value),
                        showlegend=True,
                    ),
                    row=row,
                    col=col,
                )
