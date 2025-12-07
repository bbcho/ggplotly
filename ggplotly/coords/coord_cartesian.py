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
        expand (bool): If True (default), add a small expansion to the limits.
            If False, use exact limits specified.
        default_expand (tuple): Default expansion factor (mult, add).
            Default is (0.05, 0) meaning 5% multiplicative expansion.
        clip (str): Should drawing be clipped to extent of plot panel?
            Options: 'on' (default) or 'off'.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10))
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(ylim=(-5, 5))
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10), ylim=(0, 100))
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(expand=False)
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(clip='off')
    """

    def __init__(self, xlim=None, ylim=None, expand=True, default_expand=(0.05, 0), clip='on'):
        """
        Initialize the cartesian coordinate system.

        Parameters:
            xlim (tuple): Two-element tuple (min, max) for x-axis limits.
            ylim (tuple): Two-element tuple (min, max) for y-axis limits.
            expand (bool): Whether to add expansion around limits. Default is True.
            default_expand (tuple): Expansion factor (mult, add). Default is (0.05, 0).
            clip (str): Clipping mode ('on' or 'off'). Default is 'on'.
        """
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
        self.default_expand = default_expand
        self.clip = clip

    def _apply_expansion(self, limits):
        """Apply expansion to limits if expand is True."""
        if limits is None or not self.expand:
            return limits

        low, high = limits
        data_range = high - low

        mult = self.default_expand[0]
        add = self.default_expand[1] if len(self.default_expand) > 1 else 0

        new_low = low - data_range * mult - add
        new_high = high + data_range * mult + add
        return [new_low, new_high]

    def apply(self, fig):
        """
        Apply axis limits to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        xaxis_update = {}
        yaxis_update = {}

        if self.xlim:
            expanded_xlim = self._apply_expansion(self.xlim)
            xaxis_update['range'] = expanded_xlim

        if self.ylim:
            expanded_ylim = self._apply_expansion(self.ylim)
            yaxis_update['range'] = expanded_ylim

        # Handle clipping
        # In Plotly, cliponaxis controls whether traces are clipped
        if self.clip == 'off':
            # Setting constrain to 'domain' allows overflow
            xaxis_update['constrain'] = 'domain'
            yaxis_update['constrain'] = 'domain'
            # Also update traces to not clip
            for trace in fig.data:
                if hasattr(trace, 'cliponaxis'):
                    trace.cliponaxis = False

        if xaxis_update:
            fig.update_xaxes(**xaxis_update)
        if yaxis_update:
            fig.update_yaxes(**yaxis_update)
