# scales/scale_y_continuous.py

from .scale_base import Scale
import numpy as np


class scale_y_continuous(Scale):
    def __init__(self, name=None, limits=None, breaks=None, labels=None, trans=None):
        """
        Continuous position scale for the y-axis.

        Parameters:
            name (str): Label for the y-axis.
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
        Apply the scale transformation to the y-axis of the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        yaxis_update = {}

        if self.name is not None:
            yaxis_update["title_text"] = self.name

        if self.limits is not None:
            yaxis_update["range"] = self.limits

        if self.breaks is not None:
            yaxis_update["tickmode"] = "array"
            yaxis_update["tickvals"] = self.breaks
            if self.labels is not None:
                yaxis_update["ticktext"] = self.labels

        if self.trans is not None:
            if self.trans == "log":
                yaxis_update["type"] = "log"
            elif self.trans == "sqrt":
                # Custom transformation needed as Plotly doesn't support 'sqrt' natively
                yaxis_update["type"] = "linear"
                yaxis_update["tickmode"] = "linear"
                fig.data[0].y = [np.sqrt(val) for val in fig.data[0].y]
            else:
                raise ValueError(f"Unsupported transformation: {self.trans}")

        fig.update_yaxes(**yaxis_update)
