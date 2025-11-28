# scales/scale_fill_viridis.py

from .scale_base import Scale
import numpy as np


class scale_fill_viridis_c(Scale):
    def __init__(self, option="viridis", name=None, direction=1):
        """
        Create a viridis continuous color scale for fill aesthetics.

        Parameters:
            option (str): Viridis palette option. One of:
                         'viridis', 'plasma', 'inferno', 'magma', 'cividis'
            name (str): Legend title for the fill scale.
            direction (int): Direction of the scale. 1 = normal, -1 = reversed.
        """
        self.option = option.capitalize()
        self.name = name
        self.direction = direction

    def apply(self, fig):
        """
        Apply the viridis fill scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Map option to Plotly colorscale name
        colorscale = self.option
        if self.direction == -1:
            colorscale = colorscale + "_r"

        # Update traces that use fill colors (like heatmaps)
        for trace in fig.data:
            if hasattr(trace, 'colorscale'):
                trace.colorscale = colorscale
                if self.name:
                    trace.colorbar = dict(title=self.name)

        # Update color axis if applicable
        if self.name:
            fig.update_layout(coloraxis_colorbar=dict(title=self.name))
