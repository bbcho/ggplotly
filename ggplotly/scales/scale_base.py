# scales/scale_base.py
"""
Base class for all scale transformations.

Scales control how data values are mapped to visual properties like
position, color, size, and shape. They can also modify axis appearance.
"""


class Scale:
    """
    Base class for all scales in ggplotly.

    Scales transform data values into visual properties. Subclasses implement
    specific transformations for axes, colors, sizes, shapes, etc.

    All scales must implement the apply() method which takes a Plotly figure
    and modifies it in place.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10()
        >>> ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + scale_color_manual(['red', 'blue'])
    """

    def apply(self, fig):
        """
        Apply the scale transformation to the figure.

        Parameters:
            fig (Figure): Plotly figure object to modify.

        Note:
            Subclasses must implement this method.
        """
        pass  # To be implemented by subclasses
