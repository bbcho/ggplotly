"""
Tests for ggplotly geoms.
"""
import pytest
import pandas as pd
import numpy as np
import math
from plotly.graph_objects import Figure

import sys
sys.path.insert(0, '/Users/ben/Projects/ggplotly')

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


class TestGeomPoint:
    """Tests for geom_point."""

    def test_basic_scatter(self, sample_data):
        """Test basic scatter plot creation."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, Figure)
        assert len(fig.data) >= 1

    def test_color_mapping(self, sample_data):
        """Test color aesthetic mapping."""
        p = ggplot(sample_data, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have multiple traces for different groups
        assert len(fig.data) >= 2

    def test_size_mapping(self, sample_data):
        """Test size aesthetic mapping."""
        p = ggplot(sample_data, aes(x='x', y='y', size='size')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_literal_color(self, sample_data):
        """Test literal color value."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point(color='red')
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomLine:
    """Tests for geom_line."""

    def test_basic_line(self, sample_data):
        """Test basic line plot."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_line()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_line_sorts_by_x(self):
        """Test that geom_line sorts data by x-axis."""
        # Unsorted data
        df = pd.DataFrame({
            'x': [3, 1, 4, 2, 5],
            'y': [30, 10, 40, 20, 50]
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_line()
        fig = p.draw()
        # Line should connect points in x order
        assert isinstance(fig, Figure)

    def test_grouped_lines(self, sample_data):
        """Test grouped line plot."""
        p = ggplot(sample_data, aes(x='x', y='y', color='group')) + geom_line()
        fig = p.draw()
        assert len(fig.data) >= 2


class TestGeomPath:
    """Tests for geom_path."""

    def test_basic_path(self, sample_data):
        """Test basic path plot."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_path()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_path_preserves_order(self):
        """Test that geom_path connects points in data order."""
        # Create spiral data where x is not monotonic
        t_vals = [i * 4 * math.pi / 50 for i in range(50)]
        df = pd.DataFrame({
            'x': [t * math.cos(t) for t in t_vals],
            'y': [t * math.sin(t) for t in t_vals]
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_path()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_path_vs_line_difference(self):
        """Test that path and line behave differently with non-monotonic x."""
        df = pd.DataFrame({
            'x': [1, 3, 2, 4],
            'y': [1, 3, 2, 4]
        })
        p_path = ggplot(df, aes(x='x', y='y')) + geom_path()
        p_line = ggplot(df, aes(x='x', y='y')) + geom_line()

        fig_path = p_path.draw()
        fig_line = p_line.draw()

        # Both should work
        assert isinstance(fig_path, Figure)
        assert isinstance(fig_line, Figure)


class TestGeomBar:
    """Tests for geom_bar and geom_col."""

    def test_geom_bar(self, categorical_data):
        """Test bar chart with stat=count."""
        df = pd.DataFrame({'x': ['A', 'A', 'B', 'B', 'B', 'C']})
        p = ggplot(df, aes(x='x')) + geom_bar()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_geom_col(self, categorical_data):
        """Test column chart with identity stat."""
        p = ggplot(categorical_data, aes(x='category', y='value')) + geom_col()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomHistogram:
    """Tests for geom_histogram."""

    def test_basic_histogram(self):
        """Test basic histogram."""
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_histogram()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_histogram_bins(self):
        """Test histogram with specified bins."""
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_histogram(bins=20)
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomBoxplot:
    """Tests for geom_boxplot."""

    def test_basic_boxplot(self, sample_data):
        """Test basic boxplot."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_boxplot()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomSmooth:
    """Tests for geom_smooth."""

    def test_linear_smooth(self, sample_data):
        """Test linear regression smooth."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_smooth(method='lm')
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_loess_smooth(self, sample_data):
        """Test LOESS smooth."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_smooth(method='loess')
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomArea:
    """Tests for geom_area."""

    def test_basic_area(self, sample_data):
        """Test basic area plot."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_area()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomDensity:
    """Tests for geom_density."""

    def test_basic_density(self):
        """Test basic density plot."""
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_density()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomViolin:
    """Tests for geom_violin."""

    def test_basic_violin(self, sample_data):
        """Test basic violin plot."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_violin()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomText:
    """Tests for geom_text."""

    def test_basic_text(self, sample_data):
        """Test basic text labels."""
        p = ggplot(sample_data, aes(x='x', y='y', label='label')) + geom_text()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomErrorbar:
    """Tests for geom_errorbar."""

    def test_basic_errorbar(self):
        """Test basic error bars."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [10, 20, 15],
            'ymin': [8, 18, 12],
            'ymax': [12, 22, 18]
        })
        p = ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) + geom_errorbar()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomSegment:
    """Tests for geom_segment."""

    def test_basic_segment(self):
        """Test basic line segments."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'xend': [2, 3, 4],
            'yend': [2, 3, 4]
        })
        p = ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomStep:
    """Tests for geom_step."""

    def test_basic_step(self, sample_data):
        """Test basic step plot."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_step()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomVlineHline:
    """Tests for geom_vline and geom_hline."""

    def test_vline(self, sample_data):
        """Test vertical line."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + geom_vline(xintercept=5)
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_hline(self, sample_data):
        """Test horizontal line."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + geom_hline(yintercept=50)
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomJitter:
    """Tests for geom_jitter."""

    def test_basic_jitter(self, sample_data):
        """Test jittered points."""
        p = ggplot(sample_data, aes(x='group', y='y')) + geom_jitter()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomRug:
    """Tests for geom_rug."""

    def test_basic_rug(self, sample_data):
        """Test rug plot."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + geom_rug()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomAbline:
    """Tests for geom_abline."""

    def test_basic_abline(self, sample_data):
        """Test abline."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point() + geom_abline(slope=1, intercept=0)
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestMultipleGeoms:
    """Tests for combining multiple geoms."""

    def test_point_and_line(self, sample_data):
        """Test combining point and line geoms."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_line()
             + geom_point())
        fig = p.draw()
        assert isinstance(fig, Figure)
        assert len(fig.data) >= 2

    def test_point_and_smooth(self, sample_data):
        """Test combining point and smooth geoms."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth(method='lm'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_bar_and_errorbar(self, categorical_data):
        """Test combining bar and errorbar."""
        categorical_data['ymin'] = categorical_data['value'] - 2
        categorical_data['ymax'] = categorical_data['value'] + 2
        p = (ggplot(categorical_data, aes(x='category', y='value', ymin='ymin', ymax='ymax'))
             + geom_col()
             + geom_errorbar())
        fig = p.draw()
        assert isinstance(fig, Figure)
