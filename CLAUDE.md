# CLAUDE.md - Project Context for AI Assistants

## Development Philosophy

**IMPORTANT**: This library aims to faithfully replicate R's ggplot2 API in Python.

When contributing or modifying code:
1. **Follow ggplot2 conventions** - Match R's ggplot2 function names, parameter names, and behavior as closely as possible
2. **Consult ggplot2 documentation** - When implementing existing ggplot2 features, reference https://ggplot2.tidyverse.org/reference/
3. **Extrapolate for new features** - For functionality not in ggplot2 (e.g., `geom_candlestick`, `geom_stl`, `geom_sankey`), follow ggplot2 naming conventions and design patterns:
   - Use `geom_*` prefix for geometric objects
   - Use `stat_*` prefix for statistical transformations
   - Use `scale_*_*` pattern for scales (e.g., `scale_x_log10`, `scale_color_manual`)
   - Accept `aes()` mappings consistently
   - Support `data=` parameter override in geoms
4. **Pythonic adaptations** - Only deviate from ggplot2 when Python requires it (e.g., strings for column names in `aes()`)

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

# Run example notebooks as tests (catches real-world usage bugs)
pytest --nbmake examples/*.ipynb

# Run all tests including notebooks
pytest pytest/ -v && pytest --nbmake examples/*.ipynb

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

## Testing Requirements

**When adding new features or modifying existing code, tests MUST include all four categories:**

### 1. Basic Functionality Tests
Verify the feature works as expected in isolation:
```python
def test_stroke_with_value(self):
    """Test stroke parameter sets marker border width."""
    df = pd.DataFrame({"x": [1, 2], "y": [1, 2]})
    plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2)
    fig = plot.draw()
    assert fig.data[0].marker.line.width == 2
```

### 2. Edge Case Tests
Test boundary conditions, empty data, type variations:
```python
def test_stroke_with_large_value(self):
    """Test stroke with unusually large value."""
    # ...

def test_stroke_empty_dataframe(self):
    """Test stroke with empty DataFrame doesn't crash."""
    df = pd.DataFrame({"x": [], "y": []})
    plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2)
    fig = plot.draw()  # Should not raise

def test_stroke_with_float_value(self):
    """Test stroke accepts float values."""
    # ...
```

### 3. Integration Tests (Faceting & Color Mappings)
Test with faceting, color aesthetics, and multiple geoms:
```python
def test_stroke_with_facet_wrap(self):
    """Test stroke parameter works with faceting."""
    df = pd.DataFrame({
        "x": [1, 2, 3, 4], "y": [1, 2, 3, 4],
        "cat": ["A", "A", "B", "B"]
    })
    plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2) + facet_wrap("cat")
    fig = plot.draw()
    # Verify stroke applied across all facets
    for trace in fig.data:
        if hasattr(trace, "marker") and trace.marker:
            assert trace.marker.line.width == 2

def test_stroke_with_color_aesthetic(self):
    """Test stroke works when color aesthetic is mapped."""
    df = pd.DataFrame({
        "x": [1, 2, 3], "y": [1, 2, 3],
        "cat": ["A", "B", "C"]
    })
    plot = ggplot(df, aes(x="x", y="y", color="cat")) + geom_point(stroke=1.5)
    fig = plot.draw()
    # Each category trace should have stroke
    for trace in fig.data:
        assert trace.marker.line.width == 1.5
```

### 4. Visual Regression Tests
Capture and verify figure structure/properties:
```python
class TestVisualRegression:
    """Visual regression tests that verify figure structure."""

    def get_figure_signature(self, fig):
        """Extract key properties from figure for comparison."""
        signature = {"num_traces": len(fig.data), "traces": []}
        for trace in fig.data:
            trace_sig = {"type": trace.type, "mode": getattr(trace, "mode", None)}
            if hasattr(trace, "marker") and trace.marker:
                trace_sig["marker"] = {
                    "size": getattr(trace.marker, "size", None),
                    "line_width": getattr(trace.marker.line, "width", None) if trace.marker.line else None,
                }
            signature["traces"].append(trace_sig)
        return signature

    def test_stroke_visual_signature(self):
        """Test that stroke produces expected visual signature."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2.5)
        fig = plot.draw()
        sig = self.get_figure_signature(fig)
        assert sig["num_traces"] == 1
        assert sig["traces"][0]["type"] == "scatter"
        assert sig["traces"][0]["marker"]["line_width"] == 2.5
```

### Test Naming Convention
- `test_<feature>_default` - Test default behavior
- `test_<feature>_with_value` - Test with explicit value
- `test_<feature>_with_<aesthetic>` - Test with specific aesthetic
- `test_<feature>_empty_dataframe` - Test empty data handling
- `test_<feature>_with_facet_wrap` - Test with faceting
- `test_<feature>_visual_signature` - Visual regression test

### Reference Test File
See `pytest/test_new_parameters.py` for comprehensive examples of all four test categories.

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

## Scales

```python
# Axis transforms
scale_x_log10()                    # Log scale
scale_x_continuous(limits=(0,100)) # Set range
scale_x_date(date_labels='%Y-%m')  # Date formatting

# Manual colors
scale_color_manual(['red', 'blue', 'green'])
scale_fill_manual({'A': 'red', 'B': 'blue'})  # Dict mapping

# Color gradients
scale_color_gradient(low='white', high='red')
scale_fill_viridis_c()             # Viridis colorscale

# ColorBrewer palettes
scale_color_brewer(palette='Set1')
scale_fill_brewer(palette='Blues')

# Interactive
scale_x_rangeslider()              # Add range slider
scale_x_rangeselector()            # Add range buttons
```

## Stats Reference

| Stat | Purpose | Used By |
|------|---------|---------|
| `stat_identity` | No transformation | `geom_col`, `geom_point` |
| `stat_count` | Count observations | `geom_bar` |
| `stat_bin` | Bin data | `geom_histogram` |
| `stat_density` | Kernel density | `geom_density` |
| `stat_smooth` | Smoothed line + CI | `geom_smooth` |
| `stat_boxplot` | Boxplot stats | `geom_boxplot` |
| `stat_ecdf` | Empirical CDF | - |
| `stat_summary` | Summary statistics | - |
| `stat_function` | Apply function | - |
| `stat_qq` | Q-Q plot points | `geom_qq` |

## Specialized Features

### Financial Charts
```python
# Candlestick (requires open, high, low, close columns)
geom_candlestick(aes(x='date', open='open', high='high', low='low', close='close'))
geom_ohlc()      # OHLC bars
geom_waterfall() # Waterfall charts
```

### 3D Plots
```python
geom_point_3d(aes(x='x', y='y', z='z'))
geom_surface()   # 3D surface
geom_wireframe() # Wireframe surface
```

### Geographic (requires geopandas)
```python
geom_map(aes(fill='value'))  # Choropleth
geom_sf()                     # Simple features
coord_sf(projection='...')    # Map projections
```

### Network (requires igraph)
```python
geom_edgebundle()  # Edge bundling
geom_sankey()      # Sankey diagrams
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

## Geom Implementation Patterns

### Default Parameters

Geom parameters follow a three-level inheritance pattern:

```python
class geom_example(Geom):
    # Subclass defaults - override base class defaults
    default_params = {"size": 2, "alpha": 0.8}
```

Parameter resolution order (later takes precedence):
1. **Base class defaults** (always applied): `{"na_rm": False, "show_legend": True}`
2. **Subclass `default_params`**: Class-specific defaults like `{"size": 2}`
3. **User-provided params**: Explicit values passed to constructor

**Important**: Do NOT include `na_rm` or `show_legend` in subclass `default_params` - they are automatically inherited from the base class.

#### Parameter Aliases

The base class handles these ggplot2 compatibility aliases:
- `linewidth` → `size` (ggplot2 3.4+ compatibility)
- `colour` → `color` (British spelling)
- `showlegend` → `show_legend` (Plotly convention)

Explicit user params take precedence: if both `linewidth=10` and `size=5` are passed, `size=5` wins.

### The `before_add()` Hook

The `before_add()` method is called when a geom is added to a plot via the `+` operator. Use it to:
- Create sub-layers (e.g., `geom_ribbon` creates multiple `geom_line` layers)
- Transform the geom before it's added to the plot
- Return additional layers to be added

```python
class geom_ribbon(Geom):
    def before_add(self):
        # Create additional layers for ribbon edges
        color = self.params.get("color", None)

        # Create line layers for ymin and ymax edges
        min_line = geom_line(mapping=aes(x=self.mapping['x'], y=self.mapping['ymin']),
                           color=color)
        max_line = geom_line(mapping=aes(x=self.mapping['x'], y=self.mapping['ymax']),
                           color=color)

        # Return list of additional layers
        return [min_line, max_line]
```

**When to use `before_add()`:**
- Composite geoms that consist of multiple sub-geoms
- Geoms that need to generate additional visual elements
- When the geom itself shouldn't render but spawns other geoms

**Implementation notes:**
- Return `None` (or omit return) if no additional layers needed
- Returned layers are added to the plot after the original geom
- The method is called by `ggplot.__add__()` during composition

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

9. **Access Plotly figure**: Get underlying figure for custom modifications:
   ```python
   fig = plot.draw()  # Returns plotly.graph_objects.Figure
   fig.update_layout(...)  # Standard Plotly customization
   ```

10. **Per-geom data**: Override plot data for specific geoms:
    ```python
    (ggplot(df1, aes(x='x', y='y'))
     + geom_point()
     + geom_line(data=df2))  # Different data for this geom
    ```

## Key Example Notebooks

Located in `examples/`:
- `ggplotly_master_examples.ipynb` - Comprehensive examples
- `Examples.ipynb` - Core functionality
- `view_all.ipynb` - Gallery of all features
- `prices.ipynb` - Financial data
- `maps.ipynb` - Geographic mapping
- `EdgeBundling.ipynb` - Network visualization

## Differences from R's ggplot2

| ggplot2 (R) | ggplotly (Python) |
|-------------|-------------------|
| `aes(x = col)` | `aes(x='col')` (strings required) |
| `%+%` for data replacement | Not supported |
| `stat_bin(geom="line")` | Use `geom_line(stat=stat_bin)` |
| `theme(text = element_text(...))` | `theme(text=element_text(...))` |
| Automatic printing | Use `.show()` or Jupyter auto-display |

## Debugging

```python
# Check what data a geom receives
plot = ggplot(df, aes(x='x', y='y')) + geom_point()
fig = plot.draw()  # Renders and returns figure

# Inspect Plotly traces
for trace in fig.data:
    print(trace)

# Check aesthetic mappings
print(plot.mapping)  # Shows aes mappings

# Verify data normalization
from ggplotly.data_utils import normalize_data
normalized_df, mapping = normalize_data(df, aes(x='x', y='y'))
```

## Code Auditing Best Practices

**Always test before flagging issues.** When auditing code for bugs or missing features:

1. **Don't grep-and-flag** - Pattern matching on code structure without understanding behavior leads to false positives

2. **Run the code** - A 30-second `python3 -c "..."` test catches most false positives:
   ```python
   # Instead of assuming geom_bar fill is broken because it's commented out:
   python3 -c "
   from ggplotly import ggplot, aes, geom_bar
   import pandas as pd
   df = pd.DataFrame({'x': ['A', 'B', 'C']})
   fig = (ggplot(df, aes(x='x')) + geom_bar(fill='red')).draw()
   print(fig.data[0].marker.color)  # Actually works!
   "
   ```

3. **Trace cross-file interactions** - Code in one file may have fallback logic in another (e.g., `geom_bar` relies on `geom_base._apply_color_targets` fallback)

4. **Ask "why" before flagging** - If something looks wrong, investigate whether it's intentional design (e.g., `stat_edgebundle` doesn't inherit from `Stat` because it has a different API contract)

5. **Check existing tests** - If tests pass for a "broken" feature, the feature probably works

6. **Test diverse input types** - Don't just test the happy path. Test edge cases like:
   - Dict input vs DataFrame vs Series
   - Empty data, single row, large data
   - Different column types (numeric, categorical, datetime)
   - Missing values, NaN handling

   Example: The test suite only used DataFrames, so dict input to `ggplot()` was broken and went undetected.
