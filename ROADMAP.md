# GGPLOTLY Roadmap

## Current Status: v0.3.5 (Beta)

---

## Changelog

### [Unreleased]

#### Added
- `stroke` parameter for `geom_point` (marker border width)
- `arrow` and `arrow_size` parameters for `geom_segment`
- `width` parameter for `geom_errorbar` (cap width)
- `parse` parameter for `geom_text` (MathJax/LaTeX support)
- `linewidth` as alias for `size` (ggplot2 3.4+ compatibility)
- Exported position functions: `position_fill`, `position_nudge`, `position_identity`, `position_dodge2`
- Comprehensive MkDocs documentation
- GitHub Actions workflow for automatic docs deployment
- pyproject.toml for modern Python packaging
- 61 new parameter tests with full coverage

#### Changed
- Migrated from setup.py to pyproject.toml

### [0.3.1] - 2024-12-11

#### Added
- Automatic Pandas index handling (`x='index'` or automatic detection)
- `geom_range` for 5-year historical range plots
- `geom_searoute` for maritime shipping routes
- `geom_edgebundle` for network visualization
- `geom_candlestick` and `geom_ohlc` for financial charts
- `geom_point_3d`, `geom_surface`, `geom_wireframe` for 3D plots
- `scale_x_rangeslider` and `scale_x_rangeselector` for interactive time series
- `coord_sf` for map projections
- 15 built-in datasets (mpg, diamonds, iris, mtcars, economics, etc.)
- `guide_legend` and `guide_colorbar` for legend customization
- Facet labellers (`label_both`, `label_value`)

#### Changed
- Improved faceting with consistent colors across panels

### [0.3.0] - 2024-11-01

#### Added
- `geom_contour` and `geom_contour_filled`
- `geom_jitter` and `geom_rug`
- `geom_abline` for diagonal reference lines
- `position_dodge`, `position_stack`, `position_fill`, `position_nudge`
- `stat_summary` and `stat_ecdf`
- `scale_color_gradient` and `scale_fill_viridis_c`
- `theme_bbc` and `theme_nytimes`

### [0.2.0] - 2024-09-01

#### Added
- `geom_map` and `geom_sf` for geographic data
- `coord_polar` for pie charts
- `scale_x_date` and `scale_x_datetime`
- `scale_color_brewer` and `scale_fill_brewer`
- `annotate` function for text and shape annotations

### [0.1.0] - 2024-08-01

#### Added
- Initial release
- Core ggplot grammar: `ggplot`, `aes`, `+` operator
- Basic geoms: point, line, bar, histogram, boxplot, violin, area, ribbon
- Scales: continuous, log10, manual colors
- Themes: minimal, classic, dark, ggplot2
- Faceting: `facet_wrap`, `facet_grid`
- Labels: `labs`, `ggtitle`
- Utilities: `ggsave`, `ggsize`

---

## Roadmap to v1.0.0

### Must-Have (Required for 1.0)

| Item | Type | Description | Status |
|------|------|-------------|--------|
| `geom_rect` | Geom | Rectangles for highlighting regions | TODO |
| `geom_label` | Geom | Text labels with background box | TODO |
| `scale_x_reverse` | Scale | Reversed x-axis | TODO |
| `scale_y_reverse` | Scale | Reversed y-axis | TODO |
| `coord_fixed` | Coord | Fixed aspect ratio (essential for maps) | TODO |
| Parameter audit | Quality | Review all geom params vs ggplot2 | In Progress |

### Nice-to-Have (Target 1.0, can defer)

| Item | Type | Description | Status |
|------|------|-------------|--------|
| `geom_polygon` | Geom | Arbitrary polygons | TODO |
| `geom_dotplot` | Geom | Dot plots | TODO |
| `geom_freqpoly` | Geom | Frequency polygons | TODO |
| `geom_spoke` | Geom | Line segments by angle | TODO |
| `geom_curve` | Geom | Curved line segments | TODO |
| `scale_alpha` | Scale | Alpha/transparency scaling | TODO |
| `scale_linetype` | Scale | Linetype scaling | TODO |
| `scale_x_sqrt` | Scale | Square root x-axis | TODO |
| `scale_y_sqrt` | Scale | Square root y-axis | TODO |
| `scale_color_viridis_c` | Scale | Viridis for color aesthetic | TODO |
| `scale_color_distiller` | Scale | ColorBrewer continuous for color | TODO |
| `coord_trans` | Coord | Transformed coordinates | TODO |
| `stat_boxplot` | Stat | Boxplot statistics | TODO |
| `stat_unique` | Stat | Remove duplicates | TODO |

---

## Future Roadmap (Post 1.0)

### v1.1 - Enhanced Interactivity
- [ ] Animation slider (Plotly animation frames)
- [ ] Dropdown selectors for data filtering
- [ ] Linked brushing between plots
- [ ] Custom hover templates via parameter

### v1.2 - Advanced Geoms
- [ ] `geom_density_2d` - 2D density estimation
- [ ] `geom_hex` - Hexagonal binning
- [ ] `geom_quantile` - Quantile regression lines
- [ ] `geom_crossbar` - Crossbar error bars

### v1.3 - Statistical Extensions
- [ ] `stat_bin_2d` - 2D binning
- [ ] `stat_ellipse` - Confidence ellipses
- [ ] `stat_function` enhancements
- [ ] Better integration with statsmodels

### v1.4 - Theming & Polish
- [ ] `element_*` functions for fine-grained theming
- [ ] More theme presets (economist, fivethirtyeight, etc.)
- [ ] Better default color palettes
- [ ] Improved legend positioning

---

## Completed Features

### Geoms (44+)
- Basic: `geom_point`, `geom_line`, `geom_path`, `geom_bar`, `geom_col`, `geom_area`, `geom_ribbon`
- Distribution: `geom_histogram`, `geom_density`, `geom_boxplot`, `geom_violin`, `geom_qq`
- Statistical: `geom_smooth`, `geom_errorbar`, `geom_pointrange`, `geom_linerange`
- Annotation: `geom_text`, `geom_hline`, `geom_vline`, `geom_abline`, `geom_segment`
- Specialized: `geom_tile`, `geom_raster`, `geom_contour`, `geom_contour_filled`
- Financial: `geom_candlestick`, `geom_ohlc`, `geom_waterfall`
- 3D: `geom_point_3d`, `geom_surface`, `geom_wireframe`
- Geographic: `geom_map`, `geom_sf`, `geom_searoute`
- Network: `geom_edgebundle`, `geom_sankey`
- Other: `geom_step`, `geom_jitter`, `geom_rug`, `geom_range`

### Stats (13)
`stat_identity`, `stat_count`, `stat_bin`, `stat_density`, `stat_smooth`, `stat_summary`, `stat_ecdf`, `stat_function`, `stat_qq`, `stat_stl`, `stat_spoke`, `stat_bin_2d`, `stat_contour`

### Scales (17+)
- Continuous: `scale_x_continuous`, `scale_y_continuous`, `scale_x_log10`, `scale_y_log10`
- Date/Time: `scale_x_date`, `scale_x_datetime`
- Color: `scale_color_manual`, `scale_color_gradient`, `scale_color_brewer`, `scale_fill_*` variants
- Viridis: `scale_fill_viridis_c`, `scale_fill_viridis_d`
- Interactive: `scale_x_rangeslider`, `scale_x_rangeselector`

### Coords (4)
`coord_cartesian`, `coord_flip`, `coord_polar`, `coord_sf`

### Positions (7)
`position_identity`, `position_dodge`, `position_dodge2`, `position_stack`, `position_fill`, `position_jitter`, `position_nudge`

### Themes (9)
`theme_default`, `theme_minimal`, `theme_classic`, `theme_dark`, `theme_ggplot2`, `theme_bw`, `theme_void`, `theme_bbc`, `theme_nytimes`

### Other
- Faceting: `facet_wrap`, `facet_grid` with labellers
- Guides: `guides`, `guide_legend`, `guide_colorbar`
- Labels: `labs`, `ggtitle`, `xlab`, `ylab`
- Utilities: `ggsave`, `ggsize`, `annotate`
- 16 built-in datasets

---

## Contributing

When implementing new features:
1. Follow ggplot2 conventions (see [CLAUDE.md](CLAUDE.md))
2. Add tests covering all 4 categories (basic, edge cases, integration, visual regression)
3. Update this roadmap when features are completed
4. Add examples to `examples/` directory

## Links

- [ggplot2 Reference](https://ggplot2.tidyverse.org/reference/)
- [Plotly Python](https://plotly.com/python/)
- [GitHub Repository](https://github.com/bbcho/ggplotly)
