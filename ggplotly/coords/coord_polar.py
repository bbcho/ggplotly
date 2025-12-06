"""Polar coordinate system for circular plots."""

from .coord_base import Coord


class coord_polar(Coord):
    """
    Polar coordinate system for circular/radial plots.

    Transforms cartesian coordinates into polar coordinates where
    x maps to angle and y maps to radius. Useful for pie charts,
    radar charts, and other circular visualizations.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_polar()
    """

    def apply(self, fig):
        """
        Apply polar coordinate transformation to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True), angularaxis=dict(visible=True)),
            showlegend=False,
        )
        fig.update_traces(mode="lines")
