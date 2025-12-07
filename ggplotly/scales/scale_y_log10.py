"""Logarithmic scale transformation for the y-axis."""

from .scale_base import Scale


class scale_y_log10(Scale):
    """
    Transform the y-axis to a log10 scale.

    This scale is useful for data that spans several orders of magnitude,
    making patterns in the lower range more visible.

    Parameters:
        name (str, optional): Title for the y-axis.
        breaks (list, optional): List of positions at which to place tick marks.
            Should be on the original (non-logged) scale.
        minor_breaks (list, optional): List of positions for minor tick marks.
        labels (list, optional): List of labels corresponding to the breaks.
            Can also be a callable that takes breaks and returns labels.
        limits (tuple, optional): Two-element tuple (min, max) for axis limits.
            Should be on the original (non-logged) scale.
        expand (tuple, optional): Expansion to add around the data range.
            Default is (0.05, 0).
        oob (str, optional): How to handle out-of-bounds values.
            Options: 'censor' (default), 'squish', 'keep'.
        na_value (float, optional): Value to use for NA/negative data.
        guide (str, optional): Type of guide. Default is 'axis'.

    Examples:
        >>> ggplot(df, aes(x='x', y='income')) + geom_point() + scale_y_log10()
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_y_log10(name='Income (log scale)')
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_y_log10(breaks=[1, 10, 100, 1000])
    """

    def __init__(self, name=None, breaks=None, minor_breaks=None, labels=None,
                 limits=None, expand=(0.05, 0), oob='censor', na_value=None,
                 guide='axis'):
        """
        Initialize the log10 y-axis scale.

        Parameters:
            name (str, optional): Axis title.
            breaks (list, optional): Tick positions (on original scale).
            minor_breaks (list, optional): Minor tick positions.
            labels (list or callable, optional): Labels for breaks.
            limits (tuple, optional): Axis limits (on original scale).
            expand (tuple): Expansion factor (mult, add). Default is (0.05, 0).
            oob (str): Out-of-bounds handling. Default is 'censor'.
            na_value (float, optional): Value for NA data.
            guide (str): Guide type. Default is 'axis'.
        """
        self.name = name
        self.breaks = breaks
        self.minor_breaks = minor_breaks
        self.labels = labels
        self.limits = limits
        self.expand = expand
        self.oob = oob
        self.na_value = na_value
        self.guide = guide

    def apply(self, fig):
        """
        Apply log10 transformation to the y-axis.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        yaxis_update = {"type": "log"}

        if self.name is not None:
            yaxis_update["title_text"] = self.name

        if self.limits is not None:
            yaxis_update["range"] = self.limits

        if self.breaks is not None:
            yaxis_update["tickmode"] = "array"
            yaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                if callable(self.labels):
                    yaxis_update["ticktext"] = self.labels(self.breaks)
                else:
                    yaxis_update["ticktext"] = self.labels

        fig.update_yaxes(**yaxis_update)
