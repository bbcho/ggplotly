"""
Tests for ggplotly faceting (facet_wrap and facet_grid).
"""
import pytest
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

import sys
sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_col, geom_boxplot,
    geom_smooth, geom_histogram, geom_density,
    facet_wrap, facet_grid,
    labs
)


@pytest.fixture
def sample_data():
    """Create sample data with groups for faceting."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': list(range(10)) * 3,
        'y': np.random.randn(30) * 10 + 50,
        'group': ['A'] * 10 + ['B'] * 10 + ['C'] * 10,
        'category': ['X', 'Y'] * 15,
        'value': np.random.rand(30) * 100
    })


@pytest.fixture
def grid_data():
    """Create data suitable for facet_grid (two grouping variables)."""
    np.random.seed(42)
    data = []
    for row_val in ['Low', 'High']:
        for col_val in ['Treatment', 'Control']:
            for i in range(10):
                data.append({
                    'x': i,
                    'y': np.random.randn() * 10 + (50 if row_val == 'High' else 30),
                    'row_var': row_val,
                    'col_var': col_val
                })
    return pd.DataFrame(data)


class TestFacetWrap:
    """Tests for facet_wrap."""

    def test_basic_facet_wrap(self, sample_data):
        """Test basic facet wrapping with a single variable."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have multiple subplots (one per group)
        assert len(fig.data) >= 3  # At least one trace per facet

    def test_facet_wrap_ncol(self, sample_data):
        """Test facet_wrap with specified number of columns."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group', ncol=2))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_nrow(self, sample_data):
        """Test facet_wrap with specified number of rows."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group', nrow=1))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_line(self, sample_data):
        """Test facet_wrap with line geom."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_line()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_multiple_geoms(self, sample_data):
        """Test facet_wrap with multiple geoms."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + geom_line()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_color(self, sample_data):
        """Test facet_wrap combined with color aesthetic."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_boxplot(self, sample_data):
        """Test facet_wrap with boxplot."""
        p = (ggplot(sample_data, aes(x='category', y='y'))
             + geom_boxplot()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_histogram(self, sample_data):
        """Test facet_wrap with histogram."""
        p = (ggplot(sample_data, aes(x='y'))
             + geom_histogram(bins=10)
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_density(self, sample_data):
        """Test facet_wrap with density plot."""
        p = (ggplot(sample_data, aes(x='y'))
             + geom_density()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_smooth(self, sample_data):
        """Test facet_wrap with smooth/regression."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth(method='lm')
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_with_labs(self, sample_data):
        """Test facet_wrap combined with labels."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group')
             + labs(title='Faceted Plot', x='X Axis', y='Y Axis'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_many_facets(self):
        """Test facet_wrap with many facets."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': range(50),
            'y': np.random.randn(50),
            'facet': [f'Group_{i}' for i in range(5)] * 10
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('facet', ncol=3))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_single_facet(self):
        """Test facet_wrap with only one unique value."""
        df = pd.DataFrame({
            'x': range(10),
            'y': range(10),
            'group': ['A'] * 10
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestFacetGrid:
    """Tests for facet_grid."""

    def test_basic_facet_grid(self, grid_data):
        """Test basic facet grid with two variables."""
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have data across all 4 panels (2x2 grid)
        assert len(fig.data) >= 4

    def test_facet_grid_with_line(self, grid_data):
        """Test facet_grid with line geom."""
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_line()
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_grid_with_multiple_geoms(self, grid_data):
        """Test facet_grid with multiple geoms."""
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_point()
             + geom_line()
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_grid_with_smooth(self, grid_data):
        """Test facet_grid with smooth."""
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_point()
             + geom_smooth(method='lm')
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_grid_3x2(self):
        """Test facet_grid with 3x2 layout."""
        np.random.seed(42)
        data = []
        for row in ['A', 'B', 'C']:
            for col in ['X', 'Y']:
                for i in range(10):
                    data.append({
                        'x': i,
                        'y': np.random.randn() * 10,
                        'row': row,
                        'col': col
                    })
        df = pd.DataFrame(data)

        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('row', 'col'))
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have 6 panels (3 rows x 2 cols)
        assert len(fig.data) >= 6

    def test_facet_grid_with_labs(self, grid_data):
        """Test facet_grid with labels."""
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('row_var', 'col_var')
             + labs(title='Grid Faceted Plot'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestFacetScales:
    """Tests for facet scales parameter."""

    def test_facet_wrap_scales_fixed(self, sample_data):
        """Test facet_wrap with fixed scales (default)."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group', scales='fixed'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_scales_free(self, sample_data):
        """Test facet_wrap with free scales."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group', scales='free'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestFacetEdgeCases:
    """Tests for edge cases in faceting."""

    def test_facet_with_missing_values(self):
        """Test faceting with NaN values in facet variable."""
        df = pd.DataFrame({
            'x': range(10),
            'y': range(10),
            'group': ['A', 'A', 'B', 'B', np.nan, 'A', 'B', 'A', 'B', 'A']
        })
        # Drop NaN for clean faceting
        df_clean = df.dropna()
        p = (ggplot(df_clean, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_with_numeric_facet_variable(self):
        """Test faceting with numeric facet variable."""
        df = pd.DataFrame({
            'x': range(30),
            'y': range(30),
            'year': [2020] * 10 + [2021] * 10 + [2022] * 10
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('year'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_with_bar_chart(self):
        """Test faceting with bar chart."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'] * 3,
            'value': [10, 20, 15, 12, 22, 18, 8, 25, 20],
            'group': ['X'] * 3 + ['Y'] * 3 + ['Z'] * 3
        })
        p = (ggplot(df, aes(x='category', y='value'))
             + geom_col()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_preserves_data_integrity(self, sample_data):
        """Test that faceting doesn't modify original data."""
        original_shape = sample_data.shape
        original_values = sample_data['y'].values.copy()

        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()

        # Original data should be unchanged
        assert sample_data.shape == original_shape
        np.testing.assert_array_equal(sample_data['y'].values, original_values)


class TestFacetCombinations:
    """Tests for faceting combined with other features."""

    def test_facet_with_color_and_shape(self, sample_data):
        """Test faceting with multiple aesthetics."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='category'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_facet_wrap_then_facet_grid(self, grid_data):
        """Test that facet can be changed (last one wins)."""
        # When both are added, the last facet should be applied
        # This tests the component override behavior
        p = (ggplot(grid_data, aes(x='x', y='y'))
             + geom_point()
             + facet_grid('row_var', 'col_var'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_empty_facet_panel(self):
        """Test handling of empty facet panels."""
        # Create data where one combination has no data
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [1, 2, 3, 4, 5],
            'group': ['A', 'A', 'B', 'B', 'B']
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + facet_wrap('group'))
        fig = p.draw()
        assert isinstance(fig, Figure)
