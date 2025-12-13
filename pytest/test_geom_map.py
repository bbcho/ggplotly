# pytest/test_geom_map.py
"""
Tests for geom_map, geom_sf, and map_data.
Tests cover base map layers, choropleths, geo context detection, and GeoJSON support.
"""

import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest
from ggplotly import (
    aes,
    facet_wrap,
    geom_map,
    geom_point,
    ggplot,
    map_data,
)
from ggplotly.themes import theme_classic, theme_dark

# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def us_state_data():
    """Create sample data for US states."""
    np.random.seed(42)
    states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI']
    return pd.DataFrame({
        'state': states,
        'population': np.random.randint(1000000, 40000000, len(states)),
        'region': ['West', 'South', 'South', 'East', 'East'] * 4
    })


@pytest.fixture
def world_data():
    """Create sample data for world countries."""
    np.random.seed(42)
    countries = ['USA', 'CAN', 'MEX', 'BRA', 'ARG', 'GBR', 'FRA', 'DEU', 'ITA', 'ESP',
                 'CHN', 'JPN', 'IND', 'AUS', 'RUS']
    return pd.DataFrame({
        'country': countries,
        'gdp': np.random.randint(100, 20000, len(countries)),
        'continent': ['NA', 'NA', 'NA', 'SA', 'SA', 'EU', 'EU', 'EU', 'EU', 'EU',
                      'AS', 'AS', 'AS', 'OC', 'EU']
    })


@pytest.fixture
def point_location_data():
    """Create sample data for point locations on maps."""
    np.random.seed(42)
    return pd.DataFrame({
        'city': ['Los Angeles', 'New York', 'Chicago', 'Houston', 'Phoenix'],
        'lat': [34.05, 40.71, 41.88, 29.76, 33.45],
        'lon': [-118.24, -74.01, -87.63, -95.37, -112.07],
        'population': [3900000, 8300000, 2700000, 2300000, 1600000]
    })


@pytest.fixture
def simple_polygon_geojson():
    """Create a simple GeoJSON with two polygons."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "region1",
                "properties": {"name": "Region 1"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-74.0, 40.7],
                        [-74.0, 41.0],
                        [-73.7, 41.0],
                        [-73.7, 40.7],
                        [-74.0, 40.7]
                    ]]
                }
            },
            {
                "type": "Feature",
                "id": "region2",
                "properties": {"name": "Region 2"},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-73.7, 40.7],
                        [-73.7, 41.0],
                        [-73.4, 41.0],
                        [-73.4, 40.7],
                        [-73.7, 40.7]
                    ]]
                }
            }
        ]
    }


@pytest.fixture
def line_geojson():
    """Create a simple GeoJSON with lines."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "route1",
                "properties": {"name": "Route 1"},
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [-74.0, 40.7],
                        [-73.5, 41.0],
                        [-73.0, 40.8]
                    ]
                }
            }
        ]
    }


@pytest.fixture
def point_geojson():
    """Create a simple GeoJSON with points."""
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "id": "city1",
                "properties": {"name": "NYC"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-74.0, 40.7]
                }
            },
            {
                "type": "Feature",
                "id": "city2",
                "properties": {"name": "Boston"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [-71.0, 42.4]
                }
            }
        ]
    }


# =============================================================================
# map_data() function tests
# =============================================================================

class TestMapData:
    """Tests for map_data function."""

    def test_map_data_state_returns_dataframe(self):
        """Test getting US state map data returns correct structure."""
        states = map_data('state')
        assert isinstance(states, pd.DataFrame)
        assert 'id' in states.columns
        assert 'name' in states.columns
        # Should have 51 entries (50 states + DC)
        assert len(states) == 51

    def test_map_data_usa_alias(self):
        """Test 'usa' alias for state map data."""
        states = map_data('usa')
        assert isinstance(states, pd.DataFrame)
        assert len(states) == 51

    def test_map_data_world_returns_dataframe(self):
        """Test getting world map data returns correct structure."""
        countries = map_data('world')
        assert isinstance(countries, pd.DataFrame)
        assert 'id' in countries.columns
        assert 'name' in countries.columns
        assert len(countries) > 40

    def test_map_data_invalid_raises_error(self):
        """Test invalid map name raises error."""
        with pytest.raises(ValueError):
            map_data('invalid_map')

    def test_map_data_state_codes_are_valid(self):
        """Test that state codes are valid US states."""
        states = map_data('state')
        assert 'CA' in states['id'].values
        assert 'NY' in states['id'].values
        assert 'TX' in states['id'].values

    def test_map_data_world_codes_are_iso3(self):
        """Test that country codes are valid ISO-3."""
        countries = map_data('world')
        # All codes should be 3 characters
        assert all(len(code) == 3 for code in countries['id'])
        # Check some known countries
        assert 'USA' in countries['id'].values
        assert 'GBR' in countries['id'].values
        assert 'CHN' in countries['id'].values


# =============================================================================
# Base Map Layer tests
# =============================================================================

class TestGeomMapBaseLayer:
    """Tests for using geom_map as a base map layer."""

    def test_base_map_usa_creates_geo_context(self):
        """Test that geom_map creates a geo context for other geoms."""
        cities = pd.DataFrame({
            'name': ['NYC', 'LA', 'Chicago'],
            'lon': [-74.0060, -118.2437, -87.6298],
            'lat': [40.7128, 34.0522, 41.8781],
        })

        fig = (
            ggplot(cities, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        # Should have 2 traces: the invisible geo marker and the points
        assert len(fig.data) == 2
        # First trace is the invisible marker from geom_map
        assert fig.data[0].type == 'scattergeo'
        assert fig.data[0].name == '_geo_context'
        # Second trace is the points using Scattergeo (not Scatter)
        assert fig.data[1].type == 'scattergeo'

    def test_base_map_world_sets_scope(self):
        """Test base map with world scope."""
        cities = pd.DataFrame({
            'name': ['London', 'Tokyo', 'Sydney'],
            'lon': [-0.1278, 139.6917, 151.2093],
            'lat': [51.5074, 35.6895, -33.8688],
        })

        fig = (
            ggplot(cities, aes(x='lon', y='lat'))
            + geom_map(map_type='world')
            + geom_point()
        ).draw()

        assert fig.layout.geo.scope == 'world'
        assert fig.layout.geo.projection.type == 'natural earth'

    def test_base_map_custom_colors(self):
        """Test base map with custom styling."""
        cities = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(cities, aes(x='lon', y='lat'))
            + geom_map(
                map_type='usa',
                landcolor='rgb(40, 40, 40)',
                oceancolor='rgb(17, 17, 17)',
                bgcolor='rgb(0, 0, 0)',
            )
            + geom_point()
        ).draw()

        assert fig.layout.geo.landcolor == 'rgb(40, 40, 40)'
        assert fig.layout.geo.oceancolor == 'rgb(17, 17, 17)'
        assert fig.layout.geo.bgcolor == 'rgb(0, 0, 0)'

    def test_base_map_custom_projection(self):
        """Test base map with custom projection."""
        cities = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(cities, aes(x='lon', y='lat'))
            + geom_map(map_type='world', projection='orthographic')
            + geom_point()
        ).draw()

        assert fig.layout.geo.projection.type == 'orthographic'


# =============================================================================
# Choropleth tests
# =============================================================================

class TestGeomMapChoropleth:
    """Tests for choropleth functionality."""

    def test_choropleth_requires_map_id(self):
        """Test that choropleth mode requires map_id aesthetic."""
        data = pd.DataFrame({
            'value': [100, 200, 300],
        })

        with pytest.raises(ValueError, match="map_id"):
            fig = (
                ggplot(data, aes(fill='value'))
                + geom_map()
            ).draw()

    def test_choropleth_with_fill_creates_choropleth_trace(self):
        """Test choropleth with numeric fill creates correct trace type."""
        data = pd.DataFrame({
            'state': ['CA', 'TX', 'NY'],
            'value': [100, 200, 300],
        })

        fig = (
            ggplot(data, aes(map_id='state', fill='value'))
            + geom_map(map_type='usa')
        ).draw()

        assert len(fig.data) == 1
        assert fig.data[0].type == 'choropleth'
        assert fig.data[0].locationmode == 'USA-states'

    def test_choropleth_with_map_data(self, us_state_data):
        """Test choropleth with map_data."""
        states = map_data('state')

        fig = (
            ggplot(us_state_data, aes(map_id='state', fill='population'))
            + geom_map(map=states)
        ).draw()

        assert fig.data[0].type == 'choropleth'

    def test_choropleth_world_uses_iso3(self, world_data):
        """Test world choropleth uses ISO-3 location mode."""
        fig = (
            ggplot(world_data, aes(map_id='country', fill='gdp'))
            + geom_map(map_type='world')
        ).draw()

        assert fig.data[0].type == 'choropleth'
        assert fig.data[0].locationmode == 'ISO-3'
        assert fig.layout.geo.scope == 'world'

    def test_choropleth_categorical_fill(self, us_state_data):
        """Test map with categorical fill."""
        states = map_data('state')

        fig = (
            ggplot(us_state_data, aes(map_id='state', fill='region'))
            + geom_map(map=states)
        ).draw()

        assert isinstance(fig, Figure)


# =============================================================================
# Geo Context Detection tests
# =============================================================================

class TestGeomPointGeoDetection:
    """Tests for geom_point auto-detecting geo context."""

    def test_geom_point_uses_scatter_without_geo_context(self):
        """Test that geom_point uses regular Scatter without geo context."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        fig = (
            ggplot(data, aes(x='x', y='y'))
            + geom_point()
        ).draw()

        assert fig.data[0].type == 'scatter'

    def test_geom_point_detects_choropleth_context(self):
        """Test that geom_point detects choropleth and uses Scattergeo."""
        choropleth_data = pd.DataFrame({
            'state': ['CA', 'TX', 'NY'],
            'value': [100, 200, 300],
        })
        points_data = pd.DataFrame({
            'lon': [-118.24, -95.37, -74.01],
            'lat': [34.05, 29.76, 40.71],
        })

        fig = (
            ggplot(choropleth_data, aes(map_id='state', fill='value'))
            + geom_map(map_type='usa')
            + geom_point(data=points_data, mapping=aes(x='lon', y='lat'))
        ).draw()

        # First trace is choropleth
        assert fig.data[0].type == 'choropleth'
        # Second trace should be scattergeo (detected geo context)
        assert fig.data[1].type == 'scattergeo'

    def test_geom_point_detects_base_map_context(self):
        """Test that geom_point detects base map and uses Scattergeo."""
        data = pd.DataFrame({
            'lon': [-118.24, -95.37, -74.01],
            'lat': [34.05, 29.76, 40.71],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        # First trace is the invisible marker from base map
        assert fig.data[0].type == 'scattergeo'
        # Second trace should be scattergeo with actual points
        assert fig.data[1].type == 'scattergeo'
        assert len(fig.data[1].lat) == 3


# =============================================================================
# Theme tests
# =============================================================================

class TestGeomMapWithThemes:
    """Tests for geom_map with different themes."""

    def test_base_map_with_theme_dark(self):
        """Test that theme_dark applies dark geo styling to base map."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_dark()
        ).draw()

        assert fig.layout.geo.bgcolor == 'rgb(17, 17, 17)'
        assert fig.layout.geo.landcolor == 'rgb(40, 40, 40)'

    def test_choropleth_with_theme_dark(self):
        """Test that theme_dark applies to choropleth maps."""
        data = pd.DataFrame({
            'state': ['CA', 'TX', 'NY'],
            'value': [100, 200, 300],
        })

        fig = (
            ggplot(data, aes(map_id='state', fill='value'))
            + geom_map(map_type='usa')
            + theme_dark()
        ).draw()

        assert fig.layout.geo.bgcolor == 'rgb(17, 17, 17)'

    def test_base_map_with_theme_classic(self):
        """Test theme_classic on base map."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + theme_classic()
        ).draw()

        assert fig.layout.geo.bgcolor == 'white'


# =============================================================================
# Points on Maps tests
# =============================================================================

class TestGeomMapWithPoints:
    """Tests for geom_map + geom_point combination."""

    def test_basic_point_map(self, point_location_data):
        """Test basic points on a map using geom_map + geom_point."""
        fig = (
            ggplot(point_location_data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        assert isinstance(fig, Figure)
        # geom_point should auto-detect geo context and use Scattergeo
        assert any(t.type == 'scattergeo' for t in fig.data)

    def test_point_map_with_size(self, point_location_data):
        """Test points on map with size aesthetic."""
        fig = (
            ggplot(point_location_data, aes(x='lon', y='lat', size='population'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        assert isinstance(fig, Figure)

    def test_point_map_with_color(self, point_location_data):
        """Test points on map with color."""
        fig = (
            ggplot(point_location_data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point(color='red')
        ).draw()

        assert isinstance(fig, Figure)


# =============================================================================
# Faceting tests
# =============================================================================

class TestGeomMapFaceting:
    """Tests for faceted maps."""

    def test_faceted_us_map(self, us_state_data):
        """Test faceted US map."""
        states = map_data('state')
        fig = (
            ggplot(us_state_data, aes(map_id='state', fill='population'))
            + geom_map(map=states)
            + facet_wrap('region')
        ).draw()

        assert isinstance(fig, Figure)

    def test_faceted_map_with_ncol(self, us_state_data):
        """Test faceted map with specified columns."""
        states = map_data('state')
        fig = (
            ggplot(us_state_data, aes(map_id='state', fill='population'))
            + geom_map(map=states)
            + facet_wrap('region', ncol=2)
        ).draw()

        assert isinstance(fig, Figure)


# =============================================================================
# GeoJSON tests
# =============================================================================

class TestGeomMapGeoJSON:
    """Tests for GeoJSON/sf-like functionality in geom_map."""

    def test_geojson_polygon_basic(self, simple_polygon_geojson):
        """Test basic GeoJSON polygon rendering."""
        data = pd.DataFrame({
            'id': ['region1', 'region2'],
            'value': [100, 200],
        })

        fig = (
            ggplot(data, aes(fill='value'))
            + geom_map(geojson=simple_polygon_geojson, featureidkey='id')
        ).draw()

        assert len(fig.data) >= 1
        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')

    def test_geojson_polygon_no_fill(self, simple_polygon_geojson):
        """Test GeoJSON polygon without fill (uniform color)."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=simple_polygon_geojson)
        ).draw()

        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')
        assert fig.data[0].showscale is False

    def test_geojson_lines(self, line_geojson):
        """Test GeoJSON line rendering."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=line_geojson)
        ).draw()

        assert len(fig.data) >= 1
        assert fig.data[0].type in ('scattermap', 'scattermapbox')
        assert fig.data[0].mode == 'lines'

    def test_geojson_points(self, point_geojson):
        """Test GeoJSON point rendering."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=point_geojson)
        ).draw()

        assert len(fig.data) >= 1
        assert fig.data[0].type in ('scattermap', 'scattermapbox')
        assert fig.data[0].mode == 'markers'

    def test_geojson_auto_center_calculation(self, simple_polygon_geojson):
        """Test that map center is auto-calculated from GeoJSON bounds."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=simple_polygon_geojson)
        ).draw()

        if hasattr(fig.layout, 'map') and fig.layout.map.center:
            assert fig.layout.map.center.lat is not None
            assert fig.layout.map.center.lon is not None
        else:
            assert fig.layout.mapbox.center.lat is not None
            assert fig.layout.mapbox.center.lon is not None


# =============================================================================
# GeoDataFrame tests
# =============================================================================

class TestGeomMapGeoDataFrame:
    """Tests for GeoDataFrame support (requires geopandas)."""

    @pytest.fixture
    def skip_if_no_geopandas(self):
        """Skip test if geopandas is not installed."""
        try:
            import geopandas
        except ImportError:
            pytest.skip("geopandas not installed")

    def test_geodataframe_auto_detection(self, skip_if_no_geopandas):
        """Test that GeoDataFrame is auto-detected."""
        import geopandas as gpd
        from shapely.geometry import Polygon

        gdf = gpd.GeoDataFrame({
            'name': ['Region A', 'Region B'],
            'value': [100, 200],
            'geometry': [
                Polygon([(-74, 40.7), (-74, 41), (-73.7, 41), (-73.7, 40.7)]),
                Polygon([(-73.7, 40.7), (-73.7, 41), (-73.4, 41), (-73.4, 40.7)]),
            ]
        }, crs="EPSG:4326")

        fig = (
            ggplot(gdf, aes(fill='value'))
            + geom_map()
        ).draw()

        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')


# =============================================================================
# Edge cases tests
# =============================================================================

class TestGeomMapEdgeCases:
    """Tests for edge cases and error handling."""

    def test_missing_lon_lat_uses_regular_scatter(self):
        """Test that without geo context, regular scatter is used."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        fig = (
            ggplot(data, aes(x='x', y='y'))
            + geom_point()
        ).draw()

        assert fig.data[0].type == 'scatter'

    def test_empty_data_base_map(self):
        """Test base map with empty data."""
        data = pd.DataFrame({
            'lon': [],
            'lat': [],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
        ).draw()

        assert fig.layout.geo.scope == 'usa'

    def test_geom_map_without_mapping_creates_context(self):
        """Test geom_map with no mapping creates base map context."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        fig = (
            ggplot(data, aes(x='x', y='y'))
            + geom_map(map_type='usa')
        ).draw()

        assert len(fig.data) == 1
        assert fig.data[0].type == 'scattergeo'
        assert fig.data[0].name == '_geo_context'

    def test_multiple_geom_maps_last_one_wins(self):
        """Test behavior with multiple geom_maps (last one wins for geo layout)."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_map(map_type='world')
            + geom_point()
        ).draw()

        assert fig.layout.geo.scope == 'world'

    def test_map_empty_data(self):
        """Test map with empty dataframe."""
        empty_df = pd.DataFrame({'state': [], 'value': []})
        states = map_data('state')

        fig = (
            ggplot(empty_df, aes(map_id='state', fill='value'))
            + geom_map(map=states)
        ).draw()

        assert isinstance(fig, Figure)

    def test_map_single_state(self):
        """Test map with single state."""
        df = pd.DataFrame({
            'state': ['CA'],
            'value': [100]
        })
        states = map_data('state')

        fig = (
            ggplot(df, aes(map_id='state', fill='value'))
            + geom_map(map=states)
        ).draw()

        assert isinstance(fig, Figure)

    def test_map_preserves_original_data(self, us_state_data):
        """Test that creating a map doesn't modify original data."""
        original_shape = us_state_data.shape
        original_values = us_state_data['population'].values.copy()

        states = map_data('state')
        fig = (
            ggplot(us_state_data, aes(map_id='state', fill='population'))
            + geom_map(map=states)
        ).draw()

        assert us_state_data.shape == original_shape
        np.testing.assert_array_equal(us_state_data['population'].values, original_values)
