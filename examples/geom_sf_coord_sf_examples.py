# %% [markdown]
"""
# geom_sf and coord_sf Examples

This notebook demonstrates the use of `geom_sf` and `coord_sf` in ggplotly,
which provide ggplot2-style geographic visualization capabilities.

- `geom_sf` (alias for `geom_map`) renders simple features (sf) objects
- `coord_sf` controls map projections, bounds, and coordinate systems
"""

# %% Setup
import pandas as pd
import numpy as np
from ggplotly import (
    ggplot, aes, geom_sf, geom_map, geom_point, coord_sf,
    theme_dark, theme_minimal, theme_classic, labs, ggsize
)

# %% [markdown]
"""
## Example 1: Basic USA Map with coord_sf Bounds

Using `coord_sf` to set geographic bounds for the continental US.
"""

# %% Example 1: USA map with bounds
cities_usa = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'lon': [-74.006, -118.244, -87.630, -95.370, -112.074],
    'lat': [40.713, 34.052, 41.878, 29.760, 33.448],
    'population': [8.3, 3.9, 2.7, 2.3, 1.6]
})

example_01 = (
    ggplot(cities_usa, aes(x='lon', y='lat'))
    + geom_map(map_type='usa')
    + geom_point(aes(size='population'), color='red', alpha=0.7)
    + coord_sf(xlim=(-125, -65), ylim=(24, 50))
    + labs(title='Major US Cities', subtitle='Continental US bounds with coord_sf')
    + theme_dark()
)
example_01.show()

# %% [markdown]
"""
## Example 2: World Map with Robinson Projection

The Robinson projection is popular for world maps as it balances
distortion of area, shape, and distance.
"""

# %% Example 2: World map with Robinson projection
world_cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney', 'São Paulo', 'Cairo'],
    'lon': [-74.006, -0.128, 139.692, 151.209, -46.634, 31.236],
    'lat': [40.713, 51.507, 35.690, -33.868, -23.550, 30.044],
    'region': ['Americas', 'Europe', 'Asia', 'Oceania', 'Americas', 'Africa']
})

example_02 = (
    ggplot(world_cities, aes(x='lon', y='lat', color='region'))
    + geom_map(map_type='world')
    + geom_point(size=10)
    + coord_sf(crs='robinson')
    + labs(title='World Cities', subtitle='Robinson Projection')
    + theme_minimal()
)
example_02.show()

# %% [markdown]
"""
## Example 3: Orthographic (Globe) Projection

The orthographic projection shows Earth as it appears from space,
centered on a specific point.
"""

# %% Example 3: Globe projection
example_03 = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='yellow', size=8)
    + coord_sf(crs='orthographic')
    + labs(title='Earth from Space', subtitle='Orthographic Projection')
    + theme_dark()
)
example_03.show()

# %% [markdown]
"""
## Example 4: Mercator Projection

The Mercator projection preserves angles (conformal) but greatly
distorts area near the poles.
"""

# %% Example 4: Mercator projection
example_04 = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='#ff6b6b', size=10)
    + coord_sf(crs='mercator')
    + labs(title='World Cities', subtitle='Mercator Projection')
    + theme_classic()
)
example_04.show()

# %% [markdown]
"""
## Example 5: Natural Earth Projection

Natural Earth is a compromise projection that's neither conformal
nor equal-area, but looks natural and pleasing.
"""

# %% Example 5: Natural Earth projection
example_05 = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(aes(color='region'), size=12)
    + coord_sf(crs='natural earth')
    + labs(title='World Cities by Region', subtitle='Natural Earth Projection')
    + theme_minimal()
    + ggsize(width=900, height=500)
)
example_05.show()

# %% [markdown]
"""
## Example 6: Zooming into Europe

Using `coord_sf` bounds to focus on a specific region.
"""

# %% Example 6: Europe zoom
european_cities = pd.DataFrame({
    'city': ['London', 'Paris', 'Berlin', 'Rome', 'Madrid', 'Amsterdam', 'Vienna', 'Prague'],
    'lon': [-0.128, 2.352, 13.405, 12.496, -3.704, 4.900, 16.373, 14.418],
    'lat': [51.507, 48.857, 52.520, 41.903, 40.417, 52.370, 48.208, 50.076],
    'population': [8.98, 2.16, 3.65, 2.87, 3.22, 0.87, 1.90, 1.31]
})

example_06 = (
    ggplot(european_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(aes(size='population'), color='#e74c3c', alpha=0.8)
    + coord_sf(xlim=(-15, 30), ylim=(35, 60))
    + labs(title='Major European Cities', subtitle='Zoomed view with coord_sf bounds')
    + theme_minimal()
)
example_06.show()

# %% [markdown]
"""
## Example 7: US States Choropleth with coord_sf

Combining choropleth maps with coord_sf for projection control.
"""

# %% Example 7: US choropleth
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'value': [39.5, 29.0, 21.5, 19.5, 13.0, 12.7, 11.8, 10.7, 10.4, 10.0]
})

example_07 = (
    ggplot(state_data, aes(map_id='state', fill='value'))
    + geom_map(map_type='usa')
    + coord_sf(crs='albers usa')
    + labs(title='US States by Population (millions)', subtitle='Albers USA Projection')
    + theme_dark()
)
example_07.show()

# %% [markdown]
"""
## Example 8: geom_sf with GeoJSON Data

Using `geom_sf` (alias for `geom_map`) with GeoJSON data.
"""

# %% Example 8: GeoJSON polygons
nyc_boroughs_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "manhattan",
            "properties": {"name": "Manhattan"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.047, 40.684], [-74.004, 40.684], [-73.907, 40.797],
                    [-73.934, 40.882], [-74.020, 40.780], [-74.047, 40.684]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "brooklyn",
            "properties": {"name": "Brooklyn"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.042, 40.570], [-73.855, 40.570], [-73.855, 40.739],
                    [-73.962, 40.710], [-74.042, 40.651], [-74.042, 40.570]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "queens",
            "properties": {"name": "Queens"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-73.962, 40.710], [-73.700, 40.605], [-73.700, 40.800],
                    [-73.794, 40.800], [-73.794, 40.750], [-73.962, 40.710]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "bronx",
            "properties": {"name": "Bronx"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-73.934, 40.785], [-73.765, 40.785], [-73.765, 40.915],
                    [-73.910, 40.915], [-73.934, 40.785]
                ]]
            }
        },
        {
            "type": "Feature",
            "id": "staten_island",
            "properties": {"name": "Staten Island"},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-74.255, 40.496], [-74.052, 40.496], [-74.052, 40.649],
                    [-74.255, 40.649], [-74.255, 40.496]
                ]]
            }
        }
    ]
}

borough_data = pd.DataFrame({
    'id': ['manhattan', 'brooklyn', 'queens', 'bronx', 'staten_island'],
    'population': [1.63, 2.56, 2.27, 1.42, 0.47]
})

example_08 = (
    ggplot(borough_data, aes(fill='population'))
    + geom_sf(geojson=nyc_boroughs_geojson, featureidkey='id')
    + coord_sf(xlim=(-74.3, -73.6), ylim=(40.45, 40.95))
    + labs(title='NYC Boroughs by Population (millions)')
    + theme_minimal()
)
example_08.show()

# %% [markdown]
"""
## Example 9: Line Features with geom_sf

GeoJSON LineString geometries for routes/paths.
"""

# %% Example 9: Line features
routes_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "route1",
            "properties": {"name": "Route 1: NYC to LA"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-74.006, 40.713],  # NYC
                    [-87.630, 41.878],  # Chicago
                    [-104.990, 39.739],  # Denver
                    [-118.244, 34.052]  # LA
                ]
            }
        },
        {
            "type": "Feature",
            "id": "route2",
            "properties": {"name": "Route 2: NYC to Miami"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-74.006, 40.713],  # NYC
                    [-77.037, 38.907],  # DC
                    [-80.191, 25.762]  # Miami
                ]
            }
        },
        {
            "type": "Feature",
            "id": "route3",
            "properties": {"name": "Route 3: LA to Seattle"},
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [-118.244, 34.052],  # LA
                    [-122.419, 37.775],  # SF
                    [-122.676, 45.524],  # Portland
                    [-122.332, 47.606]  # Seattle
                ]
            }
        }
    ]
}

example_09 = (
    ggplot(pd.DataFrame({'x': []}))
    + geom_sf(geojson=routes_geojson, color='#e74c3c', linewidth=2)
    + coord_sf(xlim=(-130, -65), ylim=(20, 55))
    + labs(title='US Travel Routes')
    + theme_dark()
)
example_09.show()

# %% [markdown]
"""
## Example 10: Point Features with geom_sf

GeoJSON Point geometries.
"""

# %% Example 10: Point features
airports_geojson = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "id": "JFK", "properties": {"name": "JFK", "passengers": 62}, "geometry": {"type": "Point", "coordinates": [-73.778, 40.640]}},
        {"type": "Feature", "id": "LAX", "properties": {"name": "LAX", "passengers": 88}, "geometry": {"type": "Point", "coordinates": [-118.408, 33.943]}},
        {"type": "Feature", "id": "ORD", "properties": {"name": "ORD", "passengers": 83}, "geometry": {"type": "Point", "coordinates": [-87.904, 41.978]}},
        {"type": "Feature", "id": "DFW", "properties": {"name": "DFW", "passengers": 73}, "geometry": {"type": "Point", "coordinates": [-97.038, 32.897]}},
        {"type": "Feature", "id": "DEN", "properties": {"name": "DEN", "passengers": 69}, "geometry": {"type": "Point", "coordinates": [-104.673, 39.856]}},
        {"type": "Feature", "id": "ATL", "properties": {"name": "ATL", "passengers": 110}, "geometry": {"type": "Point", "coordinates": [-84.428, 33.637]}},
        {"type": "Feature", "id": "SFO", "properties": {"name": "SFO", "passengers": 57}, "geometry": {"type": "Point", "coordinates": [-122.379, 37.619]}},
        {"type": "Feature", "id": "SEA", "properties": {"name": "SEA", "passengers": 50}, "geometry": {"type": "Point", "coordinates": [-122.309, 47.449]}},
        {"type": "Feature", "id": "MIA", "properties": {"name": "MIA", "passengers": 46}, "geometry": {"type": "Point", "coordinates": [-80.291, 25.795]}},
        {"type": "Feature", "id": "BOS", "properties": {"name": "BOS", "passengers": 42}, "geometry": {"type": "Point", "coordinates": [-71.010, 42.366]}},
    ]
}

example_10 = (
    ggplot(pd.DataFrame({'x': []}))
    + geom_sf(geojson=airports_geojson, color='#3498db', size=12)
    + coord_sf(xlim=(-130, -65), ylim=(22, 52))
    + labs(title='Major US Airports')
    + theme_dark()
)
example_10.show()

# %% [markdown]
"""
## Example 11: Graticule Labels with coord_sf

Using `label_graticule` to show latitude/longitude grid lines.
"""

# %% Example 11: Graticule labels
example_11 = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='yellow', size=8)
    + coord_sf(crs='natural earth', label_graticule='NESW')
    + labs(title='World Map with Graticules', subtitle='Grid lines enabled')
    + theme_minimal()
)
example_11.show()

# %% [markdown]
"""
## Example 12: Multiple Projections Comparison

Comparing how different projections affect the appearance of the same data.
"""

# %% Example 12a: Equirectangular
example_12a = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='red', size=8)
    + coord_sf(crs='equirectangular')
    + labs(title='Equirectangular (Plate Carrée)')
    + theme_minimal()
)
example_12a.show()

# %% Example 12b: Mollweide
example_12b = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='red', size=8)
    + coord_sf(crs='mollweide')
    + labs(title='Mollweide (Equal-Area)')
    + theme_minimal()
)
example_12b.show()

# %% Example 12c: Winkel Tripel
example_12c = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='red', size=8)
    + coord_sf(crs='winkel tripel')
    + labs(title='Winkel Tripel')
    + theme_minimal()
)
example_12c.show()

# %% [markdown]
"""
## Example 13: Asia Focus with coord_sf

Zooming into Asia using geographic bounds.
"""

# %% Example 13: Asia zoom
asian_cities = pd.DataFrame({
    'city': ['Tokyo', 'Beijing', 'Seoul', 'Shanghai', 'Mumbai', 'Bangkok', 'Singapore', 'Jakarta'],
    'lon': [139.69, 116.41, 126.98, 121.47, 72.88, 100.50, 103.82, 106.85],
    'lat': [35.69, 39.90, 37.57, 31.23, 19.08, 13.76, 1.35, -6.21],
    'population': [13.96, 21.54, 9.77, 24.28, 20.41, 10.54, 5.69, 10.56]
})

example_13 = (
    ggplot(asian_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(aes(size='population'), color='#e74c3c', alpha=0.7)
    + coord_sf(xlim=(60, 150), ylim=(-15, 55))
    + labs(title='Major Asian Cities', subtitle='Population in millions')
    + theme_dark()
)
example_13.show()

# %% [markdown]
"""
## Example 14: South America Focus

Zooming into South America.
"""

# %% Example 14: South America
south_american_cities = pd.DataFrame({
    'city': ['São Paulo', 'Buenos Aires', 'Lima', 'Bogotá', 'Rio de Janeiro', 'Santiago'],
    'lon': [-46.63, -58.38, -77.03, -74.07, -43.17, -70.65],
    'lat': [-23.55, -34.60, -12.05, 4.71, -22.91, -33.45],
    'population': [12.33, 15.00, 10.72, 10.57, 6.75, 6.77]
})

example_14 = (
    ggplot(south_american_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(aes(size='population'), color='#2ecc71', alpha=0.8)
    + coord_sf(xlim=(-85, -30), ylim=(-60, 15))
    + labs(title='Major South American Cities')
    + theme_minimal()
)
example_14.show()

# %% [markdown]
"""
## Example 15: No Expansion Mode

Using `expand=False` for exact bounds without padding.
"""

# %% Example 15: No expansion
example_15 = (
    ggplot(cities_usa, aes(x='lon', y='lat'))
    + geom_map(map_type='usa')
    + geom_point(color='red', size=10)
    + coord_sf(xlim=(-125, -65), ylim=(25, 50), expand=False)
    + labs(title='US Cities (Exact Bounds)', subtitle='expand=False removes padding')
    + theme_classic()
)
example_15.show()

# %% [markdown]
"""
## Example 16: Categorical Choropleth with geom_sf

Using categorical fill values with GeoJSON.
"""

# %% Example 16: Categorical fill
region_data = pd.DataFrame({
    'id': ['manhattan', 'brooklyn', 'queens', 'bronx', 'staten_island'],
    'borough': ['Manhattan', 'Brooklyn', 'Queens', 'Bronx', 'Staten Island'],
    'category': ['High Density', 'High Density', 'Medium Density', 'Medium Density', 'Low Density']
})

example_16 = (
    ggplot(region_data, aes(fill='category'))
    + geom_sf(geojson=nyc_boroughs_geojson, featureidkey='id')
    + coord_sf(xlim=(-74.3, -73.6), ylim=(40.45, 40.95))
    + labs(title='NYC Boroughs by Density Category')
    + theme_dark()
)
example_16.show()

# %% [markdown]
"""
## Example 17: Combining geom_sf with geom_point

Layering GeoJSON polygons with point data.
"""

# %% Example 17: Combined layers
landmarks = pd.DataFrame({
    'name': ['Empire State', 'Statue of Liberty', 'Central Park', 'Brooklyn Bridge', 'Yankee Stadium'],
    'lon': [-73.9857, -74.0445, -73.9654, -73.9969, -73.9262],
    'lat': [40.7484, 40.6892, 40.7829, 40.7061, 40.8296]
})

example_17 = (
    ggplot(borough_data, aes(fill='population'))
    + geom_sf(geojson=nyc_boroughs_geojson, featureidkey='id', alpha=0.7)
    + geom_point(data=landmarks, mapping=aes(x='lon', y='lat'), color='yellow', size=10)
    + coord_sf(xlim=(-74.3, -73.6), ylim=(40.45, 40.95))
    + labs(title='NYC Landmarks and Borough Population')
    + theme_dark()
)
example_17.show()

# %% [markdown]
"""
## Example 18: Azimuthal Equal Area Projection

Good for showing polar regions with minimal distortion.
"""

# %% Example 18: Azimuthal Equal Area
example_18 = (
    ggplot(world_cities, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='cyan', size=8)
    + coord_sf(crs='azimuthal equal area')
    + labs(title='World Map', subtitle='Azimuthal Equal Area Projection')
    + theme_dark()
)
example_18.show()

# %% [markdown]
"""
## Example 19: Conic Projections

Good for mid-latitude regions like the continental US.
"""

# %% Example 19: Conic Equal Area
example_19 = (
    ggplot(cities_usa, aes(x='lon', y='lat'))
    + geom_map(map_type='world')
    + geom_point(color='orange', size=10)
    + coord_sf(crs='conic equal area', xlim=(-130, -60), ylim=(20, 55))
    + labs(title='US Cities', subtitle='Conic Equal Area Projection')
    + theme_minimal()
)
example_19.show()

# %% [markdown]
"""
## Example 20: Full Featured Example

Combining multiple features: choropleth, points, projection, and styling.
"""

# %% Example 20: Full featured
# More state data
full_state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI'],
    'gdp': [3598, 1987, 1111, 1893, 803, 892, 702, 637, 591, 543,
            634, 557, 632, 387, 596, 381, 381, 336, 425, 348]
})

# State capitals
capitals = pd.DataFrame({
    'capital': ['Sacramento', 'Austin', 'Tallahassee', 'Albany', 'Harrisburg',
                'Springfield', 'Columbus', 'Atlanta', 'Raleigh', 'Lansing'],
    'lon': [-121.47, -97.74, -84.28, -73.76, -76.88,
            -89.65, -82.99, -84.39, -78.64, -84.55],
    'lat': [38.58, 30.27, 30.44, 42.65, 40.27,
            39.80, 39.96, 33.75, 35.78, 42.73]
})

example_20 = (
    ggplot(full_state_data, aes(map_id='state', fill='gdp'))
    + geom_map(map_type='usa', palette='Viridis')
    + geom_point(data=capitals, mapping=aes(x='lon', y='lat'),
                 color='white', size=6, alpha=0.9)
    + coord_sf(crs='albers usa')
    + labs(
        title='US State GDP with Capital Cities',
        subtitle='GDP in billions USD (2023 estimates)'
    )
    + theme_dark()
    + ggsize(width=1000, height=600)
)
example_20.show()

# %% [markdown]
"""
## Summary

This notebook demonstrated:

1. **geom_sf** - Alias for geom_map, renders simple features (sf) objects
   - Supports GeoJSON polygons, lines, and points
   - Auto-detects geometry types
   - Works with categorical and continuous fill

2. **coord_sf** - Coordinate system for geographic data
   - `xlim`, `ylim` - Set longitude/latitude bounds
   - `crs` - Choose map projection (mercator, robinson, orthographic, etc.)
   - `expand` - Control padding around bounds
   - `label_graticule` - Show lat/lon grid lines

3. **Projections available**:
   - mercator, natural earth, albers usa, orthographic
   - robinson, mollweide, winkel tripel, equirectangular
   - azimuthal equal area, conic equal area, stereographic
   - And more...

These tools provide ggplot2-style geographic visualization in Python!
"""

# %%
