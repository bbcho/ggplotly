# pytest/test_geom_map.py
"""Tests for geom_map as a base map layer and choropleth."""

import pytest
import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_map, geom_point, map_data
from ggplotly.themes import theme_dark, theme_classic, theme_minimal


class TestGeomMapBaseLayer:
    """Tests for using geom_map as a base map layer."""

    def test_base_map_usa_creates_geo_context(self):
        """Test that geom_map without fill creates a geo context for other geoms."""
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

    def test_base_map_world(self):
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

        # Check geo layout scope
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


class TestGeomMapChoropleth:
    """Tests for choropleth functionality."""

    def test_choropleth_requires_map_id(self):
        """Test that choropleth mode requires map_id aesthetic."""
        data = pd.DataFrame({
            'value': [100, 200, 300],
        })

        # Should raise error because fill without map_id
        with pytest.raises(ValueError, match="map_id"):
            fig = (
                ggplot(data, aes(fill='value'))
                + geom_map()
            ).draw()

    def test_choropleth_with_fill(self):
        """Test choropleth with numeric fill."""
        data = pd.DataFrame({
            'state': ['CA', 'TX', 'NY'],
            'value': [100, 200, 300],
        })

        fig = (
            ggplot(data, aes(map_id='state', fill='value'))
            + geom_map(map_type='usa')
        ).draw()

        # Should have a choropleth trace
        assert len(fig.data) == 1
        assert fig.data[0].type == 'choropleth'
        assert fig.data[0].locationmode == 'USA-states'

    def test_choropleth_with_map_data(self):
        """Test choropleth with map_data."""
        states = map_data('state')
        data = pd.DataFrame({
            'state': ['CA', 'TX', 'NY'],
            'value': [100, 200, 300],
        })

        fig = (
            ggplot(data, aes(map_id='state', fill='value'))
            + geom_map(map=states)
        ).draw()

        assert fig.data[0].type == 'choropleth'

    def test_choropleth_world(self):
        """Test world choropleth."""
        data = pd.DataFrame({
            'country': ['USA', 'CAN', 'MEX'],
            'value': [100, 200, 300],
        })

        fig = (
            ggplot(data, aes(map_id='country', fill='value'))
            + geom_map(map_type='world')
        ).draw()

        assert fig.data[0].type == 'choropleth'
        assert fig.data[0].locationmode == 'ISO-3'
        assert fig.layout.geo.scope == 'world'


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

        # Should use regular Scatter, not Scattergeo
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

        # Build choropleth first, then add points
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

        # theme_dark should apply dark colors to the geo
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

        # theme_classic uses light colors
        assert fig.layout.geo.bgcolor == 'white'


class TestGeomMapEdgeCases:
    """Tests for edge cases and error handling."""

    def test_missing_lon_lat_columns(self):
        """Test error when lon/lat columns are missing for geo points."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        # This should work because geom_point will use regular scatter
        # (no geo context established by geom_map without aesthetics)
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

        # Should still create the geo layout
        assert fig.layout.geo.scope == 'usa'

    def test_geom_map_without_mapping(self):
        """Test geom_map with no mapping creates base map."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        fig = (
            ggplot(data, aes(x='x', y='y'))
            + geom_map(map_type='usa')
        ).draw()

        # Should create the invisible geo marker trace
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scattergeo'
        assert fig.data[0].name == '_geo_context'

    def test_multiple_geom_maps_not_allowed(self):
        """Test behavior with multiple geom_maps (last one wins for geo layout)."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        # Both geom_maps will add traces, last one sets the layout
        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_map(map_type='world')
            + geom_point()
        ).draw()

        # The last geom_map should set the scope
        assert fig.layout.geo.scope == 'world'


class TestGeomMapGeoJSON:
    """Tests for GeoJSON/sf-like functionality in geom_map."""

    @pytest.fixture
    def simple_polygon_geojson(self):
        """Create a simple GeoJSON with one polygon (a square)."""
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
    def line_geojson(self):
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
    def point_geojson(self):
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

        # Should have a Choroplethmap or Choroplethmapbox trace
        assert len(fig.data) >= 1
        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')

    def test_geojson_polygon_categorical_fill(self, simple_polygon_geojson):
        """Test GeoJSON with categorical fill."""
        data = pd.DataFrame({
            'id': ['region1', 'region2'],
            'category': ['A', 'B'],
        })

        fig = (
            ggplot(data, aes(fill='category'))
            + geom_map(geojson=simple_polygon_geojson, featureidkey='id')
        ).draw()

        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')

    def test_geojson_polygon_no_fill(self, simple_polygon_geojson):
        """Test GeoJSON polygon without fill (uniform color)."""
        # Use empty data since ggplot requires a dataframe
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

        # Lines should use Scattermap or Scattermapbox
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

        # Points should use Scattermap or Scattermapbox
        assert len(fig.data) >= 1
        assert fig.data[0].type in ('scattermap', 'scattermapbox')
        assert fig.data[0].mode == 'markers'

    def test_geojson_custom_mapbox_style(self, simple_polygon_geojson):
        """Test custom mapbox style parameter."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=simple_polygon_geojson, mapbox_style='open-street-map')
        ).draw()

        # Check either map or mapbox layout
        if hasattr(fig.layout, 'map') and fig.layout.map.style:
            assert fig.layout.map.style == 'open-street-map'
        else:
            assert fig.layout.mapbox.style == 'open-street-map'

    def test_geojson_auto_center_calculation(self, simple_polygon_geojson):
        """Test that map center is auto-calculated from GeoJSON bounds."""
        empty_data = pd.DataFrame({'x': []})
        fig = (
            ggplot(empty_data)
            + geom_map(geojson=simple_polygon_geojson)
        ).draw()

        # Center should be calculated from the polygon bounds
        # Check either map or mapbox layout
        if hasattr(fig.layout, 'map') and fig.layout.map.center:
            assert fig.layout.map.center.lat is not None
            assert fig.layout.map.center.lon is not None
        else:
            assert fig.layout.mapbox.center.lat is not None
            assert fig.layout.mapbox.center.lon is not None

    def test_geojson_with_data_and_map_id(self, simple_polygon_geojson):
        """Test GeoJSON with data joined via map_id."""
        data = pd.DataFrame({
            'region_code': ['region1', 'region2'],
            'population': [1000000, 500000],
        })

        fig = (
            ggplot(data, aes(map_id='region_code', fill='population'))
            + geom_map(geojson=simple_polygon_geojson, featureidkey='id')
        ).draw()

        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')
        # Should have correct locations
        assert len(fig.data[0].locations) == 2


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

        # Create a simple GeoDataFrame
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

        # Should automatically use Choroplethmap or Choroplethmapbox
        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')

    def test_geodataframe_no_fill(self, skip_if_no_geopandas):
        """Test GeoDataFrame without fill aesthetic."""
        import geopandas as gpd
        from shapely.geometry import Polygon

        gdf = gpd.GeoDataFrame({
            'name': ['Region A'],
            'geometry': [
                Polygon([(-74, 40.7), (-74, 41), (-73.7, 41), (-73.7, 40.7)]),
            ]
        }, crs="EPSG:4326")

        fig = (
            ggplot(gdf)
            + geom_map()
        ).draw()

        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')
        assert fig.data[0].showscale is False
