# test_geom_candlestick.py
# Comprehensive tests for geom_candlestick and geom_ohlc

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plotly.graph_objects import Figure

from ggplotly import (
    ggplot, aes, geom_candlestick, geom_ohlc,
    labs, theme_minimal, theme_dark,
    ggsize,
)


@pytest.fixture
def ohlc_data():
    """Generate sample OHLC data for testing."""
    np.random.seed(42)
    n = 30
    dates = pd.date_range('2024-01-01', periods=n, freq='D')

    # Generate random walk for close prices
    close = 100 + np.cumsum(np.random.randn(n) * 2)

    # Generate open, high, low based on close
    open_prices = close + np.random.randn(n) * 1
    high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 1.5
    low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 1.5

    return pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high,
        'low': low,
        'close': close,
        'volume': np.random.randint(1000000, 5000000, n),
    })


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

    def test_basic_candlestick(self, ohlc_data):
        """Test basic candlestick chart creation."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'candlestick'

    def test_candlestick_has_correct_data(self, small_ohlc_data):
        """Test that candlestick contains correct OHLC values."""
        p = (ggplot(small_ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        trace = fig.data[0]
        assert len(trace.open) == 5
        assert len(trace.high) == 5
        assert len(trace.low) == 5
        assert len(trace.close) == 5

    def test_candlestick_x_is_dates(self, ohlc_data):
        """Test that x-axis contains dates."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert len(fig.data[0].x) == len(ohlc_data)

    def test_missing_aesthetic_raises_error(self, ohlc_data):
        """Test that missing required aesthetic raises ValueError."""
        with pytest.raises(ValueError, match="geom_candlestick requires aesthetics"):
            p = ggplot(ohlc_data, aes(x='date', open='open', high='high')) + geom_candlestick()
            p.draw()

    def test_missing_multiple_aesthetics(self, ohlc_data):
        """Test error message lists all missing aesthetics."""
        with pytest.raises(ValueError, match="Missing:.*low.*close"):
            p = ggplot(ohlc_data, aes(x='date', open='open', high='high')) + geom_candlestick()
            p.draw()


class TestGeomCandlestickColors:
    """Tests for candlestick color customization."""

    def test_default_colors(self, ohlc_data):
        """Test default increasing/decreasing colors."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == '#26A69A'
        assert fig.data[0].decreasing.fillcolor == '#EF5350'

    def test_custom_increasing_color(self, ohlc_data):
        """Test custom increasing color."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(increasing_color='blue'))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == 'blue'

    def test_custom_decreasing_color(self, ohlc_data):
        """Test custom decreasing color."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(decreasing_color='orange'))
        fig = p.draw()

        assert fig.data[0].decreasing.fillcolor == 'orange'

    def test_custom_line_colors(self, ohlc_data):
        """Test custom line/wick colors."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_line_color='darkgreen',
                 decreasing_line_color='darkred'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.line.color == 'darkgreen'
        assert fig.data[0].decreasing.line.color == 'darkred'


class TestGeomCandlestickParameters:
    """Tests for candlestick parameters."""

    def test_line_width(self, ohlc_data):
        """Test custom line width."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(line_width=2))
        fig = p.draw()

        assert fig.data[0].increasing.line.width == 2
        assert fig.data[0].decreasing.line.width == 2

    def test_whisker_width(self, ohlc_data):
        """Test whisker width parameter."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(whisker_width=0.5))
        fig = p.draw()

        assert fig.data[0].whiskerwidth == 0.5

    def test_opacity(self, ohlc_data):
        """Test opacity parameter."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(opacity=0.7))
        fig = p.draw()

        assert fig.data[0].opacity == 0.7

    def test_custom_name(self, ohlc_data):
        """Test custom name for legend."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(name='AAPL'))
        fig = p.draw()

        assert fig.data[0].name == 'AAPL'

    def test_hide_legend(self, ohlc_data):
        """Test hiding from legend."""
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

    def test_with_labs(self, ohlc_data):
        """Test candlestick with custom labels."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick()
             + labs(title='Stock Price', x='Date', y='Price ($)'))
        fig = p.draw()

        assert 'Stock Price' in fig.layout.title.text

    def test_with_theme(self, ohlc_data):
        """Test candlestick with theme."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick()
             + theme_dark())
        fig = p.draw()

        assert isinstance(fig, Figure)

    def test_with_ggsize(self, ohlc_data):
        """Test candlestick with custom size."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick()
             + ggsize(width=1000, height=600))
        fig = p.draw()

        assert fig.layout.width == 1000
        assert fig.layout.height == 600


class TestGeomOhlcBasic:
    """Basic tests for geom_ohlc."""

    def test_basic_ohlc(self, ohlc_data):
        """Test basic OHLC chart creation."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'ohlc'

    def test_ohlc_has_correct_data(self, small_ohlc_data):
        """Test that OHLC contains correct values."""
        p = (ggplot(small_ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        trace = fig.data[0]
        assert len(trace.open) == 5
        assert len(trace.high) == 5
        assert len(trace.low) == 5
        assert len(trace.close) == 5

    def test_ohlc_missing_aesthetic_raises_error(self, ohlc_data):
        """Test that missing required aesthetic raises ValueError."""
        with pytest.raises(ValueError, match="geom_ohlc requires aesthetics"):
            p = ggplot(ohlc_data, aes(x='date', open='open')) + geom_ohlc()
            p.draw()


class TestGeomOhlcColors:
    """Tests for OHLC color customization."""

    def test_ohlc_default_colors(self, ohlc_data):
        """Test default OHLC colors."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc())
        fig = p.draw()

        assert fig.data[0].increasing.line.color == '#26A69A'
        assert fig.data[0].decreasing.line.color == '#EF5350'

    def test_ohlc_custom_colors(self, ohlc_data):
        """Test custom OHLC colors."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(increasing_color='navy', decreasing_color='maroon'))
        fig = p.draw()

        assert fig.data[0].increasing.line.color == 'navy'
        assert fig.data[0].decreasing.line.color == 'maroon'


class TestGeomOhlcParameters:
    """Tests for OHLC parameters."""

    def test_ohlc_line_width(self, ohlc_data):
        """Test OHLC line width."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(line_width=3))
        fig = p.draw()

        assert fig.data[0].increasing.line.width == 3
        assert fig.data[0].decreasing.line.width == 3

    def test_ohlc_tickwidth(self, ohlc_data):
        """Test OHLC tick width."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(tickwidth=0.1))
        fig = p.draw()

        assert fig.data[0].tickwidth == 0.1

    def test_ohlc_opacity(self, ohlc_data):
        """Test OHLC opacity."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(opacity=0.8))
        fig = p.draw()

        assert fig.data[0].opacity == 0.8

    def test_ohlc_custom_name(self, ohlc_data):
        """Test OHLC custom name."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_ohlc(name='MSFT'))
        fig = p.draw()

        assert fig.data[0].name == 'MSFT'


class TestDataSorting:
    """Tests for data sorting behavior."""

    def test_candlestick_sorts_by_date(self):
        """Test that candlestick sorts data by date."""
        # Create unsorted data
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

        # First date should be Jan 1
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

    def test_original_data_unchanged(self, ohlc_data):
        """Test that original dataframe is not modified."""
        original_shape = ohlc_data.shape
        original_dates = ohlc_data['date'].copy()

        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        p.draw()

        assert ohlc_data.shape == original_shape
        pd.testing.assert_series_equal(ohlc_data['date'], original_dates)

    def test_ohlc_values_preserved(self, small_ohlc_data):
        """Test that OHLC values are preserved."""
        p = (ggplot(small_ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        trace = fig.data[0]
        np.testing.assert_array_equal(trace.open, small_ohlc_data['open'].values)
        np.testing.assert_array_equal(trace.close, small_ohlc_data['close'].values)


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

        assert isinstance(fig, Figure)

    def test_large_dataset(self):
        """Test with larger dataset."""
        np.random.seed(42)
        n = 500
        df = pd.DataFrame({
            'date': pd.date_range('2022-01-01', periods=n, freq='D'),
            'open': 100 + np.cumsum(np.random.randn(n) * 0.5),
            'high': 100 + np.cumsum(np.random.randn(n) * 0.5) + 2,
            'low': 100 + np.cumsum(np.random.randn(n) * 0.5) - 2,
            'close': 100 + np.cumsum(np.random.randn(n) * 0.5) + 0.5,
        })

        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick())
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data[0].x) == n

    def test_with_gaps_in_dates(self):
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

        assert isinstance(fig, Figure)
        assert len(fig.data[0].x) == 5


class TestColorSchemes:
    """Test various color scheme combinations."""

    def test_blue_orange_scheme(self, ohlc_data):
        """Test blue/orange color scheme."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_color='#2196F3',
                 decreasing_color='#FF9800'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == '#2196F3'
        assert fig.data[0].decreasing.fillcolor == '#FF9800'

    def test_grayscale_scheme(self, ohlc_data):
        """Test grayscale color scheme."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_color='#666666',
                 decreasing_color='#CCCCCC'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == '#666666'
        assert fig.data[0].decreasing.fillcolor == '#CCCCCC'

    def test_traditional_scheme(self, ohlc_data):
        """Test traditional green/red scheme with explicit colors."""
        p = (ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(
                 increasing_color='green',
                 decreasing_color='red',
                 increasing_line_color='darkgreen',
                 decreasing_line_color='darkred'
             ))
        fig = p.draw()

        assert fig.data[0].increasing.fillcolor == 'green'
        assert fig.data[0].decreasing.fillcolor == 'red'
        assert fig.data[0].increasing.line.color == 'darkgreen'
        assert fig.data[0].decreasing.line.color == 'darkred'
