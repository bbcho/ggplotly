# scales/scale_shape_manual.py

from .scale_base import Scale


class scale_shape_manual(Scale):
    def __init__(self, values, name=None, breaks=None, labels=None):
        """
        Manually set shapes for discrete shape scales.

        Parameters:
            values (list or dict): A list or dictionary of Plotly marker symbols.
                If a list, shapes are assigned in order to categories.
                If a dict, keys should be category names and values should be Plotly symbols.

                Common Plotly marker symbols:
                - 'circle', 'circle-open'
                - 'square', 'square-open'
                - 'diamond', 'diamond-open'
                - 'cross', 'x'
                - 'triangle-up', 'triangle-down', 'triangle-left', 'triangle-right'
                - 'star', 'star-open'
                - 'hexagon', 'hexagon-open'
                - 'pentagon', 'pentagon-open'

            name (str): Legend title for the shape scale.
            breaks (list): List of categories to appear in the legend.
            labels (list): List of labels corresponding to the breaks.
        """
        self.values = values
        self.name = name
        self.breaks = breaks
        self.labels = labels

    def apply(self, fig):
        """
        Apply the manual shape scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Create a mapping of categories to shapes
        if isinstance(self.values, dict):
            shape_map = self.values
        else:
            # Assume values is a list; extract categories from the data
            categories = []
            for trace in fig.data:
                if "name" in trace and trace.name not in categories:
                    categories.append(trace.name)
            shape_map = dict(zip(categories, self.values))

        # Update trace marker symbols based on the mapping
        for trace in fig.data:
            if "name" in trace and trace.name in shape_map:
                shape = shape_map[trace.name]
                if hasattr(trace, 'marker'):
                    trace.marker.symbol = shape

        # Update the legend title if provided
        if self.name is not None:
            fig.update_layout(legend_title_text=self.name)

        # Update legend items if breaks and labels are provided
        if self.breaks is not None and self.labels is not None:
            for trace in fig.data:
                if trace.name in self.breaks:
                    idx = self.breaks.index(trace.name)
                    trace.name = self.labels[idx]
