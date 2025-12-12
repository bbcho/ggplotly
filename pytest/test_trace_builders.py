"""
Tests for trace_builders module.

These tests verify that the trace builder strategies produce correct Plotly traces
with the expected data, groupings, colors, shapes, and legend behavior.
"""
import pytest
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

from ggplotly import ggplot, aes, geom_point, geom_line
from ggplotly.trace_builders import (
    TraceBuilder,
    GroupedTraceBuilder,
    ColorAndShapeTraceBuilder,
    ColorOnlyTraceBuilder,
    ShapeOnlyTraceBuilder,
    ContinuousColorTraceBuilder,
    SingleTraceBuilder,
    get_trace_builder,
)


@pytest.fixture
def simple_data():
    """Simple fixed data for deterministic tests."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })


@pytest.fixture
def grouped_data():
    """Data with grouping columns for testing grouped traces."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5, 6],
        'y': [2, 4, 6, 8, 10, 12],
        'group': ['A', 'A', 'A', 'B', 'B', 'B'],
        'category': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
        'shape_col': ['circle', 'circle', 'square', 'square', 'circle', 'square'],
    })


@pytest.fixture
def continuous_data():
    """Data with continuous values for color mapping."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10],
        'value': [10.0, 20.0, 30.0, 40.0, 50.0]
    })


class TestSingleTraceBuilder:
    """Tests for SingleTraceBuilder - no grouping scenario."""

    def test_single_trace_creates_one_trace(self, simple_data):
        """Test that ungrouped data creates exactly one trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()

        assert len(fig.data) == 1

    def test_single_trace_contains_all_data(self, simple_data):
        """Test that the single trace contains all data points."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()

        assert list(fig.data[0].x) == [1, 2, 3, 4, 5]
        assert list(fig.data[0].y) == [2, 4, 6, 8, 10]

    def test_single_trace_literal_color(self, simple_data):
        """Test that literal color is applied correctly."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(color='blue')
        fig = p.draw()

        assert fig.data[0].marker.color == 'blue'

    def test_single_trace_literal_size(self, simple_data):
        """Test that literal size is applied correctly."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(size=15)
        fig = p.draw()

        assert fig.data[0].marker.size == 15

    def test_single_trace_opacity(self, simple_data):
        """Test that opacity/alpha is applied correctly."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(alpha=0.5)
        fig = p.draw()

        assert fig.data[0].opacity == 0.5


class TestColorOnlyTraceBuilder:
    """Tests for ColorOnlyTraceBuilder - color/fill mapped to column."""

    def test_color_mapping_creates_traces_per_category(self, grouped_data):
        """Test that color mapping creates one trace per unique value."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        assert len(fig.data) == 2  # A and B

    def test_color_mapping_traces_have_correct_names(self, grouped_data):
        """Test that each trace is named after its category value."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        trace_names = {trace.name for trace in fig.data}
        assert trace_names == {'A', 'B'}

    def test_color_mapping_data_correctly_split(self, grouped_data):
        """Test that data is correctly split across traces."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        # Find trace for group A
        trace_a = next(t for t in fig.data if t.name == 'A')
        trace_b = next(t for t in fig.data if t.name == 'B')

        # Group A has x=[1,2,3], y=[2,4,6]
        assert list(trace_a.x) == [1, 2, 3]
        assert list(trace_a.y) == [2, 4, 6]

        # Group B has x=[4,5,6], y=[8,10,12]
        assert list(trace_b.x) == [4, 5, 6]
        assert list(trace_b.y) == [8, 10, 12]

    def test_color_mapping_different_colors_per_trace(self, grouped_data):
        """Test that each trace gets a different color."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        colors = [trace.marker.color for trace in fig.data]
        assert colors[0] != colors[1]

    def test_fill_mapping_also_works(self, grouped_data):
        """Test that fill aesthetic also creates grouped traces."""
        p = ggplot(grouped_data, aes(x='x', y='y', fill='group')) + geom_point()
        fig = p.draw()

        assert len(fig.data) == 2

    def test_legendgroup_set_correctly(self, grouped_data):
        """Test that legendgroup matches trace name for facet support."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        for trace in fig.data:
            assert trace.legendgroup == trace.name


class TestShapeOnlyTraceBuilder:
    """Tests for ShapeOnlyTraceBuilder - shape mapped to column."""

    def test_shape_mapping_creates_traces_per_category(self, grouped_data):
        """Test that shape mapping creates one trace per unique shape value."""
        p = ggplot(grouped_data, aes(x='x', y='y', shape='group')) + geom_point()
        fig = p.draw()

        assert len(fig.data) == 2  # A and B

    def test_shape_mapping_different_symbols(self, grouped_data):
        """Test that each trace gets a different marker symbol."""
        p = ggplot(grouped_data, aes(x='x', y='y', shape='group')) + geom_point()
        fig = p.draw()

        symbols = [trace.marker.symbol for trace in fig.data]
        assert symbols[0] != symbols[1]

    def test_shape_mapping_data_correctly_split(self, grouped_data):
        """Test that data is correctly split by shape values."""
        p = ggplot(grouped_data, aes(x='x', y='y', shape='group')) + geom_point()
        fig = p.draw()

        trace_a = next(t for t in fig.data if t.name == 'A')
        trace_b = next(t for t in fig.data if t.name == 'B')

        assert list(trace_a.x) == [1, 2, 3]
        assert list(trace_b.x) == [4, 5, 6]


class TestColorAndShapeTraceBuilder:
    """Tests for ColorAndShapeTraceBuilder - both color and shape mapped."""

    def test_combined_mapping_creates_combination_traces(self, grouped_data):
        """Test that combining color and shape creates traces for each combo."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group', shape='category')) + geom_point()
        fig = p.draw()

        # 2 groups (A, B) x 2 categories (X, Y) = up to 4 combinations
        # But only combinations with data are created
        assert len(fig.data) >= 2

    def test_combined_mapping_legend_names(self, grouped_data):
        """Test that legend names combine both aesthetics."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group', shape='category')) + geom_point()
        fig = p.draw()

        # Names should be like "A, X" or "B, Y"
        for trace in fig.data:
            # Should have comma separator if different columns
            assert ',' in trace.name or len(fig.data) <= 2

    def test_same_column_for_color_and_shape(self, grouped_data):
        """Test behavior when color and shape map to same column."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group', shape='group')) + geom_point()
        fig = p.draw()

        # Should have 2 traces (A and B), not 4
        assert len(fig.data) == 2

        # Names should be single value, not "A, A"
        trace_names = {trace.name for trace in fig.data}
        assert trace_names == {'A', 'B'}


class TestGroupedTraceBuilder:
    """Tests for GroupedTraceBuilder - explicit group aesthetic."""

    def test_explicit_group_creates_separate_traces(self, grouped_data):
        """Test that explicit group aesthetic creates separate traces."""
        p = ggplot(grouped_data, aes(x='x', y='y', group='group')) + geom_line()
        fig = p.draw()

        assert len(fig.data) == 2

    def test_explicit_group_data_split_correctly(self, grouped_data):
        """Test that data is split correctly by group."""
        p = ggplot(grouped_data, aes(x='x', y='y', group='group')) + geom_line()
        fig = p.draw()

        # Each trace should have 3 points
        for trace in fig.data:
            assert len(trace.x) == 3


class TestContinuousColorTraceBuilder:
    """Tests for ContinuousColorTraceBuilder - numeric color mapping."""

    def test_continuous_color_creates_single_trace(self, continuous_data):
        """Test that continuous color mapping creates one trace with colorscale."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        assert len(fig.data) == 1

    def test_continuous_color_has_colorscale(self, continuous_data):
        """Test that continuous color mapping uses a colorscale."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        assert fig.data[0].marker.colorscale is not None

    def test_continuous_color_has_colorbar(self, continuous_data):
        """Test that continuous color mapping shows a colorbar."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        assert fig.data[0].marker.showscale is True

    def test_continuous_color_values_passed(self, continuous_data):
        """Test that continuous color values are passed to marker.color."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        # marker.color should be the array of values
        assert list(fig.data[0].marker.color) == [10.0, 20.0, 30.0, 40.0, 50.0]

    def test_continuous_color_no_legend(self, continuous_data):
        """Test that continuous color hides legend (colorbar serves as legend)."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        assert fig.data[0].showlegend is False


class TestGetTraceBuilder:
    """Tests for the get_trace_builder factory function."""

    def test_factory_selects_single_builder(self, simple_data):
        """Test that factory returns SingleTraceBuilder for ungrouped data."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()

        # Verify behavior matches SingleTraceBuilder
        assert len(fig.data) == 1

    def test_factory_selects_color_builder(self, grouped_data):
        """Test that factory returns ColorOnlyTraceBuilder for color-mapped data."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        # Verify behavior matches ColorOnlyTraceBuilder
        assert len(fig.data) == 2
        for trace in fig.data:
            assert trace.marker.color is not None

    def test_factory_selects_continuous_builder(self, continuous_data):
        """Test that factory returns ContinuousColorTraceBuilder for numeric color."""
        p = ggplot(continuous_data, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        # Verify behavior matches ContinuousColorTraceBuilder
        assert len(fig.data) == 1
        assert fig.data[0].marker.showscale is True


class TestLegendBehavior:
    """Tests for legend behavior across trace builders."""

    def test_showlegend_parameter_respected(self, grouped_data):
        """Test that showlegend=False hides all legends."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point(showlegend=False)
        fig = p.draw()

        for trace in fig.data:
            assert trace.showlegend is False

    def test_legendgroup_prevents_duplicates(self, grouped_data):
        """Test that legendgroup is set for faceting support."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        for trace in fig.data:
            assert trace.legendgroup is not None
            assert trace.legendgroup == trace.name


class TestSizeMappingAcrossBuilders:
    """Tests for size aesthetic mapping across different builders."""

    def test_size_literal_in_single_trace(self, simple_data):
        """Test literal size in single trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(size=20)
        fig = p.draw()

        assert fig.data[0].marker.size == 20

    def test_size_mapped_in_single_trace(self):
        """Test mapped size in single trace."""
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'size_val': [5, 10, 15]
        })
        p = ggplot(data, aes(x='x', y='y', size='size_val')) + geom_point()
        fig = p.draw()

        assert list(fig.data[0].marker.size) == [5, 10, 15]

    def test_size_mapped_in_grouped_traces(self, grouped_data):
        """Test that size is preserved when splitting by color."""
        grouped_data['size_val'] = [5, 10, 15, 20, 25, 30]
        p = ggplot(grouped_data, aes(x='x', y='y', color='group', size='size_val')) + geom_point()
        fig = p.draw()

        # Both traces should have size values
        for trace in fig.data:
            assert trace.marker.size is not None


class TestOpacityAcrossBuilders:
    """Tests for opacity/alpha across different builders."""

    def test_opacity_in_single_trace(self, simple_data):
        """Test opacity in single trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(alpha=0.3)
        fig = p.draw()

        assert fig.data[0].opacity == 0.3

    def test_opacity_in_grouped_traces(self, grouped_data):
        """Test opacity is applied to all grouped traces."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point(alpha=0.5)
        fig = p.draw()

        for trace in fig.data:
            assert trace.opacity == 0.5


class TestDataIntegrity:
    """Tests to verify data integrity through trace building."""

    def test_no_data_loss_single_trace(self, simple_data):
        """Test that no data is lost in single trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()

        total_points = len(fig.data[0].x)
        assert total_points == len(simple_data)

    def test_no_data_loss_grouped_traces(self, grouped_data):
        """Test that no data is lost when splitting into groups."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        total_points = sum(len(trace.x) for trace in fig.data)
        assert total_points == len(grouped_data)

    def test_data_correctly_partitioned(self, grouped_data):
        """Test that data is correctly partitioned by group."""
        p = ggplot(grouped_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        # Collect all x values from all traces
        all_x = []
        for trace in fig.data:
            all_x.extend(list(trace.x))

        # Should match original data
        assert sorted(all_x) == sorted(grouped_data['x'].tolist())


class TestEmptyGroups:
    """Tests for handling empty groups (e.g., in faceting scenarios)."""

    def test_empty_group_skipped(self):
        """Test that empty groups don't create empty traces."""
        # Create data where one potential group value has no data
        data = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'group': ['A', 'A', 'A']  # No 'B' data
        })

        p = ggplot(data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        # Should only have 1 trace for 'A', not an empty trace for 'B'
        assert len(fig.data) == 1
        assert fig.data[0].name == 'A'
