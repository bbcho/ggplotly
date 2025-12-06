# coords/coord_base.py
"""
Base class for coordinate system transformations.

Coordinate systems control how data coordinates are mapped to the plot plane.
They can transform, flip, or project coordinates in various ways.
"""


class Coord:
    """
    Base class for all coordinate systems in ggplotly.

    Coordinate systems transform the mapping from data coordinates to
    visual positions. They can zoom, flip axes, or apply projections
    like polar coordinates.

    All coordinate systems must implement the apply() method which
    takes a Plotly figure and modifies it in place.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10))
        >>> ggplot(df, aes(x='x', y='y')) + geom_bar() + coord_flip()
    """

    def apply(self, fig):
        """
        Apply the coordinate transformation to the figure.

        Parameters:
            fig (Figure): Plotly figure object to modify.

        Note:
            Subclasses must implement this method.
        """
        pass  # To be implemented by subclasses
