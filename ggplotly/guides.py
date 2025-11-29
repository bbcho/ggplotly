# guides.py


# # guides.py
# class Labs:
#     def __init__(self, **kwargs):
#         """
#         Initialize plot labels.

#         Parameters:
#             **kwargs: Label parameters (e.g., title, x, y).
#         """
#         self.labels = kwargs

#     def apply(self, fig):
#         """
#         Apply labels to the figure.

#         Parameters:
#             fig (Figure): Plotly figure object.
#         """
#         fig.update_layout(**self.labels)


class Labs:
    """
    Class to handle plot labels, such as title, subtitle, x-axis label, y-axis label, color legend title, and caption.
    """

    def __init__(
        self,
        title=None,
        subtitle=None,
        x=None,
        y=None,
        color=None,
        fill=None,
        caption=None,
    ):
        self.title = title
        self.subtitle = subtitle
        self.x = x
        self.y = y
        self.color = color  # Legend title for color aesthetic
        self.fill = fill  # Legend title for fill aesthetic
        self.caption = caption

    def apply(self, fig):
        """
        Apply the labels to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        layout_updates = {}

        if self.title is not None:
            # Combine title and subtitle into a single title object using HTML tags
            if self.subtitle is not None:
                title_text = f"{self.title}<br><sup>{self.subtitle}</sup>"
            else:
                title_text = self.title

            layout_updates["title"] = dict(
                text=title_text,
                x=0.5,  # Center the title
                xanchor="center",
                yanchor="top",
                font=dict(size=24),
            )

        if self.color is not None:
            layout_updates["legend_title_text"] = self.color

        if self.fill is not None:
            layout_updates["legend_title_text"] = self.fill

        if self.caption is not None:
            # Add caption as an annotation
            fig.add_annotation(
                text=self.caption,
                xref="paper",
                yref="paper",
                x=1,
                y=0,
                showarrow=False,
                xanchor="right",
                yanchor="bottom",
                font=dict(size=12),
            )

        # Apply the layout updates to the figure
        fig.update_layout(**layout_updates)

        # Update axis titles for all subplots (handles faceted plots)
        if self.x is not None:
            fig.update_xaxes(title_text=self.x)
        if self.y is not None:
            fig.update_yaxes(title_text=self.y)


# guides.py continued
def labs(**kwargs):
    """
    Create a Labs object to modify plot labels.

    Parameters:
        **kwargs: Label parameters (e.g., title, x, y).

    Returns:
        Labs: An instance of the Labs class.
    """
    return Labs(**kwargs)


class Annotate:
    """
    Add annotations to a plot at specific data coordinates.

    Supports text, rectangles, segments/arrows, and other shapes.
    Similar to ggplot2's annotate().

    Parameters:
        geom (str): Type of annotation. Options:
            - 'text': Text label at (x, y)
            - 'label': Text with background box at (x, y)
            - 'segment': Line segment from (x, y) to (xend, yend)
            - 'rect': Rectangle from (xmin, ymin) to (xmax, ymax)
            - 'point': Point marker at (x, y)
            - 'curve': Curved arrow (with curvature parameter)
        x, y: Position coordinates (data coordinates)
        xend, yend: End coordinates for segments
        xmin, xmax, ymin, ymax: Bounds for rectangles
        label: Text content for text/label annotations
        color: Color of the annotation
        fill: Fill color (for rect, label background)
        size: Size of text or point
        alpha: Transparency
        fontface: Font style ('plain', 'bold', 'italic')
        hjust, vjust: Horizontal/vertical justification (0-1)
        arrow: Whether to add arrow to segment (bool or dict)

    Examples:
        # Add text annotation
        annotate('text', x=5, y=10, label='Important point')

        # Add rectangle highlight
        annotate('rect', xmin=2, xmax=4, ymin=5, ymax=8, fill='yellow', alpha=0.3)

        # Add arrow pointing to something
        annotate('segment', x=3, y=5, xend=5, yend=8, arrow=True)
    """

    def __init__(self, geom, x=None, y=None, xend=None, yend=None,
                 xmin=None, xmax=None, ymin=None, ymax=None,
                 label=None, color=None, fill=None, size=None,
                 alpha=None, fontface=None, hjust=None, vjust=None,
                 arrow=None, **kwargs):
        self.geom = geom
        self.x = x
        self.y = y
        self.xend = xend
        self.yend = yend
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.label = label
        self.color = color
        self.fill = fill
        self.size = size
        self.alpha = alpha
        self.fontface = fontface
        self.hjust = hjust
        self.vjust = vjust
        self.arrow = arrow
        self.kwargs = kwargs

    def apply(self, fig):
        """
        Apply the annotation to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        if self.geom == 'text':
            self._add_text(fig)
        elif self.geom == 'label':
            self._add_label(fig)
        elif self.geom == 'segment':
            self._add_segment(fig)
        elif self.geom == 'rect':
            self._add_rect(fig)
        elif self.geom == 'point':
            self._add_point(fig)
        elif self.geom == 'curve':
            self._add_curve(fig)
        elif self.geom == 'hline':
            self._add_hline(fig)
        elif self.geom == 'vline':
            self._add_vline(fig)
        else:
            raise ValueError(f"Unknown annotation geom: {self.geom}")

    def _get_anchor(self, hjust=None, vjust=None):
        """Convert hjust/vjust to Plotly anchor values."""
        # hjust: 0=left, 0.5=center, 1=right
        # vjust: 0=bottom, 0.5=middle, 1=top
        xanchor = 'center'
        yanchor = 'middle'

        if hjust is not None:
            if hjust <= 0.25:
                xanchor = 'left'
            elif hjust >= 0.75:
                xanchor = 'right'

        if vjust is not None:
            if vjust <= 0.25:
                yanchor = 'bottom'
            elif vjust >= 0.75:
                yanchor = 'top'

        return xanchor, yanchor

    def _add_text(self, fig):
        """Add text annotation."""
        xanchor, yanchor = self._get_anchor(self.hjust, self.vjust)

        font_dict = {}
        if self.size:
            font_dict['size'] = self.size
        if self.color:
            font_dict['color'] = self.color
        if self.fontface:
            if self.fontface == 'bold':
                font_dict['family'] = 'Arial Black'
            elif self.fontface == 'italic':
                font_dict['family'] = 'Arial'  # Would need CSS for true italic

        fig.add_annotation(
            x=self.x,
            y=self.y,
            text=self.label or '',
            showarrow=False,
            xanchor=xanchor,
            yanchor=yanchor,
            font=font_dict if font_dict else None,
            opacity=self.alpha,
        )

    def _add_label(self, fig):
        """Add text with background box."""
        xanchor, yanchor = self._get_anchor(self.hjust, self.vjust)

        font_dict = {}
        if self.size:
            font_dict['size'] = self.size
        if self.color:
            font_dict['color'] = self.color

        fig.add_annotation(
            x=self.x,
            y=self.y,
            text=self.label or '',
            showarrow=False,
            xanchor=xanchor,
            yanchor=yanchor,
            font=font_dict if font_dict else None,
            opacity=self.alpha,
            bgcolor=self.fill or 'white',
            bordercolor=self.color or 'black',
            borderwidth=1,
            borderpad=4,
        )

    def _add_segment(self, fig):
        """Add line segment, optionally with arrow."""
        show_arrow = bool(self.arrow)
        arrow_head = 2 if show_arrow else 0

        # Segment uses annotation with arrow
        fig.add_annotation(
            x=self.xend,
            y=self.yend,
            ax=self.x,
            ay=self.y,
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=True,
            arrowhead=arrow_head,
            arrowsize=1,
            arrowwidth=self.size or 2,
            arrowcolor=self.color or 'black',
            opacity=self.alpha,
        )

    def _add_curve(self, fig):
        """Add curved arrow annotation."""
        show_arrow = bool(self.arrow) if self.arrow is not None else True
        arrow_head = 2 if show_arrow else 0

        fig.add_annotation(
            x=self.xend,
            y=self.yend,
            ax=self.x,
            ay=self.y,
            xref='x',
            yref='y',
            axref='x',
            ayref='y',
            showarrow=True,
            arrowhead=arrow_head,
            arrowsize=1,
            arrowwidth=self.size or 2,
            arrowcolor=self.color or 'black',
            opacity=self.alpha,
            standoff=5,
        )

    def _add_rect(self, fig):
        """Add rectangle shape."""
        fig.add_shape(
            type='rect',
            x0=self.xmin,
            y0=self.ymin,
            x1=self.xmax,
            y1=self.ymax,
            fillcolor=self.fill,
            opacity=self.alpha or 0.3,
            line=dict(
                color=self.color or self.fill or 'black',
                width=self.size or 1,
            ),
        )

    def _add_point(self, fig):
        """Add point marker."""
        import plotly.graph_objects as go
        fig.add_trace(go.Scatter(
            x=[self.x],
            y=[self.y],
            mode='markers',
            marker=dict(
                size=self.size or 10,
                color=self.fill or self.color or 'black',
                opacity=self.alpha or 1,
            ),
            showlegend=False,
        ))

    def _add_hline(self, fig):
        """Add horizontal line."""
        fig.add_hline(
            y=self.y,
            line_color=self.color or 'black',
            line_width=self.size or 1,
            line_dash='solid',
            opacity=self.alpha or 1,
        )

    def _add_vline(self, fig):
        """Add vertical line."""
        fig.add_vline(
            x=self.x,
            line_color=self.color or 'black',
            line_width=self.size or 1,
            line_dash='solid',
            opacity=self.alpha or 1,
        )


def annotate(geom, **kwargs):
    """
    Create an annotation to add to a plot.

    Parameters:
        geom (str): Type of annotation ('text', 'label', 'segment', 'rect', 'point', 'curve')
        **kwargs: Annotation parameters (x, y, label, color, etc.)

    Returns:
        Annotate: An Annotate object.

    Examples:
        # Text annotation
        ggplot(df, aes(x='x', y='y')) + geom_point() + annotate('text', x=5, y=10, label='Peak')

        # Highlight region
        ggplot(df, aes(x='x', y='y')) + geom_point() + annotate('rect', xmin=2, xmax=4, ymin=0, ymax=5, fill='yellow', alpha=0.2)

        # Arrow pointing to data
        ggplot(df, aes(x='x', y='y')) + geom_point() + annotate('segment', x=0, y=0, xend=5, yend=10, arrow=True)
    """
    return Annotate(geom, **kwargs)
