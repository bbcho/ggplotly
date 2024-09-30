# scales/scale_size.py

from .scale_base import Scale
import numpy as np


class scale_size(Scale):
    def __init__(self, range=(2, 10), name=None):
        """
        Map a continuous variable to size aesthetic.

        Parameters:
            range (tuple): Two-element tuple specifying the min and max sizes.
            name (str): Legend title for the size scale.
        """
        self.range = range
        self.name = name

    def apply(self, fig):
        """
        Apply the size scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Find the min and max values in the size data
        size_data = []
        for trace in fig.data:
            if "marker" in trace and "size" in trace.marker:
                size = trace.marker.size
                if isinstance(size, (list, tuple, np.ndarray)):
                    size_data.extend(size)

        if not size_data:
            return  # No size data to scale

        size_min, size_max = min(size_data), max(size_data)
        size_range = self.range

        # Apply scaling to marker sizes
        for trace in fig.data:
            if "marker" in trace and "size" in trace.marker:
                size = trace.marker.size
                if isinstance(size, (list, tuple, np.ndarray)):
                    # Normalize and scale sizes
                    normalized_sizes = [
                        ((s - size_min) / (size_max - size_min))
                        * (size_range[1] - size_range[0])
                        + size_range[0]
                        for s in size
                    ]
                    trace.marker.size = normalized_sizes
                else:
                    # Single size value; scale directly
                    trace.marker.size = size_range[0]

        # Update legend if needed
        if self.name is not None:
            fig.update_layout(legend_title_text=self.name)
