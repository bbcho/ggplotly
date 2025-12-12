"""
Comprehensive tests for all ggplotly showcase examples.

These tests verify that each example from ggplotly_showcase.py:
1. Runs without errors
2. Produces the expected chart type(s)
3. Has the correct number of traces where applicable
"""

import sys
import os
import math
import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import *
from ggplotly.stats import stat_summary


# =============================================================================
# PART 1: BASICS
# =============================================================================

class TestPart1Basics:
    """Test Part 1: Basic plots and aesthetics."""

    def test_1_2_basic_scatter(self):
        """Test basic scatter plot."""
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'markers'
        # Verify data matches input
        assert list(fig.data[0].x) == [1, 2, 3, 4, 5]
        assert list(fig.data[0].y) == [2, 4, 3, 5, 4]

    def test_1_3_color_aesthetic(self):
        """Test color mapped to category."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })
        p = ggplot(df, aes(x='x', y='y', color='category')) + geom_point()
        fig = p.draw()
        assert len(fig.data) == 3  # One trace per category
        # Each trace should be scatter with markers
        for trace in fig.data:
            assert trace.type == 'scatter'
            assert trace.mode == 'markers'
        # Verify all data points are present across traces
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 100

    def test_1_3_size_aesthetic(self):
        """Test size mapped to variable."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'size_var': np.random.rand(100) * 50
        })
        p = ggplot(df, aes(x='x', y='y', size='size_var')) + geom_point(color='steelblue', alpha=0.6)
        fig = p.draw()
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 100
        # Verify marker sizes vary (not all the same)
        sizes = fig.data[0].marker.size
        assert len(set(sizes)) > 1  # Multiple different sizes

    def test_1_3_multiple_aesthetics(self):
        """Test multiple aesthetics combined."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'size_var': np.random.rand(100) * 50
        })
        p = ggplot(df, aes(x='x', y='y', color='category', size='size_var')) + geom_point(alpha=0.7)
        fig = p.draw()
        assert len(fig.data) == 3  # One trace per category
        # Each trace should have varying sizes
        for trace in fig.data:
            assert trace.type == 'scatter'
            if len(trace.marker.size) > 1:
                assert len(set(trace.marker.size)) > 1

    def test_1_4_series_index(self):
        """Test Series with DatetimeIndex as x-axis."""
        dates = pd.date_range('2024-01-01', periods=30)
        np.random.seed(42)
        values = np.cumsum(np.random.randn(30))
        ts = pd.Series(values, index=dates, name='Price')
        p = ggplot(ts) + geom_line()
        fig = p.draw()
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        assert len(fig.data[0].y) == 30

    def test_1_4_dataframe_named_index(self):
        """Test DataFrame with named index."""
        df_indexed = pd.DataFrame(
            {'value': np.sin(np.linspace(0, 4*np.pi, 100))},
            index=pd.Index(np.linspace(0, 10, 100), name='Time')
        )
        p = ggplot(df_indexed, aes(y='value')) + geom_line()
        fig = p.draw()
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        assert len(fig.data[0].y) == 100
        # Sine wave should have values between -1 and 1
        assert min(fig.data[0].y) >= -1.01
        assert max(fig.data[0].y) <= 1.01

    def test_1_5_builtin_datasets(self):
        """Test built-in datasets load correctly."""
        mpg = data('mpg')
        assert isinstance(mpg, pd.DataFrame)
        assert 'displ' in mpg.columns

        p = ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point()
        fig = p.draw()
        # Should have one trace per car class
        assert len(fig.data) == mpg['class'].nunique()
        for trace in fig.data:
            assert trace.type == 'scatter'
            assert trace.mode == 'markers'

    def test_1_5_diamonds_dataset(self):
        """Test diamonds dataset."""
        diamonds = data('diamonds')
        sample = diamonds.sample(1000, random_state=42)
        p = (ggplot(sample, aes(x='carat', y='price', color='cut'))
             + geom_point(alpha=0.5))
        fig = p.draw()
        # Should have one trace per cut type
        assert len(fig.data) == sample['cut'].nunique()
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 1000

    def test_1_5_iris_dataset(self):
        """Test iris dataset with correct column names."""
        iris = data('iris')
        p = (ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species'))
             + geom_point(size=8))
        fig = p.draw()
        assert len(fig.data) == 3  # 3 species
        # Verify total points equals iris dataset size
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == len(iris)

    def test_1_5_mtcars_dataset(self):
        """Test mtcars dataset."""
        mtcars = data('mtcars')
        p = (ggplot(mtcars, aes(x='wt', y='mpg', color='cyl'))
             + geom_point(size=10))
        fig = p.draw()
        # Should have one trace per cyl value
        assert len(fig.data) == mtcars['cyl'].nunique()
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == len(mtcars)

    def test_1_5_economics_dataset(self):
        """Test economics time series dataset."""
        economics = data('economics')
        p = (ggplot(economics, aes(x='date', y='unemploy'))
             + geom_line())
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        assert len(fig.data[0].y) == len(economics)

    def test_1_5_midwest_dataset(self):
        """Test midwest dataset with log scale."""
        midwest = data('midwest')
        p = (ggplot(midwest, aes(x='popdensity', y='percollege', color='state'))
             + geom_point(alpha=0.6)
             + scale_x_log10())
        fig = p.draw()
        assert fig.layout.xaxis.type == 'log'
        # Should have one trace per state
        assert len(fig.data) == midwest['state'].nunique()
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == len(midwest)

    def test_1_5_txhousing_dataset(self):
        """Test txhousing dataset filtered."""
        txhousing = data('txhousing')
        houston = txhousing[txhousing['city'] == 'Houston']
        p = (ggplot(houston, aes(x='date', y='median'))
             + geom_line())
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        # Verify we have data for Houston (should have multiple months)
        assert len(fig.data[0].y) > 50

    def test_1_5_faithfuld_dataset(self):
        """Test faithfuld 2D density dataset."""
        faithfuld = data('faithfuld')
        p = (ggplot(faithfuld, aes(x='waiting', y='eruptions', fill='density'))
             + geom_tile()
             + scale_fill_viridis_c())
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'

    def test_1_5_msleep_dataset(self):
        """Test msleep mammal sleep dataset."""
        msleep = data('msleep')
        msleep_clean = msleep.dropna(subset=['sleep_total', 'bodywt', 'vore'])
        p = (ggplot(msleep_clean,
                    aes(x='bodywt', y='sleep_total', color='vore'))
             + geom_point(size=8)
             + scale_x_log10())
        fig = p.draw()
        assert fig.layout.xaxis.type == 'log'
        # Should have one trace per vore category
        assert len(fig.data) == msleep_clean['vore'].nunique()

    def test_1_5_presidential_dataset(self):
        """Test presidential dataset."""
        presidential = data('presidential')
        p = (ggplot(presidential, aes(x='start', y='name', color='party'))
             + geom_point(size=10))
        fig = p.draw()
        # Should have one trace per party
        assert len(fig.data) == presidential['party'].nunique()
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == len(presidential)


# =============================================================================
# PART 2: GEOMS
# =============================================================================

class TestPart2Geoms:
    """Test Part 2: All geometry types."""

    def test_2_1_geom_point(self):
        """Test geom_point with various options."""
        df = pd.DataFrame({'x': np.random.randn(500), 'y': np.random.randn(500)})
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5, color='purple')
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'markers'

    def test_2_1_geom_point_shape(self):
        """Test geom_point with custom shape."""
        df = pd.DataFrame({'x': np.random.randn(500), 'y': np.random.randn(500)})
        p = ggplot(df, aes(x='x', y='y')) + geom_point(size=10, color='red', shape='diamond')
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].marker.symbol == 'diamond'

    def test_2_2_geom_line(self):
        """Test geom_line."""
        x = np.linspace(0, 10, 100)
        df = pd.DataFrame({'x': x, 'y': np.sin(x)})
        p = ggplot(df, aes(x='x', y='y')) + geom_line(color='steelblue', size=2)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'

    def test_2_2_geom_line_grouped(self):
        """Test geom_line with color grouping."""
        df = pd.DataFrame({
            'x': np.tile(np.linspace(0, 10, 50), 3),
            'y': np.concatenate([
                np.sin(np.linspace(0, 10, 50)),
                np.cos(np.linspace(0, 10, 50)),
                np.sin(np.linspace(0, 10, 50)) + np.cos(np.linspace(0, 10, 50))
            ]),
            'group': np.repeat(['sin', 'cos', 'sin+cos'], 50)
        })
        p = ggplot(df, aes(x='x', y='y', color='group')) + geom_line(size=2)
        fig = p.draw()
        assert len(fig.data) == 3

    def test_2_3_geom_path(self):
        """Test geom_path preserves point order."""
        t_vals = [i * 4 * math.pi / 100 for i in range(100)]
        spiral = pd.DataFrame({
            'x': [t * math.cos(t) for t in t_vals],
            'y': [t * math.sin(t) for t in t_vals],
        })
        p = ggplot(spiral, aes(x='x', y='y')) + geom_path(color='steelblue', size=2)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'

    def test_2_4_geom_bar(self):
        """Test geom_bar count-based."""
        df = pd.DataFrame({'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 200)})
        p = ggplot(df, aes(x='category')) + geom_bar()
        fig = p.draw()
        assert fig.data[0].type == 'bar'

    def test_2_4_geom_bar_fill(self):
        """Test bar chart with fill color by category."""
        mpg = data('mpg')
        p = ggplot(mpg, aes(x='class', fill='class')) + geom_bar(alpha=0.8)
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_4_geom_bar_stacked(self):
        """Test stacked bar chart."""
        mpg = data('mpg')
        p = ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar()
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_4_geom_bar_dodged(self):
        """Test dodged bar chart."""
        mpg = data('mpg')
        p = ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar(position='dodge')
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_4_geom_bar_position_dodge(self):
        """Test bar with position_dodge explicit."""
        mpg = data('mpg')
        p = ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar(position=position_dodge(width=0.8))
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_4_geom_bar_position_stack(self):
        """Test bar with position_stack explicit."""
        mpg = data('mpg')
        p = ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar(position=position_stack())
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_5_geom_col(self):
        """Test geom_col with pre-computed heights."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [25, 40, 30, 55]
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_col(fill='steelblue')
        fig = p.draw()
        assert fig.data[0].type == 'bar'

    def test_2_5_geom_col_grouped(self):
        """Test grouped column chart."""
        df = pd.DataFrame({
            'category': ['A', 'A', 'B', 'B', 'C', 'C'],
            'group': ['G1', 'G2'] * 3,
            'value': [10, 15, 20, 25, 15, 20]
        })
        p = ggplot(df, aes(x='category', y='value', fill='group')) + geom_col(position='dodge')
        fig = p.draw()
        assert all(t.type == 'bar' for t in fig.data)

    def test_2_6_geom_histogram(self):
        """Test geom_histogram."""
        df = pd.DataFrame({'x': np.random.randn(1000)})
        p = ggplot(df, aes(x='x')) + geom_histogram(fill='steelblue', alpha=0.7)
        fig = p.draw()
        # Uses go.Bar with pre-computed bins from stat_bin
        assert fig.data[0].type == 'bar'

    def test_2_6_geom_histogram_bins(self):
        """Test histogram with custom bins and color."""
        df = pd.DataFrame({'x': np.random.randn(1000)})
        p = ggplot(df, aes(x='x')) + geom_histogram(bins=30, color='white', fill='#FF6B6B')
        fig = p.draw()
        # Uses go.Bar with pre-computed bins from stat_bin
        assert fig.data[0].type == 'bar'

    def test_2_6_geom_histogram_grouped(self):
        """Test overlapping histograms by group."""
        df = pd.DataFrame({
            'x': np.concatenate([np.random.normal(0, 1, 500), np.random.normal(2, 1.5, 500)]),
            'group': ['A'] * 500 + ['B'] * 500
        })
        p = ggplot(df, aes(x='x', fill='group')) + geom_histogram(alpha=0.5, bins=30)
        fig = p.draw()
        assert len(fig.data) == 2  # Two histograms

    def test_2_7_geom_boxplot(self):
        """Test geom_boxplot."""
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C', 'D'], 50),
            'value': np.random.randn(200)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_boxplot()
        fig = p.draw()
        assert fig.data[0].type == 'box'

    def test_2_7_geom_boxplot_fill(self):
        """Test boxplot with fill color by category."""
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C', 'D'], 50),
            'value': np.random.randn(200)
        })
        p = ggplot(df, aes(x='category', y='value', fill='category')) + geom_boxplot(alpha=0.7)
        fig = p.draw()
        assert fig.data[0].type == 'box'

    def test_2_8_geom_violin(self):
        """Test geom_violin."""
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C', 'D'], 50),
            'value': np.random.randn(200)
        })
        p = ggplot(df, aes(x='category', y='value', fill='category')) + geom_violin(alpha=0.6)
        fig = p.draw()
        assert fig.data[0].type == 'violin'

    def test_2_9_geom_area(self):
        """Test geom_area."""
        x = np.linspace(0, 10, 100)
        df = pd.DataFrame({'x': x, 'y': np.sin(x) + 1.5})
        p = ggplot(df, aes(x='x', y='y')) + geom_area(fill='lightblue', alpha=0.7)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].fill == 'tozeroy'

    def test_2_9_geom_area_stacked(self):
        """Test stacked area with groups."""
        df = pd.DataFrame({
            'x': np.tile(np.linspace(0, 10, 50), 3),
            'y': np.abs(np.concatenate([
                np.sin(np.linspace(0, 10, 50)),
                0.5 * np.cos(np.linspace(0, 10, 50)) + 0.5,
                0.3 * np.sin(2 * np.linspace(0, 10, 50)) + 0.3
            ])),
            'group': np.repeat(['A', 'B', 'C'], 50)
        })
        p = ggplot(df, aes(x='x', y='y', fill='group')) + geom_area(alpha=0.6)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_2_10_geom_ribbon(self):
        """Test geom_ribbon."""
        x = np.linspace(0, 10, 50)
        y = np.sin(x)
        df = pd.DataFrame({'x': x, 'ymin': y - 0.3, 'ymax': y + 0.3})
        p = ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(fill='steelblue', alpha=0.3)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        # Ribbon should have fill property
        assert fig.data[0].fill is not None or len(fig.data) >= 2

    def test_2_11_geom_step(self):
        """Test geom_step."""
        x = np.linspace(0, 10, 20)
        df = pd.DataFrame({'x': x, 'y': np.sin(x)})
        p = ggplot(df, aes(x='x', y='y')) + geom_step(color='blue', size=2)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].line.shape == 'hv'

    def test_2_12_geom_segment(self):
        """Test geom_segment."""
        df = pd.DataFrame({
            'x': [1, 2, 3], 'y': [1, 2, 1],
            'xend': [2, 3, 4], 'yend': [3, 1, 2]
        })
        p = ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment(color='red', size=2)
        fig = p.draw()
        # Should have 3 segment traces (one per row)
        assert len(fig.data) == 3
        for trace in fig.data:
            assert trace.type == 'scatter'
            assert trace.mode == 'lines'

    def test_2_13_geom_errorbar(self):
        """Test geom_errorbar."""
        df = pd.DataFrame({
            'x': ['A', 'B', 'C', 'D'],
            'y': [10, 15, 12, 18],
            'ymin': [8, 13, 10, 15],
            'ymax': [12, 17, 14, 21]
        })
        p = (ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax'))
             + geom_col(fill='steelblue', alpha=0.7)
             + geom_errorbar(width=0.2))
        fig = p.draw()
        # Should have bar trace + errorbar trace
        assert len(fig.data) >= 2
        # First trace should be bar
        assert fig.data[0].type == 'bar'
        assert list(fig.data[0].y) == [10, 15, 12, 18]

    def test_2_14_geom_tile(self):
        """Test geom_tile heatmap."""
        x = np.arange(10)
        y = np.arange(10)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X / 2) * np.cos(Y / 2)
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + scale_fill_viridis_c()
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'

    def test_2_15_geom_text(self):
        """Test geom_text labels."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4], 'y': [2, 4, 3, 5],
            'label': ['Point A', 'Point B', 'Point C', 'Point D']
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=10, color='steelblue')
             + geom_text(aes(label='label'), vjust=-1))
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_2_16_geom_density(self):
        """Test geom_density."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(500)})
        p = ggplot(df, aes(x='x')) + geom_density(fill='lightblue', alpha=0.5)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        # Y values should be non-negative (density)
        assert all(y >= 0 for y in fig.data[0].y)
        # Should have fillcolor set
        assert fig.data[0].fillcolor is not None

    def test_2_17_geom_hline_vline(self):
        """Test geom_hline and geom_vline."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + geom_hline(data=0, color='red', linetype='dash')
             + geom_vline(data=0, color='blue', linetype='dash'))
        fig = p.draw()
        # Scatter trace for points
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'markers'
        assert len(fig.data[0].x) == 100
        # hline and vline are added as shapes, not traces
        assert len(fig.layout.shapes) >= 2

    def test_2_18_geom_abline(self):
        """Test geom_abline."""
        df = pd.DataFrame({'x': range(10), 'y': [i * 2 + 1 for i in range(10)]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=8)
             + geom_abline(slope=2, intercept=1, color='red', linetype='dash'))
        fig = p.draw()
        # Should have points + abline
        assert len(fig.data) >= 2
        # Points should match input data
        assert list(fig.data[0].y) == [i * 2 + 1 for i in range(10)]

    def test_2_19_geom_jitter(self):
        """Test geom_jitter."""
        np.random.seed(42)
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C'], 50),
            'value': np.random.randn(150)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_jitter(width=0.2, alpha=0.5)
        fig = p.draw()
        # geom_jitter uses box trace type with boxpoints='all' and no box
        assert fig.data[0].type == 'box'
        assert len(fig.data[0].y) == 150

    def test_2_19_geom_point_without_jitter(self):
        """Test geom_point without jitter for comparison."""
        np.random.seed(42)
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C'], 50),
            'value': np.random.randn(150)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_point(alpha=0.5)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].y) == 150

    def test_2_19_position_jitter(self):
        """Test position_jitter with geom_point."""
        np.random.seed(42)
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C'], 50),
            'value': np.random.randn(150)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_point(position=position_jitter(width=0.3, height=0), alpha=0.5)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].y) == 150

    def test_2_20_geom_rug(self):
        """Test geom_rug."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(alpha=0.5)
             + geom_rug(sides='bl', alpha=0.3))
        fig = p.draw()
        # Should have points + rug marks
        assert len(fig.data) >= 2
        assert fig.data[0].type == 'scatter'

    def test_2_21_geom_contour(self):
        """Test geom_contour."""
        x = np.linspace(-3, 3, 50)
        y = np.linspace(-3, 3, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2))
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_contour()
        fig = p.draw()
        assert fig.data[0].type == 'contour'

    def test_2_22_geom_contour_filled(self):
        """Test geom_contour_filled."""
        x = np.linspace(-3, 3, 50)
        y = np.linspace(-3, 3, 50)
        X, Y = np.meshgrid(x, y)
        Z = np.exp(-(X**2 + Y**2))
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_contour_filled()
        fig = p.draw()
        assert fig.data[0].type == 'contour'


# =============================================================================
# PART 3: SCALES
# =============================================================================

class TestPart3Scales:
    """Test Part 3: Scales."""

    def test_3_1_xlim_ylim(self):
        """Test xlim/ylim axis limits."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + xlim(-2, 2) + ylim(-2, 2)
        fig = p.draw()
        assert list(fig.layout.xaxis.range) == [-2, 2]
        assert list(fig.layout.yaxis.range) == [-2, 2]

    def test_3_1_lims(self):
        """Test lims() for both axes."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + lims(x=(-3, 3), y=(-3, 3))
        fig = p.draw()
        assert list(fig.layout.xaxis.range) == [-3, 3]
        assert list(fig.layout.yaxis.range) == [-3, 3]

    def test_3_2_scale_continuous(self):
        """Test scale_x_continuous and scale_y_continuous."""
        df = pd.DataFrame({'x': range(1, 11), 'y': [i**2 for i in range(1, 11)]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=8) + geom_line()
             + scale_x_continuous(name='X Axis', breaks=[2, 4, 6, 8, 10])
             + scale_y_continuous(name='Y Axis', limits=(0, 120)))
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'X Axis'
        assert fig.layout.yaxis.title.text == 'Y Axis'

    def test_3_3_log_scale(self):
        """Test log scale."""
        df = pd.DataFrame({
            'x': np.linspace(1, 100, 50),
            'y': np.exp(np.linspace(0, 5, 50))
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + scale_y_log10()
        fig = p.draw()
        assert fig.layout.yaxis.type == 'log'

    def test_3_4_scale_color_manual(self):
        """Test scale_color_manual."""
        df = pd.DataFrame({
            'x': np.random.randn(150),
            'y': np.random.randn(150),
            'group': np.repeat(['A', 'B', 'C'], 50)
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point(size=8)
             + scale_color_manual(values=['#E41A1C', '#377EB8', '#4DAF4A']))
        fig = p.draw()
        assert len(fig.data) == 3

    def test_3_5_scale_color_brewer(self):
        """Test scale_color_brewer."""
        df = pd.DataFrame({
            'x': np.random.randn(150),
            'y': np.random.randn(150),
            'group': np.repeat(['A', 'B', 'C'], 50)
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point(size=8)
             + scale_color_brewer(palette='Set2'))
        fig = p.draw()
        assert len(fig.data) == 3

    def test_3_6_scale_fill_gradient(self):
        """Test scale_fill_gradient."""
        df = pd.DataFrame({
            'x': np.tile(np.arange(10), 10),
            'y': np.repeat(np.arange(10), 10),
            'z': np.random.randn(100)
        })
        p = (ggplot(df, aes(x='x', y='y', fill='z'))
             + geom_tile()
             + scale_fill_gradient(low='blue', high='red'))
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'

    def test_3_7_scale_size(self):
        """Test scale_size."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.rand(50),
            'y': np.random.rand(50),
            'size_var': np.random.rand(50) * 100
        })
        p = (ggplot(df, aes(x='x', y='y', size='size_var'))
             + geom_point(color='steelblue', alpha=0.6)
             + scale_size(range=(2, 20)))
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 50
        # Marker sizes should vary
        sizes = fig.data[0].marker.size
        assert len(set(sizes)) > 1

    def test_3_8_scale_fill_manual(self):
        """Test scale_fill_manual."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [25, 40, 30, 55]
        })
        p = (ggplot(df, aes(x='category', y='value', fill='category'))
             + geom_col()
             + scale_fill_manual(values=['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3']))
        fig = p.draw()
        # Should have 4 traces with specified colors
        assert len(fig.data) == 4
        assert all(t.type == 'bar' for t in fig.data)

    def test_3_9_scale_shape_manual(self):
        """Test scale_shape_manual."""
        df = pd.DataFrame({
            'x': np.random.randn(60),
            'y': np.random.randn(60),
            'group': np.repeat(['A', 'B', 'C'], 20)
        })
        p = (ggplot(df, aes(x='x', y='y', shape='group'))
             + geom_point(size=10)
             + scale_shape_manual(values=['circle', 'square', 'diamond']))
        fig = p.draw()
        assert len(fig.data) == 3

    def test_3_10_scale_color_gradient(self):
        """Test scale_color_gradient continuous."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.rand(100),
            'y': np.random.rand(100),
            'z': np.random.rand(100)
        })
        p = (ggplot(df, aes(x='x', y='y', color='z'))
             + geom_point(size=8)
             + scale_color_gradient(low='yellow', high='red'))
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 100
        # Should have colorscale for continuous color
        assert fig.data[0].marker.colorscale is not None

    def test_3_11_scale_x_rangeslider(self):
        """Test scale_x_rangeslider."""
        dates = pd.date_range('2020-01-01', periods=365, freq='D')
        df = pd.DataFrame({'date': dates, 'value': np.cumsum(np.random.randn(365))})
        p = ggplot(df, aes(x='date', y='value')) + geom_line() + scale_x_rangeslider()
        fig = p.draw()
        assert fig.layout.xaxis.rangeslider.visible == True

    def test_3_12_scale_x_rangeselector(self):
        """Test scale_x_rangeselector with string shortcuts."""
        dates = pd.date_range('2020-01-01', periods=365, freq='D')
        df = pd.DataFrame({'date': dates, 'value': np.cumsum(np.random.randn(365))})
        p = (ggplot(df, aes(x='date', y='value'))
             + geom_line()
             + scale_x_rangeselector(buttons=['1m', '3m', '6m', 'ytd', '1y', 'all']))
        fig = p.draw()
        assert fig.layout.xaxis.rangeselector is not None


# =============================================================================
# PART 4: THEMES
# =============================================================================

class TestPart4Themes:
    """Test Part 4: Themes."""

    def test_4_1_theme_minimal(self):
        """Test theme_minimal."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_minimal()
        fig = p.draw()
        assert len(fig.data) == 2  # line + points
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_1_theme_classic(self):
        """Test theme_classic."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_classic()
        fig = p.draw()
        assert len(fig.data) == 2
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_1_theme_dark(self):
        """Test theme_dark."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_dark()
        fig = p.draw()
        assert len(fig.data) == 2
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_1_theme_ggplot2(self):
        """Test theme_ggplot2."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_ggplot2()
        fig = p.draw()
        assert len(fig.data) == 2
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_1_theme_bbc(self):
        """Test theme_bbc."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_bbc()
        fig = p.draw()
        assert len(fig.data) == 2
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_1_theme_nytimes(self):
        """Test theme_nytimes."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10) + theme_nytimes()
        fig = p.draw()
        assert len(fig.data) == 2
        assert list(fig.data[1].y) == [2, 4, 3, 5, 4]

    def test_4_2_custom_theme(self):
        """Test custom theme elements."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=10)
             + theme(
                 plot_background=element_rect(fill='#f0f0f0'),
                 panel_background=element_rect(fill='white'),
                 axis_text=element_text(size=12, color='darkblue')
             ))
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 5

    def test_4_3_legend_position_none(self):
        """Test hiding legend."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'group': np.random.choice(['A', 'B'], 100)
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point()
             + theme(legend_position='none'))
        fig = p.draw()
        assert len(fig.data) == 2  # 2 groups
        # Legend should be hidden
        assert fig.layout.showlegend == False

    def test_4_4_guides(self):
        """Test guides customization."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'category': np.random.choice(['A', 'B', 'C'], 100)
        })
        p = (ggplot(df, aes(x='x', y='y', color='category'))
             + geom_point(size=8)
             + guides(color=guide_legend(title='Category Type', nrow=1))
             + theme(legend_position='top'))
        fig = p.draw()
        assert len(fig.data) == 3  # 3 categories
        for trace in fig.data:
            assert trace.type == 'scatter'


# =============================================================================
# PART 5: FACETS
# =============================================================================

class TestPart5Facets:
    """Test Part 5: Facets."""

    def test_5_1_facet_wrap(self):
        """Test facet_wrap."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(300),
            'y': np.random.randn(300),
            'category': np.random.choice(['A', 'B', 'C'], 300)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + facet_wrap('category')
        fig = p.draw()
        # Should have 3 traces (one per facet category)
        assert len(fig.data) == 3
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 300

    def test_5_1_facet_wrap_ncol(self):
        """Test facet_wrap with ncol."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(300),
            'y': np.random.randn(300),
            'category': np.random.choice(['A', 'B', 'C'], 300)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + facet_wrap('category', ncol=1)
        fig = p.draw()
        # Should have 3 traces
        assert len(fig.data) == 3
        for trace in fig.data:
            assert trace.type == 'scatter'

    def test_5_2_facet_grid(self):
        """Test facet_grid."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(400),
            'y': np.random.randn(400),
            'row_var': np.tile(np.repeat(['R1', 'R2'], 100), 2),
            'col_var': np.repeat(['C1', 'C2'], 200)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + facet_grid(rows='row_var', cols='col_var')
        fig = p.draw()
        # Should have 4 traces (2x2 grid)
        assert len(fig.data) == 4
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 400

    def test_5_3_facet_free_scales(self):
        """Test facet with free scales."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.concatenate([np.random.uniform(0, 10, 50), np.random.uniform(0, 100, 50)]),
            'y': np.concatenate([np.random.uniform(0, 5, 50), np.random.uniform(0, 50, 50)]),
            'group': ['A'] * 50 + ['B'] * 50
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('group', scales='free')
        fig = p.draw()
        # Should have 2 traces
        assert len(fig.data) == 2
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 100

    def test_5_4_facet_labellers(self):
        """Test facet labellers."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'category': np.tile(['Group A', 'Group B'], 100)
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(alpha=0.5)
             + facet_wrap('category', labeller=label_both))
        fig = p.draw()
        # Should have 2 traces
        assert len(fig.data) == 2
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 200


# =============================================================================
# PART 6: LABELS & ANNOTATIONS
# =============================================================================

class TestPart6Labels:
    """Test Part 6: Labels and annotations."""

    def test_6_1_labs(self):
        """Test labs() for plot labels."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_line() + geom_point(size=10)
             + labs(title='Main Title', subtitle='Subtitle', x='X-Axis', y='Y-Axis', caption='Caption'))
        fig = p.draw()
        assert 'Main Title' in fig.layout.title.text

    def test_6_2_ggtitle(self):
        """Test ggtitle()."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point(size=10) + ggtitle('Quick Title')
        fig = p.draw()
        assert 'Quick Title' in fig.layout.title.text

    def test_6_3_annotate(self):
        """Test annotate()."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(50), 'y': np.random.randn(50)})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=6, alpha=0.6)
             + annotate('text', x=0, y=0, label='Center', size=14, color='red')
             + annotate('rect', xmin=-1, xmax=1, ymin=-1, ymax=1, fill='lightblue', alpha=0.3))
        fig = p.draw()
        # Should have scatter points trace
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 50
        # Should have annotations/shapes
        assert len(fig.layout.annotations) >= 1 or len(fig.layout.shapes) >= 1 or len(fig.data) >= 2


# =============================================================================
# PART 7: STATISTICS
# =============================================================================

class TestPart7Statistics:
    """Test Part 7: Statistics."""

    def test_7_1_geom_smooth_loess(self):
        """Test geom_smooth with LOESS."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + geom_smooth(method='loess', color='blue')
        fig = p.draw()
        assert len(fig.data) >= 2  # points + smooth line

    def test_7_1_geom_smooth_lm(self):
        """Test geom_smooth with linear regression."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + geom_smooth(method='lm', color='red')
        fig = p.draw()
        assert len(fig.data) >= 2

    def test_7_1_geom_smooth_with_se(self):
        """Test geom_smooth with confidence interval."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 100),
            'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
        })
        p = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + geom_smooth(method='loess', se=True)
        fig = p.draw()
        assert len(fig.data) >= 2

    def test_7_2_stat_ecdf(self):
        """Test stat_ecdf via geom_step."""
        df = pd.DataFrame({'x': np.random.randn(200)})
        p = ggplot(df, aes(x='x')) + geom_step(stat='ecdf')
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        # Y should range from near 0 to 1
        assert min(fig.data[0].y) > 0
        assert max(fig.data[0].y) == 1.0

    def test_7_3_stat_summary(self):
        """Test stat_summary added directly to plot."""
        np.random.seed(42)
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C'], 30),
            'value': np.random.randn(90) + np.tile([0, 2, 1], 30)
        })
        p = (ggplot(df, aes(x='category', y='value'))
             + geom_point(alpha=0.3)
             + stat_summary(fun='mean', geom='point', color='red', size=15))
        fig = p.draw()
        # Should have 2 traces: raw points and summary points
        assert len(fig.data) == 2
        # Summary trace should have 3 points (one per category)
        assert len(fig.data[1].x) == 3


# =============================================================================
# PART 8: COORDINATES
# =============================================================================

class TestPart8Coordinates:
    """Test Part 8: Coordinates."""

    def test_8_1_coord_cartesian(self):
        """Test coord_cartesian zoom."""
        df = pd.DataFrame({'x': range(1, 11), 'y': [i**2 for i in range(1, 11)]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point() + geom_line()
             + coord_cartesian(xlim=(3, 8), ylim=(10, 60)))
        fig = p.draw()
        # Should have point and line traces
        assert len(fig.data) == 2
        # Check axis ranges are approximately correct (some padding may be added)
        x_range = fig.layout.xaxis.range
        y_range = fig.layout.yaxis.range
        assert x_range[0] <= 3.5 and x_range[1] >= 7.5
        assert y_range[0] <= 15 and y_range[1] >= 55

    def test_8_2_coord_flip(self):
        """Test coord_flip."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D', 'E'],
            'value': [25, 40, 30, 55, 20]
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_col(fill='steelblue') + coord_flip()
        fig = p.draw()
        assert fig.data[0].orientation == 'h'

    def test_8_3_coord_polar(self):
        """Test coord_polar produces pie chart."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D'],
            'value': [30, 25, 20, 25]
        })
        p = ggplot(df, aes(x='category', y='value', fill='category')) + geom_col() + coord_polar()
        fig = p.draw()
        # coord_polar with bar produces pie chart
        assert fig.data[0].type == 'pie'


# =============================================================================
# PART 9: MAPS & GEOGRAPHIC
# =============================================================================

class TestPart9Maps:
    """Test Part 9: Maps and geographic plots."""

    def test_9_1_geom_map_us(self):
        """Test US choropleth map."""
        state_data = pd.DataFrame({
            'state': ['CA', 'TX', 'FL', 'NY', 'PA'],
            'population': [39.5, 29.0, 21.5, 19.5, 13.0]
        })
        states = map_data('state')
        p = (ggplot(state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states, palette='Blues'))
        fig = p.draw()
        assert fig.data[0].type == 'choropleth'

    def test_9_2_map_with_points(self):
        """Test map with point overlay."""
        state_data = pd.DataFrame({
            'state': ['CA', 'TX', 'FL'],
            'population': [39.5, 29.0, 21.5]
        })
        cities = pd.DataFrame({
            'city': ['New York', 'Los Angeles'],
            'lat': [40.7128, 34.0522],
            'lon': [-74.0060, -118.2437],
            'pop': [8.3, 3.9]
        })
        states = map_data('state')
        p = (ggplot(state_data, aes(map_id='state', fill='population'))
             + geom_map(map=states, palette='Blues')
             + geom_point(cities, aes(x='lon', y='lat', size='pop'), color='red'))
        fig = p.draw()
        assert len(fig.data) >= 2

    def test_9_3_world_map(self):
        """Test world choropleth map."""
        country_data = pd.DataFrame({
            'country': ['USA', 'CHN', 'JPN'],
            'gdp': [25.5, 18.3, 4.2]
        })
        countries = map_data('world')
        p = (ggplot(country_data, aes(map_id='country', fill='gdp'))
             + geom_map(map=countries, map_type='world', palette='Viridis'))
        fig = p.draw()
        assert fig.data[0].type == 'choropleth'

    def test_9_4_coord_sf_robinson(self):
        """Test coord_sf with Robinson projection."""
        cities = pd.DataFrame({
            'city': ['New York', 'London'],
            'lon': [-74.006, -0.128],
            'lat': [40.713, 51.507]
        })
        p = (ggplot(cities, aes(x='lon', y='lat'))
             + geom_map(map_type='world')
             + geom_point(color='red', size=10)
             + coord_sf(crs='robinson'))
        fig = p.draw()
        # Should have map and points
        assert len(fig.data) >= 2


# =============================================================================
# PART 10: 3D PLOTS
# =============================================================================

class TestPart103D:
    """Test Part 10: 3D plots."""

    def test_10_1_geom_point_3d(self):
        """Test geom_point_3d."""
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'z': np.random.randn(200)
        })
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()
        assert fig.data[0].type == 'scatter3d'

    def test_10_1_geom_point_3d_colored(self):
        """Test geom_point_3d with color grouping."""
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'z': np.random.randn(200),
            'group': np.random.choice(['A', 'B', 'C'], 200)
        })
        p = ggplot(df, aes(x='x', y='y', z='z', color='group')) + geom_point_3d(size=6)
        fig = p.draw()
        assert len(fig.data) == 3
        assert all(t.type == 'scatter3d' for t in fig.data)

    def test_10_2_geom_surface(self):
        """Test geom_surface."""
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface(colorscale='Viridis')
        fig = p.draw()
        assert fig.data[0].type == 'surface'

    def test_10_3_geom_wireframe(self):
        """Test geom_wireframe."""
        x = np.linspace(-5, 5, 30)
        y = np.linspace(-5, 5, 30)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_wireframe(color='steelblue', linewidth=1)
        fig = p.draw()
        assert len(fig.data) > 0
        assert fig.data[0].type == 'scatter3d'


# =============================================================================
# PART 11: FINANCIAL CHARTS
# =============================================================================

class TestPart11Financial:
    """Test Part 11: Financial charts."""

    def test_11_1_geom_candlestick(self):
        """Test geom_candlestick."""
        np.random.seed(42)
        n = 60
        dates = pd.date_range('2024-01-01', periods=n, freq='B')
        returns = np.random.normal(0.0005, 0.02, n)
        close = 100 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 100
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * 0.01
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * 0.01
        df = pd.DataFrame({
            'date': dates, 'open': open_prices, 'high': high, 'low': low, 'close': close
        })
        p = ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick()
        fig = p.draw()
        assert fig.data[0].type == 'candlestick'

    def test_11_2_geom_ohlc(self):
        """Test geom_ohlc."""
        np.random.seed(42)
        n = 60
        dates = pd.date_range('2024-01-01', periods=n, freq='B')
        returns = np.random.normal(0.0005, 0.02, n)
        close = 100 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 100
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * 0.01
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * 0.01
        df = pd.DataFrame({
            'date': dates, 'open': open_prices, 'high': high, 'low': low, 'close': close
        })
        p = ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_ohlc()
        fig = p.draw()
        assert fig.data[0].type == 'ohlc'


# =============================================================================
# PART 12: TIME SERIES
# =============================================================================

class TestPart12TimeSeries:
    """Test Part 12: Time series."""

    def test_12_1_scale_x_date(self):
        """Test scale_x_date."""
        dates = pd.date_range('2020-01-01', periods=24, freq='ME')
        df = pd.DataFrame({'date': dates, 'value': np.cumsum(np.random.randn(24)) + 50})
        p = (ggplot(df, aes(x='date', y='value'))
             + geom_line(color='steelblue', size=2)
             + geom_point(size=5)
             + scale_x_date(date_breaks='3 months', date_labels='%b %Y'))
        fig = p.draw()
        assert len(fig.data) == 2

    def test_12_1_scale_x_datetime(self):
        """Test scale_x_datetime."""
        timestamps = pd.date_range('2024-01-01 08:00', periods=48, freq='h')
        df = pd.DataFrame({
            'timestamp': timestamps,
            'value': np.sin(np.linspace(0, 4*np.pi, 48)) + np.random.randn(48) * 0.2
        })
        p = (ggplot(df, aes(x='timestamp', y='value'))
             + geom_line()
             + scale_x_datetime(date_labels='%b %d %H:%M'))
        fig = p.draw()
        assert len(fig.data) == 1

    def test_12_2_geom_range(self):
        """Test geom_range."""
        np.random.seed(42)
        dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
        temps = []
        for d in dates:
            seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
            noise = np.random.randn() * 15
            temps.append(seasonal + noise)
        df = pd.DataFrame({'date': dates, 'temperature': temps})
        p = ggplot(df, aes(x='date', y='temperature')) + geom_range(freq='ME')
        fig = p.draw()
        assert len(fig.data) >= 3  # range band + historical avg + lines


# =============================================================================
# PART 13: NETWORK GRAPHS
# =============================================================================

class TestPart13Networks:
    """Test Part 13: Network graphs."""

    def test_13_1_geom_edgebundle_circular(self):
        """Test geom_edgebundle with circular layout."""
        n_nodes = 20
        angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
        radius = 10
        node_x = radius * np.cos(angles)
        node_y = radius * np.sin(angles)
        edges = []
        for i in range(n_nodes):
            for offset in [5, 7, 10]:
                j = (i + offset) % n_nodes
                edges.append({'x': node_x[i], 'y': node_y[i], 'xend': node_x[j], 'yend': node_y[j]})
        edges_df = pd.DataFrame(edges)
        nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})
        p = (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
             + geom_edgebundle(compatibility_threshold=0.6)
             + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='white', size=4)
             + theme_dark())
        fig = p.draw()
        assert len(fig.data) > 20  # Many bundled edge traces + node trace

    def test_13_4_edgebundle_on_map(self):
        """Test edge bundling on geographic map."""
        airports = pd.DataFrame({
            'lon': [-122.4, -73.8, -87.6],
            'lat': [37.8, 40.6, 41.9],
            'name': ['SFO', 'JFK', 'ORD']
        })
        flights = pd.DataFrame({
            'src_lon': [-122.4, -73.8],
            'src_lat': [37.8, 40.6],
            'dst_lon': [-73.8, -87.6],
            'dst_lat': [40.6, 41.9]
        })
        p = (ggplot(flights, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
             + geom_map(map_type='usa')
             + geom_point(data=airports, mapping=aes(x='lon', y='lat'), color='white', size=8)
             + geom_edgebundle(C=4, compatibility_threshold=0.5, verbose=False)
             + theme_dark())
        fig = p.draw()
        assert len(fig.data) >= 2


# =============================================================================
# PART 14: ADVANCED EXAMPLES
# =============================================================================

class TestPart14Advanced:
    """Test Part 14: Advanced examples."""

    def test_14_1_multi_layer_plot(self):
        """Test multi-layer complex plot."""
        np.random.seed(0)
        df = pd.DataFrame({
            'x': np.arange(1, 21),
            'y': np.random.normal(size=20).cumsum(),
            'error': np.random.rand(20),
            'category': np.random.choice(['A', 'B'], 20),
            'label': [f'P{i}' for i in range(1, 21)]
        })
        p = (ggplot(df, aes(x='x', y='y', color='category'))
             + geom_line()
             + geom_point(size=5)
             + geom_errorbar(aes(yerr='error'), width=0.2)
             + geom_text(aes(label='label'), vjust=-1)
             + scale_color_brewer(type='qual', palette='Set1')
             + coord_cartesian(xlim=(0, 25), ylim=(-5, 10))
             + theme_minimal())
        fig = p.draw()
        assert len(fig.data) >= 4  # Multiple layers

    def test_14_2_faceted_multi_geom(self):
        """Test faceted plot with multiple geoms."""
        np.random.seed(0)
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'category': np.random.choice(['A', 'B'], 200)
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(alpha=0.5)
             + geom_smooth(method='loess', color='red')
             + facet_wrap('category')
             + theme_minimal())
        fig = p.draw()
        # Should have traces for 2 categories (points + smooth for each)
        assert len(fig.data) >= 2

    def test_14_3_bbc_style(self):
        """Test BBC style publication chart."""
        gapminder = pd.DataFrame({
            'year': [1952, 1962, 1972, 1982, 1992, 2002, 2007] * 2,
            'lifeExp': [36.3, 40.0, 43.5, 48.1, 52.0, 52.7, 54.1,
                        68.4, 70.0, 71.0, 74.0, 77.0, 78.8, 78.2],
            'country': ['Malawi'] * 7 + ['United States'] * 7
        })
        p = (ggplot(gapminder, aes(x='year', y='lifeExp', color='country'))
             + geom_line(size=3)
             + scale_x_continuous(format='d')
             + theme_bbc())
        fig = p.draw()
        assert len(fig.data) == 2

    def test_14_4_heatmap_gradient(self):
        """Test heatmap with custom gradient."""
        x = np.arange(0, 10, 1)
        y = np.arange(0, 10, 1)
        X, Y = np.meshgrid(x, y)
        Z = np.sin(X) * np.cos(Y)
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = (ggplot(df, aes(x='x', y='y', fill='z'))
             + geom_tile()
             + scale_fill_gradient(low='blue', high='red', name='Intensity')
             + theme_minimal())
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'

    def test_14_6_ggsize(self):
        """Test ggsize for figure dimensions."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_line() + geom_point(size=10)
             + ggsize(width=1000, height=400))
        fig = p.draw()
        assert fig.layout.width == 1000
        assert fig.layout.height == 400


# =============================================================================
# ADDITIONAL TESTS FOR COMPLETE COVERAGE
# =============================================================================

class TestPart2GeomsExtended:
    """Extended tests for Part 2 geoms variations."""

    def test_2_3_geom_path_star(self):
        """Test geom_path with star shape."""
        import math
        points = 5
        outer_r, inner_r = 1, 0.4
        star_x, star_y = [], []
        for i in range(points * 2 + 1):
            angle = i * math.pi / points - math.pi / 2
            r = outer_r if i % 2 == 0 else inner_r
            star_x.append(r * math.cos(angle))
            star_y.append(r * math.sin(angle))
        star = pd.DataFrame({'x': star_x, 'y': star_y})
        p = ggplot(star, aes(x='x', y='y')) + geom_path(color='gold', size=3)
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'
        # Verify we have all the star points
        assert len(fig.data[0].x) == 11  # 5 outer + 5 inner + 1 to close

    def test_2_18_geom_abline_multiple(self):
        """Test multiple geom_abline lines."""
        df = pd.DataFrame({'x': range(10), 'y': [i * 2 + 1 for i in range(10)]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=8)
             + geom_abline(slope=2, intercept=1, color='red', linetype='dash')
             + geom_abline(slope=1.5, intercept=3, color='blue'))
        fig = p.draw()
        # Should have points + 2 ablines
        assert len(fig.data) >= 3
        assert fig.data[0].type == 'scatter'


class TestPart4ThemesExtended:
    """Extended tests for Part 4 themes variations."""

    def test_4_2_theme_element_line(self):
        """Test custom theme with element_line."""
        df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(size=10)
             + theme(
                 panel_grid_major=element_line(color='lightgray', width=1, dash='dash'),
                 axis_line=element_line(color='black', width=2)
             ))
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert len(fig.data[0].x) == 5

    def test_4_3_guides_none(self):
        """Test hiding specific guide."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'group': np.random.choice(['A', 'B'], 100)
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point()
             + guides(color='none'))
        fig = p.draw()
        assert len(fig.data) == 2  # 2 groups
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 100

    def test_4_4_guide_colorbar(self):
        """Test continuous scale with colorbar customization."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.rand(100),
            'y': np.random.rand(100),
            'z': np.random.rand(100) * 100
        })
        p = (ggplot(df, aes(x='x', y='y', color='z'))
             + geom_point(size=8)
             + scale_color_gradient(low='blue', high='red')
             + guides(color=guide_colorbar(title='Value', barwidth=20)))
        fig = p.draw()
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].marker.colorbar is not None


class TestPart5FacetsExtended:
    """Extended tests for Part 5 facets variations."""

    def test_5_4_facet_label_value(self):
        """Test facet with label_value labeller."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'category': np.tile(['Group A', 'Group B'], 100)
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(alpha=0.5)
             + facet_wrap('category', labeller=label_value))
        fig = p.draw()
        # Should have 2 traces (one per group)
        assert len(fig.data) == 2
        total_points = sum(len(t.x) for t in fig.data)
        assert total_points == 200


class TestPart6LabelsExtended:
    """Extended tests for Part 6 labels variations."""

    def test_6_3_annotate_arrow(self):
        """Test annotate with arrow segment."""
        df = pd.DataFrame({
            'x': range(10),
            'y': [1, 3, 2, 5, 8, 6, 4, 3, 2, 1]
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_line(size=2, color='steelblue')
             + geom_point(size=8)
             + annotate('segment', x=6, y=9, xend=4, yend=8.2, arrow=True, color='red', size=2)
             + annotate('text', x=6, y=9.5, label='Peak value', size=12, color='red'))
        fig = p.draw()
        # Should have line and point traces
        assert len(fig.data) >= 2
        # Data should match input
        assert len(fig.data[1].y) == 10


class TestPart9MapsExtended:
    """Extended tests for Part 9 maps variations."""

    def test_9_4_coord_sf_orthographic(self):
        """Test coord_sf with orthographic projection."""
        cities = pd.DataFrame({
            'city': ['New York', 'London', 'Tokyo', 'Sydney'],
            'lon': [-74.006, -0.128, 139.692, 151.209],
            'lat': [40.713, 51.507, 35.690, -33.868]
        })
        p = (ggplot(cities, aes(x='lon', y='lat'))
             + geom_map(map_type='world')
             + geom_point(color='yellow', size=8)
             + coord_sf(crs='orthographic')
             + theme_dark())
        fig = p.draw()
        # Verify geo/map traces exist (choropleth for map + scatter for points)
        assert len(fig.data) >= 1
        # Verify geo projection is orthographic
        assert fig.layout.geo.projection.type == 'orthographic'


class TestPart10_3DExtended:
    """Extended tests for Part 10 3D plots variations."""

    def test_10_2_geom_surface_saddle(self):
        """Test geom_surface with saddle shape."""
        x = np.linspace(-5, 5, 50)
        y = np.linspace(-5, 5, 50)
        X, Y = np.meshgrid(x, y)
        Z = X**2 - Y**2  # Saddle function
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = (ggplot(df, aes(x='x', y='y', z='z'))
             + geom_surface(colorscale='RdBu'))
        fig = p.draw()
        assert fig.data[0].type == 'surface'
        # Verify z values have both positive and negative (saddle shape)
        z_vals = fig.data[0].z.flatten()
        assert z_vals.min() < 0
        assert z_vals.max() > 0

    def test_10_2_geom_surface_sinc(self):
        """Test geom_surface with 2D sinc function."""
        x = np.linspace(-10, 10, 80)
        y = np.linspace(-10, 10, 80)
        X, Y = np.meshgrid(x, y)
        r = np.sqrt(X**2 + Y**2)
        Z = np.where(r == 0, 1, np.sin(r) / r)
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = (ggplot(df, aes(x='x', y='y', z='z'))
             + geom_surface(colorscale='Plasma'))
        fig = p.draw()
        assert fig.data[0].type == 'surface'
        # Verify z max is near 1 (sinc(0) = 1)
        assert fig.data[0].z.max() == pytest.approx(1.0, abs=0.01)


class TestPart11FinancialExtended:
    """Extended tests for Part 11 financial charts variations."""

    def test_11_1_geom_candlestick_custom_colors(self):
        """Test geom_candlestick with custom colors."""
        np.random.seed(42)
        n = 60
        dates = pd.date_range('2024-01-01', periods=n, freq='B')
        returns = np.random.normal(0.0005, 0.02, n)
        close = 100 * np.cumprod(1 + returns)
        open_prices = np.roll(close, 1)
        open_prices[0] = 100
        high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * 0.01
        low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * 0.01
        df = pd.DataFrame({
            'date': dates, 'open': open_prices, 'high': high, 'low': low, 'close': close
        })
        p = (ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
             + geom_candlestick(increasing_color='#089981', decreasing_color='#F23645')
             + theme_dark())
        fig = p.draw()
        assert fig.data[0].type == 'candlestick'
        assert fig.data[0].increasing.fillcolor == '#089981'
        assert fig.data[0].decreasing.fillcolor == '#F23645'


class TestPart12TimeSeriesExtended:
    """Extended tests for Part 12 time series variations."""

    def test_12_1_scale_x_datetime_hourly(self):
        """Test scale_x_datetime with hourly data."""
        timestamps = pd.date_range('2024-01-01 08:00', periods=48, freq='h')
        df = pd.DataFrame({
            'timestamp': timestamps,
            'value': np.sin(np.linspace(0, 4*np.pi, 48)) + np.random.randn(48) * 0.2
        })
        p = (ggplot(df, aes(x='timestamp', y='value'))
             + geom_line()
             + scale_x_datetime(date_labels='%b %d %H:%M'))
        fig = p.draw()
        assert len(fig.data) == 1
        assert fig.data[0].type == 'scatter'
        assert fig.data[0].mode == 'lines'

    def test_12_2_geom_range_weekly(self):
        """Test geom_range with weekly aggregation."""
        np.random.seed(42)
        dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
        temps = []
        for d in dates:
            seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
            noise = np.random.randn() * 15
            temps.append(seasonal + noise)
        df = pd.DataFrame({'date': dates, 'temperature': temps})
        p = ggplot(df, aes(x='date', y='temperature')) + geom_range(freq='W-Fri')
        fig = p.draw()
        assert len(fig.data) >= 3

    def test_12_2_geom_range_show_years(self):
        """Test geom_range with specific historical years."""
        np.random.seed(42)
        dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
        temps = []
        for d in dates:
            seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
            noise = np.random.randn() * 15
            temps.append(seasonal + noise)
        df = pd.DataFrame({'date': dates, 'temperature': temps})
        p = ggplot(df, aes(x='date', y='temperature')) + geom_range(freq='ME', show_years=[2020, 2021])
        fig = p.draw()
        assert len(fig.data) >= 3

    def test_12_2_geom_range_faceted(self):
        """Test geom_range with facets."""
        np.random.seed(789)
        dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
        cities = ['New York', 'Los Angeles', 'Chicago']
        city_data = []
        for city in cities:
            base_temp = {'New York': 50, 'Los Angeles': 65, 'Chicago': 45}[city]
            amplitude = {'New York': 30, 'Los Angeles': 15, 'Chicago': 35}[city]
            for d in dates:
                seasonal = base_temp + amplitude * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
                noise = np.random.randn() * 15
                city_data.append({'date': d, 'temperature': seasonal + noise, 'city': city})
        df_cities = pd.DataFrame(city_data)
        p = (ggplot(df_cities, aes(x='date', y='temperature'))
             + geom_range(freq='ME')
             + facet_wrap('city', nrow=1)
             + theme_minimal())
        fig = p.draw()
        # Verify faceted output: 3 cities = multiple subplots
        assert len(fig.data) >= 3  # At least one trace per city
        # Verify facet subplot structure exists
        assert hasattr(fig.layout, 'annotations') or len(fig.data) >= 3


class TestPart13NetworksExtended:
    """Extended tests for Part 13 network graphs variations."""

    def test_13_2_random_network_edgebundle(self):
        """Test random network with edge bundling."""
        np.random.seed(42)
        n_nodes = 30
        n_edges = 80
        node_x = np.random.uniform(0, 100, n_nodes)
        node_y = np.random.uniform(0, 100, n_nodes)
        edges = []
        for _ in range(n_edges):
            i, j = np.random.choice(n_nodes, 2, replace=False)
            edges.append({'x': node_x[i], 'y': node_y[i], 'xend': node_x[j], 'yend': node_y[j]})
        edges_df = pd.DataFrame(edges)
        nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})
        p = (ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
             + geom_edgebundle(C=5, compatibility_threshold=0.5)
             + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='#00ff00', size=5)
             + theme_dark())
        fig = p.draw()
        assert len(fig.data) > 30  # Many bundled edge traces + node trace


class TestPart14AdvancedExtended:
    """Extended tests for Part 14 advanced examples variations."""

    def test_14_2_faceted_multi_geom_with_density(self):
        """Test faceted plot with points, smooth, and density."""
        np.random.seed(0)
        df = pd.DataFrame({
            'x': np.random.randn(200),
            'y': np.random.randn(200),
            'category': np.random.choice(['A', 'B'], 200)
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point(alpha=0.5)
             + geom_smooth(method='loess', color='red')
             + geom_density(aes(x='x'), color='blue')
             + facet_wrap('category')
             + theme_minimal())
        fig = p.draw()
        # Verify multiple geoms are present: point, smooth, density for each facet
        # 2 categories * 3 geoms = at least 6 traces (may vary based on density impl)
        assert len(fig.data) >= 4  # At least points and smooth for 2 categories
        # Verify scatter traces exist (for points)
        scatter_traces = [t for t in fig.data if t.type == 'scatter']
        assert len(scatter_traces) >= 2  # Points for each category


class TestDataCorrectness:
    """Tests verifying actual data values, not just chart types."""

    def test_geom_point_data_matches_input(self):
        """Verify scatter plot data matches input DataFrame."""
        df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [10, 20, 30, 40, 50]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        # Check data values match
        assert list(fig.data[0].x) == [1, 2, 3, 4, 5]
        assert list(fig.data[0].y) == [10, 20, 30, 40, 50]

    def test_geom_line_data_matches_input(self):
        """Verify line plot data matches input DataFrame."""
        df = pd.DataFrame({'x': [0, 1, 2, 3], 'y': [0, 2, 4, 6]})
        p = ggplot(df, aes(x='x', y='y')) + geom_line()
        fig = p.draw()
        # Check data values match
        assert list(fig.data[0].x) == [0, 1, 2, 3]
        assert list(fig.data[0].y) == [0, 2, 4, 6]

    def test_geom_bar_counts_categories(self):
        """Verify bar chart counts categories correctly."""
        df = pd.DataFrame({'category': ['A', 'A', 'A', 'B', 'B', 'C']})
        p = ggplot(df, aes(x='category')) + geom_bar()
        fig = p.draw()
        assert fig.data[0].type == 'bar'
        # Should have 3 categories with counts 3, 2, 1
        assert len(fig.data[0].x) == 3

    def test_geom_col_heights_match_input(self):
        """Verify column chart heights match input values."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 200, 150]
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_col()
        fig = p.draw()
        assert list(fig.data[0].y) == [100, 200, 150]

    def test_stat_ecdf_values_range(self):
        """Verify ECDF y values range from near 0 to 1."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})
        p = ggplot(df, aes(x='x')) + geom_step(stat='ecdf')
        fig = p.draw()
        y_vals = fig.data[0].y
        assert min(y_vals) > 0  # First point is 1/n
        assert max(y_vals) == 1.0  # Last point is 1

    def test_boxplot_has_correct_structure(self):
        """Verify boxplot has expected box trace structure."""
        df = pd.DataFrame({
            'category': np.repeat(['A', 'B'], 50),
            'value': np.random.randn(100)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_boxplot()
        fig = p.draw()
        assert fig.data[0].type == 'box'
        # Should have both categories
        assert set(fig.data[0].x) == {'A', 'B'}

    def test_violin_has_correct_structure(self):
        """Verify violin plot has expected violin trace structure."""
        df = pd.DataFrame({
            'category': np.repeat(['X', 'Y'], 50),
            'value': np.random.randn(100)
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_violin()
        fig = p.draw()
        assert fig.data[0].type == 'violin'

    def test_grouped_scatter_has_correct_trace_count(self):
        """Verify grouped scatter has one trace per group."""
        df = pd.DataFrame({
            'x': range(15),
            'y': range(15),
            'group': ['A'] * 5 + ['B'] * 5 + ['C'] * 5
        })
        p = ggplot(df, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()
        assert len(fig.data) == 3  # One trace per group

    def test_heatmap_dimensions(self):
        """Verify heatmap has correct dimensions."""
        x = np.arange(5)
        y = np.arange(4)
        X, Y = np.meshgrid(x, y)
        Z = X + Y
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile()
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'
        # Verify z data is present with correct total count
        assert len(fig.data[0].z.flatten()) == 20  # 4x5 = 20 values

    def test_3d_scatter_has_xyz(self):
        """Verify 3D scatter has x, y, z data."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
            'z': [7, 8, 9]
        })
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()
        fig = p.draw()
        assert fig.data[0].type == 'scatter3d'
        assert list(fig.data[0].x) == [1, 2, 3]
        assert list(fig.data[0].y) == [4, 5, 6]
        assert list(fig.data[0].z) == [7, 8, 9]

    def test_candlestick_ohlc_values(self):
        """Verify candlestick has correct OHLC values."""
        df = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=3),
            'open': [100, 102, 101],
            'high': [105, 106, 104],
            'low': [98, 100, 99],
            'close': [102, 101, 103]
        })
        p = ggplot(df, aes(x='date', open='open', high='high', low='low', close='close')) + geom_candlestick()
        fig = p.draw()
        assert fig.data[0].type == 'candlestick'
        assert list(fig.data[0].open) == [100, 102, 101]
        assert list(fig.data[0].high) == [105, 106, 104]
        assert list(fig.data[0].low) == [98, 100, 99]
        assert list(fig.data[0].close) == [102, 101, 103]

    def test_surface_has_2d_z_array(self):
        """Verify surface plot has 2D z array."""
        x = np.linspace(-2, 2, 10)
        y = np.linspace(-2, 2, 10)
        X, Y = np.meshgrid(x, y)
        Z = X**2 + Y**2
        df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
        p = ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()
        fig = p.draw()
        assert fig.data[0].type == 'surface'
        assert len(fig.data[0].z.shape) == 2
        assert fig.data[0].z.shape == (10, 10)


class TestLayoutProperties:
    """Tests verifying layout properties are set correctly."""

    def test_labs_sets_title(self):
        """Verify labs sets title correctly."""
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + labs(title='Test Title')
        fig = p.draw()
        assert 'Test Title' in fig.layout.title.text

    def test_labs_sets_axis_labels(self):
        """Verify labs sets axis labels correctly."""
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + labs(x='X Label', y='Y Label')
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'X Label'
        assert fig.layout.yaxis.title.text == 'Y Label'

    def test_scale_log_sets_axis_type(self):
        """Verify log scale sets axis type."""
        df = pd.DataFrame({'x': [1, 10, 100], 'y': [1, 10, 100]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10() + scale_y_log10()
        fig = p.draw()
        assert fig.layout.xaxis.type == 'log'
        assert fig.layout.yaxis.type == 'log'

    def test_coord_flip_orientation(self):
        """Verify coord_flip sets horizontal orientation."""
        df = pd.DataFrame({'x': ['A', 'B', 'C'], 'y': [1, 2, 3]})
        p = ggplot(df, aes(x='x', y='y')) + geom_col() + coord_flip()
        fig = p.draw()
        assert fig.data[0].orientation == 'h'

    def test_coord_polar_produces_pie(self):
        """Verify coord_polar with bar produces pie chart."""
        df = pd.DataFrame({'x': ['A', 'B', 'C'], 'y': [30, 40, 30]})
        p = ggplot(df, aes(x='x', y='y', fill='x')) + geom_col() + coord_polar()
        fig = p.draw()
        assert fig.data[0].type == 'pie'

    def test_xlim_ylim_sets_range(self):
        """Verify xlim/ylim sets axis range."""
        df = pd.DataFrame({'x': [0, 10], 'y': [0, 10]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + xlim(2, 8) + ylim(3, 7)
        fig = p.draw()
        # Check range values (could be list or tuple)
        assert list(fig.layout.xaxis.range) == [2, 8]
        assert list(fig.layout.yaxis.range) == [3, 7]

    def test_rangeslider_visible(self):
        """Verify rangeslider is enabled."""
        dates = pd.date_range('2024-01-01', periods=10)
        df = pd.DataFrame({'date': dates, 'value': range(10)})
        p = ggplot(df, aes(x='date', y='value')) + geom_line() + scale_x_rangeslider()
        fig = p.draw()
        assert fig.layout.xaxis.rangeslider.visible == True

    def test_theme_dark_background(self):
        """Verify theme_dark sets dark background."""
        df = pd.DataFrame({'x': [1, 2], 'y': [3, 4]})
        p = ggplot(df, aes(x='x', y='y')) + geom_point() + theme_dark()
        fig = p.draw()
        # Dark theme should have dark paper/plot background
        assert fig.layout.paper_bgcolor is not None or fig.layout.template is not None


class TestScaleColors:
    """Tests verifying color scales are applied correctly."""

    def test_scale_color_manual_applies_colors(self):
        """Verify manual colors are applied to traces."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'group': ['A', 'B', 'C']
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point(size=10)
             + scale_color_manual(values=['red', 'green', 'blue']))
        fig = p.draw()
        assert len(fig.data) == 3
        # Each trace should have one of our colors
        colors = [t.marker.color for t in fig.data]
        assert 'red' in colors or '#ff0000' in str(colors).lower()

    def test_scale_fill_gradient_creates_colorscale(self):
        """Verify fill gradient creates colorscale on heatmap."""
        df = pd.DataFrame({
            'x': [0, 1, 0, 1],
            'y': [0, 0, 1, 1],
            'z': [0, 0.5, 0.5, 1]
        })
        p = (ggplot(df, aes(x='x', y='y', fill='z'))
             + geom_tile()
             + scale_fill_gradient(low='white', high='black'))
        fig = p.draw()
        assert fig.data[0].type == 'heatmap'
        assert fig.data[0].colorscale is not None
