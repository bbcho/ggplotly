# scales/scale_x_continuous.py

from .scale_base import Scale
import numpy as np


class scale_x_continuous(Scale):
    def __init__(self, name=None, limits=None, breaks=None, labels=None, trans=None):
        """
        Continuous position scale for the x-axis.

        Parameters:
            name (str): Label for the x-axis.
            limits (tuple): Two-element tuple specifying the axis limits (min, max).
            breaks (list): List of positions at which to place ticks.
            labels (list): List of labels corresponding to the breaks.
            trans (str): Transformation to apply ('log', 'sqrt', etc.).
        """
        self.name = name
        self.limits = limits
        self.breaks = breaks
        self.labels = labels
        self.trans = trans

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
            xaxis_update["range"] = self.limits

        if self.breaks is not None:
            xaxis_update["tickmode"] = "array"
            xaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                xaxis_update["ticktext"] = self.labels

        if self.trans is not None:
            if self.trans == "log":
                xaxis_update["type"] = "log"
            elif self.trans == "sqrt":
                # Custom transformation needed as Plotly doesn't support 'sqrt' natively
                xaxis_update["type"] = "linear"
                xaxis_update["tickmode"] = "linear"
                fig.data[0].x = [np.sqrt(val) for val in fig.data[0].x]
            else:
                raise ValueError(f"Unsupported transformation: {self.trans}")

        fig.update_xaxes(**xaxis_update)
