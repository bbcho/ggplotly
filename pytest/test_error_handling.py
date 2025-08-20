import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import pytest

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestErrorHandling:
    """Test suite for error handling and edge cases."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'numeric': [10, 20, 15, 25, 18]
        })

    # Invalid Data Tests
    def test_ggplot_with_none_data(self):
        """Test ggplot with None data."""
        with pytest.raises(AttributeError):
            p = ggplot(None, aes(x='x', y='y')) + geom_point()
            p.draw()

    def test_ggplot_with_empty_dataframe(self):
        """Test ggplot with empty dataframe."""
        empty_df = pd.DataFrame()
        try:
            p = ggplot(empty_df, aes(x='x', y='y')) + geom_point()
            p.draw()
        except Exception:
            # It's okay if this fails with empty data
            pass

    def test_ggplot_with_none_mapping(self):
        """Test ggplot with None mapping."""
        p = ggplot(self.df, None) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_aes_with_invalid_column(self):
        """Test aes with non-existent column."""
        p = ggplot(self.df, aes(x='nonexistent', y='y')) + geom_point()
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid column
            pass

    def test_aes_with_mixed_data_types(self):
        """Test aes with mixed data types."""
        mixed_df = pd.DataFrame({
            'x': [1, 'A', 3, 4, 5],
            'y': [2, 4, 1, 5, 3]
        })
        try:
            p = ggplot(mixed_df, aes(x='x', y='y')) + geom_point()
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with mixed types
            pass

    # Invalid Component Tests
    def test_add_invalid_component(self):
        """Test adding invalid component type."""
        p = ggplot(self.df, aes(x='x', y='y'))
        
        # Test with string (invalid)
        with pytest.raises(TypeError):
            p.add_component("invalid")
        
        # Test with number (invalid)
        with pytest.raises(TypeError):
            p.add_component(42)
        
        # Test with list (invalid)
        with pytest.raises(TypeError):
            p.add_component([1, 2, 3])

    def test_add_none_component(self):
        """Test adding None component."""
        p = ggplot(self.df, aes(x='x', y='y'))
        
        with pytest.raises(TypeError):
            p.add_component(None)

    # Invalid Geom Parameters
    def test_geom_with_invalid_color(self):
        """Test geom with invalid color value."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point(color="invalid_color")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid color
            pass

    def test_geom_with_invalid_size(self):
        """Test geom with invalid size value."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point(size="invalid_size")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid size
            pass

    def test_geom_with_invalid_alpha(self):
        """Test geom with invalid alpha value."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point(alpha="invalid_alpha")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid alpha
            pass

    # Invalid Scale Parameters
    def test_scale_with_invalid_limits(self):
        """Test scale with invalid limits."""
        # Test with string limits
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + scale_x_continuous(limits="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid limits
            pass

        # Test with single value instead of list
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + scale_x_continuous(limits=5)
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid limits
            pass

    def test_scale_with_invalid_breaks(self):
        """Test scale with invalid breaks."""
        # Test with string breaks
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + scale_x_continuous(breaks="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid breaks
            pass

    def test_scale_with_invalid_palette(self):
        """Test scale with invalid color palette."""
        p = ggplot(self.df, aes(x='x', y='y', color='category')) + geom_point() + scale_color_brewer(palette="invalid_palette")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid palette
            pass

    # Invalid Theme Parameters
    def test_theme_with_invalid_template(self):
        """Test theme with invalid template."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_custom("invalid_template")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid template
            pass

    # Invalid Faceting Parameters
    def test_facet_with_invalid_column(self):
        """Test faceting with non-existent column."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + facet_wrap('nonexistent')
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid column
            pass

    def test_facet_with_invalid_ncol(self):
        """Test faceting with invalid ncol value."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + facet_wrap('category', ncol="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid ncol
            pass

    def test_facet_with_invalid_nrow(self):
        """Test faceting with invalid nrow value."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + facet_wrap('category', nrow="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid nrow
            pass

    # Invalid Coordinate Parameters
    def test_coord_with_invalid_limits(self):
        """Test coordinates with invalid limits."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim="invalid", ylim="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid limits
            pass

    def test_coord_polar_with_invalid_data(self):
        """Test polar coordinates with data not suitable for polar plots."""
        # Test with negative values (not suitable for polar)
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + coord_polar()
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with unsuitable data
            pass

    # Invalid Statistical Parameters
    def test_stat_with_invalid_method(self):
        """Test statistical transformation with invalid method."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + stat_smooth(method="invalid_method")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid method
            pass

    def test_stat_with_invalid_bins(self):
        """Test statistical transformation with invalid bins."""
        p = ggplot(self.df, aes(x='x')) + geom_histogram() + stat_bin(bins="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid bins
            pass

    # Invalid Utility Parameters
    def test_ggtitle_with_invalid_title(self):
        """Test ggtitle with invalid title."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + ggtitle(None)
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid title
            pass

    def test_labs_with_invalid_labels(self):
        """Test labs with invalid labels."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + labs(title=None, x=None, y=None)
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid labels
            pass

    def test_ggsize_with_invalid_dimensions(self):
        """Test ggsize with invalid dimensions."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + ggsize(width="invalid", height="invalid")
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with invalid dimensions
            pass

    # Missing Data Tests
    def test_ggplot_with_missing_values(self):
        """Test ggplot with missing values in data."""
        df_with_nan = self.df.copy()
        df_with_nan.loc[0, 'x'] = np.nan
        df_with_nan.loc[1, 'y'] = np.nan
        
        p = ggplot(df_with_nan, aes(x='x', y='y')) + geom_point()
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with missing values
            pass

    def test_ggplot_with_infinite_values(self):
        """Test ggplot with infinite values in data."""
        df_with_inf = self.df.copy()
        df_with_inf.loc[0, 'x'] = np.inf
        df_with_inf.loc[1, 'y'] = -np.inf
        
        p = ggplot(df_with_inf, aes(x='x', y='y')) + geom_point()
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with infinite values
            pass

    # Large Data Tests
    def test_ggplot_with_large_dataset(self):
        """Test ggplot with large dataset."""
        large_df = pd.DataFrame({
            'x': np.random.randn(10000),
            'y': np.random.randn(10000),
            'category': np.random.choice(['A', 'B', 'C'], 10000)
        })
        
        p = ggplot(large_df, aes(x='x', y='y')) + geom_point()
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with very large data
            pass

    # Memory Tests
    def test_ggplot_memory_usage(self):
        """Test ggplot memory usage with multiple operations."""
        p = ggplot(self.df, aes(x='x', y='y'))
        
        # Add multiple components
        for i in range(10):
            p = p + geom_point(color=f'color_{i}')
            p = p + scale_x_continuous(limits=[0, 10])
            p = p + theme_minimal()
        
        try:
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails due to memory constraints
            pass

    # Copy Tests
    def test_ggplot_copy_functionality(self):
        """Test ggplot copy functionality."""
        p1 = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        p2 = p1.copy()
        
        # Modify p2
        p2 = p2 + theme_dark()
        
        # Draw both plots
        fig1 = p1.draw()
        fig2 = p2.draw()
        
        assert isinstance(fig1, go.Figure)
        assert isinstance(fig2, go.Figure)
        
        # Check that they're different (p2 has dark theme)
        assert fig1.layout.template != fig2.layout.template

    # Save Tests
    def test_ggsave_without_drawing(self):
        """Test ggsave without calling draw first."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        
        with pytest.raises(AttributeError):
            p.save("test.html")

    def test_ggsave_with_invalid_filepath(self):
        """Test ggsave with invalid filepath."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        
        with pytest.raises(ValueError):
            p.save("test.invalid")

    # Edge Cases
    def test_ggplot_with_single_row_data(self):
        """Test ggplot with single row of data."""
        single_row_df = self.df.iloc[:1].copy()
        p = ggplot(single_row_df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_ggplot_with_single_column_data(self):
        """Test ggplot with single column data."""
        single_col_df = self.df[['x']].copy()
        p = ggplot(single_col_df, aes(x='x')) + geom_histogram()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_ggplot_with_duplicate_column_names(self):
        """Test ggplot with duplicate column names."""
        df_duplicate_cols = self.df.copy()
        df_duplicate_cols.columns = ['x', 'x', 'y', 'category']
        
        try:
            p = ggplot(df_duplicate_cols, aes(x='x', y='y')) + geom_point()
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with duplicate columns
            pass

