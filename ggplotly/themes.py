class Theme:
    def apply(self, fig):
        """
        Base Theme class.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
        """
        pass  # To be implemented by subclasses


class theme_bw(Theme):
    def apply(self, fig):
        fig.update_layout(template="ggplot2")


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
        Default theme that applies a light background with gridlines.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
        """
        fig.update_layout(
            template="plotly_white",
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
            font=dict(color="black"),
        )


class theme_minimal(Theme):
    def apply(self, fig):
        """
        Minimal theme that removes background and gridlines for a cleaner look.

        Parameters:
            fig (Figure): The Plotly figure to which the theme will be applied.
        """
        fig.update_layout(
            template="simple_white",
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
            font=dict(color="black"),
        )


# themes.py
class theme_custom(Theme):
    def __init__(self, background_color="white", grid_color="grey", text_color="black"):
        self.background_color = background_color
        self.grid_color = grid_color
        self.text_color = text_color

    def apply(self, fig):
        fig.update_layout(
            plot_bgcolor=self.background_color,
            paper_bgcolor=self.background_color,
            font=dict(color=self.text_color),
            xaxis=dict(showgrid=True, gridcolor=self.grid_color),
            yaxis=dict(showgrid=True, gridcolor=self.grid_color),
        )


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
