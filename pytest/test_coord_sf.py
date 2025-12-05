# pytest/test_coord_sf.py
"""
Tests for coord_sf coordinate system.
"""

import pytest
import pandas as pd

from ggplotly import (
    ggplot, aes, geom_map, geom_sf, geom_point, coord_sf, theme_dark
)


class TestCoordSfBasic:
    """Basic tests for coord_sf."""

    def test_coord_sf_import(self):
        """Test that coord_sf can be imported."""
        from ggplotly import coord_sf
        assert coord_sf is not None

    def test_coord_sf_instantiation(self):
        """Test basic coord_sf instantiation."""
        cs = coord_sf()
        assert cs.xlim is None
        assert cs.ylim is None
        assert cs.expand is True
        assert cs.crs is None

    def test_coord_sf_with_limits(self):
        """Test coord_sf with xlim and ylim."""
        cs = coord_sf(xlim=(-125, -65), ylim=(25, 50))
        assert cs.xlim == (-125, -65)
        assert cs.ylim == (25, 50)

    def test_coord_sf_with_crs(self):
        """Test coord_sf with CRS parameter."""
        cs = coord_sf(crs='mercator')
        assert cs.crs == 'mercator'


class TestCoordSfProjectionMapping:
    """Tests for CRS to projection mapping."""

    def test_mercator_projection(self):
        """Test Mercator projection mapping."""
        cs = coord_sf(crs='mercator')
        proj = cs._get_projection_type('mercator')
        assert proj == 'mercator'

    def test_natural_earth_projection(self):
        """Test Natural Earth projection mapping."""
        cs = coord_sf()
        proj = cs._get_projection_type('natural earth')
        assert proj == 'natural earth'

    def test_albers_usa_projection(self):
        """Test Albers USA projection mapping."""
        cs = coord_sf()
        proj = cs._get_projection_type('albers usa')
        assert proj == 'albers usa'

    def test_orthographic_projection(self):
        """Test Orthographic projection mapping."""
        cs = coord_sf()
        proj = cs._get_projection_type('orthographic')
        assert proj == 'orthographic'

    def test_globe_alias(self):
        """Test 'globe' as alias for orthographic."""
        cs = coord_sf()
        proj = cs._get_projection_type('globe')
        assert proj == 'orthographic'

    def test_epsg_4326(self):
        """Test EPSG:4326 (WGS84) mapping."""
        cs = coord_sf()
        proj = cs._get_projection_type('EPSG:4326')
        assert proj == 'equirectangular'

    def test_robinson_projection(self):
        """Test Robinson projection mapping."""
        cs = coord_sf()
        proj = cs._get_projection_type('robinson')
        assert proj == 'robinson'

    def test_case_insensitive(self):
        """Test that projection mapping is case-insensitive."""
        cs = coord_sf()
        assert cs._get_projection_type('MERCATOR') == 'mercator'
        assert cs._get_projection_type('Natural Earth') == 'natural earth'


class TestCoordSfWithGeoMap:
    """Tests for coord_sf with geo-based maps."""

    def test_coord_sf_with_base_map(self):
        """Test coord_sf with base map."""
        data = pd.DataFrame({
            'lon': [-74.0060, -118.2437],
            'lat': [40.7128, 34.0522],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf()
        ).draw()

        # Should have geo traces
        assert len(fig.data) >= 1

    def test_coord_sf_with_xlim_ylim(self):
        """Test coord_sf with geographic bounds."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(xlim=(-125, -65), ylim=(25, 50))
        ).draw()

        # Check that bounds were applied
        # Note: with expand=True (default), bounds are slightly larger
        assert fig.layout.geo.lonaxis.range[0] <= -125
        assert fig.layout.geo.lonaxis.range[1] >= -65
        assert fig.layout.geo.lataxis.range[0] <= 25
        assert fig.layout.geo.lataxis.range[1] >= 50

    def test_coord_sf_no_expand(self):
        """Test coord_sf without expansion."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(xlim=(-125, -65), ylim=(25, 50), expand=False)
        ).draw()

        # Check exact bounds (Plotly may return tuple or list)
        assert list(fig.layout.geo.lonaxis.range) == [-125, -65]
        assert list(fig.layout.geo.lataxis.range) == [25, 50]

    def test_coord_sf_with_projection(self):
        """Test coord_sf with custom projection."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='world')
            + geom_point()
            + coord_sf(crs='robinson')
        ).draw()

        # Check projection was set
        assert fig.layout.geo.projection.type == 'robinson'

    def test_coord_sf_orthographic_projection(self):
        """Test coord_sf with orthographic (globe) projection."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='world')
            + geom_point()
            + coord_sf(crs='orthographic')
        ).draw()

        assert fig.layout.geo.projection.type == 'orthographic'

    def test_coord_sf_center_calculated(self):
        """Test that center is calculated from bounds."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(xlim=(-100, -80), ylim=(30, 40), expand=False)
        ).draw()

        # Center should be at (-90, 35)
        assert fig.layout.geo.center.lon == -90
        assert fig.layout.geo.center.lat == 35


class TestCoordSfWithMapbox:
    """Tests for coord_sf with mapbox-based maps."""

    @pytest.fixture
    def simple_geojson(self):
        """Create a simple GeoJSON for testing."""
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
                }
            ]
        }

    def test_coord_sf_with_geojson(self, simple_geojson):
        """Test coord_sf with GeoJSON (mapbox mode)."""
        empty_data = pd.DataFrame({'x': []})

        fig = (
            ggplot(empty_data)
            + geom_sf(geojson=simple_geojson)
            + coord_sf(xlim=(-75, -73), ylim=(40, 42))
        ).draw()

        # Should have mapbox-style trace
        assert fig.data[0].type in ('choroplethmap', 'choroplethmapbox')

        # Check center (mapbox uses center, not axis ranges)
        if hasattr(fig.layout, 'map') and fig.layout.map.center:
            center = fig.layout.map.center
        else:
            center = fig.layout.mapbox.center

        assert center.lon is not None
        assert center.lat is not None


class TestCoordSfGraticules:
    """Tests for graticule/grid line control."""

    def test_label_graticule_ns(self):
        """Test label_graticule with NS (latitude labels)."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(label_graticule='NS')
        ).draw()

        # Should show lat grid
        assert fig.layout.geo.lataxis.showgrid is True

    def test_label_graticule_ew(self):
        """Test label_graticule with EW (longitude labels)."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(label_graticule='EW')
        ).draw()

        # Should show lon grid
        assert fig.layout.geo.lonaxis.showgrid is True

    def test_label_graticule_nesw(self):
        """Test label_graticule with all directions."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(label_graticule='NESW')
        ).draw()

        # Should show both grids
        assert fig.layout.geo.lonaxis.showgrid is True
        assert fig.layout.geo.lataxis.showgrid is True


class TestCoordSfNonGeo:
    """Tests for coord_sf with non-geo figures."""

    def test_coord_sf_no_effect_on_cartesian(self):
        """Test that coord_sf has no effect on non-geo figures."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
        })

        fig = (
            ggplot(data, aes(x='x', y='y'))
            + geom_point()
            + coord_sf(xlim=(-125, -65), ylim=(25, 50))
        ).draw()

        # Should be a regular scatter plot
        assert fig.data[0].type == 'scatter'
        # Cartesian axes should not be affected by coord_sf
        # (coord_sf only applies to geo traces)


class TestCoordSfWithThemes:
    """Tests for coord_sf combined with themes."""

    def test_coord_sf_with_theme_dark(self):
        """Test coord_sf with dark theme."""
        data = pd.DataFrame({
            'lon': [-74.0060],
            'lat': [40.7128],
        })

        fig = (
            ggplot(data, aes(x='lon', y='lat'))
            + geom_map(map_type='usa')
            + geom_point()
            + coord_sf(crs='albers usa')
            + theme_dark()
        ).draw()

        # Should have dark theme applied
        assert fig.layout.geo.bgcolor == 'rgb(17, 17, 17)'
        # And projection set
        assert fig.layout.geo.projection.type == 'albers usa'
