import plotly.graph_objects as go


class Theme:
    """Base theme class for styling ggplot figures."""

    def __init__(self, template=None, legend_position='right', legend_show=True):
        """
        Initialize the theme.

        Parameters
        ----------
        template : go.layout.Template, optional
            Plotly template to apply to the figure.
        legend_position : str, default='right'
            Position of the legend ('right', 'left', 'top', 'bottom', 'none').
        legend_show : bool, default=True
            Whether to show the legend.
        """
        self.template = template
        self.legend_position = legend_position
        self.legend_show = legend_show

    def apply(self, fig):
        """
        Apply the theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to which the theme will be applied.
        """
        self._apply_legend_settings(fig)

        if self.template:
            fig.update_layout(template=self.template)

    def _apply_legend_settings(self, fig):
        """Apply legend position and visibility settings."""
        if self.legend_position == 'none' or not self.legend_show:
            fig.update_layout(showlegend=False)
        else:
            position_map = {
                'right': dict(x=1.02, y=1, xanchor='left', yanchor='top'),
                'left': dict(x=-0.02, y=1, xanchor='right', yanchor='top'),
                'top': dict(x=0.5, y=1.02, xanchor='center', yanchor='bottom'),
                'bottom': dict(x=0.5, y=-0.1, xanchor='center', yanchor='top')
            }

            legend_settings = {'showlegend': True}
            if self.legend_position in position_map:
                legend_settings['legend'] = position_map[self.legend_position]

            fig.update_layout(**legend_settings)

    def _apply_3d_scene_style(self, fig, bgcolor=None, gridcolor=None, linecolor=None):
        """
        Apply styling to all 3D scenes in the figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to modify.
        bgcolor : str, optional
            Background color for the 3D scene.
        gridcolor : str, optional
            Grid line color.
        linecolor : str, optional
            Axis line color.
        """
        # Check if figure has 3D traces
        has_3d = any(hasattr(trace, 'type') and trace.type == 'scatter3d' for trace in fig.data)
        if not has_3d:
            return

        # Find all scene keys
        layout_dict = fig.layout.to_plotly_json()
        scene_keys = [k for k in layout_dict.keys() if k.startswith('scene')]
        if not scene_keys:
            scene_keys = ['scene']

        # Build scene style
        axis_style = {}
        if gridcolor:
            axis_style['gridcolor'] = gridcolor
            axis_style['showgrid'] = True
        if linecolor:
            axis_style['linecolor'] = linecolor

        scene_style = {}
        if bgcolor:
            scene_style['bgcolor'] = bgcolor
        if axis_style:
            scene_style['xaxis'] = axis_style
            scene_style['yaxis'] = axis_style
            scene_style['zaxis'] = axis_style

        # Apply to all scenes
        if scene_style:
            for scene_key in scene_keys:
                fig.update_layout(**{scene_key: scene_style})

    def _apply_geo_style(self, fig, bgcolor=None, landcolor=None, oceancolor=None,
                         lakecolor=None, countrycolor=None, coastlinecolor=None,
                         subunitcolor=None):
        """
        Apply styling to geographic maps in the figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to modify.
        bgcolor : str, optional
            Background color for the geo plot.
        landcolor : str, optional
            Color of land areas.
        oceancolor : str, optional
            Color of ocean areas.
        lakecolor : str, optional
            Color of lakes.
        countrycolor : str, optional
            Color of country borders.
        coastlinecolor : str, optional
            Color of coastlines.
        subunitcolor : str, optional
            Color of subunit borders (e.g., US states).
        """
        # Check if figure has geo traces
        geo_types = ('scattergeo', 'choropleth', 'scattermapbox', 'choroplethmapbox')
        has_geo = any(
            hasattr(trace, 'type') and trace.type in geo_types
            for trace in fig.data
        )
        if not has_geo:
            return

        # Build geo style update
        geo_style = {}
        if bgcolor:
            geo_style['bgcolor'] = bgcolor
        if landcolor:
            geo_style['landcolor'] = landcolor
        if oceancolor:
            geo_style['oceancolor'] = oceancolor
        if lakecolor:
            geo_style['lakecolor'] = lakecolor
        if countrycolor:
            geo_style['countrycolor'] = countrycolor
        if coastlinecolor:
            geo_style['coastlinecolor'] = coastlinecolor
        if subunitcolor:
            geo_style['subunitcolor'] = subunitcolor

        if geo_style:
            fig.update_geos(**geo_style)

# class theme_bw(Theme):
#     def apply(self, fig):
#         fig.update_layout(template="simple_white")

def theme(legend_position='right', legend_show=True,
          # Axis title elements
          axis_title=None, axis_title_x=None, axis_title_y=None,
          # Axis text elements
          axis_text=None, axis_text_x=None, axis_text_y=None,
          # Axis line elements
          axis_line=None, axis_line_x=None, axis_line_y=None,
          # Axis ticks
          axis_ticks=None, axis_ticks_x=None, axis_ticks_y=None,
          # Panel elements
          panel_background=None, panel_grid=None, panel_grid_major=None,
          panel_grid_minor=None, panel_border=None,
          # Plot elements
          plot_title=None, plot_subtitle=None, plot_caption=None,
          plot_background=None,
          # Legend elements
          legend_title=None, legend_text=None, legend_background=None,
          # Strip elements (for facets)
          strip_text=None, strip_background=None,
          **kwargs):
    """
    Create a custom theme with granular control over plot elements (ggplot2-style).

    Parameters
    ----------
    legend_position : str, default='right'
        Position of the legend ('right', 'left', 'top', 'bottom', 'none').
    legend_show : bool, default=True
        Whether to show the legend.
    axis_title : element_text, optional
        Style for all axis titles.
    axis_title_x : element_text, optional
        Style for x-axis title.
    axis_title_y : element_text, optional
        Style for y-axis title.
    axis_text : element_text, optional
        Style for all axis text (tick labels).
    axis_text_x : element_text, optional
        Style for x-axis text.
    axis_text_y : element_text, optional
        Style for y-axis text.
    axis_line : element_line, optional
        Style for all axis lines.
    axis_line_x : element_line, optional
        Style for x-axis line.
    axis_line_y : element_line, optional
        Style for y-axis line.
    axis_ticks : element_line, optional
        Style for all axis ticks.
    axis_ticks_x : element_line, optional
        Style for x-axis ticks.
    axis_ticks_y : element_line, optional
        Style for y-axis ticks.
    panel_background : element_rect, optional
        Background of the plot panel.
    panel_grid : element_line, optional
        Style for all grid lines.
    panel_grid_major : element_line, optional
        Style for major grid lines.
    panel_grid_minor : element_line, optional
        Style for minor grid lines.
    panel_border : element_rect, optional
        Border around plot panel.
    plot_title : element_text, optional
        Style for plot title.
    plot_subtitle : element_text, optional
        Style for plot subtitle.
    plot_caption : element_text, optional
        Style for plot caption.
    plot_background : element_rect, optional
        Background of entire plot.
    legend_title : element_text, optional
        Style for legend title.
    legend_text : element_text, optional
        Style for legend text.
    legend_background : element_rect, optional
        Background of legend.
    strip_text : element_text, optional
        Style for facet strip labels.
    strip_background : element_rect, optional
        Background of facet strips.
    **kwargs
        Additional Plotly layout parameters.

    Returns
    -------
    Theme
        A theme object that can be added to ggplot.

    Examples
    --------
    >>> from ggplotly import ggplot, aes, geom_point, theme, element_text, element_rect, data
    >>> mpg = data('mpg')

    >>> # Move legend to bottom
    >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + theme(legend_position='bottom')

    >>> # Style axis titles
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme(axis_title=element_text(size=14, color='blue'))

    >>> # Change panel background
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme(panel_background=element_rect(fill='lightgray'))

    >>> # Style plot title
    >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme(plot_title=element_text(size=20, color='darkblue'))
    """
    class CustomTheme(Theme):
        def __init__(self):
            super().__init__(legend_position=legend_position, legend_show=legend_show)

        def apply(self, fig):
            super().apply(fig)

            layout_updates = {}
            xaxis_updates = {}
            yaxis_updates = {}

            # Apply axis title styling
            if axis_title is not None or axis_title_x is not None:
                title_style = axis_title_x or axis_title
                if isinstance(title_style, element_text):
                    xaxis_updates['title_font'] = dict(
                        size=title_style.size,
                        color=title_style.color,
                        family=title_style.family
                    )

            if axis_title is not None or axis_title_y is not None:
                title_style = axis_title_y or axis_title
                if isinstance(title_style, element_text):
                    yaxis_updates['title_font'] = dict(
                        size=title_style.size,
                        color=title_style.color,
                        family=title_style.family
                    )

            # Apply axis text (tick labels) styling
            if axis_text is not None or axis_text_x is not None:
                text_style = axis_text_x or axis_text
                if isinstance(text_style, element_text):
                    xaxis_updates['tickfont'] = dict(
                        size=text_style.size,
                        color=text_style.color,
                        family=text_style.family
                    )

            if axis_text is not None or axis_text_y is not None:
                text_style = axis_text_y or axis_text
                if isinstance(text_style, element_text):
                    yaxis_updates['tickfont'] = dict(
                        size=text_style.size,
                        color=text_style.color,
                        family=text_style.family
                    )

            # Apply axis line styling
            if axis_line is not None or axis_line_x is not None:
                line_style = axis_line_x or axis_line
                if isinstance(line_style, element_line):
                    xaxis_updates['linecolor'] = line_style.color
                    xaxis_updates['linewidth'] = line_style.width
                    xaxis_updates['showline'] = True

            if axis_line is not None or axis_line_y is not None:
                line_style = axis_line_y or axis_line
                if isinstance(line_style, element_line):
                    yaxis_updates['linecolor'] = line_style.color
                    yaxis_updates['linewidth'] = line_style.width
                    yaxis_updates['showline'] = True

            # Apply axis tick styling
            if axis_ticks is not None or axis_ticks_x is not None:
                tick_style = axis_ticks_x or axis_ticks
                if isinstance(tick_style, element_line):
                    xaxis_updates['tickcolor'] = tick_style.color
                    xaxis_updates['tickwidth'] = tick_style.width
                    xaxis_updates['ticks'] = 'outside'

            if axis_ticks is not None or axis_ticks_y is not None:
                tick_style = axis_ticks_y or axis_ticks
                if isinstance(tick_style, element_line):
                    yaxis_updates['tickcolor'] = tick_style.color
                    yaxis_updates['tickwidth'] = tick_style.width
                    yaxis_updates['ticks'] = 'outside'

            # Apply panel background
            if panel_background is not None:
                if isinstance(panel_background, element_rect):
                    layout_updates['plot_bgcolor'] = panel_background.fill

            # Apply panel grid
            grid_style = panel_grid_major or panel_grid
            if grid_style is not None:
                if isinstance(grid_style, element_line):
                    xaxis_updates['gridcolor'] = grid_style.color
                    xaxis_updates['gridwidth'] = grid_style.width
                    xaxis_updates['showgrid'] = True
                    yaxis_updates['gridcolor'] = grid_style.color
                    yaxis_updates['gridwidth'] = grid_style.width
                    yaxis_updates['showgrid'] = True

            # Apply plot title styling
            if plot_title is not None:
                if isinstance(plot_title, element_text):
                    layout_updates['title_font'] = dict(
                        size=plot_title.size,
                        color=plot_title.color,
                        family=plot_title.family
                    )

            # Apply plot background
            if plot_background is not None:
                if isinstance(plot_background, element_rect):
                    layout_updates['paper_bgcolor'] = plot_background.fill

            # Apply legend styling
            legend_updates = {}
            if legend_title is not None:
                if isinstance(legend_title, element_text):
                    legend_updates['title_font'] = dict(
                        size=legend_title.size,
                        color=legend_title.color,
                        family=legend_title.family
                    )

            if legend_text is not None:
                if isinstance(legend_text, element_text):
                    legend_updates['font'] = dict(
                        size=legend_text.size,
                        color=legend_text.color,
                        family=legend_text.family
                    )

            if legend_background is not None:
                if isinstance(legend_background, element_rect):
                    legend_updates['bgcolor'] = legend_background.fill
                    legend_updates['bordercolor'] = legend_background.color
                    legend_updates['borderwidth'] = legend_background.width

            if legend_updates:
                layout_updates['legend'] = legend_updates

            # Apply updates
            if xaxis_updates:
                fig.update_xaxes(**xaxis_updates)
            if yaxis_updates:
                fig.update_yaxes(**yaxis_updates)
            if layout_updates:
                fig.update_layout(**layout_updates)

            # Apply any additional customizations from kwargs
            if kwargs:
                fig.update_layout(**kwargs)

    return CustomTheme()

class theme_template(Theme):
    """Apply a custom Plotly template as a theme."""

    def __init__(self, template=None):
        """
        Apply a custom Plotly template as a theme.

        Parameters
        ----------
        template : go.layout.Template, optional
            The Plotly template to apply.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, data
        >>> from ggplotly.themes import theme_template
        >>> mpg = data('mpg')
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme_template()
        """
        super().__init__(template=template)

    def apply(self, fig):
        """
        Apply the template theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to modify.
        """
        fig.update_layout(template=self.template)


class theme_dark(Theme):
    """Dark theme with dark background and light text."""

    def __init__(self):
        """
        Create a dark theme with dark background and light text.

        Automatically applies dark styling to:

        - Standard 2D plots (via plotly_dark template)
        - 3D scenes (dark background with subtle grid)
        - Geographic maps (dark land, ocean, and borders)

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, theme_dark, data
        >>> mpg = data('mpg')
        >>> ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point() + theme_dark()
        """
        super().__init__()

    def apply(self, fig):
        """
        Apply the dark theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to modify.
        """
        fig.update_layout(template="plotly_dark")
        # Apply dark styling to 3D scenes
        self._apply_3d_scene_style(
            fig,
            bgcolor='rgb(17, 17, 17)',
            gridcolor='rgb(60, 60, 60)',
            linecolor='rgb(60, 60, 60)'
        )
        # Apply dark styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='rgb(17, 17, 17)',
            landcolor='rgb(40, 40, 40)',
            oceancolor='rgb(17, 17, 17)',
            lakecolor='rgb(30, 30, 30)',
            countrycolor='rgb(80, 80, 80)',
            coastlinecolor='rgb(80, 80, 80)',
            subunitcolor='rgb(60, 60, 60)'
        )


class theme_classic(Theme):
    """Classic theme with white background and no gridlines."""

    def __init__(self, base_size=11, base_family=""):
        """
        Create a classic theme with white background and no gridlines.

        Similar to ggplot2's theme_classic().

        Automatically applies classic styling to:

        - Standard 2D plots (white background, no gridlines)
        - 3D scenes (white background)
        - Geographic maps (light, clean appearance)

        Parameters
        ----------
        base_size : int, default=11
            Base font size in points.
        base_family : str, default=""
            Base font family (system default if empty).

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, theme_classic, data
        >>> mpg = data('mpg')
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme_classic()
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme_classic(base_size=14)
        """
        super().__init__()
        self.base_size = base_size
        self.base_family = base_family

    def apply(self, fig):
        """
        Apply the classic theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to modify.
        """
        font_dict = dict(size=self.base_size)
        if self.base_family:
            font_dict['family'] = self.base_family

        fig.update_layout(
            template="simple_white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
            font=font_dict,
        )
        # Apply classic styling to 3D scenes (white background, no grid)
        self._apply_3d_scene_style(
            fig,
            bgcolor='white',
            gridcolor='white',
        )
        # Apply classic styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='white',
            landcolor='rgb(243, 243, 243)',
            oceancolor='rgb(230, 240, 250)',
            lakecolor='rgb(230, 240, 250)',
            countrycolor='rgb(180, 180, 180)',
            coastlinecolor='rgb(180, 180, 180)',
            subunitcolor='rgb(200, 200, 200)'
        )


class theme_default(Theme):
    """Default theme with light background and gridlines."""

    def __init__(self):
        """
        Create the default theme with light background and gridlines.

        Automatically applies default styling to:

        - Standard 2D plots (white background, light gridlines)
        - Geographic maps (standard light appearance)
        """
        super().__init__()

    def apply(self, fig):
        """
        Apply the default theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to which the theme will be applied.
        """
        default_template = go.layout.Template(
            layout=dict(
                xaxis=dict(
                    showgrid=True,
                    gridcolor="lightgrey",
                    zeroline=True,
                    zerolinecolor="lightgrey",
                    zerolinewidth=1,
                    linecolor="black",
                    mirror=True,
                    ticks="outside",
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor="lightgrey",
                    zeroline=True,
                    zerolinecolor="lightgrey",
                    zerolinewidth=1,
                    linecolor="black",
                    mirror=True,
                    ticks="outside",
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=dict(color="black", size=12),
            )
        )

        # Apply the theme to the figure
        fig.update_layout(template=default_template)
        # Apply default styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='white',
            landcolor='rgb(243, 243, 243)',
            oceancolor='rgb(204, 229, 255)',
            lakecolor='rgb(204, 229, 255)',
            countrycolor='rgb(204, 204, 204)',
            coastlinecolor='rgb(204, 204, 204)',
            subunitcolor='rgb(204, 204, 204)'
        )


class theme_bbc(Theme):
    """BBC-style theme with clean white background and distinctive colors."""

    def __init__(self):
        """
        Create a BBC-style theme with clean white background and distinctive colors.

        Automatically applies BBC styling to:

        - Standard 2D plots (white background, BBC color palette)
        - Geographic maps (clean, professional appearance)
        """
        # Define a template for Plotly to apply globally
        self.template = go.layout.Template(
            layout=dict(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                font=dict(
                    color="#333333", size=12, family="Helvetica"
                ),  # Dark grey text with Helvetica font
                xaxis=dict(
                    showline=True,
                    linecolor="#333333",
                    showgrid=True,
                    gridcolor="#CBCBCB",
                    zeroline=True,
                    zerolinewidth=1,
                ),
                yaxis=dict(
                    showline=True,
                    linecolor="#333333",
                    showgrid=True,
                    gridcolor="#CBCBCB",
                    zeroline=True,
                    zerolinewidth=1,
                ),
                colorway=[
                    "#bb1919",
                    "#009639",
                    "#005293",
                    "#ff6319",
                    "#ffcd00",
                ],  # BBC-like colors
            )
        )

    def apply(self, fig):
        """
        Apply the theme's template to the Plotly figure.
        """
        fig.update_layout(template=self.template)
        # Apply BBC styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='#FFFFFF',
            landcolor='#F0F0F0',
            oceancolor='#E8F4F8',
            lakecolor='#E8F4F8',
            countrycolor='#CBCBCB',
            coastlinecolor='#999999',
            subunitcolor='#CBCBCB'
        )


class theme_ggplot2(Theme):
    """A theme that replicates the default ggplot2 style from R."""

    def __init__(self):
        """
        Create a theme that replicates the default ggplot2 style from R.

        Uses Plotly's template system to apply the style across all geoms.

        Automatically applies ggplot2 styling to:

        - Standard 2D plots (grey background, white gridlines)
        - 3D scenes (grey background)
        - Geographic maps (grey-toned appearance matching ggplot2)
        """
        # Define a template for Plotly to apply globally
        self.template = go.layout.Template(
            layout=dict(
                paper_bgcolor="#E5E5E5",  # Light grey background
                plot_bgcolor="#E5E5E5",  # Light grey background
                font=dict(color="black", size=12),  # Black text
                xaxis=dict(
                    showline=True,
                    linecolor="black",
                    showgrid=True,
                    gridcolor="white",
                    zeroline=True,
                    zerolinewidth=1,
                ),
                yaxis=dict(
                    showline=True,
                    linecolor="black",
                    showgrid=True,
                    gridcolor="white",
                    zeroline=True,
                    zerolinewidth=1,
                ),
                colorway=[
                    "#F8766D",
                    "#7CAE00",
                    "#00BFC4",
                    "#C77CFF",
                    "#00BA38",
                ],  # ggplot2-like colors
            )
        )

    def apply(self, fig):
        """
        Apply the theme's template to the Plotly figure.
        """
        fig.update_layout(template=self.template)
        # Apply ggplot2 styling to 3D scenes
        self._apply_3d_scene_style(
            fig,
            bgcolor='#E5E5E5',
            gridcolor='white',
            linecolor='black'
        )
        # Apply ggplot2 styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='#E5E5E5',
            landcolor='#FFFFFF',
            oceancolor='#D5E4EB',
            lakecolor='#D5E4EB',
            countrycolor='#969696',
            coastlinecolor='#969696',
            subunitcolor='#B0B0B0'
        )


class theme_nytimes(Theme):
    """A theme inspired by New York Times charts."""

    def __init__(self):
        """
        Create a theme inspired by New York Times charts.

        Uses Plotly's template system to apply style globally.

        Automatically applies NYT styling to:

        - Standard 2D plots (clean white background, subtle gridlines)
        - Geographic maps (clean, professional appearance)
        """
        # Define a template for Plotly to apply globally
        self.template = go.layout.Template(
            layout=dict(
                paper_bgcolor="white",  # White background
                plot_bgcolor="white",  # White plot area
                font=dict(color="#333333", size=16),  # Dark grey text
                title=dict(
                    font=dict(size=22, color="#333333", family="Arial, sans-serif"),
                    x=0.5,  # Center the title
                    xanchor="center",
                ),
                xaxis=dict(
                    showline=True,
                    linecolor="#4d4d4d",
                    showgrid=True,
                    gridcolor="#e0e0e0",
                    zeroline=False,
                ),
                yaxis=dict(
                    showline=True,
                    linecolor="#4d4d4d",
                    showgrid=True,
                    gridcolor="#e0e0e0",
                    zeroline=False,
                ),
                colorway=[
                    "#1f77b4",
                    "#ff7f0e",
                    "#2ca02c",
                    "#d62728",
                    "#9467bd",
                ],  # NYT-like colors
            )
        )

    def apply(self, fig):
        """
        Apply the theme's template to the Plotly figure.
        """
        fig.update_layout(template=self.template)
        # Apply NYT styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='white',
            landcolor='#F5F5F5',
            oceancolor='#E8F0F5',
            lakecolor='#E8F0F5',
            countrycolor='#CCCCCC',
            coastlinecolor='#999999',
            subunitcolor='#DDDDDD'
        )


class theme_minimal(Theme):
    """Minimal theme that removes background and gridlines for a cleaner look."""

    def __init__(self, base_size=11, base_family=""):
        """
        Create a minimal theme that removes background and gridlines.

        Automatically applies minimal styling to:

        - Standard 2D plots (white background, no gridlines)
        - 3D scenes (white background, subtle grid)
        - Geographic maps (clean, minimal appearance)

        Parameters
        ----------
        base_size : int, default=11
            Base font size in points.
        base_family : str, default=""
            Base font family (system default if empty).

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, theme_minimal, data
        >>> mpg = data('mpg')
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme_minimal()
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + theme_minimal(base_size=14)
        """
        super().__init__()
        self.base_size = base_size
        self.base_family = base_family

    def apply(self, fig):
        """
        Apply the minimal theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to which the theme will be applied.
        """
        font_dict = dict(color="black", size=self.base_size)
        if self.base_family:
            font_dict['family'] = self.base_family

        minimal_template = go.layout.Template(
            layout=dict(
                xaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    ticks="",
                    showticklabels=True,
                ),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showline=False,
                    ticks="",
                    showticklabels=True,
                ),
                plot_bgcolor="white",
                paper_bgcolor="white",
                font=font_dict,
            )
        )

        # Apply the minimal theme to the figure
        fig.update_layout(template=minimal_template)
        # Apply minimal styling to 3D scenes
        self._apply_3d_scene_style(
            fig,
            bgcolor='white',
            gridcolor='#eee',
        )
        # Apply minimal styling to geographic maps
        self._apply_geo_style(
            fig,
            bgcolor='white',
            landcolor='#FAFAFA',
            oceancolor='#F0F5F8',
            lakecolor='#F0F5F8',
            countrycolor='#E0E0E0',
            coastlinecolor='#D0D0D0',
            subunitcolor='#E8E8E8'
        )


class theme_custom(Theme):
    """Custom theme with user-specified colors."""

    def __init__(self, background_color="white", grid_color="grey", text_color="black"):
        """
        Create a custom theme with user-specified colors.

        Parameters
        ----------
        background_color : str, default='white'
            Background color for the plot.
        grid_color : str, default='grey'
            Color of grid lines.
        text_color : str, default='black'
            Color of text elements.
        """
        self.background_color = background_color
        self.grid_color = grid_color
        self.text_color = text_color

    def apply(self, fig):
        """
        Apply the custom theme to a figure.

        Parameters
        ----------
        fig : Figure
            The Plotly figure to which the theme will be applied.
        """
        custom_template = go.layout.Template(
            layout=dict(
                plot_bgcolor=self.background_color,
                paper_bgcolor=self.background_color,
                font=dict(color=self.text_color, size=12),
                xaxis=dict(showgrid=True, gridcolor=self.grid_color),
                yaxis=dict(showgrid=True, gridcolor=self.grid_color),
            )
        )

        # Apply the custom theme to the figure
        fig.update_layout(template=custom_template)


class element_text:
    """
    Customize text elements in themes.

    Parameters
    ----------
    size : int, default=12
        Font size in points.
    color : str, default='black'
        Text color.
    family : str, default='Arial'
        Font family.
    """

    def __init__(self, size=12, color="black", family="Arial"):
        self.size = size
        self.color = color
        self.family = family


class element_line:
    """
    Customize line elements in themes.

    Parameters
    ----------
    color : str, default='black'
        Line color.
    width : int, default=1
        Line width in pixels.
    dash : str, default='solid'
        Line dash style ('solid', 'dash', 'dot', 'dashdot').
    """

    def __init__(self, color="black", width=1, dash="solid"):
        self.color = color
        self.width = width
        self.dash = dash


class element_rect:
    """
    Customize rectangle elements in themes.

    Parameters
    ----------
    fill : str, default='white'
        Fill color.
    color : str, default='black'
        Border color.
    width : int, default=1
        Border width in pixels.
    """

    def __init__(self, fill="white", color="black", width=1):
        self.fill = fill
        self.color = color
        self.width = width
