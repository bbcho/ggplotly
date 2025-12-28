# scales/scale_x_reverse.py
"""Reversed scale for the x-axis."""

from .scale_base import Scale


class scale_x_reverse(Scale):
    """
    Reverse the x-axis direction.

    This scale reverses the x-axis so that larger values appear on the left
    and smaller values on the right. Useful for certain data presentations
    like depth charts, time running backwards, etc.

    Aesthetic: x

    Parameters:
        name (str, optional): Title for the x-axis.
        breaks (list, optional): List of positions at which to place tick marks.
        labels (list, optional): List of labels corresponding to the breaks.
            Can also be a callable that takes breaks and returns labels.
        limits (tuple, optional): Two-element tuple (min, max) for axis limits.
            Note: min should still be less than max; the reversal happens automatically.
        expand (tuple, optional): Expansion to add around the data range.
            Default is (0.05, 0).

    Examples:
        >>> # Simple reversed x-axis
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_reverse()

        >>> # Reversed x-axis with custom name
        >>> ggplot(df, aes(x='depth', y='value')) + geom_line() + scale_x_reverse(name='Depth (m)')

        >>> # Reversed with specific limits
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_reverse(limits=(0, 100))

    See Also:
        scale_y_reverse: Reverse the y-axis
        scale_x_continuous: Continuous x-axis with trans='reverse' option
    """

    aesthetic = 'x'

    def __init__(self, name=None, breaks=None, labels=None, limits=None,
                 expand=(0.05, 0)):
        """
        Initialize the reversed x-axis scale.

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
        Apply reversed transformation to the x-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        xaxis_update = {"autorange": "reversed"}

        if self.name is not None:
            xaxis_update["title_text"] = self.name

        if self.limits is not None:
            expanded_limits = self._apply_expansion(self.limits)
            # For reversed axis, we need to swap the order
            xaxis_update["range"] = [expanded_limits[1], expanded_limits[0]]
            # Remove autorange since we're setting explicit range
            xaxis_update.pop("autorange")

        if self.breaks is not None:
            xaxis_update["tickmode"] = "array"
            xaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                if callable(self.labels):
                    xaxis_update["ticktext"] = self.labels(self.breaks)
                else:
                    xaxis_update["ticktext"] = self.labels

        fig.update_xaxes(**xaxis_update)
