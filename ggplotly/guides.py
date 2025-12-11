# guides.py

"""Guide functions for controlling legends and color bars."""


class guide_legend:
    """Configure legend appearance for discrete scales."""

    def __init__(self, title=None, title_position='top', direction='vertical',
                 nrow=None, ncol=None, byrow=False, reverse=False, override_aes=None):
        """
        Configure legend appearance for discrete scales.

        Parameters
        ----------
        title : str, optional
            Legend title. Use None to suppress title.
        title_position : str, default='top'
            Position of title ('top', 'left', 'right').
        direction : str, default='vertical'
            Direction of legend keys ('horizontal', 'vertical').
        nrow : int, optional
            Number of rows for legend keys.
        ncol : int, optional
            Number of columns for legend keys.
        byrow : bool, default=False
            If True, fill by row. Default is False (fill by column).
        reverse : bool, default=False
            If True, reverse the order of keys.
        override_aes : dict, optional
            Override aesthetic properties in legend.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, guides, guide_legend, data
        >>> mpg = data('mpg')

        >>> # Customize color legend with title and columns
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + \\
        ...     guides(color=guide_legend(title='Vehicle Class', ncol=2))

        >>> # Reverse legend order
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='drv')) + geom_point() + \\
        ...     guides(color=guide_legend(reverse=True))
        """
        self.title = title
        self.title_position = title_position
        self.direction = direction
        self.nrow = nrow
        self.ncol = ncol
        self.byrow = byrow
        self.reverse = reverse
        self.override_aes = override_aes or {}


class guide_colorbar:
    """Configure colorbar appearance for continuous scales."""

    def __init__(self, title=None, title_position='top', direction='vertical',
                 barwidth=None, barheight=None, nbin=300, raster=True,
                 ticks=True, draw_ulim=True, draw_llim=True, reverse=False):
        """
        Configure colorbar appearance for continuous scales.

        Parameters
        ----------
        title : str, optional
            Colorbar title. Use None to suppress title.
        title_position : str, default='top'
            Position of title ('top', 'bottom', 'left', 'right').
        direction : str, default='vertical'
            Direction of colorbar ('horizontal', 'vertical').
        barwidth : float, optional
            Width of the colorbar.
        barheight : float, optional
            Height of the colorbar.
        nbin : int, default=300
            Number of bins for colorbar.
        raster : bool, default=True
            If True, render as raster.
        ticks : bool, default=True
            If True, show tick marks.
        draw_ulim : bool, default=True
            If True, draw upper limit.
        draw_llim : bool, default=True
            If True, draw lower limit.
        reverse : bool, default=False
            If True, reverse colorbar direction.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, guides, guide_colorbar, data
        >>> diamonds = data('diamonds')

        >>> # Horizontal colorbar with custom title
        >>> ggplot(diamonds.head(1000), aes(x='carat', y='price', color='depth')) + geom_point() + \\
        ...     guides(color=guide_colorbar(title='Depth %', direction='horizontal'))

        >>> # Customize colorbar width
        >>> ggplot(diamonds.head(1000), aes(x='carat', y='price', color='depth')) + geom_point() + \\
        ...     guides(color=guide_colorbar(barwidth=20))
        """
        self.title = title
        self.title_position = title_position
        self.direction = direction
        self.barwidth = barwidth
        self.barheight = barheight
        self.nbin = nbin
        self.raster = raster
        self.ticks = ticks
        self.draw_ulim = draw_ulim
        self.draw_llim = draw_llim
        self.reverse = reverse


class Guides:
    """Control guide (legend/colorbar) display for aesthetics."""

    def __init__(self, color=None, fill=None, shape=None, size=None,
                 alpha=None, linetype=None, **kwargs):
        """
        Control guide (legend/colorbar) display for aesthetics.

        This class allows you to customize or hide guides for specific aesthetics.

        Parameters
        ----------
        color : guide_legend, guide_colorbar, str, or bool, optional
            Guide for color aesthetic. Use 'none' or False to hide.
        fill : guide_legend, guide_colorbar, str, or bool, optional
            Guide for fill aesthetic.
        shape : guide_legend or str, optional
            Guide for shape aesthetic.
        size : guide_legend or str, optional
            Guide for size aesthetic.
        alpha : guide_legend or str, optional
            Guide for alpha aesthetic.
        linetype : guide_legend or str, optional
            Guide for linetype aesthetic.
        **kwargs
            Additional aesthetic-guide mappings.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, guides, guide_legend, data
        >>> mpg = data('mpg')

        >>> # Hide color legend
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + guides(color='none')

        >>> # Customize legend
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + \\
        ...     guides(color=guide_legend(title='Vehicle Class'))
        """
        self.guides = {
            'color': color,
            'fill': fill,
            'shape': shape,
            'size': size,
            'alpha': alpha,
            'linetype': linetype,
        }
        # Add any additional aesthetics
        self.guides.update(kwargs)

    def apply(self, fig):
        """
        Apply guide settings to the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        """
        layout_updates = {}
        legend_updates = {}

        # Process each aesthetic's guide
        for aesthetic, guide in self.guides.items():
            if guide is None:
                continue

            # Handle 'none' or False to hide the guide
            if guide == 'none' or guide is False:
                if aesthetic in ('color', 'fill', 'shape', 'size', 'alpha', 'linetype'):
                    layout_updates['showlegend'] = False
                continue

            # Handle guide_legend
            if isinstance(guide, guide_legend):
                if guide.title is not None:
                    legend_updates['title_text'] = guide.title

                # Handle direction
                if guide.direction == 'horizontal':
                    legend_updates['orientation'] = 'h'
                else:
                    legend_updates['orientation'] = 'v'

                # Handle title position
                if guide.title_position == 'left':
                    legend_updates['title_side'] = 'left'
                elif guide.title_position == 'right':
                    legend_updates['title_side'] = 'right'
                else:
                    legend_updates['title_side'] = 'top'

                # Handle reverse
                if guide.reverse:
                    legend_updates['traceorder'] = 'reversed'

            # Handle guide_colorbar
            elif isinstance(guide, guide_colorbar):
                colorbar_updates = {}

                if guide.title is not None:
                    colorbar_updates['title'] = guide.title

                if guide.direction == 'horizontal':
                    colorbar_updates['orientation'] = 'h'

                if guide.barwidth is not None:
                    colorbar_updates['thickness'] = guide.barwidth

                if guide.barheight is not None:
                    colorbar_updates['len'] = guide.barheight

                if not guide.ticks:
                    colorbar_updates['ticks'] = ''

                # Apply colorbar settings to traces with colorbars
                if colorbar_updates:
                    for trace in fig.data:
                        if hasattr(trace, 'marker') and trace.marker is not None:
                            if hasattr(trace.marker, 'colorbar'):
                                trace.marker.colorbar.update(colorbar_updates)

        # Apply legend updates
        if legend_updates:
            layout_updates['legend'] = legend_updates

        if layout_updates:
            fig.update_layout(**layout_updates)


def guides(**kwargs):
    """
    Control guide (legend/colorbar) display for aesthetics.

    Parameters
    ----------
    **kwargs
        Aesthetic-guide mappings. Keys are aesthetic names (color, fill, shape, etc.)
        Values can be:

        - 'none' or False: Hide the guide
        - guide_legend(...): Configure legend appearance
        - guide_colorbar(...): Configure colorbar appearance

    Returns
    -------
    Guides
        A Guides object that can be added to ggplot.

    Examples
    --------
    >>> from ggplotly import ggplot, aes, geom_point, guides, guide_legend, guide_colorbar, data
    >>> mpg = data('mpg')
    >>> diamonds = data('diamonds')

    >>> # Hide color legend
    >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + guides(color='none')

    >>> # Customize legend with title and columns
    >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + \\
    ...     guides(color=guide_legend(title='Vehicle Class', ncol=2))

    >>> # Customize colorbar direction
    >>> ggplot(diamonds.head(1000), aes(x='carat', y='price', color='depth')) + geom_point() + \\
    ...     guides(color=guide_colorbar(direction='horizontal'))
    """
    return Guides(**kwargs)


class Labs:
    """Set plot labels including title, subtitle, axis labels, legend titles, and caption."""

    def __init__(
        self,
        title=None,
        subtitle=None,
        x=None,
        y=None,
        z=None,
        color=None,
        colour=None,
        fill=None,
        size=None,
        shape=None,
        alpha=None,
        linetype=None,
        caption=None,
        tag=None,
        alt=None,
        **kwargs
    ):
        """
        Set plot labels including title, subtitle, axis labels, legend titles, and caption.

        Parameters
        ----------
        title : str, optional
            Main plot title.
        subtitle : str, optional
            Subtitle displayed below the title.
        x : str, optional
            X-axis label.
        y : str, optional
            Y-axis label.
        z : str, optional
            Z-axis label (for 3D plots).
        color : str, optional
            Legend title for color aesthetic.
        colour : str, optional
            Alias for color (British spelling).
        fill : str, optional
            Legend title for fill aesthetic.
        size : str, optional
            Legend title for size aesthetic.
        shape : str, optional
            Legend title for shape aesthetic.
        alpha : str, optional
            Legend title for alpha aesthetic.
        linetype : str, optional
            Legend title for linetype aesthetic.
        caption : str, optional
            Caption displayed at bottom-right of plot.
        tag : str, optional
            Plot tag (e.g., 'A', 'B' for figure panels).
        alt : str, optional
            Alternative text for accessibility.
        **kwargs
            Additional label parameters for other aesthetics.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, labs, data
        >>> mpg = data('mpg')

        >>> # Set title and axis labels
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
        ...     labs(title='Fuel Efficiency', x='Engine Displacement (L)', y='Highway MPG')

        >>> # Set legend title
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + \\
        ...     labs(color='Vehicle Class')

        >>> # Add subtitle and caption
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
        ...     labs(title='Fuel Efficiency', subtitle='1999-2008 vehicles', caption='Source: EPA')
        """
        self.title = title
        self.subtitle = subtitle
        self.x = x
        self.y = y
        self.z = z
        self.color = color or colour  # Support both spellings
        self.fill = fill
        self.size = size
        self.shape = shape
        self.alpha = alpha
        self.linetype = linetype
        self.caption = caption
        self.tag = tag
        self.alt = alt
        self.extra_labels = kwargs  # Store any additional aesthetic labels

    def apply(self, fig):
        """
        Apply the labels to the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
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

        # Check if figure has 3D scenes and update their axis labels
        has_3d = any(trace.type in ('scatter3d', 'surface', 'mesh3d') for trace in fig.data)
        if has_3d:
            # Find all scene keys in the layout
            layout_dict = fig.layout.to_plotly_json()
            scene_keys = [k for k in layout_dict.keys() if k.startswith('scene')]
            if not scene_keys:
                scene_keys = ['scene']

            for scene_key in scene_keys:
                scene_updates = {}
                if self.x is not None:
                    scene_updates['xaxis_title'] = self.x
                if self.y is not None:
                    scene_updates['yaxis_title'] = self.y
                if self.z is not None:
                    scene_updates['zaxis_title'] = self.z
                if scene_updates:
                    fig.update_layout(**{scene_key: scene_updates})


def labs(**kwargs):
    """
    Create a Labs object to modify plot labels.

    Parameters
    ----------
    **kwargs
        Label parameters (e.g., title, x, y, color, fill).

    Returns
    -------
    Labs
        An instance of the Labs class.
    """
    return Labs(**kwargs)


class Annotate:
    """Add annotations to a plot at specific data coordinates."""

    def __init__(self, geom, x=None, y=None, xend=None, yend=None,
                 xmin=None, xmax=None, ymin=None, ymax=None,
                 label=None, color=None, fill=None, size=None,
                 alpha=None, fontface=None, hjust=None, vjust=None,
                 arrow=None, **kwargs):
        """
        Add annotations to a plot at specific data coordinates.

        Supports text, rectangles, segments/arrows, and other shapes.
        Similar to ggplot2's annotate().

        Parameters
        ----------
        geom : str
            Type of annotation. Options: 'text', 'label', 'segment', 'rect',
            'point', 'curve', 'hline', 'vline'.
        x : float, optional
            X position coordinate (data coordinates).
        y : float, optional
            Y position coordinate (data coordinates).
        xend : float, optional
            End x coordinate for segments.
        yend : float, optional
            End y coordinate for segments.
        xmin : float, optional
            Left bound for rectangles.
        xmax : float, optional
            Right bound for rectangles.
        ymin : float, optional
            Bottom bound for rectangles.
        ymax : float, optional
            Top bound for rectangles.
        label : str, optional
            Text content for text/label annotations.
        color : str, optional
            Color of the annotation.
        fill : str, optional
            Fill color (for rect, label background).
        size : float, optional
            Size of text or point.
        alpha : float, optional
            Transparency (0-1).
        fontface : str, optional
            Font style ('plain', 'bold', 'italic').
        hjust : float, optional
            Horizontal justification (0-1).
        vjust : float, optional
            Vertical justification (0-1).
        arrow : bool or dict, optional
            Whether to add arrow to segment.
        **kwargs
            Additional parameters.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, annotate, data
        >>> mpg = data('mpg')

        >>> # Add text annotation
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
        ...     annotate('text', x=5, y=40, label='High efficiency zone')

        >>> # Add highlighted rectangle region
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
        ...     annotate('rect', xmin=1.5, xmax=2.5, ymin=30, ymax=45, fill='yellow', alpha=0.3)

        >>> # Add segment with arrow
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
        ...     annotate('segment', x=3, y=35, xend=2, yend=44, arrow=True)
        """
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

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
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

    Parameters
    ----------
    geom : str
        Type of annotation ('text', 'label', 'segment', 'rect', 'point', 'curve').
    **kwargs
        Annotation parameters (x, y, label, color, etc.).

    Returns
    -------
    Annotate
        An Annotate object.

    Examples
    --------
    >>> from ggplotly import ggplot, aes, geom_point, annotate, data
    >>> mpg = data('mpg')

    >>> # Text annotation
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
    ...     annotate('text', x=5, y=40, label='Outliers')

    >>> # Rectangle highlight
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
    ...     annotate('rect', xmin=1.5, xmax=2.5, ymin=30, ymax=45, fill='yellow', alpha=0.2)

    >>> # Arrow pointing to a feature
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + \\
    ...     annotate('segment', x=4, y=35, xend=2.5, yend=44, arrow=True)
    """
    return Annotate(geom, **kwargs)
