# coords/coord_cartesian.py
"""Cartesian coordinate system with optional limits (zoom)."""

from .coord_base import Coord


class coord_cartesian(Coord):
    """
    Cartesian coordinate system with optional axis limits.

    Unlike setting limits via scales, coord_cartesian zooms into the plot
    without removing data points outside the range. This preserves
    statistical summaries computed on the full data.

    Parameters:
        xlim (tuple): Two-element tuple (min, max) for x-axis limits.
        ylim (tuple): Two-element tuple (min, max) for y-axis limits.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10))
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(ylim=(-5, 5))
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10), ylim=(0, 100))
    """

    def __init__(self, xlim=None, ylim=None):
        """
        Initialize the cartesian coordinate system.

        Parameters:
            xlim (tuple): Two-element tuple (min, max) for x-axis limits.
            ylim (tuple): Two-element tuple (min, max) for y-axis limits.
        """
        self.xlim = xlim
        self.ylim = ylim

    def apply(self, fig):
        """
        Apply axis limits to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        if self.xlim:
            fig.update_xaxes(range=self.xlim)
        if self.ylim:
            fig.update_yaxes(range=self.ylim)
