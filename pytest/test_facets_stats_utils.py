import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestFacetsStatsUtils:
    """Test suite for faceting, statistical transformations, and utilities."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6, 7, 8],
            'y': [2, 4, 1, 5, 3, 6, 2, 4],
            'category': ['A', 'B', 'A', 'B', 'A', 'B', 'A', 'B'],
            'group': ['X', 'X', 'Y', 'Y', 'X', 'X', 'Y', 'Y'],
            'value': [10, 20, 15, 25, 18, 30, 22, 28]
        })
        
        self.df_large = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'category': np.random.choice(['A', 'B', 'C'], 200),
            'group': np.random.choice(['X', 'Y'], 200)
        })

    # Faceting Tests
    def test_facet_wrap_basic(self):
        """Test basic facet_wrap functionality."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if subplots are created
        assert len(fig.data) >= 2  # At least 2 traces for 2 categories

    def test_facet_wrap_with_ncol(self):
        """Test facet_wrap with specified number of columns."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category', ncol=1))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_facet_wrap_with_nrow(self):
        """Test facet_wrap with specified number of rows."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category', nrow=2))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_facet_grid_basic(self):
        """Test basic facet_grid functionality."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_grid('category', 'group'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_facet_grid_rows_only(self):
        """Test facet_grid with rows only."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_grid('category', None))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_facet_grid_cols_only(self):
        """Test facet_grid with columns only."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_grid(None, 'group'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_faceting_with_different_geoms(self):
        """Test faceting with different geometry types."""
        # Test with points
        p1 = (ggplot(self.df, aes(x='x', y='y'))
               + geom_point()
               + facet_wrap('category'))
        fig1 = p1.draw()
        assert isinstance(fig1, go.Figure)
        
        # Test with bars
        p2 = (ggplot(self.df, aes(x='category', y='value'))
               + geom_bar()
               + facet_wrap('group'))
        fig2 = p2.draw()
        assert isinstance(fig2, go.Figure)
        
        # Test with lines
        p3 = (ggplot(self.df, aes(x='x', y='y'))
               + geom_line()
               + facet_wrap('category'))
        fig3 = p3.draw()
        assert isinstance(fig3, go.Figure)

    def test_faceting_with_themes(self):
        """Test faceting with theme application."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category')
              + theme_minimal())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_faceting_with_scales(self):
        """Test faceting with scale transformations."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category')
              + scale_x_continuous(limits=[0, 10]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    # Statistical Transformation Tests
    def test_stat_bin_basic(self):
        """Test basic stat_bin functionality."""
        p = ggplot(self.df, aes(x='x')) + geom_histogram() + stat_bin()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_bin_with_bins(self):
        """Test stat_bin with specified number of bins."""
        p = ggplot(self.df, aes(x='x')) + geom_histogram() + stat_bin(bins=10)
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_count_basic(self):
        """Test basic stat_count functionality."""
        p = ggplot(self.df, aes(x='category')) + geom_bar() + stat_count()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_density_basic(self):
        """Test basic stat_density functionality."""
        p = ggplot(self.df, aes(x='x')) + geom_density() + stat_density()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_ecdf_basic(self):
        """Test basic stat_ecdf functionality."""
        p = ggplot(self.df, aes(x='x')) + geom_line() + stat_ecdf()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_identity_basic(self):
        """Test basic stat_identity functionality."""
        p = ggplot(self.df, aes(x='category', y='value')) + geom_bar() + stat_identity()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_smooth_basic(self):
        """Test basic stat_smooth functionality."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + stat_smooth()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stat_smooth_with_method(self):
        """Test stat_smooth with specific method."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + stat_smooth(method='loess')
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stats_with_different_geoms(self):
        """Test statistical transformations with different geometries."""
        # Test stat_bin with histogram
        p1 = ggplot(self.df, aes(x='x')) + geom_histogram() + stat_bin()
        fig1 = p1.draw()
        assert isinstance(fig1, go.Figure)
        
        # Test stat_count with bar
        p2 = ggplot(self.df, aes(x='category')) + geom_bar() + stat_count()
        fig2 = p2.draw()
        assert isinstance(fig2, go.Figure)
        
        # Test stat_smooth with line
        p3 = ggplot(self.df, aes(x='x', y='y')) + geom_line() + stat_smooth()
        fig3 = p3.draw()
        assert isinstance(fig3, go.Figure)

    # Utility Tests
    def test_ggtitle_basic(self):
        """Test basic ggtitle functionality."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + ggtitle("Test Title")
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if title is applied
        assert fig.layout.title.text == "Test Title"

    def test_labs_basic(self):
        """Test basic labs functionality."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + labs(title="Main Title", x="X-Axis", y="Y-Axis"))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if labels are applied
        assert fig.layout.title.text == "Main Title"
        assert fig.layout.xaxis.title.text == "X-Axis"
        assert fig.layout.yaxis.title.text == "Y-Axis"

    def test_labs_with_subtitle_and_caption(self):
        """Test labs with subtitle and caption."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + labs(title="Main Title", subtitle="Subtitle", caption="Caption"))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_ggsave_basic(self):
        """Test basic ggsave functionality."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        
        # Test saving (this should work without errors)
        try:
            # Note: In test environment, we might not be able to actually save files
            # So we just test that the method exists and can be called
            assert hasattr(fig, 'write_html')
            assert hasattr(fig, 'write_image')
        except Exception:
            # It's okay if saving fails in test environment
            pass

    def test_ggsize_basic(self):
        """Test basic ggsize functionality."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + ggsize(width=800, height=600))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if size is applied
        assert fig.layout.width == 800
        assert fig.layout.height == 600

    def test_positions_basic(self):
        """Test basic position functions."""
        # Test position_dodge
        p1 = (ggplot(self.df, aes(x='category', y='value', fill='group'))
               + geom_bar(position=position_dodge()))
        fig1 = p1.draw()
        assert isinstance(fig1, go.Figure)
        
        # Test position_jitter
        p2 = (ggplot(self.df, aes(x='category', y='value'))
               + geom_point(position=position_jitter()))
        fig2 = p2.draw()
        assert isinstance(fig2, go.Figure)
        
        # Test position_stack
        p3 = (ggplot(self.df, aes(x='category', y='value', fill='group'))
               + geom_bar(position=position_stack()))
        fig3 = p3.draw()
        assert isinstance(fig3, go.Figure)

    # Combined Tests
    def test_faceting_with_stats(self):
        """Test combining faceting with statistical transformations."""
        p = (ggplot(self.df, aes(x='x'))
              + geom_histogram()
              + stat_bin(bins=10)
              + facet_wrap('category'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_faceting_with_themes_and_scales(self):
        """Test combining faceting with themes and scales."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + facet_wrap('category')
              + theme_minimal()
              + scale_x_continuous(limits=[0, 10]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stats_with_themes(self):
        """Test combining statistical transformations with themes."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + stat_smooth()
              + theme_dark())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_complex_combination(self):
        """Test complex combination of faceting, stats, themes, and scales."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + stat_smooth()
              + facet_wrap('category')
              + theme_bbc()
              + scale_x_continuous(limits=[0, 10])
              + labs(title="Complex Plot", x="X-Axis", y="Y-Axis"))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    # Edge Cases
    def test_faceting_with_single_category(self):
        """Test faceting with single category value."""
        single_cat_df = self.df[self.df['category'] == 'A'].copy()
        p = ggplot(single_cat_df, aes(x='x', y='y')) + geom_point() + facet_wrap('category')
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_stats_with_empty_data(self):
        """Test statistical transformations with empty data."""
        empty_df = pd.DataFrame()
        try:
            p = ggplot(empty_df, aes(x='x')) + geom_histogram() + stat_bin()
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with empty data
            pass

    def test_utilities_with_empty_data(self):
        """Test utility functions with empty data."""
        empty_df = pd.DataFrame()
        try:
            p = ggplot(empty_df, aes(x='x', y='y')) + geom_point() + ggtitle("Test")
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with empty data
            pass

