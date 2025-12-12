# Geoms

Geoms (geometric objects) are the visual elements that represent your data. ggplotly provides 34 geoms for different visualization types.

## Basic Geoms

### geom_point

Scatter plots for showing individual observations.

```python
ggplot(df, aes(x='x', y='y')) + geom_point()

# With aesthetics
ggplot(df, aes(x='x', y='y', color='category', size='value')) + geom_point()

# Parameters
geom_point(size=5, alpha=0.7, shape='diamond')
```

### geom_line

Line plots connecting points in order of x values.

```python
ggplot(df, aes(x='date', y='value')) + geom_line()

# Multiple lines
ggplot(df, aes(x='date', y='value', color='series')) + geom_line()
```

### geom_path

Like `geom_line`, but connects points in data order (not sorted by x).

```python
ggplot(df, aes(x='x', y='y')) + geom_path()
```

### geom_bar

Bar charts for categorical data.

```python
# Count occurrences
ggplot(df, aes(x='category')) + geom_bar()

# Pre-computed heights
ggplot(df, aes(x='category', y='count')) + geom_bar(stat='identity')

# Stacked bars
ggplot(df, aes(x='category', fill='group')) + geom_bar()
```

### geom_col

Alias for `geom_bar(stat='identity')`.

```python
ggplot(df, aes(x='category', y='value')) + geom_col()
```

## Distribution Geoms

### geom_histogram

```python
ggplot(df, aes(x='value')) + geom_histogram()

# Control bins
geom_histogram(bins=30)
geom_histogram(binwidth=0.5)
```

### geom_density

Kernel density estimation.

```python
ggplot(df, aes(x='value')) + geom_density()

# Filled density
ggplot(df, aes(x='value', fill='group')) + geom_density(alpha=0.5)
```

### geom_boxplot

Box-and-whisker plots.

```python
ggplot(df, aes(x='category', y='value')) + geom_boxplot()
```

### geom_violin

Violin plots showing distribution shape.

```python
ggplot(df, aes(x='category', y='value')) + geom_violin()
```

## Area Geoms

### geom_area

Filled area under a line.

```python
ggplot(df, aes(x='x', y='y')) + geom_area()

# Stacked areas
ggplot(df, aes(x='x', y='y', fill='category')) + geom_area()
```

### geom_ribbon

Area between ymin and ymax.

```python
ggplot(df, aes(x='x', ymin='lower', ymax='upper')) + geom_ribbon(alpha=0.3)
```

## Statistical Geoms

### geom_smooth

Smoothed conditional means with confidence intervals.

```python
ggplot(df, aes(x='x', y='y')) + geom_smooth()

# Linear regression
geom_smooth(method='lm')

# LOESS smoothing
geom_smooth(method='loess')

# Without confidence interval
geom_smooth(se=False)
```

## Text Geoms

### geom_text

Add text labels to points.

```python
ggplot(df, aes(x='x', y='y', label='name')) + geom_text()

# Positioning
geom_text(hjust=0, vjust=1)  # Horizontal/vertical alignment
```

## Reference Lines

### geom_hline / geom_vline / geom_abline

```python
# Horizontal line
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_hline(yintercept=5)

# Vertical line
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_vline(xintercept=3)

# Diagonal line
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_abline(slope=1, intercept=0)
```

## Specialty Geoms

### geom_tile

Heatmaps and tile plots.

```python
ggplot(df, aes(x='x', y='y', fill='value')) + geom_tile()
```

### geom_contour / geom_contour_filled

Contour plots for 3D data on 2D.

```python
ggplot(df, aes(x='x', y='y', z='z')) + geom_contour()
ggplot(df, aes(x='x', y='y', z='z')) + geom_contour_filled()
```

### geom_segment

Line segments between two points.

```python
ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment()
```

### geom_errorbar

Error bars.

```python
ggplot(df, aes(x='x', y='y', ymin='y-err', ymax='y+err')) + geom_errorbar()
```

## Geographic Geoms

### geom_map

Choropleth maps.

```python
ggplot(gdf, aes(fill='value')) + geom_map()
```

### geom_sf

Simple features for geographic data.

```python
ggplot(gdf) + geom_sf()
```

### geom_point_map

Points on a map.

```python
ggplot(df, aes(x='lon', y='lat')) + geom_point_map()
```

## 3D Geoms

### geom_point_3d

3D scatter plots.

```python
ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
```

### geom_surface

3D surface plots.

```python
ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
```

## Financial Geoms

### geom_candlestick

OHLC candlestick charts.

```python
ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick()
```

### geom_ohlc

OHLC bar charts.

```python
ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_ohlc()
```

## Network Geoms

### geom_edgebundle

Edge bundling for network visualization.

```python
ggplot() + geom_edgebundle(nodes=nodes_df, edges=edges_df)
```

## Complete Geom List

| Geom | Description |
|------|-------------|
| `geom_point` | Scatter plots |
| `geom_line` | Line plots (sorted by x) |
| `geom_path` | Path plots (data order) |
| `geom_bar` | Bar charts |
| `geom_col` | Column charts |
| `geom_histogram` | Histograms |
| `geom_boxplot` | Box plots |
| `geom_violin` | Violin plots |
| `geom_density` | Density plots |
| `geom_area` | Area plots |
| `geom_ribbon` | Ribbon plots |
| `geom_smooth` | Smoothed lines |
| `geom_tile` | Heatmaps |
| `geom_text` | Text labels |
| `geom_errorbar` | Error bars |
| `geom_segment` | Line segments |
| `geom_step` | Step plots |
| `geom_rug` | Rug plots |
| `geom_jitter` | Jittered points |
| `geom_vline` | Vertical lines |
| `geom_hline` | Horizontal lines |
| `geom_abline` | Diagonal lines |
| `geom_contour` | Contour lines |
| `geom_contour_filled` | Filled contours |
| `geom_map` | Choropleth maps |
| `geom_sf` | Simple features |
| `geom_point_map` | Map points |
| `geom_range` | Range plots |
| `geom_edgebundle` | Edge bundling |
| `geom_searoute` | Sea routes |
| `geom_point_3d` | 3D points |
| `geom_surface` | 3D surfaces |
| `geom_wireframe` | 3D wireframes |
| `geom_candlestick` | Candlesticks |
| `geom_ohlc` | OHLC charts |
