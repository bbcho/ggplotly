import plotly.graph_objects as go


class Theme:
    def __init__(self, template=None, legend_position='right', legend_show=True):
        """
        Base Theme class.

        Parameters:
            template (go.layout.Template, optional): Plotly template to apply to the figure.
            legend_position (str): Position of the legend ('right', 'left', 'top', 'bottom', 'none').
            legend_show (bool): Whether to show the legend.
        """
        self.template = template
        self.legend_position = legend_position
        self.legend_show = legend_show

    def apply(self, fig):
        """
        Apply the theme to a figure.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.

        Returns:
            None: Modifies the figure in place.
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

        Parameters:
            fig (Figure): The Plotly figure to modify.
            bgcolor (str): Background color for the 3D scene.
            gridcolor (str): Grid line color.
            linecolor (str): Axis line color.
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

        Parameters:
            fig (Figure): The Plotly figure to modify.
            bgcolor (str): Background color for the geo plot.
            landcolor (str): Color of land areas.
            oceancolor (str): Color of ocean areas.
            lakecolor (str): Color of lakes.
            countrycolor (str): Color of country borders.
            coastlinecolor (str): Color of coastlines.
            subunitcolor (str): Color of subunit borders (e.g., US states).
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

    Parameters:
        legend_position (str): 'right', 'left', 'top', 'bottom', 'none'
        legend_show (bool): Whether to show legend

        Axis Title Elements:
            axis_title (element_text): Style for all axis titles
            axis_title_x (element_text): Style for x-axis title
            axis_title_y (element_text): Style for y-axis title

        Axis Text Elements (tick labels):
            axis_text (element_text): Style for all axis text
            axis_text_x (element_text): Style for x-axis text
            axis_text_y (element_text): Style for y-axis text

        Axis Line Elements:
            axis_line (element_line): Style for all axis lines
            axis_line_x (element_line): Style for x-axis line
            axis_line_y (element_line): Style for y-axis line

        Axis Ticks:
            axis_ticks (element_line): Style for all axis ticks
            axis_ticks_x (element_line): Style for x-axis ticks
            axis_ticks_y (element_line): Style for y-axis ticks

        Panel Elements:
            panel_background (element_rect): Background of the plot panel
            panel_grid (element_line): All grid lines
            panel_grid_major (element_line): Major grid lines
            panel_grid_minor (element_line): Minor grid lines
            panel_border (element_rect): Border around plot panel

        Plot Elements:
            plot_title (element_text): Style for plot title
            plot_subtitle (element_text): Style for plot subtitle
            plot_caption (element_text): Style for plot caption
            plot_background (element_rect): Background of entire plot

        Legend Elements:
            legend_title (element_text): Style for legend title
            legend_text (element_text): Style for legend text
            legend_background (element_rect): Background of legend

        Strip Elements (for faceted plots):
            strip_text (element_text): Style for facet strip labels
            strip_background (element_rect): Background of facet strips

        **kwargs: Additional Plotly layout parameters

    Returns:
        Theme: A theme object that can be added to ggplot

    Examples:
        >>> theme(legend_position='bottom')
        >>> theme(axis_title=element_text(size=14, color='blue'))
        >>> theme(panel_background=element_rect(fill='lightgray'))
        >>> theme(plot_title=element_text(size=20, color='darkblue'))
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
    """
    Apply a custom Plotly template as a theme.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_template()
    """

    def apply(self, fig):
        """
        Apply the template theme to a figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        fig.update_layout(template=self.template)


class theme_dark(Theme):
    """
    Dark theme with dark background and light text.

    Automatically applies dark styling to:
    - Standard 2D plots (via plotly_dark template)
    - 3D scenes (dark background with subtle grid)
    - Geographic maps (dark land, ocean, and borders)

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_dark()
    """

    def apply(self, fig):
        """
        Apply the dark theme to a figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
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
    """
    Classic theme with white background and no gridlines.

    Similar to ggplot2's theme_classic().

    Parameters:
        base_size (int): Base font size in points. Default is 11.
        base_family (str): Base font family. Default is "" (system default).

    Automatically applies classic styling to:
    - Standard 2D plots (white background, no gridlines)
    - 3D scenes (white background)
    - Geographic maps (light, clean appearance)

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_classic()
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_classic(base_size=14)
    """

    def __init__(self, base_size=11, base_family=""):
        """
        Initialize theme_classic.

        Parameters:
            base_size (int): Base font size in points. Default is 11.
            base_family (str): Base font family. Default is "" (system default).
        """
        super().__init__()
        self.base_size = base_size
        self.base_family = base_family

    def apply(self, fig):
        """
        Apply the classic theme to a figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
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
    """
    Default theme with light background and gridlines.

    Automatically applies default styling to:
    - Standard 2D plots (white background, light gridlines)
    - Geographic maps (standard light appearance)
    """

    def apply(self, fig):
        """
        Default theme that applies a light background with gridlines using the go.layout.Template.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
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
    """
    BBC-style theme with clean white background and distinctive colors.

    Automatically applies BBC styling to:
    - Standard 2D plots (white background, BBC color palette)
    - Geographic maps (clean, professional appearance)
    """

    def __init__(self):
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
    """
    A theme that replicates the default ggplot2 style from R, including color palette and other global settings.
    This theme uses Plotly's template system to apply the style across all geoms.

    Automatically applies ggplot2 styling to:
    - Standard 2D plots (grey background, white gridlines)
    - 3D scenes (grey background)
    - Geographic maps (grey-toned appearance matching ggplot2)
    """

    def __init__(self):
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
    """
    A theme inspired by New York Times charts, using Plotly's template system to apply style globally.

    Automatically applies NYT styling to:
    - Standard 2D plots (clean white background, subtle gridlines)
    - Geographic maps (clean, professional appearance)
    """

    def __init__(self):
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
    """
    Minimal theme that removes background and gridlines for a cleaner look.

    Parameters:
        base_size (int): Base font size in points. Default is 11.
        base_family (str): Base font family. Default is "" (system default).

    Automatically applies minimal styling to:
    - Standard 2D plots (white background, no gridlines)
    - 3D scenes (white background, subtle grid)
    - Geographic maps (clean, minimal appearance)

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal()
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal(base_size=14)
    """

    def __init__(self, base_size=11, base_family=""):
        """
        Initialize theme_minimal.

        Parameters:
            base_size (int): Base font size in points. Default is 11.
            base_family (str): Base font family. Default is "" (system default).
        """
        super().__init__()
        self.base_size = base_size
        self.base_family = base_family

    def apply(self, fig):
        """
        Minimal theme that removes background and gridlines for a cleaner look, using go.layout.Template.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
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
    def __init__(self, background_color="white", grid_color="grey", text_color="black"):
        self.background_color = background_color
        self.grid_color = grid_color
        self.text_color = text_color

    def apply(self, fig):
        """
        Apply a custom theme using go.layout.Template with customizable background, grid, and text colors.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
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


# themes.py
class element_text:
    def __init__(self, size=12, color="black", family="Arial"):
        """
        Customize text elements.

        Parameters:
            size (int): Font size.
            color (str): Text color.
            family (str): Font family.
        """
        self.size = size
        self.color = color
        self.family = family


class element_line:
    def __init__(self, color="black", width=1, dash="solid"):
        """
        Customize line elements.

        Parameters:
            color (str): Line color.
            width (int): Line width.
            dash (str): Line dash style.
        """
        self.color = color
        self.width = width
        self.dash = dash


class element_rect:
    def __init__(self, fill="white", color="black", width=1):
        """
        Customize rectangle elements.

        Parameters:
            fill (str): Fill color.
            color (str): Border color.
            width (int): Border width.
        """
        self.fill = fill
        self.color = color
        self.width = width
