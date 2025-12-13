# Time Series & Financial Charts

ggplotly provides specialized features for time series visualization, including date axis formatting, interactive range selection, and financial chart types.

## Date Axis Formatting

### Basic Date Axis

```python
import pandas as pd
import numpy as np
from ggplotly import *

dates = pd.date_range('2020-01-01', periods=24, freq='ME')
df = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.randn(24)) + 50
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line(color='steelblue', size=2)
 + geom_point(size=5)
 + scale_x_date(date_breaks='3 months', date_labels='%b %Y')
 + labs(title='Monthly Time Series'))
```

### DateTime Axis

For data with time components:

```python
timestamps = pd.date_range('2024-01-01 08:00', periods=48, freq='h')
df_hourly = pd.DataFrame({
    'timestamp': timestamps,
    'value': np.sin(np.linspace(0, 4*np.pi, 48)) + np.random.randn(48) * 0.2
})

(ggplot(df_hourly, aes(x='timestamp', y='value'))
 + geom_line()
 + scale_x_datetime(date_labels='%b %d %H:%M')
 + labs(title='Hourly Data'))
```

### Date Format Codes

| Code | Meaning | Example |
|------|---------|---------|
| `%Y` | 4-digit year | 2024 |
| `%y` | 2-digit year | 24 |
| `%m` | Month (01-12) | 03 |
| `%b` | Abbreviated month | Mar |
| `%B` | Full month | March |
| `%d` | Day (01-31) | 15 |
| `%H` | Hour (00-23) | 14 |
| `%M` | Minute (00-59) | 30 |
| `%S` | Second (00-59) | 45 |

## Interactive Range Selection

### Range Slider

Add a draggable range slider below the chart:

```python
dates = pd.date_range('2020-01-01', periods=365, freq='D')
df = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.randn(365))
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line()
 + scale_x_rangeslider()
 + labs(title='Drag the slider below to zoom'))
```

### Range Selector Buttons

Add buttons for quick time range selection:

```python
(ggplot(df, aes(x='date', y='value'))
 + geom_line()
 + scale_x_rangeselector(buttons=['1m', '3m', '6m', 'ytd', '1y', 'all'])
 + labs(title='Click buttons to select date range'))
```

### Available Button Presets

| Button | Description |
|--------|-------------|
| `1d` | Last day |
| `1w` | Last week |
| `1m` | Last month |
| `3m` | Last 3 months |
| `6m` | Last 6 months |
| `ytd` | Year to date |
| `1y` | Last year |
| `5y` | Last 5 years |
| `all` | All data |

## Historical Range Plots

`geom_range` shows current year data compared to historical min/max/average:

### Basic Range Plot

```python
# Generate multi-year daily data
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
temps = []
for d in dates:
    seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
    trend = (d.year - 2019) * 0.5
    noise = np.random.randn() * 15
    temps.append(seasonal + trend + noise)

df_temp = pd.DataFrame({'date': dates, 'temperature': temps})

# 5-year range plot with monthly aggregation
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='ME')
 + labs(
     title='Temperature: 5-Year Historical Range',
     subtitle='Gray: 5yr min/max, Black: 5yr avg, Blue: prior year, Red: current year'
 ))
```

### Weekly Aggregation

```python
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='W-Fri')
 + labs(title='Weekly Temperature Range'))
```

### Show Specific Historical Years

```python
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='ME', show_years=[2020, 2021])
 + labs(title='Temperature with 2020 and 2021 highlighted'))
```

### Range Plots with Facets

```python
np.random.seed(789)
cities = ['New York', 'Los Angeles', 'Chicago']
city_data = []
for city in cities:
    base_temp = {'New York': 50, 'Los Angeles': 65, 'Chicago': 45}[city]
    amplitude = {'New York': 30, 'Los Angeles': 15, 'Chicago': 35}[city]
    for d in dates:
        seasonal = base_temp + amplitude * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
        noise = np.random.randn() * 15
        city_data.append({'date': d, 'temperature': seasonal + noise, 'city': city})

df_cities = pd.DataFrame(city_data)

(ggplot(df_cities, aes(x='date', y='temperature'))
 + geom_range(freq='ME')
 + facet_wrap('city', nrow=1)
 + labs(title='Temperature by City')
 + theme_minimal())
```

## Financial Charts

### Candlestick Charts

```python
from datetime import datetime, timedelta

# Generate OHLC data
np.random.seed(42)
n = 60
dates = pd.date_range('2024-01-01', periods=n, freq='B')
returns = np.random.normal(0.0005, 0.02, n)
close = 100 * np.cumprod(1 + returns)
open_prices = np.roll(close, 1)
open_prices[0] = 100
high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * 0.01
low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * 0.01

df = pd.DataFrame({
    'date': dates,
    'open': open_prices,
    'high': high,
    'low': low,
    'close': close
})

(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_candlestick()
 + labs(title='Stock Price', y='Price ($)'))
```

### Custom Candlestick Colors

```python
# TradingView-style colors
(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_candlestick(increasing_color='#089981', decreasing_color='#F23645')
 + theme_dark()
 + labs(title='TradingView Style'))
```

### OHLC Bar Charts

Alternative to candlesticks using horizontal bars:

```python
(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_ohlc()
 + labs(title='OHLC Bar Chart'))
```

### Financial Chart Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `increasing_color` | 'green' | Color for up days |
| `decreasing_color` | 'red' | Color for down days |
| `line_width` | 1 | Width of wicks/bars |

## Combining Time Series Elements

### Line with Range Slider

```python
(ggplot(df, aes(x='date', y='close'))
 + geom_line(color='steelblue', size=2)
 + scale_x_rangeslider()
 + scale_x_rangeselector(buttons=['1m', '3m', 'all'])
 + labs(title='Interactive Stock Price'))
```

### Multiple Time Series

```python
# Multiple series
df_multi = pd.DataFrame({
    'date': np.tile(dates, 2),
    'value': np.concatenate([close, close * 0.8 + np.random.randn(n) * 2]),
    'series': ['Stock A'] * n + ['Stock B'] * n
})

(ggplot(df_multi, aes(x='date', y='value', color='series'))
 + geom_line(size=2)
 + scale_x_rangeslider()
 + labs(title='Comparing Two Stocks'))
```

### Candlesticks with Volume

```python
# Add volume bars below candlesticks using facets
df['volume'] = np.abs(np.random.randn(n)) * 1e6

from plotly.subplots import make_subplots

# For complex financial charts, you may want to use Plotly directly
# or layer multiple geoms with careful positioning
```

## Time Series with Annotations

```python
df = pd.DataFrame({
    'date': dates,
    'value': close
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line(size=2, color='steelblue')
 + geom_point(size=5)
 + annotate('segment', x=dates[20], y=max(close) + 5, xend=dates[20], yend=close[20] + 2,
            arrow=True, color='red', size=2)
 + annotate('text', x=dates[20], y=max(close) + 7, label='Important Event', size=12, color='red')
 + labs(title='Time Series with Annotation'))
```

## Using Pandas Index

ggplotly automatically handles DatetimeIndex:

```python
# Series with DatetimeIndex - x is automatically the index
dates = pd.date_range('2024-01-01', periods=30)
values = np.cumsum(np.random.randn(30))
ts = pd.Series(values, index=dates, name='Price')

ggplot(ts) + geom_line()
```

```python
# DataFrame with named DatetimeIndex
df_indexed = pd.DataFrame(
    {'value': np.sin(np.linspace(0, 4*np.pi, 100))},
    index=pd.DatetimeIndex(pd.date_range('2024-01-01', periods=100, freq='D'), name='Date')
)

ggplot(df_indexed, aes(y='value')) + geom_line()  # x automatically uses index
```
