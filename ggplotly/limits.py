# limits.py

from .coords.coord_base import Coord


class xlim(Coord):
    """
    Set x-axis limits.

    This zooms the plot to the specified range without clipping data.
    Equivalent to coord_cartesian(xlim=...).

    Parameters:
        *args: Either two positional arguments (min, max) or a tuple/list.

    Examples:
        ggplot(df, aes(x='x', y='y')) + geom_point() + xlim(0, 10)
        ggplot(df, aes(x='x', y='y')) + geom_point() + xlim((0, 10))
    """

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            self.limits = tuple(args[0])
        elif len(args) == 2:
            self.limits = (args[0], args[1])
        else:
            raise ValueError("xlim requires two values: xlim(min, max) or xlim((min, max))")

    def apply(self, fig):
        """
        Apply x-axis limits to the figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        fig.update_xaxes(range=self.limits)


class ylim(Coord):
    """
    Set y-axis limits.

    This zooms the plot to the specified range without clipping data.
    Equivalent to coord_cartesian(ylim=...).

    Parameters:
        *args: Either two positional arguments (min, max) or a tuple/list.

    Examples:
        ggplot(df, aes(x='x', y='y')) + geom_point() + ylim(0, 100)
        ggplot(df, aes(x='x', y='y')) + geom_point() + ylim((0, 100))
    """

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], '__iter__'):
            self.limits = tuple(args[0])
        elif len(args) == 2:
            self.limits = (args[0], args[1])
        else:
            raise ValueError("ylim requires two values: ylim(min, max) or ylim((min, max))")

    def apply(self, fig):
        """
        Apply y-axis limits to the figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        fig.update_yaxes(range=self.limits)


class lims(Coord):
    """
    Set axis limits for multiple aesthetics.

    This zooms the plot to the specified ranges without clipping data.

    Parameters:
        x: Tuple of (min, max) for x-axis limits.
        y: Tuple of (min, max) for y-axis limits.

    Examples:
        ggplot(df, aes(x='x', y='y')) + geom_point() + lims(x=(0, 10), y=(0, 100))
        ggplot(df, aes(x='x', y='y')) + geom_point() + lims(y=(0, 100))
    """

    def __init__(self, x=None, y=None):
        self.xlim = tuple(x) if x is not None else None
        self.ylim = tuple(y) if y is not None else None

    def apply(self, fig):
        """
        Apply axis limits to the figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        if self.xlim is not None:
            fig.update_xaxes(range=self.xlim)
        if self.ylim is not None:
            fig.update_yaxes(range=self.ylim)
