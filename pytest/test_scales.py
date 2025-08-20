import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestScales:
    """Test suite for all scale components."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'color_var': ['red', 'blue', 'green', 'red', 'blue'],
            'size_var': [10, 20, 15, 25, 18]
        })

    def test_scale_x_continuous_basic(self):
        """Test basic x-axis continuous scale."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_x_continuous_with_limits(self):
        """Test x-axis continuous scale with limits."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if limits are applied
        assert fig.layout.xaxis.range[0] == 0
        assert fig.layout.xaxis.range[1] == 6

    def test_scale_x_continuous_with_breaks(self):
        """Test x-axis continuous scale with custom breaks."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(breaks=[1, 3, 5]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_y_continuous_basic(self):
        """Test basic y-axis continuous scale."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_y_continuous())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_y_continuous_with_limits(self):
        """Test y-axis continuous scale with limits."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_y_continuous(limits=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        # Check if limits are applied
        assert fig.layout.yaxis.range[0] == 0
        assert fig.layout.yaxis.range[1] == 6

    def test_scale_x_log10(self):
        """Test x-axis log10 scale."""
        # Use positive data for log scale
        df_positive = self.df[self.df['x'] > 0].copy()
        p = (ggplot(df_positive, aes(x='x', y='y'))
              + geom_point()
              + scale_x_log10())
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert fig.layout.xaxis.type == 'log'

    def test_scale_y_log10(self):
        """Test y-axis log10 scale."""
        # Use positive data for log scale
        df_positive = self.df[self.df['y'] > 0].copy()
        p = (ggplot(df_positive, aes(x='x', y='y'))
              + geom_point()
              + scale_y_log10())
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert fig.layout.yaxis.type == 'log'

    def test_scale_color_manual(self):
        """Test manual color scale."""
        p = (ggplot(self.df, aes(x='x', y='y', color='category'))
              + geom_point()
              + scale_color_manual(values=['red', 'blue']))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_color_brewer(self):
        """Test color brewer scale."""
        p = (ggplot(self.df, aes(x='x', y='y', color='category'))
              + geom_point()
              + scale_color_brewer(palette='Set1'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_color_gradient(self):
        """Test color gradient scale."""
        p = (ggplot(self.df, aes(x='x', y='y', color='size_var'))
              + geom_point()
              + scale_color_gradient(low='blue', high='red'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_fill_manual(self):
        """Test manual fill scale."""
        p = (ggplot(self.df, aes(x='category', y='y'))
              + geom_bar()
              + scale_fill_manual(values=['lightblue', 'lightgreen']))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_fill_gradient(self):
        """Test fill gradient scale."""
        # Create data suitable for fill gradient
        grid_data = pd.DataFrame({
            'x': [1, 2, 3, 1, 2, 3],
            'y': [1, 1, 1, 2, 2, 2],
            'value': [0.1, 0.5, 0.9, 0.3, 0.7, 0.2]
        })
        
        p = (ggplot(grid_data, aes(x='x', y='y', fill='value'))
              + geom_tile()
              + scale_fill_gradient(low='white', high='darkblue'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_size(self):
        """Test size scale."""
        p = (ggplot(self.df, aes(x='x', y='y', size='size_var'))
              + geom_point()
              + scale_size(range=[5, 20]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_multiple_scales(self):
        """Test combining multiple scales."""
        p = (ggplot(self.df, aes(x='x', y='y', color='category'))
              + geom_point()
              + scale_x_continuous(limits=[0, 6])
              + scale_y_continuous(limits=[0, 6])
              + scale_color_manual(values=['red', 'blue']))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scales_with_themes(self):
        """Test scales with theme application."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=[0, 6])
              + scale_y_continuous(limits=[0, 6])
              + theme_minimal())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scales_with_faceting(self):
        """Test scales with faceting."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=[0, 6])
              + scale_y_continuous(limits=[0, 6])
              + facet_wrap('category'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_limits_edge_cases(self):
        """Test scale limits with edge cases."""
        # Test with single value
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=[0, 10]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

        # Test with None limits (should use data range)
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=None))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_scale_breaks_edge_cases(self):
        """Test scale breaks with edge cases."""
        # Test with empty breaks
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(breaks=[]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

        # Test with None breaks (should use default)
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(breaks=None))
        fig = p.draw()
        assert isinstance(fig, go.Figure)

