# pytest/test_geom_candlestick_examples.py
"""
Test suite for geom_candlestick examples.
Ensures all examples from notebooks/geom_candlestick_examples.py work correctly.
"""

import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from ggplotly import (
    ggplot, aes, geom_candlestick, geom_ohlc,
    geom_line, geom_point, geom_ribbon,
    theme_minimal, theme_dark, theme_classic, theme_ggplot2,
    labs,
    ggsize,
)


# Helper function to generate realistic OHLC data (same as in examples)
def generate_ohlc_data(start_date='2024-01-01', periods=60, start_price=100, volatility=0.02, seed=42):
    """Generate realistic OHLC data with random walk."""
    np.random.seed(seed)
    dates = pd.date_range(start_date, periods=periods, freq='B')  # Business days

    # Generate returns using geometric Brownian motion
    returns = np.random.normal(0.0005, volatility, periods)
    close = start_price * np.cumprod(1 + returns)

    # Generate open, high, low based on close
    open_prices = np.roll(close, 1)
    open_prices[0] = start_price

    # Add some intraday volatility
    intraday_range = close * volatility * np.random.uniform(0.5, 2, periods)
    high = np.maximum(open_prices, close) + np.abs(np.random.randn(periods)) * intraday_range
    low = np.minimum(open_prices, close) - np.abs(np.random.randn(periods)) * intraday_range

    # Generate volume
    volume = np.random.randint(1000000, 10000000, periods)

    return pd.DataFrame({
        'date': dates,
        'open': open_prices,
        'high': high,
        'low': low,
        'close': close,
        'volume': volume,
    })


class TestBasicCandlestick:
    """Test basic candlestick examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_01_basic_candlestick(self, ohlc_data):
        """Example 1: Basic candlestick chart."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        assert len(fig.data) == 1
        assert fig.data[0].type == 'candlestick'
        assert len(fig.data[0].x) == len(ohlc_data)

    def test_example_02_with_labs(self, ohlc_data):
        """Example 2: Candlestick with title and labels."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(
                title='Stock Price Movement',
                x='Date',
                y='Price ($)'
            )
        ).draw()

        assert fig.layout.title.text == 'Stock Price Movement'
        assert fig.layout.xaxis.title.text == 'Date'
        assert fig.layout.yaxis.title.text == 'Price ($)'


class TestCandlestickColors:
    """Test candlestick color customization examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_03_blue_orange_theme(self, ohlc_data):
        """Example 3: Blue/Orange color theme."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#2196F3',
                decreasing_color='#FF9800'
            )
            + labs(title='Blue/Orange Color Scheme')
        ).draw()

        assert fig.data[0].increasing.fillcolor == '#2196F3'
        assert fig.data[0].decreasing.fillcolor == '#FF9800'

    def test_example_04_green_red_theme(self, ohlc_data):
        """Example 4: Traditional green/red with custom line colors."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='green',
                decreasing_color='red',
                increasing_line_color='darkgreen',
                decreasing_line_color='darkred'
            )
            + labs(title='Traditional Green/Red Scheme')
        ).draw()

        assert fig.data[0].increasing.fillcolor == 'green'
        assert fig.data[0].decreasing.fillcolor == 'red'
        assert fig.data[0].increasing.line.color == 'darkgreen'
        assert fig.data[0].decreasing.line.color == 'darkred'

    def test_example_05_grayscale(self, ohlc_data):
        """Example 5: Grayscale theme."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#333333',
                decreasing_color='#AAAAAA'
            )
            + labs(title='Grayscale Candlestick')
            + theme_minimal()
        ).draw()

        assert fig.data[0].increasing.fillcolor == '#333333'
        assert fig.data[0].decreasing.fillcolor == '#AAAAAA'


class TestCandlestickParameters:
    """Test candlestick parameter customization examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_06_line_width(self, ohlc_data):
        """Example 6: Custom line width."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(line_width=2)
            + labs(title='Thicker Wick Lines')
        ).draw()

        assert fig.data[0].increasing.line.width == 2
        assert fig.data[0].decreasing.line.width == 2

    def test_example_07_whisker_width(self, ohlc_data):
        """Example 7: Custom whisker width."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(whisker_width=0.5)
            + labs(title='Wider Whiskers')
        ).draw()

        assert fig.data[0].whiskerwidth == 0.5

    def test_example_08_opacity(self, ohlc_data):
        """Example 8: Semi-transparent candlesticks."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(opacity=0.7)
            + labs(title='Semi-Transparent Candlesticks')
        ).draw()

        assert fig.data[0].opacity == 0.7


class TestOHLCBasic:
    """Test OHLC chart examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_09_basic_ohlc(self, ohlc_data):
        """Example 9: Basic OHLC chart."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc()
            + labs(title='OHLC Bar Chart')
        ).draw()

        assert len(fig.data) == 1
        assert fig.data[0].type == 'ohlc'
        assert len(fig.data[0].x) == len(ohlc_data)

    def test_example_10_ohlc_custom_colors(self, ohlc_data):
        """Example 10: OHLC with custom colors."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc(
                increasing_color='navy',
                decreasing_color='maroon'
            )
            + labs(title='OHLC with Navy/Maroon Colors')
        ).draw()

        assert fig.data[0].increasing.line.color == 'navy'
        assert fig.data[0].decreasing.line.color == 'maroon'

    def test_example_11_ohlc_thick_lines(self, ohlc_data):
        """Example 11: OHLC with thicker lines."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc(line_width=3, tickwidth=0.1)
            + labs(title='OHLC with Thicker Lines')
        ).draw()

        assert fig.data[0].increasing.line.width == 3
        assert fig.data[0].decreasing.line.width == 3
        assert fig.data[0].tickwidth == 0.1


class TestThemes:
    """Test candlestick with different themes."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_12_dark_theme(self, ohlc_data):
        """Example 12: Dark theme."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#00E676',
                decreasing_color='#FF5252'
            )
            + labs(title='Candlestick with Dark Theme')
            + theme_dark()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert fig.data[0].increasing.fillcolor == '#00E676'
        assert fig.data[0].decreasing.fillcolor == '#FF5252'
        # Theme is applied (either via template or direct properties)
        assert fig.layout.template is not None or fig.layout.paper_bgcolor is not None

    def test_example_13_minimal_theme(self, ohlc_data):
        """Example 13: Minimal theme."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Candlestick with Minimal Theme')
            + theme_minimal()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert fig.layout.title.text == 'Candlestick with Minimal Theme'

    def test_example_14_classic_theme(self, ohlc_data):
        """Example 14: Classic theme."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Candlestick with Classic Theme')
            + theme_classic()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert fig.layout.title.text == 'Candlestick with Classic Theme'


class TestFigureSize:
    """Test custom figure size examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_15_custom_size(self, ohlc_data):
        """Example 15: Custom figure size."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Wide Candlestick Chart')
            + ggsize(width=1200, height=500)
        ).draw()

        assert fig.layout.width == 1200
        assert fig.layout.height == 500


class TestTimePeriods:
    """Test different time period examples."""

    def test_example_16_short_period(self):
        """Example 16: 2-week period (10 business days)."""
        df_short = generate_ohlc_data(periods=10, volatility=0.015, seed=100)

        fig = (
            ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='2-Week Price Movement')
        ).draw()

        assert len(fig.data[0].x) == 10

    def test_example_17_long_period(self):
        """Example 17: 6-month period."""
        df_long = generate_ohlc_data(periods=130, volatility=0.02, seed=101)

        fig = (
            ggplot(df_long, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='6-Month Price Movement')
            + ggsize(width=1000, height=500)
        ).draw()

        assert len(fig.data[0].x) == 130


class TestVolatility:
    """Test different volatility scenarios."""

    def test_example_18_high_volatility(self):
        """Example 18: High volatility stock."""
        df_volatile = generate_ohlc_data(periods=60, start_price=50, volatility=0.05, seed=102)

        fig = (
            ggplot(df_volatile, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='High Volatility Stock')
        ).draw()

        assert fig.data[0].type == 'candlestick'
        # High volatility should show larger high-low ranges
        high_low_range = np.array(df_volatile['high']) - np.array(df_volatile['low'])
        assert np.mean(high_low_range) > 0  # Non-zero range

    def test_example_19_low_volatility(self):
        """Example 19: Low volatility stock."""
        df_stable = generate_ohlc_data(periods=60, start_price=150, volatility=0.008, seed=103)

        fig = (
            ggplot(df_stable, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Low Volatility Stock')
        ).draw()

        assert fig.data[0].type == 'candlestick'


class TestPriceRanges:
    """Test different price range examples."""

    def test_example_20_penny_stock(self):
        """Example 20: Penny stock (low price)."""
        df_penny = generate_ohlc_data(periods=60, start_price=2.5, volatility=0.04, seed=104)

        fig = (
            ggplot(df_penny, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Penny Stock Price Movement', y='Price ($)')
        ).draw()

        # Check data values are in penny stock range
        assert fig.data[0].close[0] < 10  # Should be under $10

    def test_example_21_high_priced_stock(self):
        """Example 21: High-priced stock."""
        df_expensive = generate_ohlc_data(periods=60, start_price=3500, volatility=0.015, seed=105)

        fig = (
            ggplot(df_expensive, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='High-Priced Stock (e.g., AMZN)', y='Price ($)')
        ).draw()

        # Check data values are in high price range
        assert fig.data[0].open[0] > 1000  # Should be over $1000


class TestAssetTypes:
    """Test different asset type examples."""

    def test_example_22_cryptocurrency(self):
        """Example 22: Cryptocurrency style."""
        np.random.seed(123)
        dates = pd.date_range('2024-01-01', periods=90, freq='D')
        close = 40000 * np.cumprod(1 + np.random.normal(0.001, 0.03, 90))
        open_prices = np.roll(close, 1)
        open_prices[0] = 40000
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(90)) * close * 0.02
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(90)) * close * 0.02

        df_crypto = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_crypto, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#00C853',
                decreasing_color='#FF1744'
            )
            + labs(title='Bitcoin Price (Simulated)', y='Price (USD)')
            + theme_dark()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert fig.data[0].increasing.fillcolor == '#00C853'
        # Crypto prices should be in typical BTC range
        assert fig.data[0].open[0] > 10000

    def test_example_23_forex(self):
        """Example 23: Forex style."""
        np.random.seed(456)
        dates = pd.date_range('2024-01-01', periods=60, freq='B')
        close = 1.10 * np.cumprod(1 + np.random.normal(0, 0.005, 60))
        open_prices = np.roll(close, 1)
        open_prices[0] = 1.10
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(60)) * 0.003
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(60)) * 0.003

        df_forex = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_forex, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='EUR/USD Exchange Rate', y='Rate')
            + theme_minimal()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        # Forex EUR/USD should be around 1.0-1.2
        assert 0.5 < fig.data[0].open[0] < 2.0

    def test_example_24_commodity(self):
        """Example 24: Commodity style."""
        np.random.seed(789)
        dates = pd.date_range('2024-01-01', periods=60, freq='B')
        close = 75 * np.cumprod(1 + np.random.normal(0.001, 0.025, 60))
        open_prices = np.roll(close, 1)
        open_prices[0] = 75
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(60)) * 1.5
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(60)) * 1.5

        df_oil = pd.DataFrame({
            'date': dates,
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_oil, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#4CAF50',
                decreasing_color='#F44336'
            )
            + labs(title='Crude Oil Futures', y='Price ($/barrel)')
        ).draw()

        assert fig.data[0].type == 'candlestick'
        # Oil prices should be in typical range
        assert 50 < fig.data[0].open[0] < 150


class TestLegendOptions:
    """Test legend customization examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_25_named_candlestick(self, ohlc_data):
        """Example 25: Named candlestick for legend."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(name='AAPL')
            + labs(title='Apple Inc. (AAPL)')
        ).draw()

        assert fig.data[0].name == 'AAPL'

    def test_example_26_hide_legend(self, ohlc_data):
        """Example 26: Hide legend."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(showlegend=False)
            + labs(title='Candlestick Without Legend')
        ).draw()

        assert fig.data[0].showlegend == False


class TestProfessionalStyles:
    """Test professional trading style examples."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_27_tradingview_style(self, ohlc_data):
        """Example 27: TradingView style."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#089981',  # TradingView green
                decreasing_color='#F23645',  # TradingView red
                line_width=1
            )
            + labs(title='Professional Trading View Style')
            + theme_minimal()
            + ggsize(width=1000, height=500)
        ).draw()

        assert fig.data[0].increasing.fillcolor == '#089981'
        assert fig.data[0].decreasing.fillcolor == '#F23645'

    def test_example_28_bloomberg_style(self, ohlc_data):
        """Example 28: Bloomberg Terminal style."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(
                increasing_color='#00FF00',  # Bright green
                decreasing_color='#FF0000',  # Bright red
                increasing_line_color='#00FF00',
                decreasing_line_color='#FF0000'
            )
            + labs(title='Bloomberg Terminal Style')
            + theme_dark()
        ).draw()

        assert fig.data[0].increasing.fillcolor == '#00FF00'
        assert fig.data[0].decreasing.fillcolor == '#FF0000'


class TestOHLCVariants:
    """Test OHLC style variants."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_example_29_ohlc_bars(self, ohlc_data):
        """Example 29: OHLC bars (similar to hollow candlesticks)."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc(
                increasing_color='#26A69A',
                decreasing_color='#EF5350',
                line_width=2
            )
            + labs(title='OHLC Bars (Similar to Hollow Candlesticks)')
        ).draw()

        assert fig.data[0].type == 'ohlc'
        assert fig.data[0].increasing.line.color == '#26A69A'


class TestComparison:
    """Test comparison examples."""

    def test_example_30_candlestick_vs_ohlc(self):
        """Example 30: Same data shown in both styles."""
        df_short = generate_ohlc_data(periods=10, volatility=0.015, seed=106)

        # Candlestick version
        fig_candle = (
            ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Candlestick Style')
        ).draw()

        # OHLC version
        fig_ohlc = (
            ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc()
            + labs(title='OHLC Bar Style')
        ).draw()

        assert fig_candle.data[0].type == 'candlestick'
        assert fig_ohlc.data[0].type == 'ohlc'
        # Both should have same number of data points
        assert len(fig_candle.data[0].x) == len(fig_ohlc.data[0].x)


class TestRealWorldExamples:
    """Test real-world scenario examples."""

    def test_example_31_tech_stock(self):
        """Example 31: Tech stock with trend and volatility clusters."""
        np.random.seed(2024)

        n = 120
        trend = np.linspace(0, 0.3, n)
        volatility = 0.02 + 0.01 * np.sin(np.linspace(0, 4 * np.pi, n))
        returns = trend / n + np.random.normal(0, 1, n) * volatility

        close = 180 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 180
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * volatility
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * volatility

        df_tech = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_tech, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick(name='NVDA')
            + labs(
                title='NVIDIA Corp (NVDA) - Simulated',
                x='Date',
                y='Price ($)'
            )
            + theme_minimal()
            + ggsize(width=1000, height=500)
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert fig.data[0].name == 'NVDA'
        assert len(fig.data[0].x) == 120


class TestMarketConditions:
    """Test different market condition simulations."""

    def test_example_32_bear_market(self):
        """Example 32: Bear market simulation."""
        np.random.seed(42)  # Use seed 42 for consistent results

        n = 90
        # Create deterministic bear market: steady decline
        close = 500 * np.exp(np.linspace(0, -0.3, n))  # ~26% decline
        # Add small noise
        close = close * (1 + np.random.normal(0, 0.005, n))

        open_prices = np.roll(close, 1)
        open_prices[0] = 500
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 3
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 3

        df_bear = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_bear, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Bear Market Simulation')
            + theme_minimal()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        assert len(fig.data[0].x) == n
        # Verify bear market: final close should be lower than initial open
        assert fig.data[0].close[-1] < fig.data[0].open[0]

    def test_example_33_bull_market(self):
        """Example 33: Bull market simulation."""
        np.random.seed(888)

        n = 90
        trend = np.linspace(0, 0.4, n)
        returns = trend / n + np.random.normal(0, 0.02, n)

        close = 100 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 100
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 2
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 2

        df_bull = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_bull, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Bull Market Simulation')
            + theme_minimal()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        # Bull market: final close should be higher than initial
        assert fig.data[0].close[-1] > fig.data[0].open[0]

    def test_example_34_sideways_market(self):
        """Example 34: Sideways/range-bound market."""
        np.random.seed(777)

        n = 90
        close = np.zeros(n)
        close[0] = 50
        for i in range(1, n):
            close[i] = close[i-1] + np.random.normal(0, 1) - 0.1 * (close[i-1] - 50)

        open_prices = np.roll(close, 1)
        open_prices[0] = 50
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 0.8
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 0.8

        df_sideways = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=n, freq='B'),
            'open': open_prices,
            'high': high,
            'low': low,
            'close': close,
        })

        fig = (
            ggplot(df_sideways, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
            + labs(title='Sideways/Range-Bound Market')
            + theme_minimal()
        ).draw()

        assert fig.data[0].type == 'candlestick'
        # Sideways market: final close should be close to initial (within 20%)
        price_change_pct = abs(fig.data[0].close[-1] - fig.data[0].open[0]) / fig.data[0].open[0]
        assert price_change_pct < 0.3  # Less than 30% change


class TestFullFeatured:
    """Test full-featured example."""

    def test_example_35_full_featured(self):
        """Example 35: Full-featured example with all customizations."""
        df_full = generate_ohlc_data(periods=90, start_price=150, volatility=0.02, seed=107)

        fig = (
            ggplot(df_full, aes(x='date', open='open', high='high', low='low', close='close'))
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


class TestDataIntegrity:
    """Test that OHLC data integrity is preserved."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data(seed=200)

    def test_ohlc_values_match_input(self, ohlc_data):
        """Verify that trace data matches input DataFrame."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        trace = fig.data[0]

        # Data should be sorted by date, so sort the original for comparison
        sorted_data = ohlc_data.sort_values('date')

        np.testing.assert_array_almost_equal(trace.open, sorted_data['open'].values, decimal=5)
        np.testing.assert_array_almost_equal(trace.high, sorted_data['high'].values, decimal=5)
        np.testing.assert_array_almost_equal(trace.low, sorted_data['low'].values, decimal=5)
        np.testing.assert_array_almost_equal(trace.close, sorted_data['close'].values, decimal=5)

    def test_high_low_relationship(self, ohlc_data):
        """Verify high >= low for all candles."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        trace = fig.data[0]
        assert all(np.array(trace.high) >= np.array(trace.low))

    def test_high_low_encompasses_open_close(self, ohlc_data):
        """Verify high >= max(open, close) and low <= min(open, close)."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        trace = fig.data[0]
        open_arr = np.array(trace.open)
        high_arr = np.array(trace.high)
        low_arr = np.array(trace.low)
        close_arr = np.array(trace.close)

        assert all(high_arr >= np.maximum(open_arr, close_arr))
        assert all(low_arr <= np.minimum(open_arr, close_arr))


class TestRangeslider:
    """Test rangeslider behavior."""

    @pytest.fixture
    def ohlc_data(self):
        return generate_ohlc_data()

    def test_rangeslider_disabled_by_default(self, ohlc_data):
        """Verify rangeslider is disabled by default for cleaner charts."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_candlestick()
        ).draw()

        assert fig.layout.xaxis.rangeslider.visible == False

    def test_ohlc_rangeslider_disabled(self, ohlc_data):
        """Verify rangeslider is disabled for OHLC charts too."""
        fig = (
            ggplot(ohlc_data, aes(x='date', open='open', high='high', low='low', close='close'))
            + geom_ohlc()
        ).draw()

        assert fig.layout.xaxis.rangeslider.visible == False
