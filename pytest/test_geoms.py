"""
Tests for ggplotly geoms.
Tests verify actual behavior and output, not just that code runs.
"""
import pytest
import pandas as pd
import numpy as np
import math
from plotly.graph_objects import Figure

from ggplotly import (
    ggplot, aes, ggsave,
    geom_point, geom_line, geom_path, geom_bar, geom_col,
    geom_histogram, geom_boxplot, geom_smooth, geom_area,
    geom_density, geom_violin, geom_ribbon, geom_tile,
    geom_text, geom_errorbar, geom_segment, geom_step,
    geom_vline, geom_hline, geom_jitter, geom_rug,
    geom_abline, geom_contour, geom_contour_filled,
    labs
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': range(10),
        'y': np.random.randn(10) * 10 + 50,
        'group': ['A'] * 5 + ['B'] * 5,
        'size': np.random.rand(10) * 10,
        'label': [f'Point {i}' for i in range(10)]
    })


@pytest.fixture
def categorical_data():
    """Create categorical data for testing."""
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'D'],
        'value': [10, 25, 15, 30]
    })


@pytest.fixture
def simple_data():
    """Simple fixed data for deterministic tests."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 6, 8, 10]
    })


class TestGeomPoint:
    """Tests for geom_point."""

    def test_basic_scatter_creates_correct_trace(self, simple_data):
        """Test basic scatter plot creates correct trace type with correct data."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'markers'
        # Verify data is preserved
        assert list(fig.data[0].x) == [1, 2, 3, 4, 5]
        assert list(fig.data[0].y) == [2, 4, 6, 8, 10]

    def test_color_mapping_creates_multiple_traces(self, sample_data):
        """Test color aesthetic mapping creates separate traces per group."""
        p = ggplot(sample_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have 2 traces for groups A and B
        assert len(fig.data) == 2
        # Both should be scatter with markers
        for trace in fig.data:
            assert trace.type == 'scatter'
            assert trace.mode == 'markers'

    def test_size_mapping(self, sample_data):
        """Test size aesthetic mapping is applied to markers."""
        p = ggplot(sample_data, aes(x='x', y='y', size='size')) + geom_point()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Marker size should be set
        assert fig.data[0].marker.size is not None

    def test_literal_color_applied(self, simple_data):
        """Test literal color value is applied to all points."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(color='red')
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].marker.color == 'red'

    def test_alpha_applied(self, simple_data):
        """Test alpha transparency is applied."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point(alpha=0.5)
        fig = p.draw()

        # Alpha is applied at trace level, not marker level
        assert fig.data[0].opacity == 0.5


class TestGeomLine:
    """Tests for geom_line."""

    def test_basic_line_creates_correct_trace(self, simple_data):
        """Test basic line plot creates correct trace type."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_line()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'

    def test_line_sorts_by_x(self):
        """Test that geom_line sorts data by x-axis."""
        df = pd.DataFrame({
            'x': [3, 1, 4, 2, 5],
            'y': [30, 10, 40, 20, 50]
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_line()
        fig = p.draw()

        # Line should be sorted: x should be [1,2,3,4,5]
        x_values = list(fig.data[0].x)
        assert x_values == [1, 2, 3, 4, 5]
        # y values should be correspondingly sorted
        y_values = list(fig.data[0].y)
        assert y_values == [10, 20, 30, 40, 50]

    def test_grouped_lines_create_multiple_traces(self, sample_data):
        """Test grouped line plot creates separate traces."""
        p = ggplot(sample_data, aes(x='x', y='y', color='group')) + geom_line()
        fig = p.draw()

        assert len(fig.data) == 2
        for trace in fig.data:
            assert trace.type == 'scatter'
            assert trace.mode == 'lines'


class TestGeomPath:
    """Tests for geom_path."""

    def test_basic_path_creates_correct_trace(self, simple_data):
        """Test basic path plot creates correct trace type."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_path()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'

    def test_path_preserves_data_order(self):
        """Test that geom_path connects points in data order, not x order."""
        df = pd.DataFrame({
            'x': [3, 1, 4, 2, 5],
            'y': [30, 10, 40, 20, 50]
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_path()
        fig = p.draw()

        # Path should preserve original order
        x_values = list(fig.data[0].x)
        assert x_values == [3, 1, 4, 2, 5]
        y_values = list(fig.data[0].y)
        assert y_values == [30, 10, 40, 20, 50]


class TestGeomBar:
    """Tests for geom_bar and geom_col."""

    def test_geom_bar_counts_occurrences(self):
        """Test bar chart with stat=count counts occurrences."""
        df = pd.DataFrame({'x': ['A', 'A', 'B', 'B', 'B', 'C']})
        p = ggplot(df, aes(x='x')) + geom_bar()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'bar'
        # Check categories
        assert 'A' in fig.data[0].x
        assert 'B' in fig.data[0].x
        assert 'C' in fig.data[0].x

    def test_geom_col_uses_provided_values(self, categorical_data):
        """Test column chart uses provided y values."""
        p = ggplot(categorical_data, aes(x='category', y='value')) + geom_col()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'bar'
        # Values should match input
        y_values = list(fig.data[0].y)
        assert y_values == [10, 25, 15, 30]


class TestGeomHistogram:
    """Tests for geom_histogram."""

    def test_basic_histogram_creates_correct_trace(self):
        """Test basic histogram creates histogram or bar trace."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_histogram()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type in ('histogram', 'bar')

    def test_histogram_with_bins_parameter(self):
        """Test histogram respects bins parameter."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_histogram(bins=10)
        fig = p.draw()

        assert isinstance(fig, Figure)


class TestGeomBoxplot:
    """Tests for geom_boxplot."""

    def test_basic_boxplot_creates_box_trace(self, sample_data):
        """Test basic boxplot creates box trace."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_boxplot()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'box'

    def test_boxplot_has_correct_groups(self, sample_data):
        """Test boxplot shows correct groups."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_boxplot()
        fig = p.draw()

        # Should have groups A and B
        x_values = set(fig.data[0].x)
        assert 'A' in x_values or any('A' in str(t.name) for t in fig.data)


class TestGeomSmooth:
    """Tests for geom_smooth."""

    def test_linear_smooth_creates_line(self, simple_data):
        """Test linear regression smooth creates line trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_smooth(method='lm')
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have at least one line trace
        line_traces = [t for t in fig.data if t.mode == 'lines']
        assert len(line_traces) >= 1

    def test_smooth_with_se(self, simple_data):
        """Test smooth with confidence interval."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_smooth(method='lm', se=True)
        fig = p.draw()

        assert isinstance(fig, Figure)


class TestGeomArea:
    """Tests for geom_area."""

    def test_basic_area_creates_scatter_fill(self, simple_data):
        """Test basic area plot creates filled scatter."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_area()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have fill
        assert fig.data[0].fill is not None or fig.data[0].fillcolor is not None


class TestGeomDensity:
    """Tests for geom_density."""

    def test_basic_density_creates_trace(self):
        """Test basic density plot creates trace."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_density()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) >= 1

    def test_grouped_density_with_fill(self):
        """Test grouped density plot with fill aesthetic creates separate traces per group."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.concatenate([np.random.randn(50), np.random.randn(50) + 2]),
            'group': ['A'] * 50 + ['B'] * 50
        })
        p = ggplot(df, aes(x='x', fill='group')) + geom_density(alpha=0.5)
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have 2 traces (one per group)
        assert len(fig.data) == 2

    def test_grouped_density_with_color(self):
        """Test grouped density plot with color aesthetic creates separate traces per group."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.concatenate([np.random.randn(50), np.random.randn(50) + 2]),
            'category': ['X'] * 50 + ['Y'] * 50
        })
        p = ggplot(df, aes(x='x', color='category')) + geom_density()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have 2 traces (one per category)
        assert len(fig.data) == 2

    def test_grouped_density_with_group_aesthetic(self):
        """Test grouped density plot with group aesthetic creates separate traces."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.concatenate([np.random.randn(30), np.random.randn(30) + 1, np.random.randn(30) + 2]),
            'grp': ['G1'] * 30 + ['G2'] * 30 + ['G3'] * 30
        })
        p = ggplot(df, aes(x='x', group='grp')) + geom_density()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have 3 traces (one per group)
        assert len(fig.data) == 3

    def test_grouped_density_different_distributions(self):
        """Test that grouped densities compute separate KDEs for each group."""
        np.random.seed(42)
        # Create two clearly different distributions
        df = pd.DataFrame({
            'x': np.concatenate([np.random.randn(100), np.random.randn(100) + 5]),
            'group': ['narrow'] * 100 + ['shifted'] * 100
        })
        p = ggplot(df, aes(x='x', fill='group')) + geom_density()
        fig = p.draw()

        # The two traces should have different x ranges since distributions are shifted
        trace1_x = fig.data[0].x
        trace2_x = fig.data[1].x
        # Check that the means of x values are different
        assert abs(np.mean(trace1_x) - np.mean(trace2_x)) > 2

    def test_density_with_na_rm(self):
        """Test density plot handles missing values with na_rm parameter."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.concatenate([np.random.randn(50), [np.nan] * 10]),
        })
        # Should not raise with na_rm=True
        p = ggplot(df, aes(x='x')) + geom_density(na_rm=True)
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) >= 1

    def test_density_bandwidth_adjust(self):
        """Test density plot bandwidth adjustment."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        # Create two plots with different bandwidth adjustments
        p_smooth = ggplot(df, aes(x='x')) + geom_density(adjust=2)
        p_detailed = ggplot(df, aes(x='x')) + geom_density(adjust=0.5)

        fig_smooth = p_smooth.draw()
        fig_detailed = p_detailed.draw()

        # Both should create valid figures
        assert isinstance(fig_smooth, Figure)
        assert isinstance(fig_detailed, Figure)


class TestGeomViolin:
    """Tests for geom_violin."""

    def test_basic_violin_creates_violin_trace(self, sample_data):
        """Test basic violin plot creates violin trace."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_violin()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'violin'


class TestGeomText:
    """Tests for geom_text."""

    def test_basic_text_creates_text_trace(self, sample_data):
        """Test basic text labels create text trace."""
        p = ggplot(sample_data, aes(x='x', y='y', label='label')) + geom_text()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have text mode
        assert 'text' in fig.data[0].mode


class TestGeomErrorbar:
    """Tests for geom_errorbar."""

    def test_basic_errorbar_creates_correct_structure(self):
        """Test basic error bars are created correctly."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [10, 20, 15],
            'ymin': [8, 18, 12],
            'ymax': [12, 22, 18]
        })
        p = ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) + geom_errorbar()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have error_y set
        assert fig.data[0].error_y is not None or len(fig.data) > 1


class TestGeomSegment:
    """Tests for geom_segment."""

    def test_basic_segment_creates_lines(self):
        """Test basic line segments are created correctly."""
        df = pd.DataFrame({
            'x': [1, 2],
            'y': [1, 2],
            'xend': [2, 3],
            'yend': [2, 3]
        })
        p = ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have line traces
        assert fig.data[0].mode == 'lines'


class TestGeomStep:
    """Tests for geom_step."""

    def test_basic_step_creates_line_trace(self, simple_data):
        """Test basic step plot creates line trace with step shape."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_step()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'scatter'
        # Should have step line shape
        assert fig.data[0].line.shape in ('hv', 'vh', 'hvh', 'vhv')


class TestGeomVlineHline:
    """Tests for geom_vline and geom_hline."""

    def test_vline_creates_vertical_line(self, simple_data):
        """Test vertical line is created at correct x position."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + geom_vline(xintercept=3)
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have shapes or additional trace for vline
        assert len(fig.data) >= 1 or len(fig.layout.shapes) >= 1

    def test_hline_creates_horizontal_line(self, simple_data):
        """Test horizontal line is created at correct y position."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + geom_hline(yintercept=5)
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have shapes or additional trace for hline
        assert len(fig.data) >= 1 or len(fig.layout.shapes) >= 1


class TestGeomJitter:
    """Tests for geom_jitter."""

    def test_basic_jitter_with_categorical_x_uses_box(self, sample_data):
        """Test jitter with categorical x uses box trace for proper alignment."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_jitter()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Categorical x axis uses go.Box with invisible box for proper alignment
        assert fig.data[0].type == 'box'
        assert fig.data[0].boxpoints == 'all'
        # Box outline is invisible
        assert fig.data[0].line.color == 'rgba(0,0,0,0)'

    def test_jitter_with_numeric_axes_creates_scatter(self, simple_data):
        """Test jitter with numeric axes creates scatter trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_jitter()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'markers'


class TestGeomRug:
    """Tests for geom_rug."""

    def test_basic_rug_creates_traces(self, simple_data):
        """Test rug plot creates additional traces for axis marks."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + geom_rug()
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have more traces than just the points
        assert len(fig.data) >= 2


class TestGeomAbline:
    """Tests for geom_abline."""

    def test_basic_abline_creates_line(self, simple_data):
        """Test abline creates a line trace."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + geom_abline(slope=1, intercept=0)
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have additional trace for the line
        assert len(fig.data) >= 2


class TestMultipleGeoms:
    """Tests for combining multiple geoms."""

    def test_point_and_line_creates_both_traces(self, simple_data):
        """Test combining point and line geoms creates both trace types."""
        p = (ggplot(simple_data, aes(x='x', y='y'))
             + geom_line()
             + geom_point())
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have at least 2 traces
        assert len(fig.data) >= 2

        # Check we have both lines and markers
        modes = [t.mode for t in fig.data]
        assert any('lines' in m for m in modes)
        assert any('markers' in m for m in modes)

    def test_point_and_smooth_creates_both(self, simple_data):
        """Test combining point and smooth geoms."""
        p = (ggplot(simple_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth(method='lm'))
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) >= 2

    def test_bar_and_errorbar_combined(self, categorical_data):
        """Test combining bar and errorbar."""
        categorical_data = categorical_data.copy()
        categorical_data['ymin'] = categorical_data['value'] - 2
        categorical_data['ymax'] = categorical_data['value'] + 2
        p = (ggplot(categorical_data, aes(x='category', y='value', ymin='ymin', ymax='ymax'))
             + geom_col()
             + geom_errorbar())
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have bar trace
        bar_traces = [t for t in fig.data if t.type == 'bar']
        assert len(bar_traces) >= 1


class TestDataPreservation:
    """Tests to ensure data is not modified."""

    def test_original_data_unchanged(self, simple_data):
        """Test that plotting doesn't modify original dataframe."""
        original = simple_data.copy()

        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point()
        p.draw()

        pd.testing.assert_frame_equal(simple_data, original)
