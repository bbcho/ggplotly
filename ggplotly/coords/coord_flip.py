from .coord_base import Coord


class coord_flip(Coord):
    """
    Flip cartesian coordinates so x becomes y and y becomes x.

    This is useful for horizontal bar charts and other cases where
    you want to swap the axes.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_flip()
    """

    def apply(self, fig):
        """
        Apply coordinate flip to the figure.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        fig.update_layout(xaxis=dict(autorange="reversed"))
