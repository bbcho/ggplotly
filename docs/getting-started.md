# Getting Started

## Installation

Install ggplotly using pip:

```bash
pip install ggplotly
```

### Dependencies

ggplotly requires:

- Python 3.8+
- pandas
- plotly
- numpy

Optional dependencies for specific features:

```bash
# For geographic plots (geom_map, geom_sf)
pip install geopandas shapely

# For smoothing (geom_smooth, stat_smooth)
pip install scipy scikit-learn
```

## Basic Usage

### Import

```python
from ggplotly import *
import pandas as pd
```

### Your First Plot

```python
# Create some data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 4]
})

# Create a scatter plot
ggplot(df, aes(x='x', y='y')) + geom_point()
```

### The Grammar of Graphics

Every ggplotly visualization is built from these components:

1. **Data** - A pandas DataFrame
2. **Aesthetics** (`aes()`) - Map columns to visual properties
3. **Geoms** - Geometric objects that represent data (points, lines, bars)
4. **Optional layers** - Scales, themes, facets, labels

```python
(
    ggplot(df, aes(x='x', y='y', color='category'))  # Data + aesthetics
    + geom_point(size=3)                              # Geom
    + scale_color_brewer(palette='Set1')              # Scale
    + theme_minimal()                                 # Theme
    + labs(title='My Plot', x='X Axis', y='Y Axis')  # Labels
)
```

## Common Patterns

### Color by Category

```python
ggplot(df, aes(x='x', y='y', color='category')) + geom_point()
```

### Multiple Geoms

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_line()
```

### Faceting

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('category')
```

### Using Index as X-Axis

```python
# Automatically use DataFrame index
ggplot(df, aes(y='values')) + geom_line()

# Or explicitly
ggplot(df, aes(x='index', y='values')) + geom_line()

# Works with Series too
series = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
ggplot(series) + geom_point()
```

## Saving Plots

```python
# Create plot
p = ggplot(df, aes(x='x', y='y')) + geom_point()

# Save as HTML (interactive)
p.draw().write_html('plot.html')

# Save as image (requires kaleido)
p.draw().write_image('plot.png')

# Or use ggsave
ggsave(p, 'plot.png', width=800, height=600)
```

## Built-in Datasets

ggplotly includes classic datasets for learning:

```python
from ggplotly import data

# Load a dataset
mpg = data('mpg')
diamonds = data('diamonds')
iris = data('iris')

# See all available datasets
data()
```

## Next Steps

- [Aesthetics Guide](guide/aesthetics.md) - Learn about mapping data to visual properties
- [Geoms Reference](guide/geoms.md) - Explore all available geometric objects
- [Themes](guide/themes.md) - Customize the look of your plots
