# TODO

- [ ] go thru geoms one by one to make sure I've replicated all of the parameters from ggplot
- [ ] Add plotly charts that don't exist in ggplot2 like 3D scatter plots
  - [ ] sliders and range controls
  - [ ] 3D plots
  - [ ] waterfall charts

## Base

- [ ] deal with datetime index and Series


## Plotly Functionality I want to port over

- [X] range slider
- [X] range selector
- [ ] slider
- [ ] drop down

## Missing ggplot2 Functions

### Geoms

- [ ] `geom_polygon` - Polygons
- [ ] `geom_rect` - Rectangles
- [ ] `geom_label` - Text labels with background
- [ ] `geom_dotplot` - Dot plots
- [ ] `geom_freqpoly` - Frequency polygons
- [ ] `geom_qq` - Q-Q plots
- [ ] `geom_spoke` - Line segments parameterized by angle
- [ ] `geom_curve` - Curved line segments

### Stats

- [ ] `stat_boxplot` - Boxplot statistics
- [ ] `stat_qq` - Q-Q plot statistics
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
- [ ] `coord_sf` - Spatial coordinates

### Positions

- [ ] `position_fill` - Stack and normalize to 100%
- [ ] `position_nudge` - Nudge points by fixed amount
- [ ] `position_identity` - No adjustment

### Guides

- [ ] `guides` - Customize legends/colorbars
- [ ] `guide_legend` - Legend customization
- [ ] `guide_colorbar` - Colorbar customization
