# coords/coord_fixed.py
"""Fixed aspect ratio coordinate system."""

from .coord_base import Coord


class coord_fixed(Coord):
    """
    Cartesian coordinate system with a fixed aspect ratio.

    A fixed aspect ratio ensures that one unit on the x-axis is the same length
    as one unit on the y-axis (when ratio=1). This is essential for:
    - Maps where distortion must be avoided
    - Scatter plots where the relationship shape matters
    - Any plot where physical proportions are important

    Parameters:
        ratio (float): The aspect ratio, expressed as y/x. Default is 1, meaning
            one unit on the x-axis equals one unit on the y-axis.
            - ratio > 1: y-axis units are longer than x-axis units
            - ratio < 1: x-axis units are longer than y-axis units
        xlim (tuple, optional): Two-element tuple (min, max) for x-axis limits.
        ylim (tuple, optional): Two-element tuple (min, max) for y-axis limits.
        expand (bool): If True (default), add a small expansion to the limits.
        clip (str): Should drawing be clipped to extent of plot panel?
            Options: 'on' (default) or 'off'.

    Examples:
        >>> # Equal aspect ratio (1:1)
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_fixed()

        >>> # Map with equal coordinates
        >>> ggplot(map_df, aes(x='lon', y='lat')) + geom_polygon() + coord_fixed()

        >>> # Custom aspect ratio (y is twice as long as x)
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_fixed(ratio=2)

        >>> # Fixed ratio with explicit limits
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + coord_fixed(xlim=(0, 10), ylim=(0, 10))

        >>> # Circle should look like a circle, not an ellipse
        >>> ggplot(circle_df, aes(x='x', y='y')) + geom_path() + coord_fixed()

    See Also:
        coord_cartesian: Cartesian coordinates without fixed ratio
        coord_sf: Coordinate system for spatial data (also maintains aspect ratio)
    """

    def __init__(self, ratio=1, xlim=None, ylim=None, expand=True, clip='on'):
        """
        Initialize the fixed aspect ratio coordinate system.

        Parameters:
            ratio (float): Aspect ratio y/x. Default is 1 (equal scaling).
            xlim (tuple, optional): X-axis limits (min, max).
            ylim (tuple, optional): Y-axis limits (min, max).
            expand (bool): Whether to add expansion around limits. Default is True.
            clip (str): Clipping mode ('on' or 'off'). Default is 'on'.
        """
        self.ratio = ratio
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
        self.clip = clip

    def _apply_expansion(self, limits, default_expand=(0.05, 0)):
        """Apply expansion to limits if expand is True."""
        if limits is None or not self.expand:
            return limits

        low, high = limits
        data_range = high - low

        mult = default_expand[0]
        add = default_expand[1] if len(default_expand) > 1 else 0

        new_low = low - data_range * mult - add
        new_high = high + data_range * mult + add
        return [new_low, new_high]

    def apply(self, fig):
        """
        Apply fixed aspect ratio to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        xaxis_update = {}
        yaxis_update = {
            "scaleanchor": "x",
            "scaleratio": self.ratio,
        }

        # Apply limits if specified
        if self.xlim is not None:
            expanded_xlim = self._apply_expansion(self.xlim)
            xaxis_update["range"] = expanded_xlim

        if self.ylim is not None:
            expanded_ylim = self._apply_expansion(self.ylim)
            yaxis_update["range"] = expanded_ylim

        # Handle clipping
        if self.clip == 'off':
            for trace in fig.data:
                if hasattr(trace, 'cliponaxis'):
                    trace.cliponaxis = False

        fig.update_xaxes(**xaxis_update)
        fig.update_yaxes(**yaxis_update)
