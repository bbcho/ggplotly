# geom_candlestick Examples
# Comprehensive examples for candlestick and OHLC charts in ggplotly
# Each cell is self-contained and can be run independently in Jupyter

# %% [markdown]
# # geom_candlestick and geom_ohlc Examples
#
# This notebook demonstrates the various features of `geom_candlestick` and `geom_ohlc`
# for creating interactive financial charts with ggplotly.

# %% [markdown]
# ## Setup

# %%
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

# Set random seed for reproducibility
np.random.seed(42)


# Helper function to generate realistic OHLC data
def generate_ohlc_data(start_date='2024-01-01', periods=60, start_price=100, volatility=0.02):
    """Generate realistic OHLC data with random walk."""
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


# %% [markdown]
# ## 1. Basic Candlestick Chart

# %%
# Generate sample stock data
df = generate_ohlc_data()

# Basic candlestick chart
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
)

# %% [markdown]
# ## 2. Candlestick with Title and Labels

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(
        title='Stock Price Movement',
        x='Date',
        y='Price ($)'
    )
)

# %% [markdown]
# ## 3. Custom Colors - Blue/Orange Theme

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#2196F3',  # Blue for up
        decreasing_color='#FF9800'   # Orange for down
    )
    + labs(title='Blue/Orange Color Scheme')
)

# %% [markdown]
# ## 4. Custom Colors - Traditional Green/Red

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='green',
        decreasing_color='red',
        increasing_line_color='darkgreen',
        decreasing_line_color='darkred'
    )
    + labs(title='Traditional Green/Red Scheme')
)

# %% [markdown]
# ## 5. Grayscale Theme

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#333333',
        decreasing_color='#AAAAAA'
    )
    + labs(title='Grayscale Candlestick')
    + theme_minimal()
)

# %% [markdown]
# ## 6. Custom Line Width

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(line_width=2)
    + labs(title='Thicker Wick Lines')
)

# %% [markdown]
# ## 7. Custom Whisker Width

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(whisker_width=0.5)
    + labs(title='Wider Whiskers')
)

# %% [markdown]
# ## 8. Semi-Transparent Candlesticks

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(opacity=0.7)
    + labs(title='Semi-Transparent Candlesticks')
)

# %% [markdown]
# ## 9. Basic OHLC Chart

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_ohlc()
    + labs(title='OHLC Bar Chart')
)

# %% [markdown]
# ## 10. OHLC with Custom Colors

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_ohlc(
        increasing_color='navy',
        decreasing_color='maroon'
    )
    + labs(title='OHLC with Navy/Maroon Colors')
)

# %% [markdown]
# ## 11. OHLC with Thicker Lines

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_ohlc(line_width=3, tickwidth=0.1)
    + labs(title='OHLC with Thicker Lines')
)

# %% [markdown]
# ## 12. Dark Theme

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#00E676',  # Bright green
        decreasing_color='#FF5252'   # Bright red
    )
    + labs(title='Candlestick with Dark Theme')
    + theme_dark()
)

# %% [markdown]
# ## 13. Minimal Theme

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Candlestick with Minimal Theme')
    + theme_minimal()
)

# %% [markdown]
# ## 14. Classic Theme

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Candlestick with Classic Theme')
    + theme_classic()
)

# %% [markdown]
# ## 15. Custom Figure Size

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Wide Candlestick Chart')
    + ggsize(width=1200, height=500)
)

# %% [markdown]
# ## 16. Shorter Time Period (2 Weeks)

# %%
df_short = generate_ohlc_data(periods=10, volatility=0.015)

(
    ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='2-Week Price Movement')
)

# %% [markdown]
# ## 17. Longer Time Period (6 Months)

# %%
df_long = generate_ohlc_data(periods=130, volatility=0.02)

(
    ggplot(df_long, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='6-Month Price Movement')
    + ggsize(width=1000, height=500)
)

# %% [markdown]
# ## 18. High Volatility Stock

# %%
df_volatile = generate_ohlc_data(periods=60, start_price=50, volatility=0.05)

(
    ggplot(df_volatile, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='High Volatility Stock')
)

# %% [markdown]
# ## 19. Low Volatility Stock

# %%
df_stable = generate_ohlc_data(periods=60, start_price=150, volatility=0.008)

(
    ggplot(df_stable, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Low Volatility Stock')
)

# %% [markdown]
# ## 20. Penny Stock (Low Price)

# %%
df_penny = generate_ohlc_data(periods=60, start_price=2.5, volatility=0.04)

(
    ggplot(df_penny, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Penny Stock Price Movement', y='Price ($)')
)

# %% [markdown]
# ## 21. High-Priced Stock

# %%
df_expensive = generate_ohlc_data(periods=60, start_price=3500, volatility=0.015)

(
    ggplot(df_expensive, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='High-Priced Stock (e.g., AMZN)', y='Price ($)')
)

# %% [markdown]
# ## 22. Cryptocurrency Style (24/7 Trading)

# %%
# Generate crypto data with all days (not just business days)
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

(
    ggplot(df_crypto, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#00C853',
        decreasing_color='#FF1744'
    )
    + labs(title='Bitcoin Price (Simulated)', y='Price (USD)')
    + theme_dark()
)

# %% [markdown]
# ## 23. Forex Style

# %%
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

(
    ggplot(df_forex, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='EUR/USD Exchange Rate', y='Rate')
    + theme_minimal()
)

# %% [markdown]
# ## 24. Commodity Style

# %%
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

(
    ggplot(df_oil, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#4CAF50',
        decreasing_color='#F44336'
    )
    + labs(title='Crude Oil Futures', y='Price ($/barrel)')
)

# %% [markdown]
# ## 25. Named Candlestick for Legend

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(name='AAPL')
    + labs(title='Apple Inc. (AAPL)')
)

# %% [markdown]
# ## 26. Hide Legend

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(showlegend=False)
    + labs(title='Candlestick Without Legend')
)

# %% [markdown]
# ## 27. Professional Trading Style

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#089981',  # TradingView green
        decreasing_color='#F23645',  # TradingView red
        line_width=1
    )
    + labs(title='Professional Trading View Style')
    + theme_minimal()
    + ggsize(width=1000, height=500)
)

# %% [markdown]
# ## 28. Bloomberg Terminal Style

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(
        increasing_color='#00FF00',  # Bright green
        decreasing_color='#FF0000',  # Bright red
        increasing_line_color='#00FF00',
        decreasing_line_color='#FF0000'
    )
    + labs(title='Bloomberg Terminal Style')
    + theme_dark()
)

# %% [markdown]
# ## 29. Hollow Candlesticks Style (using OHLC)
#
# OHLC bars can give a similar effect to hollow candlesticks

# %%
(
    ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_ohlc(
        increasing_color='#26A69A',
        decreasing_color='#EF5350',
        line_width=2
    )
    + labs(title='OHLC Bars (Similar to Hollow Candlesticks)')
)

# %% [markdown]
# ## 30. Comparison: Candlestick vs OHLC
#
# Same data shown in both styles

# %%
# Candlestick version
(
    ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Candlestick Style')
)

# %%
# OHLC version
(
    ggplot(df_short, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_ohlc()
    + labs(title='OHLC Bar Style')
)

# %% [markdown]
# ## 31. Real-World Example: Tech Stock Simulation

# %%
np.random.seed(2024)

# Simulate a tech stock with trend and volatility clusters
n = 120
trend = np.linspace(0, 0.3, n)  # Upward trend
volatility = 0.02 + 0.01 * np.sin(np.linspace(0, 4 * np.pi, n))  # Varying volatility
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

(
    ggplot(df_tech, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick(name='NVDA')
    + labs(
        title='NVIDIA Corp (NVDA) - Simulated',
        x='Date',
        y='Price ($)'
    )
    + theme_minimal()
    + ggsize(width=1000, height=500)
)

# %% [markdown]
# ## 32. Bear Market Simulation

# %%
np.random.seed(999)

n = 90
# Downward trend
trend = np.linspace(0, -0.25, n)
returns = trend / n + np.random.normal(0, 0.025, n)

close = 500 * np.cumprod(1 + returns)
open_prices = np.roll(close, 1)
open_prices[0] = 500
high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * 5
low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * 5

df_bear = pd.DataFrame({
    'date': pd.date_range('2024-01-01', periods=n, freq='B'),
    'open': open_prices,
    'high': high,
    'low': low,
    'close': close,
})

(
    ggplot(df_bear, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Bear Market Simulation')
    + theme_minimal()
)

# %% [markdown]
# ## 33. Bull Market Simulation

# %%
np.random.seed(888)

n = 90
# Strong upward trend
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

(
    ggplot(df_bull, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Bull Market Simulation')
    + theme_minimal()
)

# %% [markdown]
# ## 34. Sideways/Range-Bound Market

# %%
np.random.seed(777)

n = 90
# Mean-reverting process (sideways market)
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

(
    ggplot(df_sideways, aes(x='date', open='open', high='high', low='low', close='close'))
    + geom_candlestick()
    + labs(title='Sideways/Range-Bound Market')
    + theme_minimal()
)

# %% [markdown]
# ## 35. Full-Featured Example

# %%
# Generate comprehensive data
df_full = generate_ohlc_data(periods=90, start_price=150, volatility=0.02)

(
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
)

# %%
