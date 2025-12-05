# geoms/geom_candlestick.py

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom


class geom_candlestick(Geom):
    """
    Geom for drawing candlestick charts for financial data.

    Creates interactive candlestick charts using Plotly's Candlestick trace.
    Candlestick charts are used to visualize price movements over time,
    showing open, high, low, and close (OHLC) values for each time period.

    Required Aesthetics:
        x: Date/time column (typically datetime).
        open: Opening price for each period.
        high: Highest price during each period.
        low: Lowest price during each period.
        close: Closing price for each period.

    Parameters:
        increasing_color (str): Color for candles where close > open.
            Default is '#26A69A' (green).
        decreasing_color (str): Color for candles where close < open.
            Default is '#EF5350' (red).
        increasing_line_color (str): Line/wick color for increasing candles.
            Default is same as increasing_color.
        decreasing_line_color (str): Line/wick color for decreasing candles.
            Default is same as decreasing_color.
        line_width (float): Width of the wick lines. Default is 1.
        whisker_width (float): Width of whisker lines (0-1). Default is 0
            (whiskers same width as body).
        opacity (float): Opacity of candlesticks. Default is 1.
        name (str): Name for legend. Default is 'Candlestick'.
        showlegend (bool): Whether to show in legend. Default is True.

    Examples:
        >>> # Basic candlestick chart
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick()

        >>> # Custom colors (blue/orange theme)
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick(
        ...     increasing_color='#2196F3',
        ...     decreasing_color='#FF9800'
        ... )

        >>> # With title and labels
        >>> (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
        ...  + geom_candlestick()
        ...  + labs(title='Stock Price', x='Date', y='Price ($)'))
    """

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        # Set default colors (standard financial chart colors)
        if 'increasing_color' not in self.params:
            self.params['increasing_color'] = '#26A69A'  # Green
        if 'decreasing_color' not in self.params:
            self.params['decreasing_color'] = '#EF5350'  # Red

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw candlestick chart on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Validate required aesthetics
        required = ['x', 'open', 'high', 'low', 'close']
        missing = [aes for aes in required if aes not in self.mapping]
        if missing:
            raise ValueError(
                f"geom_candlestick requires aesthetics: {', '.join(required)}. "
                f"Missing: {', '.join(missing)}"
            )

        # Get column names from mapping
        x_col = self.mapping['x']
        open_col = self.mapping['open']
        high_col = self.mapping['high']
        low_col = self.mapping['low']
        close_col = self.mapping['close']

        # Get parameters
        increasing_color = self.params.get('increasing_color', '#26A69A')
        decreasing_color = self.params.get('decreasing_color', '#EF5350')
        increasing_line_color = self.params.get('increasing_line_color', increasing_color)
        decreasing_line_color = self.params.get('decreasing_line_color', decreasing_color)
        line_width = self.params.get('line_width', 1)
        whisker_width = self.params.get('whisker_width', 0)
        opacity = self.params.get('opacity', 1.0)
        name = self.params.get('name', 'Candlestick')
        showlegend = self.params.get('showlegend', True)

        # Sort data by x (date) to ensure proper ordering
        plot_data = data.sort_values(x_col).copy()

        # Create candlestick trace
        trace = go.Candlestick(
            x=plot_data[x_col],
            open=plot_data[open_col],
            high=plot_data[high_col],
            low=plot_data[low_col],
            close=plot_data[close_col],
            increasing=dict(
                line=dict(color=increasing_line_color, width=line_width),
                fillcolor=increasing_color,
            ),
            decreasing=dict(
                line=dict(color=decreasing_line_color, width=line_width),
                fillcolor=decreasing_color,
            ),
            whiskerwidth=whisker_width,
            opacity=opacity,
            name=name,
            showlegend=showlegend,
        )

        fig.add_trace(trace, row=row, col=col)

        # Disable rangeslider by default (can be enabled via theme/layout)
        fig.update_layout(xaxis_rangeslider_visible=False)


class geom_ohlc(Geom):
    """
    Geom for drawing OHLC (Open-High-Low-Close) bar charts.

    Similar to candlestick but uses bars instead of filled bodies.
    The left tick shows the opening price, the right tick shows
    the closing price, and the vertical line shows the high-low range.

    Required Aesthetics:
        x: Date/time column (typically datetime).
        open: Opening price for each period.
        high: Highest price during each period.
        low: Lowest price during each period.
        close: Closing price for each period.

    Parameters:
        increasing_color (str): Color for bars where close > open.
            Default is '#26A69A' (green).
        decreasing_color (str): Color for bars where close < open.
            Default is '#EF5350' (red).
        line_width (float): Width of the lines. Default is 2.
        tickwidth (float): Width of open/close ticks. Default is 0.05.
        opacity (float): Opacity of bars. Default is 1.
        name (str): Name for legend. Default is 'OHLC'.
        showlegend (bool): Whether to show in legend. Default is True.

    Examples:
        >>> # Basic OHLC chart
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_ohlc()

        >>> # Custom colors
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_ohlc(
        ...     increasing_color='blue',
        ...     decreasing_color='orange'
        ... )
    """

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        if 'increasing_color' not in self.params:
            self.params['increasing_color'] = '#26A69A'
        if 'decreasing_color' not in self.params:
            self.params['decreasing_color'] = '#EF5350'

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw OHLC chart on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Validate required aesthetics
        required = ['x', 'open', 'high', 'low', 'close']
        missing = [aes for aes in required if aes not in self.mapping]
        if missing:
            raise ValueError(
                f"geom_ohlc requires aesthetics: {', '.join(required)}. "
                f"Missing: {', '.join(missing)}"
            )

        # Get column names from mapping
        x_col = self.mapping['x']
        open_col = self.mapping['open']
        high_col = self.mapping['high']
        low_col = self.mapping['low']
        close_col = self.mapping['close']

        # Get parameters
        increasing_color = self.params.get('increasing_color', '#26A69A')
        decreasing_color = self.params.get('decreasing_color', '#EF5350')
        line_width = self.params.get('line_width', 2)
        tickwidth = self.params.get('tickwidth', 0.05)
        opacity = self.params.get('opacity', 1.0)
        name = self.params.get('name', 'OHLC')
        showlegend = self.params.get('showlegend', True)

        # Sort data by x (date)
        plot_data = data.sort_values(x_col).copy()

        # Create OHLC trace
        trace = go.Ohlc(
            x=plot_data[x_col],
            open=plot_data[open_col],
            high=plot_data[high_col],
            low=plot_data[low_col],
            close=plot_data[close_col],
            increasing=dict(line=dict(color=increasing_color, width=line_width)),
            decreasing=dict(line=dict(color=decreasing_color, width=line_width)),
            tickwidth=tickwidth,
            opacity=opacity,
            name=name,
            showlegend=showlegend,
        )

        fig.add_trace(trace, row=row, col=col)

        # Disable rangeslider by default
        fig.update_layout(xaxis_rangeslider_visible=False)
