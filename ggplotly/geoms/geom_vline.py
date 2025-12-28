
from .geom_base import Geom


class geom_vline(Geom):
    """Geom for drawing vertical reference lines."""

    required_aes = []  # xintercept comes from data/params, not mapping
    default_params = {"size": 2}

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw vertical lines at specified x-intercepts.

        Parameters
        ----------
        data : float or list of float
            X-coordinate(s) for vertical line(s). Same as xintercept.
        mapping : aes, optional
            Aesthetic mappings (typically not used for vline).
        color : str, default='black'
            Line color.
        linetype : str, default='solid'
            Line style: 'solid', 'dash', 'dot', 'dashdot'.
        alpha : float, default=1
            Transparency (0-1).
        size : float, default=2
            Line width.
        name : str, optional
            Legend name.

        Examples
        --------
        >>> geom_vline(data=5)
        >>> geom_vline(data=[1, 2, 3], color='red', linetype='dash')
        """
        # data parameter is the xintercept value (matching ggplot2's data parameter)
        if data is not None:
            params['xintercept'] = data
        super().__init__(None, mapping, **params)

    def _draw_impl(self, fig, data, row, col):

        # Get xintercept from params (ggplot2 convention)
        x = self.params.get("xintercept", None)

        # Fallback to x param if xintercept not provided
        if x is None:
            x = self.params.get("x", None)

        if x is None:
            raise ValueError("Parameter 'xintercept' must be provided for geom_vline")

        if not isinstance(x, list):
            x = [x]

        color = self._get_reference_line_color()
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
