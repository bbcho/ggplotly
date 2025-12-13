import numpy as np
import pandas as pd
import pytest

from ggplotly import ggplot, aes, geom_fanchart


class TestGeomFanchart:
    """Tests for geom_fanchart."""

    def test_basic_usage(self):
        """Test simplest case: ggplot(df) + geom_fanchart()"""
        df = pd.DataFrame(np.random.randn(100, 50))
        plot = ggplot(df) + geom_fanchart()
        fig = plot.draw()
        # Should have traces for bands + median
        assert len(fig.data) >= 3

    def test_default_percentiles(self):
        """Test default percentiles create correct bands."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart()
        fig = plot.draw()
        # Default [10, 25, 50, 75, 90] = 2 bands + median = 5 traces
        # (2 bands × 2 traces each) + 1 median = 5
        assert len(fig.data) == 5

    def test_custom_percentiles(self):
        """Test custom percentile levels."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(percentiles=[5, 50, 95])
        fig = plot.draw()
        # 1 band + median = 3 traces
        assert len(fig.data) == 3

    def test_with_index_as_x(self):
        """Test that index is used as x by default."""
        dates = pd.date_range('2024-01-01', periods=50)
        df = pd.DataFrame(np.random.randn(50, 20), index=dates)
        plot = ggplot(df) + geom_fanchart()
        fig = plot.draw()
        assert len(fig.data) >= 3

    def test_explicit_x_column(self):
        """Test explicit x aesthetic."""
        df = pd.DataFrame({
            'time': np.linspace(0, 10, 50),
            **{f'sim_{i}': np.random.randn(50) for i in range(20)}
        })
        plot = ggplot(df) + geom_fanchart(aes(x='time'))
        fig = plot.draw()
        assert len(fig.data) >= 3

    def test_custom_color(self):
        """Test custom base color."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(color='coral')
        fig = plot.draw()
        # Check that fillcolor contains rgba
        assert 'rgba' in fig.data[1].fillcolor

    def test_custom_alpha(self):
        """Test custom alpha."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(alpha=0.5)
        fig = plot.draw()
        assert len(fig.data) >= 3

    def test_no_median(self):
        """Test hiding median line."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(show_median=False)
        fig = plot.draw()
        # 2 bands × 2 traces = 4 (no median)
        assert len(fig.data) == 4

    def test_select_columns(self):
        """Test selecting specific columns."""
        df = pd.DataFrame({
            'a': np.random.randn(50),
            'b': np.random.randn(50),
            'c': np.random.randn(50),
            'other': np.random.randn(50),
        })
        plot = ggplot(df) + geom_fanchart(columns=['a', 'b', 'c'])
        fig = plot.draw()
        assert len(fig.data) >= 3

    def test_non_numeric_excluded(self):
        """Test non-numeric columns are excluded."""
        df = pd.DataFrame({
            **{f'sim_{i}': np.random.randn(50) for i in range(10)},
            'label': ['a'] * 50,
        })
        plot = ggplot(df) + geom_fanchart()
        fig = plot.draw()
        assert len(fig.data) >= 3

    def test_single_band(self):
        """Test with percentiles that create a single band."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(percentiles=[25, 50, 75])
        fig = plot.draw()
        # 1 band + median = 3 traces
        assert len(fig.data) == 3

    def test_hex_color(self):
        """Test hex color format."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(color='#FF5733')
        fig = plot.draw()
        assert 'rgba' in fig.data[1].fillcolor

    def test_median_width(self):
        """Test custom median line width."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(median_width=4)
        fig = plot.draw()
        # Last trace is median
        assert fig.data[-1].line.width == 4

    def test_median_color(self):
        """Test custom median color."""
        df = pd.DataFrame(np.random.randn(50, 20))
        plot = ggplot(df) + geom_fanchart(median_color='red')
        fig = plot.draw()
        # Last trace is median
        assert fig.data[-1].line.color == 'red'

    def test_x_excluded_from_columns(self):
        """Test that x column is not included in percentile calculation."""
        df = pd.DataFrame({
            'x': np.linspace(0, 10, 50),
            **{f'y{i}': np.random.randn(50) for i in range(5)}
        })
        plot = ggplot(df) + geom_fanchart(aes(x='x'))
        fig = plot.draw()
        # Should compute percentiles from y columns only
        assert len(fig.data) >= 3

    def test_uses_stat_fanchart(self):
        """Test that geom_fanchart uses stat_fanchart internally."""
        from ggplotly.stats.stat_fanchart import stat_fanchart

        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        # Verify stat_fanchart can be imported and used
        stat = stat_fanchart(mapping={})
        result, _ = stat.compute(df)

        # Verify stat produces expected columns
        assert 'x' in result.columns
        assert 'p50' in result.columns

        # Verify geom produces same output structure
        plot = ggplot(df) + geom_fanchart()
        fig = plot.draw()
        # 2 bands × 2 traces + median = 5
        assert len(fig.data) == 5
