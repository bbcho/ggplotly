from .geom_base import Geom


class geom_hline(Geom):
    """
    Geom for drawing horizontal lines.

    Parameters:
        y (float or list of floats): The y-coordinate(s) where the horizontal line(s) should be drawn.
        color (str, optional): Color of the lines. Default is 'black'.
        linetype (str, optional): Line style ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the lines. Default is 1.
        name (str, optional): Name of the line(s) for the legend.
    """

    __name__ = "geom_hline"

    def draw(self, fig, data=None, row=1, col=1):
        y = data if data is not None else self.data

        if y is None:
            raise ValueError("Parameter 'y' must be provided for geom_hline")

        if not isinstance(y, list):
            y = [y]

        color = self.params.get("color", "red")
        linetype = self.params.get("linetype", "solid")
        alpha = self.params.get("alpha", 1)
        name = self.params.get("name", "hline")

        for y_coord in y:
            fig.add_hline(
                y=y_coord,
                line=dict(color=color, dash=linetype, width=2),
                opacity=alpha,
                row=row,
                col=col,
                name=name,
            )
