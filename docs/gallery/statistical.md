# Statistical Visualizations

ggplotly includes statistical transformations for smoothing, density estimation, and summary statistics.

## Smoothed Lines

### LOESS Smoothing

Local regression smoothing (default):

```python
import pandas as pd
import numpy as np
from ggplotly import *

np.random.seed(42)
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', color='blue'))
```

### Linear Regression

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='lm', color='red'))
```

### Confidence Intervals

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', se=True, color='green')
 + labs(title='LOESS with Confidence Interval'))
```

### Smooth by Group

```python
df = pd.DataFrame({
    'x': np.tile(np.linspace(0, 10, 50), 2),
    'y': np.concatenate([
        np.sin(np.linspace(0, 10, 50)) + np.random.normal(0, 0.3, 50),
        np.cos(np.linspace(0, 10, 50)) + np.random.normal(0, 0.3, 50)
    ]),
    'group': ['A'] * 50 + ['B'] * 50
})

(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', se=True))
```

### Smooth Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `method` | 'loess' | 'loess', 'lm', 'lowess' |
| `se` | True | Show confidence interval |
| `span` | 0.75 | Smoothing span for LOESS (0-1) |
| `level` | 0.95 | Confidence level |

## Density Plots

### Basic Density

```python
df = pd.DataFrame({'x': np.random.randn(500)})
ggplot(df, aes(x='x')) + geom_density(fill='lightblue', alpha=0.5)
```

### Overlapping Densities

```python
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 1, 500), np.random.normal(2, 1.5, 500)]),
    'group': ['A'] * 500 + ['B'] * 500
})

ggplot(df, aes(x='x', fill='group')) + geom_density(alpha=0.5)
```

### Density with Histogram

```python
df = pd.DataFrame({'x': np.random.randn(1000)})

(ggplot(df, aes(x='x'))
 + geom_histogram(aes(y='..density..'), bins=30, fill='lightgray', color='white')
 + geom_density(color='red', size=2))
```

## Empirical CDF

Cumulative distribution function:

```python
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_step(stat='ecdf') + labs(title='Empirical CDF')
```

### Compare Distributions

```python
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 1, 200), np.random.normal(1, 0.5, 200)]),
    'group': ['A'] * 200 + ['B'] * 200
})

(ggplot(df, aes(x='x', color='group'))
 + geom_step(stat='ecdf')
 + labs(title='Comparing CDFs'))
```

## Summary Statistics

### Mean Points

```python
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 30),
    'value': np.random.randn(90) + np.tile([0, 2, 1], 30)
})

(ggplot(df, aes(x='category', y='value'))
 + geom_point(alpha=0.3)
 + stat_summary(fun='mean', geom='point', color='red', size=15))
```

### Mean with Error Bars

```python
(ggplot(df, aes(x='category', y='value'))
 + geom_jitter(width=0.2, alpha=0.3)
 + stat_summary(fun='mean', geom='point', color='red', size=10)
 + stat_summary(fun='mean', fun_min=lambda x: x.mean() - x.std(),
                fun_max=lambda x: x.mean() + x.std(), geom='errorbar', color='red'))
```

## Contour Plots

### Contour Lines

```python
# Create 2D density data
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))

df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

ggplot(df, aes(x='x', y='y', z='z')) + geom_contour()
```

### Filled Contours

```python
(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_contour_filled()
 + labs(title='Filled Contour Plot'))
```

### Contour with Points

```python
# Sample points
points = pd.DataFrame({
    'x': np.random.uniform(-2, 2, 50),
    'y': np.random.uniform(-2, 2, 50)
})

(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_contour_filled(alpha=0.7)
 + geom_point(data=points, color='white', size=5))
```

## Error Bars

### Basic Error Bars

```python
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [10, 15, 12, 18],
    'ymin': [8, 13, 10, 15],
    'ymax': [12, 17, 14, 21]
})

(ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax'))
 + geom_col(fill='steelblue', alpha=0.7)
 + geom_errorbar(width=0.2))
```

### Error Bars from Standard Error

```python
# Compute statistics
summary = df.groupby('category')['value'].agg(['mean', 'std', 'count']).reset_index()
summary['se'] = summary['std'] / np.sqrt(summary['count'])
summary['ymin'] = summary['mean'] - summary['se']
summary['ymax'] = summary['mean'] + summary['se']

(ggplot(summary, aes(x='category', y='mean', ymin='ymin', ymax='ymax'))
 + geom_col(fill='steelblue', alpha=0.7)
 + geom_errorbar(width=0.2, color='black'))
```

## Violin with Box Plot

Combine violin and box for distribution overview:

```python
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 100),
    'value': np.random.randn(300) * np.tile([1, 2, 1.5], 100) + np.tile([0, 2, 1], 100)
})

(ggplot(df, aes(x='category', y='value', fill='category'))
 + geom_violin(alpha=0.5)
 + geom_boxplot(width=0.1, fill='white'))
```

## Scatter with Marginal Distributions

```python
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200)
})

# Main scatter
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_density(aes(x='x'), color='blue', inherit_aes=False)
 + geom_density(aes(y='y'), color='red', inherit_aes=False)
 + geom_rug(sides='bl', alpha=0.3))
```

## Quantile-Quantile Plots

Compare distribution to theoretical:

```python
from scipy import stats

# Generate data
data = np.random.randn(100)

# Compute theoretical quantiles
theoretical = stats.norm.ppf(np.linspace(0.01, 0.99, len(data)))
sample = np.sort(data)

qq_df = pd.DataFrame({'theoretical': theoretical, 'sample': sample})

(ggplot(qq_df, aes(x='theoretical', y='sample'))
 + geom_point()
 + geom_abline(slope=1, intercept=0, color='red', linetype='dash')
 + labs(title='Q-Q Plot', x='Theoretical Quantiles', y='Sample Quantiles'))
```

## 2D Density / Hexbin

For large scatter plots, show density:

```python
# Large dataset
df = pd.DataFrame({
    'x': np.random.randn(10000),
    'y': np.random.randn(10000)
})

# 2D histogram as tiles
(ggplot(df, aes(x='x', y='y'))
 + geom_bin2d(bins=30)
 + scale_fill_viridis_c()
 + labs(title='2D Histogram'))
```

## Regression Diagnostics

```python
# Fit a model and plot residuals
from sklearn.linear_model import LinearRegression

df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': 2 * np.linspace(0, 10, 100) + np.random.normal(0, 2, 100)
})

model = LinearRegression()
model.fit(df[['x']], df['y'])
df['predicted'] = model.predict(df[['x']])
df['residual'] = df['y'] - df['predicted']

# Residuals vs Fitted
(ggplot(df, aes(x='predicted', y='residual'))
 + geom_point(alpha=0.5)
 + geom_hline(data=0, color='red', linetype='dash')
 + labs(title='Residuals vs Fitted', x='Fitted Values', y='Residuals'))
```
