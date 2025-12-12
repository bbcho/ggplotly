# Coordinate Systems

Coordinate systems control how x and y positions are mapped to the plot.

## coord_cartesian

The default Cartesian coordinate system. Use it to zoom without clipping data.

```python
# Zoom to a region (data outside is still used for calculations)
ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 10), ylim=(0, 5))
```

!!! note "xlim/ylim vs coord_cartesian"
    `xlim()` and `ylim()` filter the data before plotting. `coord_cartesian()` zooms the view without removing data points. This matters for statistical calculations like `geom_smooth`.

## coord_flip

Flip x and y axes.

```python
# Horizontal bar chart
ggplot(df, aes(x='category', y='value')) + geom_bar(stat='identity') + coord_flip()

# Horizontal boxplot
ggplot(df, aes(x='category', y='value')) + geom_boxplot() + coord_flip()
```

## coord_polar

Polar coordinates for pie charts and radial plots.

```python
# Pie chart
ggplot(df, aes(x='', y='value', fill='category')) + \
    geom_bar(stat='identity', width=1) + \
    coord_polar(theta='y')

# Rose/wind diagram
ggplot(df, aes(x='direction', y='count', fill='speed')) + \
    geom_bar(stat='identity') + \
    coord_polar()
```

### Parameters

```python
coord_polar(
    theta='x',      # Variable mapped to angle ('x' or 'y')
    start=0,        # Starting angle in radians
    direction=1     # 1 = clockwise, -1 = counter-clockwise
)
```

## coord_sf

For geographic/spatial data with proper map projections.

```python
import geopandas as gpd

# Load geographic data
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Plot with projection
ggplot(world) + geom_sf() + coord_sf(crs='EPSG:4326')
```

### Projections

```python
# Web Mercator (Google Maps style)
coord_sf(crs='mercator')

# Albers USA (good for US maps)
coord_sf(crs='albers usa')

# Globe view
coord_sf(crs='orthographic')

# Natural Earth
coord_sf(crs='natural earth')

# Robinson
coord_sf(crs='robinson')
```

### Setting Bounds

```python
# Zoom to region
coord_sf(xlim=(-130, -60), ylim=(20, 55))  # Continental US
```

## Coordinate Reference

| Function | Description |
|----------|-------------|
| `coord_cartesian` | Default Cartesian, zoom without clipping |
| `coord_flip` | Flip x and y axes |
| `coord_polar` | Polar coordinates |
| `coord_sf` | Geographic projections |
