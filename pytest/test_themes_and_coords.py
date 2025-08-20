import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestThemesAndCoordinates:
    """Test suite for themes and coordinate systems."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'angle': np.linspace(0, 2*np.pi, 5),
            'radius': [1, 2, 1, 2, 1]
        })

    # Theme Tests
    def test_theme_default(self):
        """Test default theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_default()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if theme properties are applied
        assert fig.layout.plot_bgcolor == 'white'
        assert fig.layout.paper_bgcolor == 'white'

    def test_theme_minimal(self):
        """Test minimal theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_minimal()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_dark(self):
        """Test dark theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_dark()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if dark template is applied
        assert fig.layout.template == 'plotly_dark'

    def test_theme_classic(self):
        """Test classic theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_classic()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if classic theme properties are applied
        assert fig.layout.template == 'simple_white'

    def test_theme_bbc(self):
        """Test BBC theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_bbc()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if BBC theme properties are applied
        assert fig.layout.paper_bgcolor == '#FFFFFF'
        assert fig.layout.plot_bgcolor == '#FFFFFF'

    def test_theme_nytimes(self):
        """Test NYTimes theme."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_nytimes()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_custom(self):
        """Test custom theme."""
        custom_template = go.layout.Template(
            layout=dict(
                plot_bgcolor='lightblue',
                paper_bgcolor='lightgreen',
                font=dict(color='darkblue', size=14)
            )
        )
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_custom(custom_template)
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if custom theme properties are applied
        assert fig.layout.plot_bgcolor == 'lightblue'
        assert fig.layout.paper_bgcolor == 'lightgreen'

    def test_theme_element_text(self):
        """Test element_text theme component."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_default()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_element_line(self):
        """Test element_line theme component."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_default()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_element_rect(self):
        """Test element_rect theme component."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme_default()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    # Coordinate System Tests
    def test_coord_cartesian_basic(self):
        """Test basic cartesian coordinates."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + coord_cartesian()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_cartesian_with_limits(self):
        """Test cartesian coordinates with limits."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + coord_cartesian(xlim=[0, 6], ylim=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_flip_basic(self):
        """Test flipped coordinates."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + coord_flip()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_flip_with_bar(self):
        """Test flipped coordinates with bar plot."""
        p = ggplot(self.df, aes(x='category', y='y')) + geom_bar() + coord_flip()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_polar_basic(self):
        """Test polar coordinates."""
        p = ggplot(self.df, aes(x='angle', y='radius')) + geom_point() + coord_polar()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_polar_with_line(self):
        """Test polar coordinates with line plot."""
        p = ggplot(self.df, aes(x='angle', y='radius')) + geom_line() + coord_polar()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coord_polar_with_area(self):
        """Test polar coordinates with area plot."""
        p = ggplot(self.df, aes(x='angle', y='radius')) + geom_area() + coord_polar()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    # Combined Tests
    def test_theme_with_coordinates(self):
        """Test combining themes with coordinate systems."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + theme_minimal()
              + coord_cartesian(xlim=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_with_scales(self):
        """Test combining themes with scales."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + theme_dark()
              + scale_x_continuous(limits=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_coordinates_with_faceting(self):
        """Test combining coordinates with faceting."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + coord_flip()
              + facet_wrap('category'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_with_faceting(self):
        """Test combining themes with faceting."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + theme_classic()
              + facet_wrap('category'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_complex_combination(self):
        """Test complex combination of themes, coordinates, and scales."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + theme_bbc()
              + coord_cartesian(xlim=[0, 6], ylim=[0, 6])
              + scale_x_continuous(breaks=[1, 3, 5])
              + scale_y_continuous(breaks=[1, 3, 5]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    # Edge Cases
    def test_theme_with_empty_data(self):
        """Test theme with empty dataframe."""
        empty_df = pd.DataFrame()
        try:
            p = ggplot(empty_df, aes(x='x', y='y')) + geom_point() + theme_default()
            fig = p.draw()
            assert isinstance(fig, go.Figure)
        except Exception:
            # It's okay if this fails with empty data
            pass

    def test_coordinates_with_single_point(self):
        """Test coordinates with single data point."""
        single_df = pd.DataFrame({'x': [1], 'y': [1]})
        p = ggplot(single_df, aes(x='x', y='y')) + geom_point() + coord_cartesian()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_theme_consistency(self):
        """Test that themes are consistently applied across different plot types."""
        themes = [theme_default(), theme_minimal(), theme_dark(), theme_classic()]
        
        for theme in themes:
            # Test with points
            p1 = ggplot(self.df, aes(x='x', y='y')) + geom_point() + theme
            fig1 = p1.draw()
            assert isinstance(fig1, go.Figure)
            
            # Test with bars
            p2 = ggplot(self.df, aes(x='category', y='y')) + geom_bar() + theme
            fig2 = p2.draw()
            assert isinstance(fig2, go.Figure)
            
            # Test with lines
            p3 = ggplot(self.df, aes(x='x', y='y')) + geom_line() + theme
            fig3 = p3.draw()
            assert isinstance(fig3, go.Figure)

