# CLAUDE.md - Project Context for AI Assistants

## Project Overview

**GGPLOTLY** is a Python data visualization library that combines R's ggplot2 Grammar of Graphics with Plotly's interactive capabilities.

- Version: 0.3.5 (Beta)
- Author: Ben Cho
- Python: 3.9+
- License: MIT

## Quick Start

```python
from ggplotly import ggplot, aes, geom_point, theme_minimal

(ggplot(df, aes(x='col1', y='col2', color='category'))
 + geom_point()
 + theme_minimal())
```

## Project Structure

```
ggplotly/
├── ggplotly/           # Main package
│   ├── ggplot.py       # Core ggplot class
│   ├── aes.py          # Aesthetic mappings
│   ├── layer.py        # Layer abstraction
│   ├── geoms/          # 44+ geometric objects
│   ├── stats/          # 13 statistical transformations
│   ├── scales/         # 17+ scales
│   ├── coords/         # Coordinate systems
│   ├── themes.py       # 9 built-in themes
│   ├── facets.py       # facet_wrap, facet_grid
│   └── data/           # Built-in datasets (CSV)
├── pytest/             # Test suite (39 files)
├── examples/           # Jupyter notebooks (43)
└── docs/               # MkDocs documentation
```

## Key Files

- `ggplotly/ggplot.py` - Main ggplot class, rendering pipeline
- `ggplotly/layer.py` - Layer abstraction combining data, geom, stat, position
- `ggplotly/aes.py` - `aes()` function and `after_stat()` for aesthetic mappings
- `ggplotly/trace_builders.py` - Strategy pattern for Plotly trace creation
- `ggplotly/aesthetic_mapper.py` - Maps aesthetics to visual properties
- `ggplotly/data_utils.py` - Data normalization, index handling

## Common Commands

```bash
# Install
pip install -e .

# Run tests
pytest pytest/ -v

# Run specific test file
pytest pytest/test_geoms.py -v

# Build docs
mkdocs build

# Serve docs locally
mkdocs serve
```

## Dependencies

Core: pandas, plotly, numpy, scikit-learn, scipy, statsmodels

Optional:
- `pip install ggplotly[geo]` - geopandas, shapely
- `pip install ggplotly[network]` - igraph, searoute

## Architecture Notes

1. **Grammar of Graphics**: Uses `+` operator for composition
2. **Immutable**: `+` returns copy, doesn't modify in place
3. **Strategy Pattern**: `trace_builders.py` handles different grouping scenarios
4. **Registry Pattern**: `ScaleRegistry` enforces one scale per aesthetic

## Component Counts

| Component | Count | Location |
|-----------|-------|----------|
| Geoms | 44+ | `ggplotly/geoms/` |
| Stats | 13 | `ggplotly/stats/` |
| Scales | 17+ | `ggplotly/scales/` |
| Themes | 9 | `ggplotly/themes.py` |
| Coords | 4 | `ggplotly/coords/` |
| Datasets | 16 | `ggplotly/data/` |

## Testing Patterns

Tests are in `pytest/` using pytest framework:
- `test_geoms.py` - Geom functionality
- `test_showcase.py` - Integration/showcase tests
- `test_stats_positions_limits.py` - Stats and positions
- `test_facets.py` - Faceting
- `test_scales.py` - Scale functionality

## Available Aesthetics

```python
aes(
    x='column',           # X-axis mapping
    y='column',           # Y-axis mapping
    color='column',       # Line/point color (categorical or continuous)
    fill='column',        # Fill color (bars, areas)
    size='column',        # Point/line size
    shape='column',       # Point shape (categorical)
    alpha=0.5,            # Transparency (0-1)
    group='column',       # Grouping without color
    label='column',       # Text labels
)
```

Use `after_stat()` to reference computed statistics:
```python
aes(y=after_stat('density'))  # Use density instead of count in histograms
aes(y=after_stat('count / count.sum()'))  # Proportions
```

## Common Geoms Reference

| Geom | Use Case |
|------|----------|
| `geom_point()` | Scatter plots |
| `geom_line()` | Line charts |
| `geom_bar()` | Bar charts (stat='count' default) |
| `geom_col()` | Bar charts (stat='identity') |
| `geom_histogram()` | Histograms |
| `geom_boxplot()` | Box plots |
| `geom_violin()` | Violin plots |
| `geom_density()` | Density curves |
| `geom_smooth()` | Trend lines with CI |
| `geom_area()` | Area charts |
| `geom_tile()` | Heatmaps |
| `geom_text()` | Text labels |
| `geom_errorbar()` | Error bars |
| `geom_vline()`, `geom_hline()` | Reference lines |
| `geom_candlestick()` | Financial OHLC |
| `geom_map()` | Choropleth maps |

## Built-in Datasets

```python
from ggplotly import diamonds, mpg, iris, mtcars, economics, msleep, faithfuld
```

Available: diamonds, mpg, iris, mtcars, economics, msleep, faithfuld, seals, txhousing, midwest, and more in `ggplotly/data/`

## Themes

```python
theme_default()    # Default Plotly theme
theme_minimal()    # Clean, minimal
theme_classic()    # Classic ggplot2 style
theme_dark()       # Dark background
theme_ggplot2()    # R ggplot2 style
theme_bw()         # Black and white
theme_nytimes()    # NYT style
theme_bbc()        # BBC News style
```

## Position Adjustments

```python
position_dodge()   # Side by side (grouped bars)
position_jitter()  # Add random noise (overlapping points)
position_stack()   # Stack on top of each other
position_fill()    # Stack normalized to 100%
position_nudge()   # Shift by fixed amount
```

## Coordinate Systems

```python
coord_cartesian(xlim=(0, 10))  # Zoom without clipping data
coord_flip()                    # Swap x and y axes
coord_polar()                   # Polar coordinates (pie charts)
coord_sf()                      # Geographic projections
```

## Index Handling

Pandas index is automatically available:
```python
# Series: index becomes x-axis automatically
ggplot(series, aes(y='value'))  # x uses index

# DataFrame: reference index with 'index'
ggplot(df, aes(x='index', y='col'))

# Named index becomes axis label automatically
```

## Faceting

```python
# Wrap into rows/columns
facet_wrap('category', ncol=3)

# Grid by two variables
facet_grid(rows='var1', cols='var2')

# Free scales
facet_wrap('category', scales='free')  # 'free_x', 'free_y'
```

## Adding New Features

### New Geom
1. Create `ggplotly/geoms/geom_newname.py`
2. Inherit from `GeomBase` in `geom_base.py`
3. Implement `_draw_impl()` method
4. Export in `ggplotly/__init__.py`
5. Add tests in `pytest/test_geoms.py`

### New Stat
1. Create `ggplotly/stats/stat_newname.py`
2. Inherit from `Stat` in `stat_base.py`
3. Implement `compute()` method returning `(data, mapping)` tuple
4. Export in `ggplotly/__init__.py`

### New Scale
1. Create `ggplotly/scales/scale_newname.py`
2. Inherit from `Scale` in `scale_base.py`
3. Implement `apply()` method
4. Export in `ggplotly/__init__.py`

## Tips & Gotchas

1. **String column names**: Always use strings in `aes()`: `aes(x='col')` not `aes(x=col)`

2. **Parentheses for chaining**: Wrap in `()` for multi-line `+` chains:
   ```python
   (ggplot(df, aes(x='x', y='y'))
    + geom_point()
    + theme_minimal())
   ```

3. **geom_bar vs geom_col**:
   - `geom_bar()` counts rows (stat='count')
   - `geom_col()` uses y values directly (stat='identity')

4. **Color vs Fill**:
   - `color` = outline/line color
   - `fill` = interior color (bars, areas, boxes)

5. **Saving plots**:
   ```python
   from ggplotly import ggsave
   ggsave(plot, 'output.html')  # Interactive HTML
   ggsave(plot, 'output.png')   # Static image (requires kaleido)
   ```

6. **Plot sizing**:
   ```python
   from ggplotly import ggsize
   plot + ggsize(width=800, height=600)
   ```

7. **Labels and titles**:
   ```python
   from ggplotly import labs
   plot + labs(title='Title', x='X Label', y='Y Label', color='Legend')
   ```

8. **Multiple geoms**: Layer geoms for complex plots:
   ```python
   (ggplot(df, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth()
    + geom_hline(yintercept=0))
   ```
