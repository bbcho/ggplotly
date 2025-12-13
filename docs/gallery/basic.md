# Basic Charts

Fundamental chart types for everyday data visualization.

## Scatter Plots

### Basic Scatter

```python
import pandas as pd
import numpy as np
from ggplotly import *

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 4]
})

ggplot(df, aes(x='x', y='y')) + geom_point()
```

### Scatter with Color Mapping

```python
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

ggplot(df, aes(x='x', y='y', color='category')) + geom_point()
```

### Scatter with Size Mapping

```python
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'size_var': np.random.rand(100) * 50
})

ggplot(df, aes(x='x', y='y', size='size_var')) + geom_point(color='steelblue', alpha=0.6)
```

### Multiple Aesthetics

```python
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'size_var': np.random.rand(100) * 50
})

ggplot(df, aes(x='x', y='y', color='category', size='size_var')) + geom_point(alpha=0.7)
```

### Custom Point Styles

```python
ggplot(df, aes(x='x', y='y')) + geom_point(size=10, color='red', shape='diamond')
```

Available shapes: `'circle'`, `'square'`, `'diamond'`, `'cross'`, `'x'`, `'triangle-up'`, `'triangle-down'`, `'star'`

## Line Charts

### Basic Line

```python
x = np.linspace(0, 10, 100)
df = pd.DataFrame({'x': x, 'y': np.sin(x)})

ggplot(df, aes(x='x', y='y')) + geom_line(color='steelblue', size=2)
```

### Multiple Lines

```python
df = pd.DataFrame({
    'x': np.tile(np.linspace(0, 10, 50), 3),
    'y': np.concatenate([
        np.sin(np.linspace(0, 10, 50)),
        np.cos(np.linspace(0, 10, 50)),
        np.sin(np.linspace(0, 10, 50)) + np.cos(np.linspace(0, 10, 50))
    ]),
    'group': np.repeat(['sin', 'cos', 'sin+cos'], 50)
})

ggplot(df, aes(x='x', y='y', color='group')) + geom_line(size=2)
```

### Line with Points

```python
df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})

ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10)
```

## Path Charts

`geom_path` connects points in data order (not sorted by x):

### Spiral

```python
import math

t_vals = [i * 4 * math.pi / 100 for i in range(100)]
spiral = pd.DataFrame({
    'x': [t * math.cos(t) for t in t_vals],
    'y': [t * math.sin(t) for t in t_vals],
})

(ggplot(spiral, aes(x='x', y='y'))
 + geom_path(color='steelblue', size=2)
 + labs(title='Spiral with geom_path'))
```

### Star Shape

```python
points = 5
outer_r, inner_r = 1, 0.4
star_x, star_y = [], []
for i in range(points * 2 + 1):
    angle = i * math.pi / points - math.pi / 2
    r = outer_r if i % 2 == 0 else inner_r
    star_x.append(r * math.cos(angle))
    star_y.append(r * math.sin(angle))

star = pd.DataFrame({'x': star_x, 'y': star_y})
ggplot(star, aes(x='x', y='y')) + geom_path(color='gold', size=3)
```

## Bar Charts

### Count-Based Bar Chart

```python
df = pd.DataFrame({'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 200)})
ggplot(df, aes(x='category')) + geom_bar()
```

### Colored by Category

```python
mpg = data('mpg')
ggplot(mpg, aes(x='class', fill='class')) + geom_bar(alpha=0.8)
```

### Stacked Bar Chart

```python
ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar()
```

### Dodged (Side-by-Side) Bar Chart

```python
ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar(position='dodge')
```

### Custom Dodge Width

```python
(ggplot(mpg, aes(x='cyl', fill='drv'))
 + geom_bar(position=position_dodge(width=0.8)))
```

## Column Charts

For pre-computed values, use `geom_col`:

```python
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [25, 40, 30, 55]
})

ggplot(df, aes(x='category', y='value')) + geom_col(fill='steelblue')
```

### Grouped Column Chart

```python
df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'group': ['G1', 'G2'] * 3,
    'value': [10, 15, 20, 25, 15, 20]
})

ggplot(df, aes(x='category', y='value', fill='group')) + geom_col(position='dodge')
```

## Histograms

### Basic Histogram

```python
df = pd.DataFrame({'x': np.random.randn(1000)})
ggplot(df, aes(x='x')) + geom_histogram(fill='steelblue', alpha=0.7)
```

### Custom Bins

```python
ggplot(df, aes(x='x')) + geom_histogram(bins=30, color='white', fill='#FF6B6B')
```

### Overlapping Histograms

```python
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 1, 500), np.random.normal(2, 1.5, 500)]),
    'group': ['A'] * 500 + ['B'] * 500
})

ggplot(df, aes(x='x', fill='group')) + geom_histogram(alpha=0.5, bins=30)
```

## Box Plots

### Basic Boxplot

```python
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C', 'D'], 50),
    'value': np.random.randn(200) * np.tile([1, 2, 1.5, 0.8], 50) + np.tile([0, 1, -1, 2], 50)
})

ggplot(df, aes(x='category', y='value')) + geom_boxplot()
```

### Colored Boxplot

```python
ggplot(df, aes(x='category', y='value', fill='category')) + geom_boxplot(alpha=0.7)
```

## Violin Plots

```python
ggplot(df, aes(x='category', y='value', fill='category')) + geom_violin(alpha=0.6)
```

## Area Charts

### Simple Area

```python
x = np.linspace(0, 10, 100)
df = pd.DataFrame({'x': x, 'y': np.sin(x) + 1.5})

ggplot(df, aes(x='x', y='y')) + geom_area(fill='lightblue', alpha=0.7)
```

### Stacked Area

```python
df = pd.DataFrame({
    'x': np.tile(np.linspace(0, 10, 50), 3),
    'y': np.abs(np.concatenate([
        np.sin(np.linspace(0, 10, 50)),
        0.5 * np.cos(np.linspace(0, 10, 50)) + 0.5,
        0.3 * np.sin(2 * np.linspace(0, 10, 50)) + 0.3
    ])),
    'group': np.repeat(['A', 'B', 'C'], 50)
})

ggplot(df, aes(x='x', y='y', fill='group')) + geom_area(alpha=0.6)
```

## Step Charts

```python
x = np.linspace(0, 10, 20)
df = pd.DataFrame({'x': x, 'y': np.sin(x)})

ggplot(df, aes(x='x', y='y')) + geom_step(color='blue', size=2)
```

## Ribbon Charts

Confidence bands or ranges:

```python
x = np.linspace(0, 10, 50)
y = np.sin(x)
df = pd.DataFrame({
    'x': x,
    'ymin': y - 0.3,
    'ymax': y + 0.3
})

ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(fill='steelblue', alpha=0.3)
```

## Heatmaps

```python
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)
Z = np.sin(X / 2) * np.cos(Y / 2)

df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + scale_fill_viridis_c()
```

## Text Labels

```python
df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [2, 4, 3, 5],
    'label': ['Point A', 'Point B', 'Point C', 'Point D']
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10, color='steelblue')
 + geom_text(aes(label='label'), vjust=-1))
```

## Reference Lines

### Horizontal and Vertical Lines

```python
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + geom_hline(data=0, color='red', linetype='dash')
 + geom_vline(data=0, color='blue', linetype='dash'))
```

### Slope/Intercept Lines

```python
df = pd.DataFrame({'x': range(10), 'y': [i * 2 + 1 for i in range(10)]})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=8)
 + geom_abline(slope=2, intercept=1, color='red', linetype='dash')
 + geom_abline(slope=1.5, intercept=3, color='blue'))
```

## Jittered Points

Avoid overplotting for categorical x-axes:

```python
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 50),
    'value': np.random.randn(150)
})

# Without jitter - points overlap
(ggplot(df, aes(x='category', y='value'))
 + geom_point(alpha=0.5)
 + labs(title='Without Jitter'))

# With jitter - points spread out
(ggplot(df, aes(x='category', y='value'))
 + geom_jitter(width=0.2, alpha=0.5)
 + labs(title='With Jitter'))
```

## Rug Plots

Add marginal tick marks:

```python
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_rug(sides='bl', alpha=0.3)  # bottom and left
 + labs(title='Scatter with Marginal Rugs'))
```
