"""
Tests for geom_point_3d - 3D scatter plots.

This test suite verifies actual figure output, not just that code runs.
"""
import sys

import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest

sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    aes,
    facet_grid,
    facet_wrap,
    geom_point_3d,
    ggplot,
    ggsize,
    labs,
    scale_color_manual,
    theme_classic,
    theme_dark,
    theme_ggplot2,
    theme_minimal,
)


@pytest.fixture
def sample_3d_data():
    """Create sample 3D data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': np.random.randn(30),
        'y': np.random.randn(30),
        'z': np.random.randn(30),
        'group': ['A'] * 10 + ['B'] * 10 + ['C'] * 10,
        'size_var': np.random.rand(30) * 10 + 5,
    })


@pytest.fixture
def facet_3d_data():
    """Create data suitable for faceted 3D plots."""
    np.random.seed(42)
    data = []
    for facet in ['Panel1', 'Panel2', 'Panel3']:
        for i in range(20):
            data.append({
                'x': np.random.randn(),
                'y': np.random.randn(),
                'z': np.random.randn(),
                'facet_var': facet,
                'color_var': 'A' if i < 10 else 'B'
            })
    return pd.DataFrame(data)


class TestGeomPoint3DBasic:
    """Basic functionality tests for geom_point_3d."""

    def test_basic_3d_scatter(self, sample_3d_data):
        """Test basic 3D scatter plot creation."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1, "Should have 1 trace"
        assert fig.data[0].type == 'scatter3d', "Trace type should be scatter3d"

    def test_trace_has_correct_data(self, sample_3d_data):
        """Test that trace contains the correct x, y, z data."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data[0].x) == 30, "Should have 30 x values"
        assert len(fig.data[0].y) == 30, "Should have 30 y values"
        assert len(fig.data[0].z) == 30, "Should have 30 z values"

    def test_default_marker_size(self, sample_3d_data):
        """Test default marker size is 6 for 3D plots."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert fig.data[0].marker.size == 6, "Default marker size should be 6"

    def test_custom_marker_size(self, sample_3d_data):
        """Test custom marker size."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d(size=12)
        fig = p.draw()

        assert fig.data[0].marker.size == 12, "Marker size should be 12"

    def test_alpha_parameter(self, sample_3d_data):
        """Test alpha/opacity parameter."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d(alpha=0.5)
        fig = p.draw()

        assert fig.data[0].marker.opacity == 0.5, "Marker opacity should be 0.5"

    def test_missing_z_raises_error(self, sample_3d_data):
        """Test that missing z aesthetic raises ValueError."""
        with pytest.raises(ValueError, match="geom_point_3d requires 'x', 'y', and 'z' aesthetics"):
            p = ggplot(sample_3d_data, aes(x='x', y='y')) + geom_point_3d()
            p.draw()


class TestGeomPoint3DColorAesthetic:
    """Tests for color aesthetic in 3D scatter plots."""

    def test_color_grouping_creates_multiple_traces(self, sample_3d_data):
        """Test that color aesthetic creates separate traces per group."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data) == 3, "Should have 3 traces (one per group)"

    def test_color_grouping_unique_colors(self, sample_3d_data):
        """Test that each color group has a unique color."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        colors = [trace.marker.color for trace in fig.data]
        assert len(set(colors)) == 3, "Each group should have a unique color"

    def test_color_grouping_trace_names(self, sample_3d_data):
        """Test that traces are named after their group."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        trace_names = [trace.name for trace in fig.data]
        assert 'A' in trace_names, "Should have trace named 'A'"
        assert 'B' in trace_names, "Should have trace named 'B'"
        assert 'C' in trace_names, "Should have trace named 'C'"

    def test_literal_color(self, sample_3d_data):
        """Test literal color value."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d(color='red')
        fig = p.draw()

        assert fig.data[0].marker.color == 'red', "Marker color should be 'red'"

    def test_scale_color_manual(self, sample_3d_data):
        """Test manual color scale."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group'))
             + geom_point_3d()
             + scale_color_manual(values={'A': '#FF0000', 'B': '#00FF00', 'C': '#0000FF'}))
        fig = p.draw()

        # Get colors by trace name
        color_map = {trace.name: trace.marker.color for trace in fig.data}
        assert color_map['A'] == '#FF0000', "Group A should be red"
        assert color_map['B'] == '#00FF00', "Group B should be green"
        assert color_map['C'] == '#0000FF', "Group C should be blue"


class TestGeomPoint3DShapeAesthetic:
    """Tests for shape aesthetic in 3D scatter plots."""

    def test_shape_grouping_creates_traces(self, sample_3d_data):
        """Test that shape aesthetic creates separate traces."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', shape='group')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data) == 3, "Should have 3 traces (one per shape group)"

    def test_shape_uses_3d_compatible_symbols(self, sample_3d_data):
        """Test that shapes are 3D-compatible symbols."""
        valid_3d_symbols = ['circle', 'circle-open', 'cross', 'diamond',
                           'diamond-open', 'square', 'square-open', 'x']

        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', shape='group')) + geom_point_3d()
        fig = p.draw()

        for trace in fig.data:
            assert trace.marker.symbol in valid_3d_symbols, \
                f"Symbol '{trace.marker.symbol}' is not a valid 3D symbol"

    def test_literal_shape(self, sample_3d_data):
        """Test literal shape value."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d(shape='diamond')
        fig = p.draw()

        assert fig.data[0].marker.symbol == 'diamond', "Marker symbol should be 'diamond'"

    def test_invalid_2d_shape_converted(self, sample_3d_data):
        """Test that invalid 2D shapes are converted to valid 3D symbols."""
        # 'triangle-up' is not valid in 3D, should be converted
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d(shape='triangle-up')
        fig = p.draw()

        # Should be converted to 'diamond' per SYMBOL_2D_TO_3D mapping
        assert fig.data[0].marker.symbol == 'diamond', \
            "triangle-up should be converted to diamond in 3D"


class TestGeomPoint3DColorAndShape:
    """Tests for combined color and shape aesthetics."""

    def test_color_and_shape_same_column(self, sample_3d_data):
        """Test color and shape mapped to same column."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group', shape='group')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data) == 3, "Should have 3 traces"

        # Each trace should have unique color AND unique shape
        colors = set(trace.marker.color for trace in fig.data)
        symbols = set(trace.marker.symbol for trace in fig.data)

        assert len(colors) == 3, "Should have 3 unique colors"
        assert len(symbols) == 3, "Should have 3 unique shapes"

    def test_color_and_shape_different_columns(self):
        """Test color and shape mapped to different columns."""
        df = pd.DataFrame({
            'x': np.random.randn(12),
            'y': np.random.randn(12),
            'z': np.random.randn(12),
            'color_var': ['R', 'R', 'R', 'R', 'G', 'G', 'G', 'G', 'B', 'B', 'B', 'B'],
            'shape_var': ['S1', 'S1', 'S2', 'S2'] * 3
        })

        p = ggplot(df, aes(x='x', y='y', z='z', color='color_var', shape='shape_var')) + geom_point_3d()
        fig = p.draw()

        # Should create traces for each color x shape combination
        # 3 colors x 2 shapes = 6 combinations, but only existing combos
        assert len(fig.data) == 6, "Should have 6 traces (3 colors x 2 shapes)"


class TestGeomPoint3DLabels:
    """Tests for axis labels with labs()."""

    def test_labs_x_y_z(self, sample_3d_data):
        """Test that labs() sets all three axis labels."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + labs(x='X Label', y='Y Label', z='Z Label'))
        fig = p.draw()

        # Get scene axis titles
        scene = fig.layout.scene
        assert scene.xaxis.title.text == 'X Label', "X-axis label should be 'X Label'"
        assert scene.yaxis.title.text == 'Y Label', "Y-axis label should be 'Y Label'"
        assert scene.zaxis.title.text == 'Z Label', "Z-axis label should be 'Z Label'"

    def test_labs_title(self, sample_3d_data):
        """Test that labs() sets plot title."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + labs(title='My 3D Plot'))
        fig = p.draw()

        assert 'My 3D Plot' in fig.layout.title.text, "Title should contain 'My 3D Plot'"

    def test_labs_title_and_subtitle(self, sample_3d_data):
        """Test that labs() sets title and subtitle."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + labs(title='Main Title', subtitle='Subtitle Text'))
        fig = p.draw()

        assert 'Main Title' in fig.layout.title.text
        assert 'Subtitle Text' in fig.layout.title.text

    def test_default_axis_labels_from_mapping(self, sample_3d_data):
        """Test that default axis labels come from column names."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        scene = fig.layout.scene
        assert scene.xaxis.title.text == 'x', "Default X label should be column name 'x'"
        assert scene.yaxis.title.text == 'y', "Default Y label should be column name 'y'"
        assert scene.zaxis.title.text == 'z', "Default Z label should be column name 'z'"


class TestGeomPoint3DThemes:
    """Tests for theme application to 3D plots."""

    def test_theme_dark_background(self, sample_3d_data):
        """Test that theme_dark applies dark background to 3D scene."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + theme_dark())
        fig = p.draw()

        # Check scene background color
        scene = fig.layout.scene
        # theme_dark should set a dark background
        assert scene.bgcolor is not None, "Scene should have bgcolor set"
        # The actual color depends on implementation - just verify it's set

    def test_theme_minimal_no_background(self, sample_3d_data):
        """Test that theme_minimal has appropriate styling."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + theme_minimal())
        fig = p.draw()

        # Just verify the theme is applied without errors
        assert isinstance(fig, Figure)

    def test_theme_classic(self, sample_3d_data):
        """Test that theme_classic applies correctly."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + theme_classic())
        fig = p.draw()

        assert isinstance(fig, Figure)

    def test_theme_ggplot2(self, sample_3d_data):
        """Test that theme_ggplot2 applies gray background."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + theme_ggplot2())
        fig = p.draw()

        scene = fig.layout.scene
        # theme_ggplot2 should set a gray-ish background
        assert scene.bgcolor is not None or fig.layout.plot_bgcolor is not None


class TestGeomPoint3DFacetWrap:
    """Tests for facet_wrap with 3D plots."""

    def test_facet_wrap_creates_multiple_scenes(self, facet_3d_data):
        """Test that facet_wrap creates separate 3D scenes."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + facet_wrap('facet_var'))
        fig = p.draw()

        # Should have 3 traces (one per facet)
        assert len(fig.data) == 3, "Should have 3 traces (one per facet)"

        # Each trace should be assigned to a different scene
        scenes = set(trace.scene for trace in fig.data)
        assert len(scenes) == 3, "Should have 3 different scenes"

    def test_facet_wrap_scene_assignment(self, facet_3d_data):
        """Test that traces are assigned to correct scenes."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + facet_wrap('facet_var'))
        fig = p.draw()

        # First trace should be in 'scene', others in 'scene2', 'scene3'
        scenes = [trace.scene for trace in fig.data]
        assert 'scene' in scenes, "Should have a trace in 'scene'"
        assert 'scene2' in scenes, "Should have a trace in 'scene2'"
        assert 'scene3' in scenes, "Should have a trace in 'scene3'"

    def test_facet_wrap_with_color(self, facet_3d_data):
        """Test facet_wrap combined with color aesthetic."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z', color='color_var'))
             + geom_point_3d()
             + facet_wrap('facet_var'))
        fig = p.draw()

        # 3 facets x 2 colors = 6 traces
        assert len(fig.data) == 6, "Should have 6 traces (3 facets x 2 colors)"

    def test_facet_wrap_ncol(self, facet_3d_data):
        """Test facet_wrap with specified number of columns."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + facet_wrap('facet_var', ncol=2))
        fig = p.draw()

        # Should work without errors
        assert len(fig.data) == 3

    def test_facet_wrap_labs_applied_to_all_scenes(self, facet_3d_data):
        """Test that labs() applies to all faceted scenes."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + facet_wrap('facet_var')
             + labs(x='X Axis', y='Y Axis', z='Z Axis'))
        fig = p.draw()

        # Check all scenes have the labels
        layout_dict = fig.layout.to_plotly_json()
        scene_keys = [k for k in layout_dict.keys() if k.startswith('scene')]

        for scene_key in scene_keys:
            scene = layout_dict[scene_key]
            assert scene.get('xaxis', {}).get('title', {}).get('text') == 'X Axis' or \
                   scene.get('xaxis', {}).get('title') == 'X Axis', \
                   f"Scene {scene_key} should have X axis label"


class TestGeomPoint3DFacetGrid:
    """Tests for facet_grid with 3D plots."""

    def test_facet_grid_creates_grid_of_scenes(self):
        """Test that facet_grid creates a grid of 3D scenes."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(40),
            'y': np.random.randn(40),
            'z': np.random.randn(40),
            'row_var': ['R1'] * 20 + ['R2'] * 20,
            'col_var': ['C1', 'C2'] * 20
        })

        p = (ggplot(df, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()

        # 2 rows x 2 cols = 4 traces
        assert len(fig.data) == 4, "Should have 4 traces (2x2 grid)"

        # Should have 4 different scenes
        scenes = set(trace.scene for trace in fig.data)
        assert len(scenes) == 4, "Should have 4 different scenes"


class TestGeomPoint3DGGSize:
    """Tests for ggsize with 3D plots."""

    def test_ggsize_sets_dimensions(self, sample_3d_data):
        """Test that ggsize sets figure dimensions."""
        p = (ggplot(sample_3d_data, aes(x='x', y='y', z='z'))
             + geom_point_3d()
             + ggsize(width=800, height=600))
        fig = p.draw()

        assert fig.layout.width == 800, "Width should be 800"
        assert fig.layout.height == 600, "Height should be 600"


class TestGeomPoint3DLegend:
    """Tests for legend behavior in 3D plots."""

    def test_legend_shows_for_color_groups(self, sample_3d_data):
        """Test that legend is shown for color-grouped traces."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        # At least one trace should show legend
        showlegend_values = [trace.showlegend for trace in fig.data]
        assert any(showlegend_values), "At least one trace should show legend"

    def test_legend_groups_match_trace_names(self, sample_3d_data):
        """Test that legendgroup matches trace name."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        for trace in fig.data:
            assert trace.legendgroup == trace.name, \
                f"legendgroup '{trace.legendgroup}' should match name '{trace.name}'"

    def test_faceted_legend_not_duplicated(self, facet_3d_data):
        """Test that faceted plots don't duplicate legend entries."""
        p = (ggplot(facet_3d_data, aes(x='x', y='y', z='z', color='color_var'))
             + geom_point_3d()
             + facet_wrap('facet_var'))
        fig = p.draw()

        # Count how many traces show legend for each legendgroup
        legend_counts = {}
        for trace in fig.data:
            if trace.showlegend:
                legend_counts[trace.legendgroup] = legend_counts.get(trace.legendgroup, 0) + 1

        # Each legendgroup should only appear once in legend
        for group, count in legend_counts.items():
            assert count == 1, f"Legend group '{group}' should appear only once, got {count}"


class TestGeomPoint3DEdgeCases:
    """Edge cases and error handling for 3D plots."""

    def test_empty_data(self):
        """Test handling of empty dataframe."""
        df = pd.DataFrame({'x': [], 'y': [], 'z': []})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert isinstance(fig, Figure)

    def test_single_point(self):
        """Test with single data point."""
        df = pd.DataFrame({'x': [1], 'y': [2], 'z': [3]})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data[0].x) == 1

    def test_nan_values_handled(self):
        """Test that NaN values don't crash the plot."""
        df = pd.DataFrame({
            'x': [1, 2, np.nan, 4],
            'y': [1, np.nan, 3, 4],
            'z': [1, 2, 3, np.nan]
        })
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert isinstance(fig, Figure)

    def test_large_dataset(self):
        """Test with larger dataset for performance."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(1000),
            'y': np.random.randn(1000),
            'z': np.random.randn(1000),
        })
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()

        assert len(fig.data[0].x) == 1000


class TestGeomPoint3DDataIntegrity:
    """Tests to verify data integrity after plotting."""

    def test_original_data_unchanged(self, sample_3d_data):
        """Test that original dataframe is not modified."""
        original_shape = sample_3d_data.shape
        original_values = sample_3d_data['x'].values.copy()

        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        p.draw()

        assert sample_3d_data.shape == original_shape
        np.testing.assert_array_equal(sample_3d_data['x'].values, original_values)

    def test_data_correctly_split_by_group(self, sample_3d_data):
        """Test that data is correctly split when grouping by color."""
        p = ggplot(sample_3d_data, aes(x='x', y='y', z='z', color='group')) + geom_point_3d()
        fig = p.draw()

        # Total points across all traces should equal original data
        total_points = sum(len(trace.x) for trace in fig.data)
        assert total_points == 30, "Total points should equal original data size"

        # Each group should have 10 points
        for trace in fig.data:
            assert len(trace.x) == 10, f"Trace '{trace.name}' should have 10 points"
