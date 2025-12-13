# Multi-Panel Plots (Facets)

Faceting creates multiple panels from your data, each showing a subset. This is powerful for comparing groups or exploring interactions.

## facet_wrap

Wrap panels into a grid based on one variable:

### Basic Faceting

```python
import pandas as pd
import numpy as np
from ggplotly import *

df = pd.DataFrame({
    'x': np.random.randn(300),
    'y': np.random.randn(300),
    'category': np.random.choice(['A', 'B', 'C'], 300)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category'))
```

### Control Number of Columns

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', ncol=1))
```

### Control Number of Rows

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', nrow=1))
```

### Many Categories

```python
df = pd.DataFrame({
    'x': np.random.randn(500),
    'y': np.random.randn(500),
    'category': np.random.choice(['A', 'B', 'C', 'D', 'E', 'F'], 500)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', ncol=3))
```

## facet_grid

Create a matrix of panels based on two variables:

### Basic Grid

```python
df = pd.DataFrame({
    'x': np.random.randn(400),
    'y': np.random.randn(400),
    'row_var': np.tile(np.repeat(['R1', 'R2'], 100), 2),
    'col_var': np.repeat(['C1', 'C2'], 200)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_grid(rows='row_var', cols='col_var'))
```

### Rows Only

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_grid(rows='row_var'))
```

### Columns Only

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_grid(cols='col_var'))
```

## Free Scales

When facets have different data ranges:

### Free Both Axes

```python
df = pd.DataFrame({
    'x': np.concatenate([
        np.random.uniform(0, 10, 50),
        np.random.uniform(0, 100, 50)
    ]),
    'y': np.concatenate([
        np.random.uniform(0, 5, 50),
        np.random.uniform(0, 50, 50)
    ]),
    'group': ['A'] * 50 + ['B'] * 50
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + facet_wrap('group', scales='free'))
```

### Free X Only

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + facet_wrap('group', scales='free_x'))
```

### Free Y Only

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + facet_wrap('group', scales='free_y'))
```

## Facet Labellers

### label_value (Default)

Shows just the value:

```python
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'category': np.tile(['Group A', 'Group B'], 100)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', labeller=label_value)
 + labs(title='Using label_value labeller'))
```

### label_both

Shows variable name and value:

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', labeller=label_both)
 + labs(title='Using label_both labeller'))
```

## Facets with Multiple Geoms

### Scatter with Smooth

```python
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'category': np.random.choice(['A', 'B'], 200)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', color='red')
 + facet_wrap('category'))
```

### Histogram by Group

```python
df = pd.DataFrame({
    'x': np.concatenate([
        np.random.normal(0, 1, 200),
        np.random.normal(2, 1.5, 200)
    ]),
    'group': ['A'] * 200 + ['B'] * 200
})

(ggplot(df, aes(x='x'))
 + geom_histogram(bins=20, fill='steelblue', alpha=0.7)
 + facet_wrap('group', ncol=1))
```

### Boxplots Across Facets

```python
df = pd.DataFrame({
    'treatment': np.tile(['Control', 'Treatment'], 300),
    'region': np.repeat(['North', 'South', 'East'], 200),
    'value': np.random.randn(600)
})

(ggplot(df, aes(x='treatment', y='value', fill='treatment'))
 + geom_boxplot()
 + facet_wrap('region')
 + theme(legend_position='none'))
```

## Facets with Time Series

```python
np.random.seed(42)
dates = pd.date_range('2024-01-01', periods=100, freq='D')

df = pd.DataFrame({
    'date': np.tile(dates, 3),
    'value': np.concatenate([
        np.cumsum(np.random.randn(100)),
        np.cumsum(np.random.randn(100)) + 10,
        np.cumsum(np.random.randn(100)) + 20
    ]),
    'series': np.repeat(['A', 'B', 'C'], 100)
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line(color='steelblue')
 + facet_wrap('series', ncol=1, scales='free_y')
 + theme_minimal())
```

## Facets with Maps

```python
# Multi-city temperature comparison
np.random.seed(789)
cities = ['New York', 'Los Angeles', 'Chicago']
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')

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

## Combining Facets with Color

### Color by Same Variable

```python
df = pd.DataFrame({
    'x': np.random.randn(300),
    'y': np.random.randn(300),
    'category': np.random.choice(['A', 'B', 'C'], 300)
})

(ggplot(df, aes(x='x', y='y', color='category'))
 + geom_point()
 + facet_wrap('category')
 + theme(legend_position='none'))  # Legend redundant with facets
```

### Color by Different Variable

```python
df = pd.DataFrame({
    'x': np.random.randn(400),
    'y': np.random.randn(400),
    'facet_var': np.repeat(['Panel 1', 'Panel 2'], 200),
    'color_var': np.tile(['Group A', 'Group B'], 200)
})

(ggplot(df, aes(x='x', y='y', color='color_var'))
 + geom_point()
 + facet_wrap('facet_var')
 + scale_color_brewer(palette='Set1'))
```

## Facet Parameters Reference

### facet_wrap

| Parameter | Default | Description |
|-----------|---------|-------------|
| `facets` | required | Column name for faceting |
| `ncol` | auto | Number of columns |
| `nrow` | auto | Number of rows |
| `scales` | 'fixed' | 'fixed', 'free', 'free_x', 'free_y' |
| `labeller` | label_value | Labelling function |

### facet_grid

| Parameter | Default | Description |
|-----------|---------|-------------|
| `rows` | None | Column name for row faceting |
| `cols` | None | Column name for column faceting |
| `scales` | 'fixed' | 'fixed', 'free', 'free_x', 'free_y' |
| `labeller` | label_value | Labelling function |

## Tips

1. **Use `scales='free'`** when comparing distributions with different ranges
2. **Hide redundant legends** with `theme(legend_position='none')` when faceting by the same variable
3. **Control layout** with `ncol`/`nrow` to optimize space usage
4. **Use `label_both`** when facet variable name isn't obvious from values
5. **Combine with themes** - facets work with all ggplotly themes
