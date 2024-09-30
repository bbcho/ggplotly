# scales/scale_fill_gradient.py

from .scale_base import Scale
import numpy as np


class scale_fill_gradient(Scale):
    def __init__(self, low="blue", high="red", name=None):
        """
        Create a continuous color gradient for fill aesthetics.

        Parameters:
            low (str): Color for low end of the gradient.
            high (str): Color for high end of the gradient.
            name (str): Legend title for the fill scale.
        """
        self.low = low
        self.high = high
        self.name = name

    def apply(self, fig):
        """
        Apply the gradient fill scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Define the colorscale
        colorscale = [[0, self.low], [1, self.high]]

        # Update traces that use fill colors
        for trace in fig.data:
            if "marker" in trace and "color" in trace.marker:
                if isinstance(trace.marker.color, (list, tuple, np.ndarray)):
                    trace.marker.colorscale = colorscale
                    trace.marker.colorbar = dict(title=self.name)
            elif "z" in trace:
                trace.colorscale = colorscale
                trace.colorbar = dict(title=self.name)

        # Update color axis if applicable
        fig.update_layout(coloraxis_colorbar=dict(title=self.name))
