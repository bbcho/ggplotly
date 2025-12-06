"""Logarithmic scale transformation for the y-axis."""

from .scale_base import Scale


class scale_y_log10(Scale):
    """
    Transform the y-axis to a log10 scale.

    This scale is useful for data that spans several orders of magnitude,
    making patterns in the lower range more visible.

    Examples:
        >>> ggplot(df, aes(x='x', y='income')) + geom_point() + scale_y_log10()
    """

    def apply(self, fig):
        """
        Apply log10 transformation to the y-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        fig.update_yaxes(type="log")
