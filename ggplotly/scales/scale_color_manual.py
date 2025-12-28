# scales/scale_color_manual.py

from .scale_base import Scale


class scale_color_manual(Scale):
    aesthetic = 'color'

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
        self._apply_manual_color_mapping(
            fig, self.values, name=self.name,
            breaks=self.breaks, labels=self.labels,
            update_fill=False
        )
