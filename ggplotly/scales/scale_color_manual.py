# scales/scale_color_manual.py

from .scale_base import Scale


class scale_color_manual(Scale):
    def __init__(self, values, name=None, breaks=None, labels=None):
        """
        Manually set colors for discrete color scales.

        Parameters:
            values (list or dict): A list or dictionary of colors.
            name (str): Legend title for the color scale.
            breaks (list): List of categories to appear in the legend.
            labels (list): List of labels corresponding to the breaks.
        """
        self.values = values
        self.name = name
        self.breaks = breaks
        self.labels = labels

    def apply(self, fig):
        """
        Apply the manual color scale to the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        # Create a mapping of categories to colors
        if isinstance(self.values, dict):
            color_map = self.values
        else:
            # Assume values is a list; extract categories from the data
            categories = []
            for trace in fig.data:
                if "name" in trace and trace.name not in categories:
                    categories.append(trace.name)
            color_map = dict(zip(categories, self.values))

        # Update trace colors based on the mapping
        for trace in fig.data:
            if "name" in trace and trace.name in color_map:
                color = color_map[trace.name]
                if "marker" in trace:
                    trace.marker.color = color
                elif "line" in trace:
                    trace.line.color = color
                elif "fillcolor" in trace:
                    trace.fillcolor = color

        # Update the legend title if provided
        if self.name is not None:
            fig.update_layout(legend_title_text=self.name)

        # Update legend items if breaks and labels are provided
        if self.breaks is not None and self.labels is not None:
            for trace in fig.data:
                if trace.name in self.breaks:
                    idx = self.breaks.index(trace.name)
                    trace.name = self.labels[idx]
