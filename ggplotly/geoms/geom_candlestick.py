# geoms/geom_candlestick.py

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom


class geom_candlestick(Geom):
    """Geom for drawing candlestick charts for financial OHLC data."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Create a candlestick chart for financial data.

        Visualizes price movements with open, high, low, close (OHLC) values.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x, open, high, low, close.
        increasing_color : str, default='#26A69A'
            Color for candles where close > open (green).
        decreasing_color : str, default='#EF5350'
            Color for candles where close < open (red).
        increasing_line_color : str, optional
            Wick color for increasing candles. Default same as increasing_color.
        decreasing_line_color : str, optional
            Wick color for decreasing candles. Default same as decreasing_color.
        line_width : float, default=1
            Width of wick lines.
        whisker_width : float, default=0
            Width of whisker lines (0-1). 0 = same as body.
        opacity : float, default=1
            Candlestick opacity (0-1).
        name : str, default='Candlestick'
            Name for legend.
        showlegend : bool, default=True
            Show in legend.

        Examples
        --------
        >>> # Basic candlestick
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick()

        >>> # Custom colors
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick(
        ...     increasing_color='#2196F3', decreasing_color='#FF9800')
        """
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
    """Geom for drawing OHLC (Open-High-Low-Close) bar charts."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw OHLC bar charts for financial data.

        Similar to candlestick but uses bars instead of filled bodies.
        The left tick shows the opening price, the right tick shows
        the closing price, and the vertical line shows the high-low range.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x, open, high, low, close.
        increasing_color : str, default='#26A69A'
            Color for bars where close > open (green).
        decreasing_color : str, default='#EF5350'
            Color for bars where close < open (red).
        line_width : float, default=2
            Width of the lines.
        tickwidth : float, default=0.05
            Width of open/close ticks.
        opacity : float, default=1
            Opacity of bars (0-1).
        name : str, default='OHLC'
            Name for legend.
        showlegend : bool, default=True
            Whether to show in legend.

        Examples
        --------
        >>> ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_ohlc()
        >>> geom_ohlc(increasing_color='blue', decreasing_color='orange')
        """
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
