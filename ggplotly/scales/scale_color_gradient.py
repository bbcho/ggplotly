"""Continuous color gradient scale for the color aesthetic."""

from .scale_base import Scale


class scale_color_gradient(Scale):
    """
    Create a two-color continuous gradient for the color aesthetic.

    Aesthetic: color

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

    aesthetic = 'color'

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
        Apply the color gradient to markers and line segments in the figure.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        new_colorscale = [[0, self.low], [1, self.high]]

        for trace in fig.data:
            # Handle marker-based traces (scatter points, etc.)
            if hasattr(trace, 'marker') and trace.marker is not None:
                trace.marker.colorscale = new_colorscale

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

            # Handle line gradient segments (created by ContinuousColorTraceBuilder)
            if hasattr(trace, 'meta') and trace.meta:
                meta = trace.meta
                if isinstance(meta, dict) and meta.get('_ggplotly_line_gradient'):
                    t_norm = meta.get('_color_norm', 0)
                    new_color = self._interpolate_color(new_colorscale, t_norm)
                    trace.line.color = new_color

    @staticmethod
    def _interpolate_color(colorscale, t):
        """
        Interpolate between colorscale endpoints.

        Parameters:
            colorscale: List of [position, color] pairs
            t: Normalized value between 0 and 1

        Returns:
            str: Interpolated RGB color string
        """
        t = max(0, min(1, t))  # Clamp to [0, 1]

        low_color = colorscale[0][1]
        high_color = colorscale[1][1]

        # Parse color to RGB (handles hex and named colors)
        def color_to_rgb(color):
            if color.startswith('#'):
                color = color.lstrip('#')
                return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))
            elif color.startswith('rgb'):
                # Parse rgb(r, g, b) format
                import re
                match = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', color)
                if match:
                    return tuple(int(x) for x in match.groups())
            # Fallback for named colors - approximate mapping
            named_colors = {
                'blue': (0, 0, 255), 'red': (255, 0, 0), 'green': (0, 128, 0),
                'white': (255, 255, 255), 'black': (0, 0, 0),
                'yellow': (255, 255, 0), 'orange': (255, 165, 0),
                'purple': (128, 0, 128), 'cyan': (0, 255, 255),
            }
            return named_colors.get(color.lower(), (128, 128, 128))

        low_rgb = color_to_rgb(low_color)
        high_rgb = color_to_rgb(high_color)

        # Linear interpolation
        r = int(low_rgb[0] + t * (high_rgb[0] - low_rgb[0]))
        g = int(low_rgb[1] + t * (high_rgb[1] - low_rgb[1]))
        b = int(low_rgb[2] + t * (high_rgb[2] - low_rgb[2]))

        return f'rgb({r}, {g}, {b})'
