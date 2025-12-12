"""
Tests for the Layer class.

The Layer class encapsulates the relationship between geoms, stats, data, and mappings
following the Grammar of Graphics pattern.
"""
import pytest
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

from ggplotly import ggplot, aes, geom_point, geom_line, Layer, layer
from ggplotly.stats import stat_identity, stat_smooth, stat_bin


@pytest.fixture
def simple_data():
    """Simple fixed data for deterministic tests."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })


@pytest.fixture
def grouped_data():
    """Data with grouping columns."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [2, 4, 6, 8, 10, 12],
        'group': ['A', 'A', 'A', 'B', 'B', 'B'],
    })


class TestLayerCreation:
    """Tests for Layer initialization."""

    def test_create_layer_with_geom_class(self, simple_data):
        """Test creating a layer with a geom class."""
        lyr = Layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})

        assert lyr.geom == geom_point
        assert lyr.data is simple_data
        assert lyr.mapping == {'x': 'x', 'y': 'y'}

    def test_create_layer_with_aes_object(self, simple_data):
        """Test creating a layer with an aes object for mapping."""
        mapping = aes(x='x', y='y')
        lyr = Layer(geom=geom_point, data=simple_data, mapping=mapping)

        assert lyr.mapping == {'x': 'x', 'y': 'y'}

    def test_create_layer_with_stat(self, simple_data):
        """Test creating a layer with a stat."""
        lyr = Layer(geom=geom_line, stat=stat_smooth, data=simple_data, mapping={'x': 'x', 'y': 'y'})

        assert lyr.stat == stat_smooth

    def test_layer_default_position(self, simple_data):
        """Test that default position is 'identity'."""
        lyr = Layer(geom=geom_point, data=simple_data)

        assert lyr.position == 'identity'

    def test_layer_inherit_aes_default(self, simple_data):
        """Test that inherit_aes defaults to True."""
        lyr = Layer(geom=geom_point, data=simple_data)

        assert lyr.inherit_aes is True

    def test_layer_with_params(self, simple_data):
        """Test creating a layer with additional params."""
        lyr = Layer(geom=geom_point, data=simple_data, color='red', size=10)

        assert lyr.params['color'] == 'red'
        assert lyr.params['size'] == 10


class TestLayerFunction:
    """Tests for the layer() convenience function."""

    def test_layer_function_creates_layer(self, simple_data):
        """Test that layer() function creates a Layer instance."""
        lyr = layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})

        assert isinstance(lyr, Layer)
        assert lyr.geom == geom_point

    def test_layer_function_passes_all_params(self, simple_data):
        """Test that layer() passes all parameters correctly."""
        lyr = layer(
            geom=geom_point,
            stat=stat_smooth,
            data=simple_data,
            mapping={'x': 'x', 'y': 'y'},
            position='dodge',
            inherit_aes=False,
            color='blue'
        )

        assert lyr.geom == geom_point
        assert lyr.stat == stat_smooth
        assert lyr.position == 'dodge'
        assert lyr.inherit_aes is False
        assert lyr.params['color'] == 'blue'


class TestLayerFromGeom:
    """Tests for Layer.from_geom() factory method."""

    def test_from_geom_basic(self, simple_data):
        """Test creating a Layer from an existing geom."""
        geom = geom_point(data=simple_data, mapping=aes(x='x', y='y'))
        lyr = Layer.from_geom(geom)

        assert isinstance(lyr, Layer)
        assert lyr.geom is geom
        assert lyr.mapping == {'x': 'x', 'y': 'y'}

    def test_from_geom_preserves_params(self, simple_data):
        """Test that from_geom preserves geom parameters."""
        geom = geom_point(data=simple_data, mapping=aes(x='x', y='y'), color='red', size=15)
        lyr = Layer.from_geom(geom)

        assert lyr.params.get('color') == 'red'
        assert lyr.params.get('size') == 15

    def test_from_geom_preserves_stats(self, simple_data):
        """Test that from_geom preserves geom's stats."""
        geom = geom_point(data=simple_data, mapping=aes(x='x', y='y'))
        stat = stat_identity()
        geom.stats = [stat]

        lyr = Layer.from_geom(geom)

        assert lyr.stat is stat


class TestLayerCopy:
    """Tests for Layer.copy() method."""

    def test_copy_creates_independent_layer(self, simple_data):
        """Test that copy creates an independent Layer."""
        lyr = Layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})
        lyr_copy = lyr.copy()

        assert lyr_copy is not lyr
        assert lyr_copy.mapping == lyr.mapping
        assert lyr_copy.mapping is not lyr.mapping

    def test_copy_mapping_independent(self, simple_data):
        """Test that copied layer's mapping is independent."""
        lyr = Layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})
        lyr_copy = lyr.copy()

        lyr_copy.mapping['color'] = 'group'

        assert 'color' not in lyr.mapping


class TestLayerSetupData:
    """Tests for Layer.setup_data() method."""

    def test_setup_data_inherits_plot_data(self):
        """Test that layer inherits plot data when no layer data."""
        plot_data = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        lyr = Layer(geom=geom_point, mapping={'x': 'x', 'y': 'y'})

        lyr.setup_data(plot_data, {})

        assert lyr.data is not None
        assert list(lyr.data['x']) == [1, 2, 3]

    def test_setup_data_uses_layer_data(self, simple_data):
        """Test that layer uses its own data when provided."""
        plot_data = pd.DataFrame({'a': [10, 20, 30], 'b': [40, 50, 60]})
        lyr = Layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})

        lyr.setup_data(plot_data, {})

        # Should use layer data, not plot data
        assert list(lyr.data['x']) == [1, 2, 3, 4, 5]

    def test_setup_data_combines_mappings(self):
        """Test that setup_data combines plot and layer mappings."""
        plot_data = pd.DataFrame({'x': [1, 2], 'y': [3, 4], 'color': ['A', 'B']})
        plot_mapping = {'x': 'x', 'y': 'y'}
        layer_mapping = {'color': 'color'}

        lyr = Layer(geom=geom_point, mapping=layer_mapping)
        lyr.setup_data(plot_data, plot_mapping)

        # Should have both plot and layer mappings
        assert lyr.mapping['x'] == 'x'
        assert lyr.mapping['y'] == 'y'
        assert lyr.mapping['color'] == 'color'

    def test_setup_data_layer_mapping_precedence(self):
        """Test that layer mapping takes precedence over plot mapping."""
        plot_data = pd.DataFrame({'x': [1, 2], 'y': [3, 4], 'z': [5, 6]})
        plot_mapping = {'x': 'x', 'y': 'y'}
        layer_mapping = {'y': 'z'}  # Override y

        lyr = Layer(geom=geom_point, mapping=layer_mapping)
        lyr.setup_data(plot_data, plot_mapping)

        assert lyr.mapping['y'] == 'z'  # Layer mapping wins

    def test_setup_data_inherit_aes_false(self):
        """Test that inherit_aes=False prevents inheritance."""
        plot_data = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        plot_mapping = {'x': 'x', 'y': 'y', 'color': 'group'}
        layer_mapping = {'x': 'x', 'y': 'y'}

        lyr = Layer(geom=geom_point, mapping=layer_mapping, inherit_aes=False)
        lyr.setup_data(plot_data, plot_mapping)

        # Should only have layer mappings
        assert 'color' not in lyr.mapping


class TestLayerRepr:
    """Tests for Layer string representation."""

    def test_repr_basic(self, simple_data):
        """Test basic string representation."""
        lyr = Layer(geom=geom_point, data=simple_data, mapping={'x': 'x', 'y': 'y'})
        repr_str = repr(lyr)

        assert 'Layer' in repr_str
        assert 'geom_point' in repr_str

    def test_repr_with_stat(self, simple_data):
        """Test repr shows stat when present."""
        stat = stat_smooth()
        lyr = Layer(geom=geom_line, stat=stat, data=simple_data)
        repr_str = repr(lyr)

        assert 'stat_smooth' in repr_str


class TestLayerMappingProperty:
    """Tests for Layer.mapping property."""

    def test_mapping_setter_with_dict(self, simple_data):
        """Test setting mapping with a dict."""
        lyr = Layer(geom=geom_point, data=simple_data)
        lyr.mapping = {'x': 'x', 'y': 'y'}

        assert lyr.mapping == {'x': 'x', 'y': 'y'}

    def test_mapping_setter_with_aes(self, simple_data):
        """Test setting mapping with an aes object."""
        lyr = Layer(geom=geom_point, data=simple_data)
        lyr.mapping = aes(x='x', y='y', color='group')

        assert lyr.mapping == {'x': 'x', 'y': 'y', 'color': 'group'}


class TestLayerDataProperty:
    """Tests for Layer.data property."""

    def test_data_getter(self, simple_data):
        """Test getting layer data."""
        lyr = Layer(geom=geom_point, data=simple_data)

        assert lyr.data is simple_data

    def test_data_setter(self, simple_data, grouped_data):
        """Test setting layer data."""
        lyr = Layer(geom=geom_point, data=simple_data)
        lyr.data = grouped_data

        assert lyr.data is grouped_data
