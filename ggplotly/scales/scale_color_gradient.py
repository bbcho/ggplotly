"""Continuous color gradient scale for the color aesthetic."""

from .scale_base import Scale


class scale_color_gradient(Scale):
    """
    Create a two-color continuous gradient for the color aesthetic.

    Maps numeric values to a color gradient between two colors,
    useful for visualizing continuous variables.

    Parameters:
        low (str): Color for low values. Default is 'blue'.
        high (str): Color for high values. Default is 'red'.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + scale_color_gradient(low='white', high='red')
        >>> ggplot(df, aes(x='x', y='y', color='temp')) + geom_point() + scale_color_gradient(low='blue', high='orange')
    """

    def __init__(self, low="blue", high="red"):
        """
        Initialize the color gradient scale.

        Parameters:
            low (str): Color for low values. Default is 'blue'.
            high (str): Color for high values. Default is 'red'.
        """
        self.low = low
        self.high = high

    def apply(self, fig):
        """
        Apply the color gradient to markers in the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        for trace in fig.data:
            if "marker" in trace:
                trace.marker.colorscale = [[0, self.low], [1, self.high]]
