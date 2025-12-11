# GGPLOTLY

A data visualization library for Python that combines the grammar of graphics from ggplot2 with the interactivity of Plotly.

## Installation

```bash
pip install ggplotly
```

## Usage

```python
from ggplotly import *
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5],
    'group': ['A', 'A', 'B', 'B', 'B']
})

# Simple scatter plot
ggplot(df, aes(x='x', y='y')) + geom_point()

# With color mapping and theme
ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + theme_minimal()

# Faceted plot
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('group')
```

## ggplot2 Function Coverage

### Geoms (34)

| Function | Description |
|----------|-------------|
| `geom_point` | Scatter plots |
| `geom_line` | Line plots (sorted by x) |
| `geom_path` | Path plots (unsorted) |
| `geom_bar` | Bar charts |
| `geom_col` | Column charts (pre-computed heights) |
| `geom_histogram` | Histograms |
| `geom_boxplot` | Box-and-whisker plots |
| `geom_violin` | Violin plots |
| `geom_density` | Density plots |
| `geom_area` | Filled area plots |
| `geom_ribbon` | Ribbons with ymin/ymax |
| `geom_smooth` | Smoothed lines (LOESS, linear) |
| `geom_tile` | Rectangular tiles/heatmaps |
| `geom_text` | Text labels |
| `geom_errorbar` | Error bars |
| `geom_segment` | Line segments |
| `geom_step` | Step plots |
| `geom_rug` | Rug plots |
| `geom_jitter` | Jittered points |
| `geom_vline` | Vertical reference lines |
| `geom_hline` | Horizontal reference lines |
| `geom_abline` | Diagonal lines (slope/intercept) |
| `geom_contour` | Contour lines |
| `geom_contour_filled` | Filled contours |
| `geom_map` | Choropleth maps |
| `geom_point_map` | Points on maps |
| `geom_range` | Range plots (min/max/avg) |
| `geom_edgebundle` | Edge bundling for networks |
| `geom_sf` | Simple features (geographic) |
| `geom_searoute` | Maritime shipping routes |
| `geom_point_3d` | 3D scatter plots |
| `geom_surface` | 3D surface plots |
| `geom_wireframe` | 3D wireframe plots |
| `geom_candlestick` | Candlestick charts (financial) |
| `geom_ohlc` | OHLC charts (financial) |

### Stats (7)

| Function | Description |
|----------|-------------|
| `stat_identity` | No transformation |
| `stat_count` | Count observations |
| `stat_bin` | Bin data |
| `stat_density` | Kernel density estimation |
| `stat_ecdf` | Empirical CDF |
| `stat_smooth` | Smoothing with CI |
| `stat_summary` | Summary statistics |

### Scales (17)

| Function | Description |
|----------|-------------|
| `scale_x_continuous` | Continuous x-axis |
| `scale_y_continuous` | Continuous y-axis |
| `scale_x_log10` | Log10 x-axis |
| `scale_y_log10` | Log10 y-axis |
| `scale_x_date` | Date x-axis |
| `scale_x_datetime` | DateTime x-axis |
| `scale_x_rangeslider` | Interactive range slider for zooming |
| `scale_x_rangeselector` | Range selector buttons for time series |
| `scale_color_manual` | Manual color mapping |
| `scale_color_gradient` | Continuous color gradient |
| `scale_color_brewer` | ColorBrewer palettes |
| `scale_fill_manual` | Manual fill mapping |
| `scale_fill_gradient` | Continuous fill gradient |
| `scale_fill_brewer` | ColorBrewer fill palettes |
| `scale_fill_viridis_c` | Viridis color palette |
| `scale_shape_manual` | Manual shape mapping |
| `scale_size` | Size scaling |

### Coordinates (4)

| Function | Description |
|----------|-------------|
| `coord_cartesian` | Cartesian coordinates |
| `coord_flip` | Flip x and y axes |
| `coord_polar` | Polar coordinates |
| `coord_sf` | Spatial/geographic coordinates |

### Facets (2)

| Function | Description |
|----------|-------------|
| `facet_wrap` | Wrap facets into rows/columns |
| `facet_grid` | 2D facet grid |

### Themes (9)

| Function | Description |
|----------|-------------|
| `theme_default` | Default theme |
| `theme_minimal` | Minimal theme |
| `theme_classic` | Classic ggplot2 theme |
| `theme_dark` | Dark theme |
| `theme_ggplot2` | R's ggplot2 default |
| `theme_nytimes` | New York Times style |
| `theme_bbc` | BBC News style |
| `theme_custom` | Custom theme builder |
| `theme` | Theme modification |

### Position Adjustments (6)

| Function | Description |
|----------|-------------|
| `position_dodge` | Dodge overlapping objects |
| `position_jitter` | Add random noise |
| `position_stack` | Stack objects |
| `position_fill` | Stack and normalize to 100% |
| `position_nudge` | Nudge points by fixed amount |
| `position_identity` | No adjustment (identity) |

### Guides & Labels (7)

| Function | Description |
|----------|-------------|
| `labs` | Set plot labels |
| `ggtitle` | Set title |
| `annotate` | Add annotations |
| `xlim` / `ylim` / `lims` | Set axis limits |
| `guides` | Control legend/colorbar display |
| `guide_legend` | Configure legend appearance |
| `guide_colorbar` | Configure colorbar appearance |

### Utilities (2)

| Function | Description |
|----------|-------------|
| `ggsave` | Save plots to file |
| `ggsize` | Set plot dimensions |

## Total: ~97 ggplot2-equivalent functions
