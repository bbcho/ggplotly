import numpy as np
import pandas as pd
import pytest

from ggplotly import ggplot, aes, geom_line, facet_wrap
from ggplotly.stats.stat_stl import stat_stl


class TestStatStl:
    """Tests for stat_stl."""

    def test_basic_computation(self):
        """Test basic STL decomposition computation."""
        np.random.seed(42)
        n = 60
        t = np.arange(n)
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=n, freq='ME'),
            'value': 10 * np.sin(2 * np.pi * t / 12) + 0.1 * t + np.random.randn(n)
        })

        stat = stat_stl(mapping={'x': 'date', 'y': 'value'}, period=12)
        result, mapping = stat.compute(df)

        assert 'component' in result.columns
        assert set(result['component'].unique()) == {'Observed', 'Trend', 'Seasonal', 'Residual'}
        # Should have 4× original rows (one for each component)
        assert len(result) == len(df) * 4

    def test_component_order_preserved(self):
        """Test that component order is preserved for faceting."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': range(60),
            'y': np.random.randn(60).cumsum()
        })

        stat = stat_stl(mapping={'x': 'x', 'y': 'y'}, period=12)
        result, _ = stat.compute(df)

        # Check categorical order
        assert result['component'].cat.categories.tolist() == [
            'Observed', 'Trend', 'Seasonal', 'Residual'
        ]

    def test_robust_decomposition(self):
        """Test robust STL handles outliers."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n)) + np.random.randn(n) * 0.1
        })
        df.loc[10, 'y'] = 100  # Add outlier

        stat = stat_stl(mapping={'x': 'x', 'y': 'y'}, period=12, robust=True)
        result, _ = stat.compute(df)

        assert 'component' in result.columns
        assert len(result) == len(df) * 4

    def test_missing_period_raises(self):
        """Test that missing period raises error."""
        df = pd.DataFrame({'x': range(60), 'y': np.random.randn(60)})

        stat = stat_stl(mapping={'x': 'x', 'y': 'y'})
        with pytest.raises(ValueError, match="period must be specified"):
            stat.compute(df)

    def test_missing_y_raises(self):
        """Test that missing y aesthetic raises error."""
        df = pd.DataFrame({'x': range(60), 'y': np.random.randn(60)})

        stat = stat_stl(mapping={'x': 'x'}, period=12)
        with pytest.raises(ValueError, match="requires y aesthetic"):
            stat.compute(df)

    def test_custom_seasonal(self):
        """Test custom seasonal smoother."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': range(60),
            'y': np.random.randn(60).cumsum()
        })

        stat = stat_stl(mapping={'x': 'x', 'y': 'y'}, period=12, seasonal=13)
        result, _ = stat.compute(df)

        assert 'component' in result.columns
        assert len(result) == len(df) * 4

    def test_preserves_other_columns(self):
        """Test that other columns are preserved in output."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': range(60),
            'y': np.random.randn(60).cumsum(),
            'group': ['A'] * 30 + ['B'] * 30
        })

        stat = stat_stl(mapping={'x': 'x', 'y': 'y'}, period=12)
        result, _ = stat.compute(df)

        # Original columns should be preserved
        assert 'x' in result.columns
        assert 'group' in result.columns

    def test_faceted_workflow(self):
        """Test manual stat computation followed by faceted plot."""
        np.random.seed(42)
        n = 60
        t = np.arange(n)
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=n, freq='ME'),
            'value': 10 * np.sin(2 * np.pi * t / 12) + 0.1 * t + np.random.randn(n)
        })

        # Compute stat manually
        stat = stat_stl(mapping={'x': 'date', 'y': 'value'}, period=12)
        stl_data, _ = stat.compute(df)

        # Use result in plot
        plot = (ggplot(stl_data, aes(x='date', y='value'))
                + geom_line()
                + facet_wrap('component', ncol=1))
        fig = plot.draw()

        # Should have 4 subplots (one per component)
        assert len(fig.data) >= 4
