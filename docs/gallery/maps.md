# Geographic Maps

ggplotly supports geographic visualizations including choropleths, point maps, and multiple map projections.

## Choropleth Maps

### US State Choropleth

```python
import pandas as pd
from ggplotly import *

# State data
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0]
})

# Get state boundaries
states = map_data('state')

(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues')
 + labs(title='US States by Population'))
```

### World Choropleth

```python
country_data = pd.DataFrame({
    'country': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'IND', 'FRA', 'BRA'],
    'gdp': [25.5, 18.3, 4.2, 4.1, 3.1, 3.4, 2.8, 1.9]
})

countries = map_data('world')

(ggplot(country_data, aes(map_id='country', fill='gdp'))
 + geom_map(map=countries, map_type='world', palette='Viridis')
 + labs(title='GDP by Country (Trillions USD)'))
```

### Map Palettes

Available palettes for `geom_map`:

- **Sequential**: `Blues`, `Greens`, `Reds`, `Oranges`, `Purples`, `Greys`, `YlOrRd`, `YlGnBu`, `BuPu`, `RdPu`
- **Viridis family**: `Viridis`, `Plasma`, `Inferno`, `Magma`, `Cividis`
- **Diverging**: `RdBu`, `RdYlGn`, `BrBG`, `PiYG`, `Spectral`

## Point Maps

### Adding Points to Maps

```python
# Cities data
cities = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    'pop': [8.3, 3.9, 2.7, 2.3, 1.6]
})

(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues')
 + geom_point(cities, aes(x='lon', y='lat', size='pop'), color='red')
 + labs(title='US Population: States and Major Cities'))
```

### Points on World Map

```python
cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney'],
    'lon': [-74.006, -0.128, 139.692, 151.209],
    'lat': [40.713, 51.507, 35.690, -33.868]
})

(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='red', size=10)
 + labs(title='Major World Cities'))
```

## Map Projections

Use `coord_sf()` to apply different map projections:

### Robinson Projection

A compromise projection often used for world maps:

```python
(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='red', size=10)
 + coord_sf(crs='robinson')
 + labs(title='Robinson Projection'))
```

### Orthographic (Globe)

Shows Earth as seen from space:

```python
(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='yellow', size=8)
 + coord_sf(crs='orthographic')
 + theme_dark()
 + labs(title='Orthographic Projection'))
```

### Mercator

Standard web map projection (preserves angles):

```python
(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='red', size=8)
 + coord_sf(crs='mercator')
 + labs(title='Mercator Projection'))
```

### Available Projections

| Projection | Best For |
|------------|----------|
| `equirectangular` | Default, simple lat/lon |
| `mercator` | Navigation, web maps |
| `robinson` | World thematic maps |
| `orthographic` | Globe visualization |
| `natural earth` | Balanced world view |
| `albers usa` | US-specific maps |

## Map Styling

### Custom Map Colors

```python
airports_df = pd.DataFrame({
    'lon': [-122.4, -73.8],
    'lat': [37.8, 40.6]
})

(ggplot(airports_df, aes(x='lon', y='lat'))
 + geom_map(
     map_type='usa',
     landcolor='#333333',
     oceancolor='#111111',
     bgcolor='black',
     countrycolor='#666666',
     subunitcolor='#444444'  # State borders
 )
 + geom_point(color='#00ff00', size=10)
 + theme_dark())
```

### Map Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `map_type` | 'usa' | 'usa', 'world', 'europe', 'asia', etc. |
| `palette` | 'Blues' | Color palette for choropleth |
| `landcolor` | 'rgb(243, 243, 243)' | Land fill color |
| `oceancolor` | 'rgb(255, 255, 255)' | Ocean fill color |
| `bgcolor` | 'white' | Background color |
| `countrycolor` | 'rgb(217, 217, 217)' | Country border color |
| `subunitcolor` | 'rgb(217, 217, 217)' | State/province border color |

## Theme Integration

Themes automatically style maps appropriately:

### Dark Theme

```python
(ggplot(airports_df, aes(x='lon', y='lat'))
 + geom_map(map_type='usa')
 + geom_point(color='cyan', size=10)
 + theme_dark()  # Applies dark map styling
 + labs(title='Airports'))
```

### Other Themes

```python
# NYTimes style
(ggplot(...) + geom_map() + theme_nytimes())

# BBC style
(ggplot(...) + geom_map() + theme_bbc())

# Minimal
(ggplot(...) + geom_map() + theme_minimal())
```

## Map Data Sources

### Built-in Map Data

```python
# US states
states = map_data('state')

# World countries
world = map_data('world')

# US counties
counties = map_data('county')
```

### Using GeoDataFrames

For custom geographic data, use GeoPandas:

```python
import geopandas as gpd

# Load shapefile
gdf = gpd.read_file('my_regions.shp')

# Plot with ggplotly
(ggplot(gdf, aes(fill='value'))
 + geom_sf()
 + scale_fill_viridis_c())
```

## Combining with Other Geoms

### Flight Routes

```python
airports = pd.DataFrame({
    'name': ['SFO', 'JFK', 'ORD'],
    'lon': [-122.4, -73.8, -87.6],
    'lat': [37.8, 40.6, 41.9]
})

flights = pd.DataFrame({
    'from_lon': [-122.4, -73.8],
    'from_lat': [37.8, 40.6],
    'to_lon': [-73.8, -87.6],
    'to_lat': [40.6, 41.9]
})

(ggplot()
 + geom_map(map_type='usa')
 + geom_segment(
     data=flights,
     mapping=aes(x='from_lon', y='from_lat', xend='to_lon', yend='to_lat'),
     color='red', size=1
 )
 + geom_point(
     data=airports,
     mapping=aes(x='lon', y='lat'),
     color='blue', size=10
 )
 + theme_minimal())
```

### Heatmaps on Maps

Combine `geom_tile` with geographic data for spatial heatmaps:

```python
# Grid data
grid = pd.DataFrame({
    'lon': np.repeat(np.linspace(-125, -65, 20), 15),
    'lat': np.tile(np.linspace(25, 50, 15), 20),
    'value': np.random.rand(300)
})

(ggplot(grid, aes(x='lon', y='lat', fill='value'))
 + geom_map(map_type='usa', alpha=0.3)
 + geom_tile(alpha=0.6)
 + scale_fill_viridis_c()
 + labs(title='Spatial Heatmap'))
```
