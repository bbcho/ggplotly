# scales/scale_x_rangeselector.py

from .scale_base import Scale


class scale_x_rangeselector(Scale):
    """Add range selector buttons to the x-axis."""

    def __init__(self, buttons=None, visible=True, bgcolor='white',
                 bordercolor='#444', borderwidth=0, font=None,
                 x=None, y=None, xanchor='left', yanchor='bottom'):
        """
        Add range selector buttons for quick time range selection.

        Range selector buttons appear above the plot and allow users to
        quickly select predefined time ranges. Particularly useful for
        time series data with date/datetime x-axis.

        Parameters
        ----------
        buttons : list of dict, optional
            List of button configurations. Each button is a dict with:

            - count (int): Number of steps
            - label (str): Button label text
            - step (str): Step unit ('month', 'year', 'day', 'hour', 'minute', 'second', 'all')
            - stepmode (str): 'backward' (from end) or 'todate' (from start of period)

            Default buttons: 1m, 6m, YTD, 1y, All
        visible : bool, default=True
            Whether the range selector is visible.
        bgcolor : str, default='white'
            Background color of the selector.
        bordercolor : str, default='#444'
            Border color.
        borderwidth : int, default=0
            Border width in pixels.
        font : dict, optional
            Font settings for button labels (size, color, family).
        x : float, optional
            X position of the selector (0-1, fraction of plot width).
        y : float, optional
            Y position of the selector (0-1, fraction of plot height).
        xanchor : str, default='left'
            Horizontal anchor ('left', 'center', 'right').
        yanchor : str, default='bottom'
            Vertical anchor ('top', 'middle', 'bottom').

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_line, scale_x_rangeselector, scale_x_rangeslider, data
        >>> economics = data('economics')

        >>> # Basic range selector with default buttons (1m, 6m, YTD, 1y, All)
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + scale_x_rangeselector()

        >>> # Custom buttons for weekly and monthly views
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + \\
        ...     scale_x_rangeselector(buttons=[
        ...         dict(count=7, label='1w', step='day', stepmode='backward'),
        ...         dict(count=1, label='1m', step='month', stepmode='backward'),
        ...         dict(step='all')
        ...     ])

        >>> # Combine with range slider for full interactive control
        >>> ggplot(economics, aes(x='date', y='unemploy')) + geom_line() + \\
        ...     scale_x_rangeselector() + scale_x_rangeslider()
        """
        # Default buttons if none provided
        if buttons is None:
            buttons = [
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all"),
            ]

        self.buttons = buttons
        self.visible = visible
        self.bgcolor = bgcolor
        self.bordercolor = bordercolor
        self.borderwidth = borderwidth
        self.font = font
        self.x = x
        self.y = y
        self.xanchor = xanchor
        self.yanchor = yanchor

    def apply(self, fig):
        """
        Apply the range selector to the x-axis of the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        """
        rangeselector_config = dict(
            buttons=self.buttons,
            visible=self.visible,
            bgcolor=self.bgcolor,
            bordercolor=self.bordercolor,
            borderwidth=self.borderwidth,
            xanchor=self.xanchor,
            yanchor=self.yanchor,
        )

        if self.font is not None:
            rangeselector_config['font'] = self.font

        if self.x is not None:
            rangeselector_config['x'] = self.x

        if self.y is not None:
            rangeselector_config['y'] = self.y

        fig.update_xaxes(rangeselector=rangeselector_config)
