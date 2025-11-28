"""
Test suite for the major refactoring improvements made to ggplotly.

This test suite covers:
1. Grouped + color aesthetic combinations (bug fix in _transform_fig and manual geoms)
2. Plotly fill parameter handling in geom_line and geom_ribbon
3. Migrated geoms using _transform_fig (geom_step, geom_smooth, geom_density)
4. Manual geoms with proper color handling (geom_text, geom_errorbar, geom_segment)
"""

import sys
import os
import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import ggplot, aes
from ggplotly.geoms.geom_line import geom_line
from ggplotly.geoms.geom_ribbon import geom_ribbon
from ggplotly.geoms.geom_step import geom_step
from ggplotly.geoms.geom_smooth import geom_smooth
from ggplotly.geoms.geom_density import geom_density
from ggplotly.geoms.geom_text import geom_text
from ggplotly.geoms.geom_errorbar import geom_errorbar
from ggplotly.geoms.geom_segment import geom_segment
from ggplotly.geoms.geom_point import geom_point


# ============================================================================
# Test Suite 1: Grouped + Color Aesthetic Combinations
# ============================================================================

class TestGroupedColorCombinations:
    """Test that geoms properly handle group + color aesthetic combinations."""

    @pytest.fixture
    def grouped_data(self):
        """Sample data with grouping variable."""
        np.random.seed(42)
        return pd.DataFrame({
            'x': np.tile(np.linspace(0, 10, 20), 3),
            'y': np.random.randn(60).cumsum(),
            'group': np.repeat(['A', 'B', 'C'], 20)
        })

    def test_geom_line_grouped_color(self, grouped_data):
        """Test geom_line with both group and color aesthetics."""
        p = ggplot(grouped_data, aes(x='x', y='y', group='group', color='group')) + geom_line()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 3, "Should create 3 traces for 3 groups"

        # Check that each trace has a different color
        colors = [trace.line.color for trace in fig.data]
        assert len(set(colors)) == 3, "Each group should have a unique color"

    def test_geom_step_grouped_color(self, grouped_data):
        """Test geom_step with both group and color aesthetics."""
        p = ggplot(grouped_data, aes(x='x', y='y', group='group', color='group')) + geom_step()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 3, "Should create 3 traces for 3 groups"

        colors = [trace.line.color for trace in fig.data]
        assert len(set(colors)) == 3, "Each group should have a unique color"

    def test_geom_smooth_grouped_color(self, grouped_data):
        """Test geom_smooth with both group and color aesthetics."""
        p = ggplot(grouped_data, aes(x='x', y='y', group='group', color='group')) + geom_smooth()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # With se=TRUE (default), creates 6 traces: 3 ribbons + 3 lines
        assert len(fig.data) == 6, "Should create 6 traces (3 ribbons + 3 lines for 3 groups)"

        # Check that we have 3 line traces with unique colors
        line_traces = [trace for trace in fig.data if trace.mode == 'lines']
        assert len(line_traces) == 3, "Should have 3 line traces"
        colors = [trace.line.color for trace in line_traces]
        assert len(set(colors)) == 3, "Each group should have a unique color"

    def test_geom_errorbar_grouped_color(self):
        """Test geom_errorbar with both group and color aesthetics."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6],
            'y': [2, 4, 3, 5, 4, 6],
            'ymin': [1.5, 3.5, 2.5, 4.5, 3.5, 5.5],
            'ymax': [2.5, 4.5, 3.5, 5.5, 4.5, 6.5],
            'group': ['A', 'B', 'A', 'B', 'A', 'B']
        })

        p = ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax', group='group', color='group')) + geom_errorbar()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Should create 2 traces for 2 groups"

        colors = [trace.marker.color for trace in fig.data]
        assert len(set(colors)) == 2, "Each group should have a unique color"

    def test_geom_text_grouped_color(self):
        """Test geom_text with both group and color aesthetics."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y': [1, 2, 3, 4],
            'label': ['A', 'B', 'C', 'D'],
            'group': ['G1', 'G2', 'G1', 'G2']
        })

        p = ggplot(df, aes(x='x', y='y', label='label', group='group', color='group')) + geom_text()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Should create 2 traces for 2 groups"

    def test_geom_segment_grouped_color(self):
        """Test geom_segment with both group and color aesthetics."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'xend': [2, 3, 4],
            'yend': [2, 3, 4],
            'group': ['A', 'B', 'A']
        })

        p = ggplot(df, aes(x='x', y='y', xend='xend', yend='yend', group='group', color='group')) + geom_segment()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # Each segment creates a trace, but they're grouped by legendgroup
        assert len(fig.data) == 3, "Should create 3 traces (one per segment)"


# ============================================================================
# Test Suite 2: Plotly Fill Parameter Handling
# ============================================================================

class TestPlotlyFillParameter:
    """Test that Plotly fill parameters are handled correctly."""

    def test_geom_ribbon_with_default(self):
        """Test geom_ribbon without explicit fill or color."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'ymin': np.sin(np.linspace(0, 10, 50)) - 0.5,
            'ymax': np.sin(np.linspace(0, 10, 50)) + 0.5
        })

        p = ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(alpha=0.3)
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Ribbon creates 2 geom_line traces"
        assert fig.data[1].fill == 'tonexty', "Second trace should have fill='tonexty'"

    def test_geom_ribbon_with_color(self):
        """Test geom_ribbon with explicit color parameter."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'ymin': np.sin(np.linspace(0, 10, 50)) - 0.5,
            'ymax': np.sin(np.linspace(0, 10, 50)) + 0.5
        })

        p = ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(alpha=0.3, color='red')
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Ribbon creates 2 geom_line traces"
        assert fig.data[0].line.color == 'red', "First trace should be red"
        assert fig.data[1].line.color == 'red', "Second trace should be red"

    def test_geom_ribbon_with_fill(self):
        """Test geom_ribbon with explicit fill parameter."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'ymin': np.sin(np.linspace(0, 10, 50)) - 0.5,
            'ymax': np.sin(np.linspace(0, 10, 50)) + 0.5
        })

        p = ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(alpha=0.3, fill='blue')
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Ribbon creates 2 geom_line traces"
        assert fig.data[0].line.color == 'blue', "First trace should be blue"


# ============================================================================
# Test Suite 3: Migrated Geoms Using _transform_fig
# ============================================================================

class TestMigratedGeoms:
    """Test geoms that were migrated to use _transform_fig."""

    def test_geom_step_basic(self):
        """Test basic geom_step functionality."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 20),
            'y': np.cumsum(np.random.randn(20))
        })

        p = ggplot(df, aes(x='x', y='y')) + geom_step()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].line.shape == 'hv', "Should have step line shape"

    def test_geom_step_with_ecdf(self):
        """Test geom_step with ECDF transformation."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.normal(0, 1, 100)
        })

        p = ggplot(df, aes(x='x')) + geom_step(stat='ecdf')
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].line.shape == 'hv', "Should have step line shape"

    def test_geom_smooth_basic(self):
        """Test basic geom_smooth functionality."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'y': 2 * np.linspace(0, 10, 50) + np.random.randn(50) * 2
        })

        p = ggplot(df, aes(x='x', y='y')) + geom_smooth()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # With se=TRUE (default), creates 2 traces: 1 ribbon + 1 line
        assert len(fig.data) == 2, "Should create 2 traces (ribbon + line)"
        # Check that we have one ribbon and one line
        ribbon_traces = [trace for trace in fig.data if trace.fill == 'toself']
        line_traces = [trace for trace in fig.data if trace.mode == 'lines']
        assert len(ribbon_traces) == 1, "Should have 1 ribbon trace"
        assert len(line_traces) == 1, "Should have 1 line trace"

    def test_geom_density_basic(self):
        """Test basic geom_density functionality."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.normal(0, 1, 100)
        })

        p = ggplot(df, aes(x='x')) + geom_density()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].mode == 'lines', "Should be line mode"


# ============================================================================
# Test Suite 4: Manual Geoms with Special Requirements
# ============================================================================

class TestManualGeoms:
    """Test geoms that remain manual due to special requirements."""

    def test_geom_text_basic(self):
        """Test geom_text with label aesthetic."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 3, 5, 4],
            'label': ['A', 'B', 'C', 'D', 'E']
        })

        p = ggplot(df, aes(x='x', y='y', label='label')) + geom_text()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].mode == 'text', "Should be text mode"
        assert list(fig.data[0].text) == ['A', 'B', 'C', 'D', 'E'], "Text labels should match"

    def test_geom_errorbar_basic(self):
        """Test geom_errorbar with ymin/ymax."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [2, 4, 3],
            'ymin': [1.5, 3.5, 2.5],
            'ymax': [2.5, 4.5, 3.5]
        })

        p = ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) + geom_errorbar()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].error_y is not None, "Should have error_y attribute"

    def test_geom_errorbar_with_yerr(self):
        """Test geom_errorbar with yerr aesthetic."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [2, 4, 3],
            'yerr': [0.5, 0.5, 0.5]
        })

        p = ggplot(df, aes(x='x', y='y', yerr='yerr')) + geom_errorbar()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"
        assert fig.data[0].error_y is not None, "Should have error_y attribute"

    def test_geom_segment_basic(self):
        """Test geom_segment with xend/yend."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [1, 2, 3],
            'xend': [2, 3, 4],
            'yend': [2, 3, 4]
        })

        p = ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 3, "Should create 3 traces (one per segment)"

        # Check that only first segment shows legend
        legend_count = sum(1 for trace in fig.data if trace.showlegend)
        assert legend_count == 1, "Only first segment should show legend"


# ============================================================================
# Test Suite 5: Edge Cases and Regression Tests
# ============================================================================

class TestEdgeCases:
    """Test edge cases and potential regressions."""

    def test_group_without_color(self):
        """Test that group aesthetic works without color."""
        df = pd.DataFrame({
            'x': np.tile(np.linspace(0, 10, 20), 2),
            'y': np.random.randn(40).cumsum(),
            'group': np.repeat(['A', 'B'], 20)
        })

        p = ggplot(df, aes(x='x', y='y', group='group')) + geom_line()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Should create 2 traces for 2 groups"
        # All traces should have the same default color
        colors = [trace.line.color for trace in fig.data]
        assert len(set(colors)) == 1, "All groups should have same default color"

    def test_color_without_group(self):
        """Test that color aesthetic works without group."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6],
            'y': [2, 4, 3, 5, 4, 6],
            'category': ['A', 'A', 'B', 'B', 'C', 'C']
        })

        p = ggplot(df, aes(x='x', y='y', color='category')) + geom_line()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 3, "Should create 3 traces for 3 categories"

        colors = [trace.line.color for trace in fig.data]
        assert len(set(colors)) == 3, "Each category should have a unique color"

    def test_no_group_no_color(self):
        """Test basic plot with no grouping or color."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [2, 4, 3, 5, 4]
        })

        p = ggplot(df, aes(x='x', y='y')) + geom_line()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 1, "Should create 1 trace"

    def test_multiple_geoms_same_plot(self):
        """Test multiple geoms on the same plot."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            'y': np.sin(np.linspace(0, 10, 50))
        })

        p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point()
        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Should create 2 traces (line + point)"

    def test_size_aesthetic_with_line_geoms(self):
        """Test that line geoms properly ignore size aesthetic mapped to columns."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.rand(100),
            'y': np.random.rand(100),
            'category': np.random.choice(['A', 'B', 'C'], 100),
            'size_var': np.random.rand(100) * 20
        })

        # Import additional required functions
        from ggplotly import scale_color_brewer, facet_wrap, labs, theme_minimal

        # Complex plot with size aesthetic - should work without errors
        p = (ggplot(df, aes(x='x', y='y', color='category', size='size_var')) +
             geom_point(alpha=0.6) +
             geom_smooth(method='loess') +
             facet_wrap('category') +
             scale_color_brewer(type='qual', palette='Set1') +
             labs(title='Complex Multi-Component Plot', x='X Variable', y='Y Variable') +
             theme_minimal())

        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # Should have traces from geom_point and geom_smooth (with ribbon) for each facet
        # 3 facets × (1 point + 1 ribbon + 1 smooth line) = 9 traces
        assert len(fig.data) == 9, "Should create 9 traces (3 categories × 3 geoms: point + ribbon + line)"

    def test_facet_with_geom_specific_data(self):
        """Test that faceting works with geoms that have their own data."""
        np.random.seed(42)

        # Main data
        df_main = pd.DataFrame({
            'x': np.arange(30),
            'y': np.random.rand(30),
            'category': np.repeat(['A', 'B', 'C'], 10)
        })

        # Confidence interval data (different from main)
        df_ci = pd.DataFrame({
            'x': np.tile(np.arange(10), 3),
            'upper': np.concatenate([np.random.rand(10) + 0.6 for _ in range(3)]),
            'lower': np.concatenate([np.random.rand(10) + 0.2 for _ in range(3)]),
            'category': np.repeat(['A', 'B', 'C'], 10)
        })

        # Import required functions
        from ggplotly import geom_ribbon, facet_wrap

        # Create plot with geom_ribbon using its own data
        p = (ggplot(df_main, aes(x='x', y='y', color='category')) +
             geom_ribbon(data=df_ci, mapping=aes(x='x', ymin='lower', ymax='upper', fill='category'), alpha=0.2) +
             geom_point() +
             facet_wrap('category'))

        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # Should create traces for each facet without errors
        assert len(fig.data) > 0, "Should create traces successfully"

    def test_ultra_complex_multi_dataframe_plot(self):
        """
        Ultra-complex test with 5 dataframes, 5 geoms, faceting, themes, and color scales.
        This showcases the full power of ggplotly with multiple data sources.
        """
        np.random.seed(123)

        # DataFrame 1: Scatter data with measurements
        df_measurements = pd.DataFrame({
            'time': np.tile(np.arange(1, 21), 3),
            'value': np.concatenate([
                50 + 10*np.random.randn(20) + np.arange(20)*0.5,
                60 + 12*np.random.randn(20) + np.arange(20)*0.3,
                55 + 8*np.random.randn(20) + np.arange(20)*0.4
            ]),
            'region': np.repeat(['North', 'South', 'East'], 20),
            'size': np.random.uniform(5, 15, 60)
        })

        # DataFrame 2: Trend lines
        df_trends = pd.DataFrame({
            'time': np.tile(np.arange(1, 21), 3),
            'trend': np.concatenate([
                50 + np.arange(20)*0.5,
                60 + np.arange(20)*0.3,
                55 + np.arange(20)*0.4
            ]),
            'region': np.repeat(['North', 'South', 'East'], 20)
        })

        # DataFrame 3: Confidence intervals
        df_confidence = pd.DataFrame({
            'time': np.tile(np.linspace(1, 20, 40), 3),
            'upper': np.concatenate([
                58 + np.linspace(0, 10, 40),
                68 + np.linspace(0, 6, 40),
                61 + np.linspace(0, 8, 40)
            ]),
            'lower': np.concatenate([
                42 + np.linspace(0, 10, 40),
                52 + np.linspace(0, 6, 40),
                49 + np.linspace(0, 8, 40)
            ]),
            'region': np.repeat(['North', 'South', 'East'], 40)
        })

        # DataFrame 4: Error bars at key timepoints
        df_errors = pd.DataFrame({
            'time': [5, 10, 15] * 3,
            'value': [52, 54, 58, 62, 64, 66, 57, 59, 63],
            'ymin': [48, 50, 54, 58, 60, 62, 53, 55, 59],
            'ymax': [56, 58, 62, 66, 68, 70, 61, 63, 67],
            'region': ['North', 'North', 'North', 'South', 'South', 'South', 'East', 'East', 'East']
        })

        # DataFrame 5: Text annotations
        df_labels = pd.DataFrame({
            'time': [15, 15, 15],
            'value': [62, 68, 65],
            'label': ['Peak', 'Max', 'High'],
            'region': ['North', 'South', 'East']
        })

        # Import additional required functions
        from ggplotly import (geom_ribbon, geom_errorbar, geom_text,
                             facet_wrap, scale_color_brewer, scale_fill_brewer,
                             labs, theme_dark)

        # Build the complex plot layer by layer
        p = (ggplot(df_measurements, aes(x='time', y='value', color='region')) +
             geom_ribbon(data=df_confidence, mapping=aes(x='time', ymin='lower', ymax='upper', fill='region'), alpha=0.2) +
             geom_line(data=df_trends, mapping=aes(x='time', y='trend', color='region'), size=3) +
             geom_point(alpha=0.7, size=8) +
             geom_errorbar(data=df_errors, mapping=aes(x='time', y='value', ymin='ymin', ymax='ymax', color='region'), alpha=0.6) +
             geom_text(data=df_labels, mapping=aes(x='time', y='value', label='label', color='region'), size=12) +
             facet_wrap('region', ncol=3) +
             scale_color_brewer(type='qual', palette='Dark2') +
             scale_fill_brewer(type='qual', palette='Dark2') +
             labs(
                 title='Ultra-Complex Multi-Source Analysis',
                 subtitle='Demonstrating 5 DataFrames with 5 Geoms, Faceting, and Theming',
                 x='Time Period',
                 y='Measurement Value'
             ) +
             theme_dark())

        fig = p.draw()

        assert isinstance(fig, go.Figure)
        # Should successfully create all traces across all facets
        assert len(fig.data) > 0, "Should create traces successfully"
        # Verify we have multiple subplots (3 facets)
        assert 'xaxis' in fig.layout, "Should have x-axis defined"
        assert 'xaxis2' in fig.layout, "Should have second facet"
        assert 'xaxis3' in fig.layout, "Should have third facet"

    def test_geom_col_with_alpha(self):
        """Test that geom_col properly handles the alpha parameter without duplicate keyword errors."""
        df = pd.DataFrame({
            'x': ['A', 'B', 'C', 'D'],
            'y': [3, 7, 2, 5],
            'group': ['G1', 'G1', 'G2', 'G2']
        })

        # Import required functions
        from ggplotly import geom_col, theme_minimal

        # This should not raise TypeError about duplicate 'opacity' keyword
        p = (ggplot(df, aes(x='x', y='y', fill='group', group='group')) +
             geom_col(alpha=0.7) +
             theme_minimal())

        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 2, "Should create 2 traces (one per group)"
        # Verify opacity was applied correctly
        for trace in fig.data:
            assert trace.opacity == 0.7, f"Expected opacity 0.7, got {trace.opacity}"

    def test_geom_violin_with_alpha(self):
        """Test that geom_violin properly handles the alpha parameter without duplicate keyword errors."""
        np.random.seed(42)

        df = pd.DataFrame({
            'category': np.repeat(['A', 'B', 'C'], 50),
            'value': np.concatenate([
                np.random.normal(10, 2, 50),
                np.random.normal(15, 3, 50),
                np.random.normal(12, 2.5, 50)
            ])
        })

        # Import required functions
        from ggplotly import geom_violin, theme_minimal

        # This should not raise TypeError about duplicate 'opacity' keyword
        p = (ggplot(df, aes(x='category', y='value', fill='category')) +
             geom_violin(alpha=0.6) +
             theme_minimal())

        fig = p.draw()

        assert isinstance(fig, go.Figure)
        assert len(fig.data) == 3, "Should create 3 traces (one per category)"
        # Verify opacity was applied correctly
        for trace in fig.data:
            assert trace.opacity == 0.6, f"Expected opacity 0.6, got {trace.opacity}"


# ============================================================================
# Run all tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
