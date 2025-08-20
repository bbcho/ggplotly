import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestGeoms:
    """Test suite for all geom components."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        self.df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 1, 5, 3],
            'category': ['A', 'B', 'A', 'B', 'A'],
            'size': [10, 20, 15, 25, 18],
            'color': ['red', 'blue', 'green', 'red', 'blue']
        })
        
        self.df_continuous = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)),
            'group': np.random.choice(['A', 'B'], 100)
        })

    def test_geom_point_basic(self):
        """Test basic point geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'

    def test_geom_point_with_color(self):
        """Test point geometry with color mapping."""
        p = ggplot(self.df, aes(x='x', y='y', color='category')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2  # One trace per category

    def test_geom_point_with_size(self):
        """Test point geometry with size mapping."""
        p = ggplot(self.df, aes(x='x', y='y', size='size')) + geom_point()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_line_basic(self):
        """Test basic line geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_line()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'

    def test_geom_line_with_group(self):
        """Test line geometry with grouping."""
        p = ggplot(self.df, aes(x='x', y='y', group='category')) + geom_line()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2  # One trace per category

    def test_geom_bar_basic(self):
        """Test basic bar geometry."""
        p = ggplot(self.df, aes(x='category', y='y')) + geom_bar()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'bar'

    def test_geom_bar_with_fill(self):
        """Test bar geometry with fill color."""
        p = ggplot(self.df, aes(x='category', y='y')) + geom_bar(fill='lightblue')
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_histogram_basic(self):
        """Test basic histogram geometry."""
        p = ggplot(self.df, aes(x='x')) + geom_histogram()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'histogram'

    def test_geom_histogram_with_bins(self):
        """Test histogram geometry with custom bins."""
        p = ggplot(self.df, aes(x='x')) + geom_histogram(bins=10)
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_boxplot_basic(self):
        """Test basic boxplot geometry."""
        p = ggplot(self.df, aes(x='category', y='y')) + geom_boxplot()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'box'

    def test_geom_area_basic(self):
        """Test basic area geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_area()
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].fill == 'tonexty'

    def test_geom_area_with_fill(self):
        """Test area geometry with custom fill."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_area(fill='lightgreen', alpha=0.7)
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_density_basic(self):
        """Test basic density geometry."""
        p = ggplot(self.df, aes(x='x')) + geom_density()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_violin_basic(self):
        """Test basic violin geometry."""
        p = ggplot(self.df, aes(x='category', y='y')) + geom_violin()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_smooth_basic(self):
        """Test basic smooth geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_smooth()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_smooth_with_method(self):
        """Test smooth geometry with specific method."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_smooth(method='loess')
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_text_basic(self):
        """Test basic text geometry."""
        p = ggplot(self.df, aes(x='x', y='y', text='category')) + geom_text()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_errorbar_basic(self):
        """Test basic errorbar geometry."""
        # Add error data
        df_with_error = self.df.copy()
        df_with_error['ymin'] = df_with_error['y'] - 0.5
        df_with_error['ymax'] = df_with_error['y'] + 0.5
        
        p = ggplot(df_with_error, aes(x='x', y='y', ymin='ymin', ymax='ymax')) + geom_errorbar()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_tile_basic(self):
        """Test basic tile geometry."""
        # Create grid data
        grid_data = pd.DataFrame({
            'x': [1, 2, 3, 1, 2, 3],
            'y': [1, 1, 1, 2, 2, 2],
            'value': [0.1, 0.5, 0.9, 0.3, 0.7, 0.2]
        })
        
        p = ggplot(grid_data, aes(x='x', y='y', fill='value')) + geom_tile()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_ribbon_basic(self):
        """Test basic ribbon geometry."""
        # Create ribbon data
        ribbon_data = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'ymin': np.sin(np.linspace(0, 10, 50)) - 0.2,
            'ymax': np.sin(np.linspace(0, 10, 50)) + 0.2
        })
        
        p = ggplot(ribbon_data, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_step_basic(self):
        """Test basic step geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_step()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_segment_basic(self):
        """Test basic segment geometry."""
        p = ggplot(self.df, aes(x='x', y='y', xend='x', yend='y+1')) + geom_segment()
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_vline_basic(self):
        """Test basic vline geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + geom_vline(xintercept=3)
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_hline_basic(self):
        """Test basic hline geometry."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point() + geom_hline(yintercept=3)
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_multiple_geoms(self):
        """Test combining multiple geometries."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point(color='red')
              + geom_line(color='blue')
              + geom_smooth(color='green'))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 3  # At least 3 traces

    def test_geom_with_theme(self):
        """Test geometry with theme application."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + theme_minimal())
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_geom_with_scales(self):
        """Test geometry with scale transformations."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point()
              + scale_x_continuous(limits=[0, 6])
              + scale_y_continuous(limits=[0, 6]))
        fig = p.draw()
        assert isinstance(fig, go.Figure)
