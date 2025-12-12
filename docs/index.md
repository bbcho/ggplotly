# ggplotly

A data visualization library for Python that combines the **grammar of graphics** from ggplot2 with the **interactivity** of Plotly.

## Why ggplotly?

- **Familiar syntax** - If you know ggplot2 from R, you'll feel right at home
- **Interactive plots** - Powered by Plotly for zooming, panning, and hover tooltips
- **Jupyter-friendly** - Plots render automatically in notebooks
- **Comprehensive** - 90+ ggplot2-equivalent functions

## Quick Example

```python
from ggplotly import *
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 4, 9, 16, 25],
    'group': ['A', 'A', 'B', 'B', 'B']
})

# Simple scatter plot
ggplot(df, aes(x='x', y='y')) + geom_point()

# With color mapping and theme
ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + theme_minimal()

# Faceted plot
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('group')
```

## Installation

```bash
pip install ggplotly
```

## What's Included

| Category | Count | Examples |
|----------|-------|----------|
| **Geoms** | 34 | `geom_point`, `geom_line`, `geom_bar`, `geom_boxplot`, `geom_map` |
| **Scales** | 17 | `scale_color_manual`, `scale_fill_gradient`, `scale_x_log10` |
| **Themes** | 9 | `theme_minimal`, `theme_dark`, `theme_bbc`, `theme_nytimes` |
| **Stats** | 7 | `stat_smooth`, `stat_count`, `stat_density` |
| **Coords** | 4 | `coord_flip`, `coord_polar`, `coord_sf` |
| **Facets** | 2 | `facet_wrap`, `facet_grid` |

## Coming from R?

ggplotly aims for API compatibility with ggplot2. Most code translates directly:

=== "R (ggplot2)"

    ```r
    ggplot(mpg, aes(x = displ, y = hwy, color = class)) +
      geom_point() +
      theme_minimal() +
      labs(title = "Fuel Efficiency")
    ```

=== "Python (ggplotly)"

    ```python
    ggplot(mpg, aes(x='displ', y='hwy', color='class')) + \
      geom_point() + \
      theme_minimal() + \
      labs(title='Fuel Efficiency')
    ```

The main differences:

- Column names are strings: `x='column'` not `x = column`
- Use `\` or parentheses for line continuation
- Import with `from ggplotly import *`
