# test_geom_candlestick.py
"""
Comprehensive tests for geom_candlestick and geom_ohlc.
Tests verify actual behavior, not just that functions run.
"""


import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest
from ggplotly import (
    aes,
    geom_candlestick,
    geom_ohlc,
    ggplot,
    ggsize,
    labs,
    theme_minimal,
)


def generate_ohlc_data(start_date='2024-01-01', periods=60, start_price=100, volatility=0.02, seed=42):
    """Generate realistic OHLC data with random walk."""
    np.random.seed(seed)
    dates = pd.date_range(start_date, periods=periods, freq='B')  # Business days

    returns = np.random.normal(0.0005, volatility, periods)
    close = start_price * np.cumprod(1 + returns)

    open_prices = np.roll(close, 1)
    open_prices[0] = start_price

    intraday_range = close * volatility * np.random.uniform(0.5, 2, periods)
    high = np.maximum(open_prices, close) + np.abs(np.random.randn(periods)) * intraday_range
    low = np.minimum(open_prices, close) - np.abs(np.random.randn(periods)) * intraday_range

    return pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high,
        'low': low,
        'close': close,
        'volume': np.random.randint(1000000, 10000000, periods),
    })


@pytest.fixture
def ohlc_data():
    """Generate sample OHLC data for testing."""
    return generate_ohlc_data(periods=30, seed=42)


@pytest.fixture
def small_ohlc_data():
    """Generate small OHLC dataset for simple tests."""
    return pd.DataFrame({
        'date': pd.date_range('2024-01-01', periods=5, freq='D'),
        'open': [100, 102, 101, 103, 102],
        'high': [103, 105, 104, 106, 105],
        'low': [99, 101, 100, 102, 101],
        'close': [102, 101, 103, 102, 104],
    })


class TestGeomCandlestickBasic:
    """Basic tests for geom_candlestick."""

    def test_basic_candlestick_creates_correct_trace_type(self, ohlc_data):
        """Test basic candlestick chart creates correct trace type."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'candlestick'

    def test_candlestick_data_matches_input(self, small_ohlc_data):
        """Test that candlestick trace data matches input DataFrame."""
        p = (ggplot(small_ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        trace = fig.data[0]
        assert len(trace.open) == 5
        assert len(trace.high) == 5
        assert len(trace.low) == 5
        assert len(trace.close) == 5

        # Verify actual values match input
        np.testing.assert_array_equal(trace.open, small_ohlc_data['open'].values)
        np.testing.assert_array_equal(trace.close, small_ohlc_data['close'].values)

    def test_candlestick_x_dates_preserved(self, ohlc_data):
        """Test that x-axis contains correct number of dates."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert len(fig.data[0].x) == len(ohlc_data)

    def test_missing_aesthetic_raises_error(self, ohlc_data):
        """Test that missing required aesthetic raises RequiredAestheticError."""
        from ggplotly.exceptions import RequiredAestheticError

        with pytest.raises(RequiredAestheticError, match="geom_candlestick requires aesthetics"):
            p = ggplot(ohlc_data, aes(x='date', open='open', high='high')) + geom_candlestick()
            p.draw()

    def test_missing_multiple_aesthetics_lists_all(self, ohlc_data):
        """Test error message lists all missing aesthetics."""
        from ggplotly.exceptions import RequiredAestheticError

        with pytest.raises(RequiredAestheticError, match="low.*close"):
            p = ggplot(ohlc_data, aes(x='date', open='open', high='high')) + geom_candlestick()
            p.draw()


class TestGeomCandlestickColors:
    """Tests for candlestick color customization."""

    def test_default_colors(self, ohlc_data):
        """Test default increasing/decreasing colors are applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == '#26A69A'
        assert fig.data[0].decreasing.fillcolor == '#EF5350'

    def test_custom_increasing_color(self, ohlc_data):
        """Test custom increasing color is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(increasing_color='blue'))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == 'blue'

    def test_custom_decreasing_color(self, ohlc_data):
        """Test custom decreasing color is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(decreasing_color='orange'))
        fig = p.draw()

        assert fig.data[0].decreasing.fillcolor == 'orange'

    def test_custom_line_colors(self, ohlc_data):
        """Test custom line/wick colors are applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_line_color='darkgreen',
                 decreasing_line_color='darkred'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.line.color == 'darkgreen'
        assert fig.data[0].decreasing.line.color == 'darkred'

    def test_hex_colors(self, ohlc_data):
        """Test hex color values are applied correctly."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_color='#2196F3',
                 decreasing_color='#FF9800'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == '#2196F3'
        assert fig.data[0].decreasing.fillcolor == '#FF9800'


class TestGeomCandlestickParameters:
    """Tests for candlestick parameters."""

    def test_line_width(self, ohlc_data):
        """Test custom line width is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(line_width=2))
        fig = p.draw()

        assert fig.data[0].increasing.line.width == 2
        assert fig.data[0].decreasing.line.width == 2

    def test_whisker_width(self, ohlc_data):
        """Test whisker width parameter is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(whisker_width=0.5))
        fig = p.draw()

        assert fig.data[0].whiskerwidth == 0.5

    def test_opacity(self, ohlc_data):
        """Test opacity parameter is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(opacity=0.7))
        fig = p.draw()

        assert fig.data[0].opacity == 0.7

    def test_custom_name(self, ohlc_data):
        """Test custom name for legend is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(name='AAPL'))
        fig = p.draw()

        assert fig.data[0].name == 'AAPL'

    def test_hide_legend(self, ohlc_data):
        """Test hiding from legend works."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(showlegend=False))
        fig = p.draw()

        assert fig.data[0].showlegend is False


class TestGeomCandlestickLayout:
    """Tests for layout-related behavior."""

    def test_rangeslider_disabled(self, ohlc_data):
        """Test that rangeslider is disabled by default."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert fig.layout.xaxis.rangeslider.visible is False

    def test_labs_title_applied(self, ohlc_data):
        """Test that labs title is applied correctly."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick()
             + labs(title='Stock Price', x='Date', y='Price ($)'))
        fig = p.draw()

        assert 'Stock Price' in fig.layout.title.text
        assert fig.layout.xaxis.title.text == 'Date'
        assert fig.layout.yaxis.title.text == 'Price ($)'

    def test_ggsize_applied(self, ohlc_data):
        """Test that ggsize dimensions are applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick()
             + ggsize(width=1000, height=600))
        fig = p.draw()

        assert fig.layout.width == 1000
        assert fig.layout.height == 600


class TestGeomOhlcBasic:
    """Basic tests for geom_ohlc."""

    def test_basic_ohlc_creates_correct_trace_type(self, ohlc_data):
        """Test basic OHLC chart creates correct trace type."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'ohlc'

    def test_ohlc_data_matches_input(self, small_ohlc_data):
        """Test that OHLC trace data matches input."""
        p = (ggplot(small_ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        trace = fig.data[0]
        assert len(trace.open) == 5
        assert len(trace.high) == 5
        assert len(trace.low) == 5
        assert len(trace.close) == 5

    def test_ohlc_missing_aesthetic_raises_error(self, ohlc_data):
        """Test that missing required aesthetic raises RequiredAestheticError."""
        from ggplotly.exceptions import RequiredAestheticError

        with pytest.raises(RequiredAestheticError, match="geom_ohlc requires aesthetics"):
            p = ggplot(ohlc_data, aes(x='date', open='open')) + geom_ohlc()
            p.draw()


class TestGeomOhlcColors:
    """Tests for OHLC color customization."""

    def test_ohlc_default_colors(self, ohlc_data):
        """Test default OHLC colors are applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        assert fig.data[0].increasing.line.color == '#26A69A'
        assert fig.data[0].decreasing.line.color == '#EF5350'

    def test_ohlc_custom_colors(self, ohlc_data):
        """Test custom OHLC colors are applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(increasing_color='navy', decreasing_color='maroon'))
        fig = p.draw()

        assert fig.data[0].increasing.line.color == 'navy'
        assert fig.data[0].decreasing.line.color == 'maroon'


class TestGeomOhlcParameters:
    """Tests for OHLC parameters."""

    def test_ohlc_line_width(self, ohlc_data):
        """Test OHLC line width is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(line_width=3))
        fig = p.draw()

        assert fig.data[0].increasing.line.width == 3
        assert fig.data[0].decreasing.line.width == 3

    def test_ohlc_tickwidth(self, ohlc_data):
        """Test OHLC tick width is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(tickwidth=0.1))
        fig = p.draw()

        assert fig.data[0].tickwidth == 0.1

    def test_ohlc_opacity(self, ohlc_data):
        """Test OHLC opacity is applied."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(opacity=0.8))
        fig = p.draw()

        assert fig.data[0].opacity == 0.8

    def test_ohlc_rangeslider_disabled(self, ohlc_data):
        """Test OHLC rangeslider is disabled."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        assert fig.layout.xaxis.rangeslider.visible is False


class TestDataSorting:
    """Tests for data sorting behavior."""

    def test_candlestick_sorts_by_date(self):
        """Test that candlestick sorts data by date."""
        df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-05', '2024-01-01', '2024-01-03', '2024-01-02', '2024-01-04']),
            'open': [105, 100, 103, 102, 104],
            'high': [106, 101, 104, 103, 105],
            'low': [104, 99, 102, 101, 103],
            'close': [105, 101, 103, 102, 104],
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        # First date should be Jan 1, last should be Jan 5
        dates = pd.to_datetime(fig.data[0].x)
        assert dates[0].day == 1
        assert dates[-1].day == 5

    def test_ohlc_sorts_by_date(self):
        """Test that OHLC sorts data by date."""
        df = pd.DataFrame({
            'date': pd.to_datetime(['2024-01-03', '2024-01-01', '2024-01-02']),
            'open': [103, 100, 102],
            'high': [104, 101, 103],
            'low': [102, 99, 101],
            'close': [103, 101, 102],
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        dates = pd.to_datetime(fig.data[0].x)
        assert dates[0].day == 1
        assert dates[-1].day == 3


class TestDataIntegrity:
    """Tests for data integrity."""

    def test_original_dataframe_unchanged(self, ohlc_data):
        """Test that original dataframe is not modified."""
        original_shape = ohlc_data.shape
        original_dates = ohlc_data['date'].copy()

        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        p.draw()

        assert ohlc_data.shape == original_shape
        pd.testing.assert_series_equal(ohlc_data['date'], original_dates)

    def test_high_low_relationship_preserved(self, ohlc_data):
        """Test that high >= low for all candles."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        trace = fig.data[0]
        assert all(np.array(trace.high) >= np.array(trace.low))

    def test_high_low_encompasses_open_close(self, ohlc_data):
        """Test that high >= max(open, close) and low <= min(open, close)."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        trace = fig.data[0]
        open_arr = np.array(trace.open)
        high_arr = np.array(trace.high)
        low_arr = np.array(trace.low)
        close_arr = np.array(trace.close)

        assert all(high_arr >= np.maximum(open_arr, close_arr))
        assert all(low_arr <= np.minimum(open_arr, close_arr))


class TestEdgeCases:
    """Edge cases and special scenarios."""

    def test_single_candle(self):
        """Test with single data point."""
        df = pd.DataFrame({
            'date': [pd.Timestamp('2024-01-01')],
            'open': [100],
            'high': [105],
            'low': [98],
            'close': [103],
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data[0].open) == 1
        assert fig.data[0].open[0] == 100
        assert fig.data[0].close[0] == 103

    def test_doji_candle(self):
        """Test with doji candle (open == close)."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=3, freq='D'),
            'open': [100, 102, 101],
            'high': [103, 105, 104],
            'low': [99, 101, 100],
            'close': [100, 102, 101],  # Same as open = doji
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        # Verify doji candles have open == close
        trace = fig.data[0]
        for i in range(3):
            assert trace.open[i] == trace.close[i]

    def test_large_dataset(self):
        """Test with larger dataset."""
        df = generate_ohlc_data(periods=500, seed=42)

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data[0].x) == 500

    def test_gaps_in_dates(self):
        """Test with non-consecutive dates (weekend gaps)."""
        dates = pd.to_datetime(['2024-01-01', '2024-01-02', '2024-01-05', '2024-01-08', '2024-01-09'])
        df = pd.DataFrame({
            'date': dates,
            'open': [100, 102, 104, 103, 105],
            'high': [103, 105, 107, 106, 108],
            'low': [99, 101, 103, 102, 104],
            'close': [102, 104, 103, 105, 107],
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert len(fig.data[0].x) == 5


class TestMarketConditions:
    """Test market condition simulations verify correct behavior."""

    def test_bear_market_final_lower_than_initial(self):
        """Test bear market: final close should be lower than initial open."""
        np.random.seed(42)
        n = 90
        close = 500 * np.exp(np.linspace(0, -0.3, n))
        close = close * (1 + np.random.normal(0, 0.005, n))
        open_prices = np.roll(close, 1)
        open_prices[0] = 500
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 3
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 3

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        # Verify bear market: final close should be lower than initial open
        assert fig.data[0].close[-1] < fig.data[0].open[0]

    def test_bull_market_final_higher_than_initial(self):
        """Test bull market: final close should be higher than initial open."""
        np.random.seed(888)
        n = 90
        trend = np.linspace(0, 0.4, n)
        returns = trend / n + np.random.normal(0, 0.02, n)
        close = 100 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 100
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 2
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 2

        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        # Verify bull market: final close should be higher than initial
        assert fig.data[0].close[-1] > fig.data[0].open[0]


class TestCandlestickVsOhlc:
    """Test comparison between candlestick and OHLC."""

    def test_same_data_different_trace_types(self):
        """Test same data produces correct trace types for each geom."""
        df = generate_ohlc_data(periods=10, seed=106)

        fig_candle = (
            ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        fig_ohlc = (
            ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc()
        ).draw()

        assert fig_candle.data[0].type == 'candlestick'
        assert fig_ohlc.data[0].type == 'ohlc'
        # Both should have same number of data points
        assert len(fig_candle.data[0].x) == len(fig_ohlc.data[0].x) == 10


class TestFullFeatured:
    """Test full-featured example with all customizations."""

    def test_all_customizations_applied(self):
        """Test that all customizations are correctly applied."""
        df = generate_ohlc_data(periods=90, start_price=150, volatility=0.02, seed=107)

        fig = (
            ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#089981',
                decreasing_color='#F23645',
                increasing_line_color='#089981',
                decreasing_line_color='#F23645',
                line_width=1,
                name='MSFT'
            )
            + labs(
                title='Microsoft Corporation (MSFT)',
                x='Date',
                y='Price ($)'
            )
            + theme_minimal()
            + ggsize(width=1100, height=550)
        ).draw()

        # Verify all customizations were applied
        assert fig.data[0].type == 'candlestick'
        assert fig.data[0].name == 'MSFT'
        assert fig.data[0].increasing.fillcolor == '#089981'
        assert fig.data[0].decreasing.fillcolor == '#F23645'
        assert fig.data[0].increasing.line.color == '#089981'
        assert fig.data[0].decreasing.line.color == '#F23645'
        assert fig.data[0].increasing.line.width == 1
        assert fig.layout.title.text == 'Microsoft Corporation (MSFT)'
        assert fig.layout.xaxis.title.text == 'Date'
        assert fig.layout.yaxis.title.text == 'Price ($)'
        assert fig.layout.width == 1100
        assert fig.layout.height == 550
