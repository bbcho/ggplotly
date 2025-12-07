"""Continuous color gradient scale for the color aesthetic."""

from .scale_base import Scale


class scale_color_gradient(Scale):
    """
    Create a two-color continuous gradient for the color aesthetic.

    Maps numeric values to a color gradient between two colors,
    useful for visualizing continuous variables.

    Parameters:
        low (str): Color for low values. Default is '#132B43' (dark blue).
        high (str): Color for high values. Default is '#56B1F7' (light blue).
        name (str, optional): Title for the colorbar legend.
        limits (tuple, optional): Two-element tuple (min, max) to set the range of values.
            Values outside this range will be clamped or treated as NA.
        breaks (list, optional): List of values at which to show tick marks on colorbar.
        labels (list, optional): Labels corresponding to breaks.
        na_value (str): Color for missing values. Default is 'grey50'.
        guide (str): Type of legend. 'colourbar' (default) or 'none'.
        aesthetics (str): The aesthetic this scale applies to. Default is 'color'.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + scale_color_gradient()
        >>> ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + scale_color_gradient(low='white', high='red')
        >>> ggplot(df, aes(x='x', y='y', color='temp')) + geom_point() + scale_color_gradient(low='blue', high='orange', name='Temperature')
    """

    def __init__(self, low="#132B43", high="#56B1F7", name=None, limits=None,
                 breaks=None, labels=None, na_value='grey50', guide='colourbar',
                 aesthetics='color'):
        """
        Initialize the color gradient scale.

        Parameters:
            low (str): Color for low values. Default is '#132B43' (dark blue).
            high (str): Color for high values. Default is '#56B1F7' (light blue).
            name (str, optional): Title for the colorbar legend.
            limits (tuple, optional): Range of values (min, max).
            breaks (list, optional): Values at which to show ticks.
            labels (list, optional): Labels for the breaks.
            na_value (str): Color for NA values. Default is 'grey50'.
            guide (str): Legend type ('colourbar' or 'none'). Default is 'colourbar'.
            aesthetics (str): The aesthetic this applies to. Default is 'color'.
        """
        self.low = low
        self.high = high
        self.name = name
        self.limits = limits
        self.breaks = breaks
        self.labels = labels
        self.na_value = na_value
        self.guide = guide
        self.aesthetics = aesthetics

    def apply(self, fig):
        """
        Apply the color gradient to markers in the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        for trace in fig.data:
            if hasattr(trace, 'marker') and trace.marker is not None:
                trace.marker.colorscale = [[0, self.low], [1, self.high]]

                # Apply limits if specified
                if self.limits is not None:
                    trace.marker.cmin = self.limits[0]
                    trace.marker.cmax = self.limits[1]

                # Configure colorbar
                if self.guide != 'none':
                    colorbar_config = {}
                    if self.name is not None:
                        colorbar_config['title'] = self.name
                    if self.breaks is not None:
                        colorbar_config['tickvals'] = self.breaks
                        if self.labels is not None:
                            colorbar_config['ticktext'] = self.labels
                    if colorbar_config:
                        trace.marker.colorbar = colorbar_config
                    trace.marker.showscale = True
                else:
                    trace.marker.showscale = False
