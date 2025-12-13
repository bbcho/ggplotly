import numpy as np
import pandas as pd

from ggplotly.stats.stat_fanchart import stat_fanchart


class TestStatFanchart:
    """Tests for stat_fanchart."""

    def test_basic_computation(self):
        """Test basic percentile computation."""
        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        stat = stat_fanchart(mapping={})
        result, _ = stat.compute(df)

        assert 'x' in result.columns
        assert 'p10' in result.columns
        assert 'p25' in result.columns
        assert 'p50' in result.columns
        assert 'p75' in result.columns
        assert 'p90' in result.columns
        assert 'median' in result.columns

    def test_custom_percentiles(self):
        """Test custom percentile levels."""
        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        stat = stat_fanchart(mapping={}, percentiles=[5, 50, 95])
        result, _ = stat.compute(df)

        assert 'p5' in result.columns
        assert 'p50' in result.columns
        assert 'p95' in result.columns
        assert 'p10' not in result.columns

    def test_select_columns(self):
        """Test selecting specific columns."""
        np.random.seed(42)
        df = pd.DataFrame({
            'a': np.random.randn(50),
            'b': np.random.randn(50),
            'c': np.random.randn(50),
            'other': np.random.randn(50),
        })

        stat = stat_fanchart(mapping={}, columns=['a', 'b', 'c'])
        result, _ = stat.compute(df)

        assert len(result) == 50

    def test_excludes_x_column(self):
        """Test that x column is excluded from percentile calculation."""
        np.random.seed(42)
        df = pd.DataFrame({
            'time': np.arange(50),
            **{f'y{i}': np.random.randn(50) for i in range(5)}
        })

        stat = stat_fanchart(mapping={'x': 'time'})
        result, _ = stat.compute(df)

        # Result should have 50 rows
        assert len(result) == 50
        # x values should come from 'time' column
        assert np.array_equal(result['x'].values, df['time'].values)

    def test_uses_index_when_no_x(self):
        """Test that index is used when x not specified."""
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', periods=50)
        df = pd.DataFrame(np.random.randn(50, 20), index=dates)

        stat = stat_fanchart(mapping={})
        result, _ = stat.compute(df)

        assert len(result) == 50
        # x should be the index values
        assert np.array_equal(result['x'].values, dates.values)

    def test_median_alias(self):
        """Test that median is alias for p50."""
        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        stat = stat_fanchart(mapping={})
        result, _ = stat.compute(df)

        assert np.array_equal(result['median'].values, result['p50'].values)

    def test_no_median_alias_without_p50(self):
        """Test that median alias not created when 50 not in percentiles."""
        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        stat = stat_fanchart(mapping={}, percentiles=[25, 75])
        result, _ = stat.compute(df)

        assert 'median' not in result.columns

    def test_empty_columns_returns_x_only(self):
        """Test that empty columns returns DataFrame with x only."""
        df = pd.DataFrame({'label': ['a'] * 50})  # No numeric columns

        stat = stat_fanchart(mapping={})
        result, _ = stat.compute(df)

        assert 'x' in result.columns
        assert len(result) == 50

    def test_mapping_updated(self):
        """Test that mapping is updated to include x."""
        np.random.seed(42)
        df = pd.DataFrame(np.random.randn(50, 20))

        stat = stat_fanchart(mapping={'color': 'red'})
        _, new_mapping = stat.compute(df)

        assert new_mapping['x'] == 'x'
        assert new_mapping['color'] == 'red'
