import sys
import os
import pandas as pd
import plotly.graph_objects as go
import numpy as np

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *


class TestIntegration:
    """Integration tests for complex plot combinations and real-world scenarios."""
    
    def setup_method(self):
        """Set up test data for each test method."""
        np.random.seed(42)
        
        # Create realistic dataset
        n_points = 100
        self.df = pd.DataFrame({
            'x': np.random.normal(0, 1, n_points),
            'y': np.random.normal(0, 1, n_points),
            'category': np.random.choice(['A', 'B', 'C'], n_points),
            'group': np.random.choice(['X', 'Y'], n_points),
            'size': np.random.uniform(5, 20, n_points),
            'color_value': np.random.uniform(0, 1, n_points),
            'time': pd.date_range('2023-01-01', periods=n_points, freq='D'),
            'text': [f'Point {i}' for i in range(n_points)]
        })
        
        # Create time series data
        dates = pd.date_range('2023-01-01', periods=50, freq='D')
        self.time_series = pd.DataFrame({
            'date': dates,
            'value': np.cumsum(np.random.randn(50)),
            'upper': np.cumsum(np.random.randn(50)) + 2,
            'lower': np.cumsum(np.random.randn(50)) - 2,
            'category': np.random.choice(['Series A', 'Series B'], 50)
        })

    def test_complex_scatter_plot(self):
        """Test complex scatter plot with multiple aesthetics and layers."""
        p = (ggplot(self.df, aes(x='x', y='y', color='category', size='size'))
              + geom_point(alpha=0.7)
              + geom_smooth(method='loess', color='red', se=False)
              + scale_color_brewer(palette='Set1')
              + scale_size(range=[5, 20])
              + labs(title="Complex Scatter Plot", x="X Variable", y="Y Variable")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 4  # Points + smooth line + color categories

    def test_faceted_time_series(self):
        """Test faceted time series with multiple geoms."""
        p = (ggplot(self.time_series, aes(x='date', y='value'))
              + geom_line(color='blue')
              + geom_ribbon(aes(ymin='lower', ymax='upper'), alpha=0.3, fill='lightblue')
              + geom_point(color='darkblue', size=2)
              + facet_wrap('category', ncol=1)
              + scale_x_datetime()
              + labs(title="Time Series with Confidence Intervals", x="Date", y="Value")
              + theme_classic())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_multi_layer_plot(self):
        """Test plot with multiple geometry layers."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point(alpha=0.6, color='gray')
              + geom_smooth(method='lm', color='red', se=True)
              + geom_smooth(method='loess', color='blue', se=False)
              + geom_hline(yintercept=0, linetype='dashed', color='black')
              + geom_vline(xintercept=0, linetype='dashed', color='black')
              + labs(title="Multi-Layer Plot", subtitle="Points, Lines, and Reference Lines")
              + theme_bbc())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 5  # Points + 2 smooth lines + 2 reference lines

    def test_complex_bar_plot(self):
        """Test complex bar plot with grouping and positioning."""
        # Aggregate data for bar plot
        agg_data = self.df.groupby(['category', 'group'])['y'].mean().reset_index()
        
        p = (ggplot(agg_data, aes(x='category', y='y', fill='group'))
              + geom_bar(position=position_dodge(), stat='identity')
              + scale_fill_manual(values=['lightblue', 'lightgreen'])
              + labs(title="Grouped Bar Plot", x="Category", y="Mean Value", fill="Group")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_histogram_with_density(self):
        """Test histogram with density overlay."""
        p = (ggplot(self.df, aes(x='x'))
              + geom_histogram(aes(y='..density..'), bins=20, alpha=0.7, fill='lightblue')
              + geom_density(color='red', linewidth=2)
              + labs(title="Histogram with Density", x="Value", y="Density")
              + theme_default())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_boxplot_with_points(self):
        """Test boxplot with individual points overlaid."""
        p = (ggplot(self.df, aes(x='category', y='y'))
              + geom_boxplot(fill='lightblue', alpha=0.7)
              + geom_point(position=position_jitter(width=0.2), alpha=0.5, color='darkblue')
              + labs(title="Boxplot with Points", x="Category", y="Value")
              + theme_classic())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_polar_coordinate_plot(self):
        """Test polar coordinate system with area plot."""
        # Create circular data
        angles = np.linspace(0, 2*np.pi, 36)
        values = np.sin(angles) + np.random.normal(0, 0.1, 36)
        polar_data = pd.DataFrame({'angle': angles, 'value': values})
        
        p = (ggplot(polar_data, aes(x='angle', y='value'))
              + geom_area(fill='lightgreen', alpha=0.7)
              + geom_line(color='darkgreen', linewidth=2)
              + coord_polar()
              + labs(title="Polar Area Plot", x="Angle", y="Value")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_tile_heatmap(self):
        """Test tile plot as heatmap."""
        # Create grid data
        x_coords = np.arange(-2, 3)
        y_coords = np.arange(-2, 3)
        X, Y = np.meshgrid(x_coords, y_coords)
        Z = np.sin(X) * np.cos(Y)
        
        heatmap_data = pd.DataFrame({
            'x': X.flatten(),
            'y': Y.flatten(),
            'value': Z.flatten()
        })
        
        p = (ggplot(heatmap_data, aes(x='x', y='y', fill='value'))
              + geom_tile()
              + scale_fill_gradient(low='blue', high='red', midpoint=0)
              + labs(title="Heatmap", x="X", y="Y", fill="Value")
              + theme_dark())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_error_bar_plot(self):
        """Test error bar plot with multiple groups."""
        # Create data with error bars
        error_data = pd.DataFrame({
            'category': ['A', 'B', 'C', 'A', 'B', 'C'],
            'group': ['X', 'X', 'X', 'Y', 'Y', 'Y'],
            'mean': [10, 15, 12, 8, 13, 11],
            'se': [1, 1.5, 1.2, 0.8, 1.3, 1.1]
        })
        error_data['ymin'] = error_data['mean'] - error_data['se']
        error_data['ymax'] = error_data['mean'] + error_data['se']
        
        p = (ggplot(error_data, aes(x='category', y='mean', color='group'))
              + geom_point(position=position_dodge(width=0.3), size=4)
              + geom_errorbar(aes(ymin='ymin', ymax='ymax'), 
                             position=position_dodge(width=0.3), width=0.2)
              + labs(title="Error Bar Plot", x="Category", y="Mean ± SE", color="Group")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_text_annotations(self):
        """Test plot with text annotations."""
        # Sample subset for text
        text_data = self.df.head(10)
        
        p = (ggplot(text_data, aes(x='x', y='y'))
              + geom_point(color='blue', size=3)
              + geom_text(aes(label='text'), size=8, color='red', 
                         position=position_jitter(width=0.1, height=0.1))
              + labs(title="Scatter Plot with Text Labels", x="X", y="Y")
              + theme_default())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_complex_faceting(self):
        """Test complex faceting with multiple variables."""
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point(aes(color='category', size='size'), alpha=0.7)
              + geom_smooth(method='loess', color='red', se=False)
              + facet_grid('category', 'group')
              + scale_color_brewer(palette='Set2')
              + scale_size(range=[3, 15])
              + labs(title="Faceted Scatter Plot", x="X Variable", y="Y Variable")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_log_transformed_plot(self):
        """Test plot with log-transformed scales."""
        # Use positive data for log scale
        positive_data = self.df[self.df['x'] > 0].copy()
        positive_data['x'] = np.abs(positive_data['x']) + 0.1  # Ensure positive
        
        p = (ggplot(positive_data, aes(x='x', y='y'))
              + geom_point(aes(color='category'), alpha=0.7)
              + scale_x_log10()
              + scale_y_log10()
              + labs(title="Log-Transformed Plot", x="X (log scale)", y="Y (log scale)")
              + theme_classic())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert fig.layout.xaxis.type == 'log'
        assert fig.layout.yaxis.type == 'log'

    def test_custom_theme_application(self):
        """Test custom theme creation and application."""
        # Create custom theme
        custom_theme = go.layout.Template(
            layout=dict(
                plot_bgcolor='#f0f0f0',
                paper_bgcolor='#ffffff',
                font=dict(color='#333333', size=14, family='Arial'),
                xaxis=dict(
                    showgrid=True,
                    gridcolor='#cccccc',
                    zeroline=True,
                    zerolinecolor='#666666'
                ),
                yaxis=dict(
                    showgrid=True,
                    gridcolor='#cccccc',
                    zeroline=True,
                    zerolinecolor='#666666'
                )
            )
        )
        
        p = (ggplot(self.df, aes(x='x', y='y'))
              + geom_point(color='darkblue', size=3)
              + theme_custom(custom_theme)
              + labs(title="Custom Theme Plot", x="X Variable", y="Y Variable"))
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert fig.layout.plot_bgcolor == '#f0f0f0'
        assert fig.layout.paper_bgcolor == '#ffffff'

    def test_statistical_transformations(self):
        """Test various statistical transformations."""
        p = (ggplot(self.df, aes(x='x'))
              + geom_histogram(aes(y='..density..'), bins=20, alpha=0.7)
              + stat_density(color='red', linewidth=2)
              + labs(title="Histogram with Density", x="Value", y="Density")
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_position_adjustments(self):
        """Test various position adjustments."""
        # Create data for position testing
        pos_data = pd.DataFrame({
            'category': ['A', 'A', 'B', 'B', 'C', 'C'],
            'group': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
            'value': [10, 15, 12, 18, 8, 14]
        })
        
        p = (ggplot(pos_data, aes(x='category', y='value', fill='group'))
              + geom_bar(position=position_stack(), stat='identity')
              + scale_fill_manual(values=['lightblue', 'lightgreen'])
              + labs(title="Stacked Bar Plot", x="Category", y="Value", fill="Group")
              + theme_classic())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)

    def test_plot_saving_functionality(self):
        """Test plot saving functionality."""
        p = ggplot(self.df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        
        # Test that the figure has saving methods
        assert hasattr(fig, 'write_html')
        assert hasattr(fig, 'write_image')
        
        # Test that we can access figure properties
        assert isinstance(fig.layout, dict)
        assert len(fig.data) > 0

    def test_large_dataset_performance(self):
        """Test performance with larger dataset."""
        # Create larger dataset
        large_df = pd.DataFrame({
            'x': np.random.randn(1000),
            'y': np.random.randn(1000),
            'category': np.random.choice(['A', 'B', 'C'], 1000)
        })
        
        p = (ggplot(large_df, aes(x='x', y='y', color='category'))
              + geom_point(alpha=0.6)
              + facet_wrap('category')
              + theme_minimal())
        
        fig = p.draw()
        assert isinstance(fig, go.Figure)
        assert len(fig.data) >= 3  # At least 3 traces for 3 categories
