# TODO

- [ ] go thru geoms one by one to make sure I've replicated all of the parameters from ggplot
- [X] Add plotly charts that don't exist in ggplot2 like 3D scatter plots
  - [X] sliders and range controls (scale_x_rangeslider, scale_x_rangeselector)
  - [X] 3D plots (geom_point_3d, geom_surface, geom_wireframe)
  - [X] waterfall charts (geom_waterfall)

## Base

- [X] deal with datetime index and Series


## Plotly Functionality I want to port over

- [X] range slider
- [X] range selector
- [ ] slider (animation slider)
- [ ] drop down

## Missing ggplot2 Functions

### Geoms

- [ ] `geom_polygon` - Polygons
- [ ] `geom_rect` - Rectangles
- [ ] `geom_label` - Text labels with background
- [ ] `geom_dotplot` - Dot plots
- [ ] `geom_freqpoly` - Frequency polygons
- [X] `geom_qq` - Q-Q plots (implemented)
- [ ] `geom_spoke` - Line segments parameterized by angle
- [ ] `geom_curve` - Curved line segments

### Stats

- [ ] `stat_boxplot` - Boxplot statistics
- [X] `stat_qq` - Q-Q plot statistics (implemented)
- [ ] `stat_unique` - Remove duplicates

### Scales

- [ ] `scale_alpha` - Alpha/transparency scaling
- [ ] `scale_linetype` - Linetype scaling
- [ ] `scale_x_reverse` / `scale_y_reverse` - Reversed axes
- [ ] `scale_x_sqrt` / `scale_y_sqrt` - Square root transformation
- [ ] `scale_color_viridis_c` - Viridis for color (currently only fill)
- [ ] `scale_color_distiller` - ColorBrewer continuous

### Coordinates

- [ ] `coord_fixed` - Fixed aspect ratio
- [ ] `coord_trans` - Transformed coordinates
- [X] `coord_sf` - Spatial coordinates (implemented)

### Positions

- [X] `position_fill` - Stack and normalize to 100% (implemented, needs export)
- [X] `position_nudge` - Nudge points by fixed amount (implemented, needs export)
- [X] `position_identity` - No adjustment (implemented, needs export)

### Guides

- [X] `guides` - Customize legends/colorbars (implemented)
- [X] `guide_legend` - Legend customization (implemented)
- [X] `guide_colorbar` - Colorbar customization (implemented)
