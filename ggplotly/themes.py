import plotly.graph_objects as go


class Theme:
    def __init__(self, template=None):
        """
        Base Theme class.

        Parameters:
            template (go.layout.Template, optional): Plotly template to apply to the figure.
        """
        self.template = template

    def apply(self, fig):
        """
        Base Theme class.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
        """
        pass  # To be implemented by subclasses


# class theme_bw(Theme):
#     def apply(self, fig):
#         fig.update_layout(template="simple_white")


class theme_template(Theme):
    def apply(self, fig):
        fig.update_layout(template=self.template)


class theme_dark(Theme):
    def apply(self, fig):
        fig.update_layout(template="plotly_dark")


class theme_classic(Theme):
    def apply(self, fig):
        fig.update_layout(
            template="simple_white",
            xaxis=dict(showgrid=False),
            yaxis=dict(showgrid=False),
        )


class theme_default(Theme):
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


class theme_ggplot2(Theme):
    """
    A theme that replicates the default ggplot2 style from R, including color palette and other global settings.
    This theme uses Plotly's template system to apply the style across all geoms.
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


class theme_nytimes(Theme):
    """
    A theme inspired by New York Times charts, using Plotly's template system to apply style globally.
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


class theme_minimal(Theme):
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
