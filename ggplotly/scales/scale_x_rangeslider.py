# scales/scale_x_rangeslider.py

from .scale_base import Scale


class scale_x_rangeslider(Scale):
    """Add an interactive range slider to the x-axis."""

    def __init__(self, visible=True, bgcolor='white', bordercolor='#444',
                 borderwidth=0, thickness=0.15, range=None, yaxis_rangemode='match'):
        """
        Add an interactive range slider for zooming on the x-axis.

        The range slider appears below the main plot and allows users to
        select a subset of the data to display. Particularly useful for
        time series data.

        Parameters
        ----------
        visible : bool, default=True
            Whether the range slider is visible.
        bgcolor : str, default='white'
            Background color of the range slider.
        bordercolor : str, default='#444'
            Border color of the range slider.
        borderwidth : int, default=0
            Border width in pixels.
        thickness : float, default=0.15
            Height of the range slider as a fraction of the plot (0-1).
        range : list, optional
            Initial visible range as [min, max]. If None, shows all data.
        yaxis_rangemode : str, default='match'
            How y-axis responds to range changes. Options:

            - 'match': Y-axis range matches visible data (auto-scales)
            - 'fixed': Y-axis range stays fixed

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_line, scale_x_rangeslider, data
        >>> economics = data('economics')

        >>> # Basic range slider on unemployment time series
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + scale_x_rangeslider()

        >>> # Customize appearance
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + \\
        ...     scale_x_rangeslider(bgcolor='lightgray', thickness=0.2)

        >>> # Set initial visible range
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + \\
        ...     scale_x_rangeslider(range=['1990-01-01', '2000-01-01'])

        >>> # Fixed y-axis (won't auto-scale when zooming)
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + \\
        ...     scale_x_rangeslider(yaxis_rangemode='fixed')
        """
        self.visible = visible
        self.bgcolor = bgcolor
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.thickness = thickness
        self.range = range
        self.yaxis_rangemode = yaxis_rangemode

    def apply(self, fig):
        """
        Apply the range slider to the x-axis of the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        """
        rangeslider_config = dict(
            visible=self.visible,
            bgcolor=self.bgcolor,
            bordercolor=self.bordercolor,
            borderwidth=self.borderwidth,
            thickness=self.thickness,
        )

        xaxis_update = dict(rangeslider=rangeslider_config)

        if self.range is not None:
            xaxis_update['range'] = self.range

        fig.update_xaxes(**xaxis_update)

        # Configure y-axis behavior when range slider is used
        if self.yaxis_rangemode == 'match':
            fig.update_yaxes(fixedrange=False)
        elif self.yaxis_rangemode == 'fixed':
            fig.update_yaxes(fixedrange=True)
