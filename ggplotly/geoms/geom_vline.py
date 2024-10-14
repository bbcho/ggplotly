from .geom_base import Geom


class geom_vline(Geom):
    """
    Geom for drawing vertical lines.

    Parameters:
        x (float or list of floats): The x-coordinate(s) where the vertical line(s) should be drawn.
        color (str, optional): Color of the lines. Default is 'black'.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        name (str, optional): Name of the line(s) for the legend.
    """

    __name__ = "geom_vline"

    def draw(self, fig, data=None, row=1, col=1):
        x = data if data is not None else self.data

        if x is None:
            raise ValueError("Parameter 'x' must be provided for geom_vline")

        if not isinstance(x, list):
            x = [x]

        color = self.params.get("color", "red")
        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)
        name = self.params.get("name", "vline")

        for x_coord in x:
            fig.add_vline(
                x=x_coord,
                line=dict(color=color, dash=linetype, width=2),
                opacity=alpha,
                row=row,
                col=col,
                name=name,
            )
