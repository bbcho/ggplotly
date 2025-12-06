"""Logarithmic scale transformation for the x-axis."""

from .scale_base import Scale


class scale_x_log10(Scale):
    """
    Transform the x-axis to a log10 scale.

    This scale is useful for data that spans several orders of magnitude,
    making patterns in the lower range more visible.

    Examples:
        >>> ggplot(df, aes(x='population', y='gdp')) + geom_point() + scale_x_log10()
    """

    def apply(self, fig):
        """
        Apply log10 transformation to the x-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        fig.update_xaxes(type="log")
