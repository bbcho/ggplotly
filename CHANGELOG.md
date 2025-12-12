# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive MkDocs documentation
- GitHub Actions workflow for automatic docs deployment
- pyproject.toml for modern Python packaging

### Changed
- Migrated from setup.py to pyproject.toml

## [0.3.1] - 2024-12-11

### Added
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

### Changed
- Improved faceting with consistent colors across panels

## [0.3.0] - 2024-11-01

### Added
- `geom_contour` and `geom_contour_filled`
- `geom_jitter` and `geom_rug`
- `geom_abline` for diagonal reference lines
- `position_dodge`, `position_stack`, `position_fill`, `position_nudge`
- `stat_summary` and `stat_ecdf`
- `scale_color_gradient` and `scale_fill_viridis_c`
- `theme_bbc` and `theme_nytimes`

## [0.2.0] - 2024-09-01

### Added
- `geom_map` and `geom_sf` for geographic data
- `coord_polar` for pie charts
- `scale_x_date` and `scale_x_datetime`
- `scale_color_brewer` and `scale_fill_brewer`
- `annotate` function for text and shape annotations

## [0.1.0] - 2024-08-01

### Added
- Initial release
- Core ggplot grammar: `ggplot`, `aes`, `+` operator
- Basic geoms: point, line, bar, histogram, boxplot, violin, area, ribbon
- Scales: continuous, log10, manual colors
- Themes: minimal, classic, dark, ggplot2
- Faceting: `facet_wrap`, `facet_grid`
- Labels: `labs`, `ggtitle`
- Utilities: `ggsave`, `ggsize`

[Unreleased]: https://github.com/bbcho/ggplotly/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/bbcho/ggplotly/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/bbcho/ggplotly/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/bbcho/ggplotly/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/bbcho/ggplotly/releases/tag/v0.1.0
