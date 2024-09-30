# coords/coord_base.py


class Coord:
    """
    Base class for coordinate systems.
    """

    def apply(self, fig):
        """
        Apply the coordinate transformation to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        pass  # To be implemented by subclasses
