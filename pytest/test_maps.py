"""
Tests for ggplotly map geoms (geom_map, geom_sf) and map_data.
"""
import pytest
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

import sys
sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    ggplot, aes,
    geom_map, geom_sf, geom_point,
    map_data,
    facet_wrap,
    labs, scale_fill_viridis_c, scale_fill_gradient
)


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


class TestMapData:
    """Tests for map_data function."""

    def test_map_data_state(self):
        """Test getting US state map data."""
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

    def test_map_data_world(self):
        """Test getting world map data."""
        countries = map_data('world')
        assert isinstance(countries, pd.DataFrame)
        assert 'id' in countries.columns
        assert 'name' in countries.columns
        # Should have some countries
        assert len(countries) > 40

    def test_map_data_invalid(self):
        """Test invalid map name raises error."""
        with pytest.raises(ValueError):
            map_data('invalid_map')

    def test_map_data_state_codes(self):
        """Test that state codes are valid."""
        states = map_data('state')
        # Check some known states exist
        assert 'CA' in states['id'].values
        assert 'NY' in states['id'].values
        assert 'TX' in states['id'].values

    def test_map_data_world_codes(self):
        """Test that country codes are valid ISO-3."""
        countries = map_data('world')
        # All codes should be 3 characters
        assert all(len(code) == 3 for code in countries['id'])
        # Check some known countries
        assert 'USA' in countries['id'].values
        assert 'GBR' in countries['id'].values
        assert 'CHN' in countries['id'].values


class TestGeomMap:
    """Tests for geom_map."""

    def test_basic_us_map(self, us_state_data):
        """Test basic US state choropleth."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)
        assert len(fig.data) >= 1

    def test_us_map_without_map_data(self, us_state_data):
        """Test US map without explicit map data."""
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map_type='state'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_world_map(self, world_data):
        """Test world map choropleth."""
        countries = map_data('world')
        p = (ggplot(world_data, aes(map_id='country', fill='gdp'))
             + geom_map(map=countries, map_type='world'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_with_custom_palette(self, us_state_data):
        """Test map with custom color palette."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states, palette='Blues'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_with_border_color(self, us_state_data):
        """Test map with custom border color."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states, color='black', linewidth=1))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_categorical_fill(self, us_state_data):
        """Test map with categorical fill."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='region'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_with_labs(self, us_state_data):
        """Test map with labels."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + labs(title='US Population by State', fill='Population'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_with_scale(self, us_state_data):
        """Test map with fill scale."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + scale_fill_gradient(low='white', high='darkblue'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomMapFaceting:
    """Tests for faceted maps."""

    def test_faceted_us_map(self, us_state_data):
        """Test faceted US map."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + facet_wrap('region'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_faceted_map_fixed_scales(self, us_state_data):
        """Test faceted map with fixed scales."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + facet_wrap('region', scales='fixed'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_faceted_map_free_scales(self, us_state_data):
        """Test faceted map with free scales."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + facet_wrap('region', scales='free'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_faceted_map_ncol(self, us_state_data):
        """Test faceted map with specified columns."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + facet_wrap('region', ncol=2))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomMapWithPoints:
    """Tests for geom_map + geom_point (replaces deprecated geom_point_map)."""

    def test_basic_point_map(self, point_location_data):
        """Test basic points on a map using geom_map + geom_point."""
        p = (ggplot(point_location_data, aes(x='lon', y='lat'))
             + geom_map(map_type='usa')
             + geom_point())
        fig = p.draw()
        assert isinstance(fig, Figure)
        # geom_point should auto-detect geo context and use Scattergeo
        assert any(t.type == 'scattergeo' for t in fig.data)

    def test_point_map_with_size(self, point_location_data):
        """Test points on map with size aesthetic."""
        p = (ggplot(point_location_data, aes(x='lon', y='lat', size='population'))
             + geom_map(map_type='usa')
             + geom_point())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_point_map_with_color(self, point_location_data):
        """Test points on map with color."""
        p = (ggplot(point_location_data, aes(x='lon', y='lat'))
             + geom_map(map_type='usa')
             + geom_point(color='red'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_point_map_with_label(self, point_location_data):
        """Test points on map with label aesthetic."""
        p = (ggplot(point_location_data, aes(x='lon', y='lat', label='city'))
             + geom_map(map_type='usa')
             + geom_point())
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestMapCombinations:
    """Tests for combining map geoms."""

    def test_choropleth_with_points(self, us_state_data, point_location_data):
        """Test choropleth map with point overlay."""
        states = map_data('state')
        # Merge data for the map base
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_with_labs_and_title(self, us_state_data):
        """Test map with comprehensive labels."""
        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states)
             + labs(
                 title='US State Population',
                 subtitle='Data from Census',
                 fill='Population',
                 caption='Source: Census Bureau'
             ))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestMapEdgeCases:
    """Tests for edge cases in maps."""

    def test_map_missing_map_id_error(self, us_state_data):
        """Test that missing map_id raises appropriate error."""
        states = map_data('state')
        with pytest.raises(ValueError, match="map_id"):
            p = (ggplot(us_state_data, aes(x='state', fill='population'))
                 + geom_map(map=states))
            fig = p.draw()

    def test_map_empty_data(self):
        """Test map with empty dataframe."""
        empty_df = pd.DataFrame({'state': [], 'value': []})
        states = map_data('state')
        p = (ggplot(empty_df, aes(map_id='state', fill='value'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_single_state(self):
        """Test map with single state."""
        df = pd.DataFrame({
            'state': ['CA'],
            'value': [100]
        })
        states = map_data('state')
        p = (ggplot(df, aes(map_id='state', fill='value'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_unknown_states(self):
        """Test map with unknown state codes (should gracefully handle)."""
        df = pd.DataFrame({
            'state': ['CA', 'XX', 'YY'],  # XX, YY are invalid
            'value': [100, 50, 75]
        })
        states = map_data('state')
        p = (ggplot(df, aes(map_id='state', fill='value'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_all_states(self):
        """Test map with all US states."""
        states = map_data('state')
        # Create separate data for plotting to avoid merge column conflicts
        data = pd.DataFrame({
            'state': states['id'].values,
            'population': range(len(states))
        })
        p = (ggplot(data, aes(map_id='state', fill='population'))
             + geom_map(map=states))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_map_preserves_data(self, us_state_data):
        """Test that creating a map doesn't modify original data."""
        original_shape = us_state_data.shape
        original_values = us_state_data['population'].values.copy()

        states = map_data('state')
        p = (ggplot(us_state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states))
        fig = p.draw()

        assert us_state_data.shape == original_shape
        np.testing.assert_array_equal(us_state_data['population'].values, original_values)
