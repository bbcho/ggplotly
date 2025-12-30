# scales/scale_y_reverse.py
"""Reversed scale for the y-axis."""

from .scale_base import Scale


class scale_y_reverse(Scale):
    """
    Reverse the y-axis direction.

    This scale reverses the y-axis so that larger values appear at the bottom
    and smaller values at the top. Useful for certain data presentations
    like depth charts, rankings, or inverted coordinate systems.

    Aesthetic: y

    Parameters:
        name (str, optional): Title for the y-axis.
        breaks (list, optional): List of positions at which to place tick marks.
        labels (list, optional): List of labels corresponding to the breaks.
            Can also be a callable that takes breaks and returns labels.
        limits (tuple, optional): Two-element tuple (min, max) for axis limits.
            Note: min should still be less than max; the reversal happens automatically.
        expand (tuple, optional): Expansion to add around the data range.
            Default is (0.05, 0).

    Examples:
        >>> # Simple reversed y-axis
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_y_reverse()

        >>> # Reversed y-axis with custom name (e.g., for rankings)
        >>> ggplot(df, aes(x='name', y='rank')) + geom_col() + scale_y_reverse(name='Rank')

        >>> # Reversed with specific limits
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_y_reverse(limits=(0, 100))

        >>> # Ocean depth chart (depth increases downward)
        >>> ggplot(df, aes(x='distance', y='depth')) + geom_line() + scale_y_reverse()

    See Also:
        scale_x_reverse: Reverse the x-axis
        scale_y_continuous: Continuous y-axis with trans='reverse' option
    """

    aesthetic = 'y'

    def __init__(self, name=None, breaks=None, labels=None, limits=None,
                 expand=(0.05, 0)):
        """
        Initialize the reversed y-axis scale.

        Parameters:
            name (str, optional): Axis title.
            breaks (list, optional): Tick positions.
            labels (list or callable, optional): Labels for breaks.
            limits (tuple, optional): Axis limits (min, max).
            expand (tuple): Expansion factor (mult, add). Default is (0.05, 0).
        """
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.limits = limits
        self.expand = expand

    def _apply_expansion(self, limits):
        """Apply expansion to limits."""
        if limits is None or self.expand is None:
            return limits

        low, high = limits
        data_range = high - low

        mult = self.expand[0]
        add = self.expand[1] if len(self.expand) > 1 else 0

        new_low = low - data_range * mult - add
        new_high = high + data_range * mult + add
        return [new_low, new_high]

    def apply(self, fig):
        """
        Apply reversed transformation to the y-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        yaxis_update = {"autorange": "reversed"}

        if self.name is not None:
            yaxis_update["title_text"] = self.name

        if self.limits is not None:
            expanded_limits = self._apply_expansion(self.limits)
            # For reversed axis, we need to swap the order
            yaxis_update["range"] = [expanded_limits[1], expanded_limits[0]]
            # Remove autorange since we're setting explicit range
            yaxis_update.pop("autorange")

        if self.breaks is not None:
            yaxis_update["tickmode"] = "array"
            yaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                if callable(self.labels):
                    yaxis_update["ticktext"] = self.labels(self.breaks)
                else:
                    yaxis_update["ticktext"] = self.labels

        fig.update_yaxes(**yaxis_update)
