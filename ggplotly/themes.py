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

def theme(legend_position='right', legend_show=True, **kwargs):
    """
    Create a custom theme with legend control (ggplot2-style).
    
    Parameters:
        legend_position (str): 'right', 'left', 'top', 'bottom', 'none'
        legend_show (bool): Whether to show legend
        **kwargs: Additional theme parameters
    
    Returns:
        Theme: A theme object that can be added to ggplot
    """
    class CustomTheme(Theme):
        def __init__(self):
            super().__init__(legend_position=legend_position, legend_show=legend_show)
        
        def apply(self, fig):
            super().apply(fig)
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

    Automatically applies classic styling to:
    - Standard 2D plots (white background, no gridlines)
    - 3D scenes (white background)
    - Geographic maps (light, clean appearance)

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + theme_classic()
    """

    def apply(self, fig):
        """
        Apply the classic theme to a figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        fig.update_layout(
            template="simple_white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
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

    Automatically applies minimal styling to:
    - Standard 2D plots (white background, no gridlines)
    - 3D scenes (white background, subtle grid)
    - Geographic maps (clean, minimal appearance)
    """

    def apply(self, fig):
        """
        Minimal theme that removes background and gridlines for a cleaner look, using go.layout.Template.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
        """
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
                font=dict(color="black", size=12),
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
