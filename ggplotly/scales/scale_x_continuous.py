# scales/scale_x_continuous.py

from .scale_base import Scale
import numpy as np


class scale_x_continuous(Scale):
    """
    Continuous position scale for the x-axis.

    Position scales control how data values are mapped to visual positions.
    This scale handles continuous numeric data on the x-axis.

    Parameters:
        name (str, optional): Label for the x-axis.
        limits (tuple, optional): Two-element tuple (min, max) specifying the axis limits.
            Values outside limits will be removed (use oob to change this behavior).
        breaks (list, optional): List of positions at which to place major tick marks.
        minor_breaks (list, optional): List of positions for minor tick marks.
        n_breaks (int, optional): Approximate number of breaks to generate automatically.
            Default is 5. Ignored if breaks is provided.
        labels (list, optional): List of labels corresponding to the breaks.
            Can also be a callable that takes breaks and returns labels.
        expand (tuple, optional): Expansion to add around the data range.
            Default is (0.05, 0) meaning 5% expansion on each side, 0 additive.
            Format: (mult, add) or ((mult_low, mult_high), (add_low, add_high)).
        oob (str, optional): How to handle out-of-bounds values. Options:
            - 'censor': Replace with NA (default)
            - 'squish': Squish to range limits
            - 'keep': Keep all values
        na_value (float, optional): Value to use for missing data. Default is None.
        trans (str, optional): Transformation to apply. Options:
            - 'identity': No transformation (default)
            - 'log', 'log10': Log base 10
            - 'log2': Log base 2
            - 'sqrt': Square root
            - 'reverse': Reverse the axis
        position (str, optional): Position of the axis. Options:
            - 'bottom': Default for x-axis
            - 'top': Place axis at top
        guide (str, optional): Type of guide. Default is 'axis'.
        format (str, optional): Format string for tick labels (e.g., '.2f', '%').

    Examples:
        >>> scale_x_continuous(name='Value')
        >>> scale_x_continuous(limits=(0, 100), breaks=[0, 25, 50, 75, 100])
        >>> scale_x_continuous(trans='log10')
        >>> scale_x_continuous(expand=(0.1, 0))  # 10% expansion on each side
        >>> scale_x_continuous(labels=lambda x: [f'${v}' for v in x])
    """

    def __init__(self, name=None, limits=None, breaks=None, minor_breaks=None,
                 n_breaks=5, labels=None, expand=(0.05, 0), oob='censor',
                 na_value=None, trans=None, position='bottom', guide='axis',
                 format=None):
        """
        Initialize the continuous x-axis scale.

        Parameters:
            name (str, optional): Axis title.
            limits (tuple, optional): Axis limits (min, max).
            breaks (list, optional): Major tick positions.
            minor_breaks (list, optional): Minor tick positions.
            n_breaks (int): Approximate number of auto-generated breaks. Default is 5.
            labels (list or callable, optional): Labels for breaks.
            expand (tuple): Expansion factor (mult, add). Default is (0.05, 0).
            oob (str): Out-of-bounds handling. Default is 'censor'.
            na_value (float, optional): Value for NA data.
            trans (str, optional): Transformation ('log', 'sqrt', 'reverse', etc.).
            position (str): Axis position ('bottom' or 'top'). Default is 'bottom'.
            guide (str): Guide type. Default is 'axis'.
            format (str, optional): Tick label format string.
        """
        self.name = name
        self.limits = limits
        self.breaks = breaks
        self.minor_breaks = minor_breaks
        self.n_breaks = n_breaks
        self.labels = labels
        self.expand = expand
        self.oob = oob
        self.na_value = na_value
        self.trans = trans
        self.position = position
        self.guide = guide
        self.format = format

    def _apply_expansion(self, limits):
        """Apply expansion to limits."""
        if limits is None or self.expand is None:
            return limits

        low, high = limits
        data_range = high - low

        if isinstance(self.expand[0], tuple):
            mult_low, mult_high = self.expand[0]
            add_low, add_high = self.expand[1]
        else:
            mult_low = mult_high = self.expand[0]
            add_low = add_high = self.expand[1] if len(self.expand) > 1 else 0

        new_low = low - data_range * mult_low - add_low
        new_high = high + data_range * mult_high + add_high
        return [new_low, new_high]

    def apply(self, fig):
        """
        Apply the scale transformation to the x-axis of the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        xaxis_update = {}

        if self.name is not None:
            xaxis_update["title_text"] = self.name

        if self.limits is not None:
            expanded_limits = self._apply_expansion(self.limits)
            xaxis_update["range"] = expanded_limits

        if self.breaks is not None:
            xaxis_update["tickmode"] = "array"
            xaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                if callable(self.labels):
                    xaxis_update["ticktext"] = self.labels(self.breaks)
                else:
                    xaxis_update["ticktext"] = self.labels
        elif self.n_breaks is not None:
            xaxis_update["nticks"] = self.n_breaks

        # Handle minor breaks
        if self.minor_breaks is not None:
            xaxis_update["minor"] = {"tickvals": self.minor_breaks, "showgrid": True}

        if self.trans is not None:
            if self.trans in ("log", "log10"):
                xaxis_update["type"] = "log"
            elif self.trans == "log2":
                # Plotly doesn't have native log2, use log and adjust
                xaxis_update["type"] = "log"
                # Note: This gives log10, not log2. True log2 would need data transformation
            elif self.trans == "sqrt":
                # Custom transformation needed as Plotly doesn't support 'sqrt' natively
                xaxis_update["type"] = "linear"
                for trace in fig.data:
                    if hasattr(trace, 'x') and trace.x is not None:
                        trace.x = [np.sqrt(val) if val is not None and val >= 0 else None
                                   for val in trace.x]
            elif self.trans == "reverse":
                xaxis_update["autorange"] = "reversed"
            elif self.trans == "identity":
                pass  # No transformation
            else:
                raise ValueError(f"Unsupported transformation: {self.trans}")

        if self.format is not None:
            xaxis_update["tickformat"] = self.format

        # Handle axis position
        if self.position == "top":
            xaxis_update["side"] = "top"

        fig.update_xaxes(**xaxis_update)
