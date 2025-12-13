import numpy as np
import pandas as pd

import pytest
from ggplotly import aes, geom_qq, geom_qq_line, ggplot, stat_qq, stat_qq_line


class TestStatQQ:
    """Tests for stat_qq."""

    def test_basic_computation(self):
        """Test basic Q-Q stat computation."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_qq(mapping={'sample': 'x'})
        result, new_mapping = stat.compute(df)

        assert 'theoretical' in result.columns
        assert 'sample' in result.columns
        assert len(result) == 100
        assert new_mapping['x'] == 'theoretical'
        assert new_mapping['y'] == 'sample'

    def test_custom_distribution(self):
        """Test Q-Q with custom distribution."""
        from scipy.stats import t

        np.random.seed(42)
        df = pd.DataFrame({'x': t.rvs(df=5, size=100)})

        stat = stat_qq(mapping={'sample': 'x'}, distribution=t, dparams={'df': 5})
        result, _ = stat.compute(df)

        assert len(result) == 100
        # Theoretical quantiles should be from t-distribution
        assert result['theoretical'].min() < -3

    def test_missing_sample_raises(self):
        """Test that missing sample aesthetic raises error."""
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_qq(mapping={})
        with pytest.raises(ValueError, match="requires 'sample'"):
            stat.compute(df)

    def test_missing_column_raises(self):
        """Test that missing column raises error."""
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_qq(mapping={'sample': 'nonexistent'})
        with pytest.raises(ValueError, match="not found in data"):
            stat.compute(df)


class TestStatQQLine:
    """Tests for stat_qq_line."""

    def test_basic_computation(self):
        """Test basic Q-Q line computation."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_qq_line(mapping={'sample': 'x'})
        result, new_mapping = stat.compute(df)

        assert 'theoretical' in result.columns
        assert 'sample' in result.columns
        assert len(result) == 2  # Line defined by 2 points
        assert new_mapping['x'] == 'theoretical'
        assert new_mapping['y'] == 'sample'

    def test_custom_line_p(self):
        """Test custom quantile positions for line."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_qq_line(mapping={'sample': 'x'}, line_p=(0.10, 0.90))
        result, _ = stat.compute(df)

        assert len(result) == 2

    def test_custom_distribution(self):
        """Test Q-Q line with custom distribution."""
        from scipy.stats import t

        np.random.seed(42)
        df = pd.DataFrame({'x': t.rvs(df=5, size=100)})

        stat = stat_qq_line(mapping={'sample': 'x'}, distribution=t, dparams={'df': 5})
        result, _ = stat.compute(df)

        assert len(result) == 2


class TestGeomQQ:
    """Tests for geom_qq."""

    def test_basic_usage(self):
        """Test basic Q-Q plot."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq()
        fig = plot.draw()
        assert len(fig.data) >= 1
        # Should render as scatter points
        assert fig.data[0].mode == 'markers'

    def test_qq_with_line(self):
        """Test Q-Q plot with reference line."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq() + geom_qq_line()
        fig = plot.draw()
        assert len(fig.data) >= 2

    def test_custom_distribution(self):
        """Test Q-Q plot against t-distribution."""
        from scipy.stats import t

        np.random.seed(42)
        df = pd.DataFrame({'x': t.rvs(df=5, size=100)})

        plot = (ggplot(df, aes(sample='x'))
                + geom_qq(distribution=t, dparams={'df': 5}))
        fig = plot.draw()
        assert len(fig.data) >= 1

    def test_custom_color(self):
        """Test custom point color."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq(color='blue')
        fig = plot.draw()
        assert fig.data[0].marker.color == 'blue'

    def test_custom_size(self):
        """Test custom point size."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq(size=12)
        fig = plot.draw()
        assert fig.data[0].marker.size == 12


class TestGeomQQLine:
    """Tests for geom_qq_line."""

    def test_basic_usage(self):
        """Test basic Q-Q reference line."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq_line()
        fig = plot.draw()
        assert len(fig.data) >= 1
        # Should render as lines
        assert fig.data[0].mode == 'lines'

    def test_custom_color(self):
        """Test custom line color."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq_line(color='blue')
        fig = plot.draw()
        assert fig.data[0].line.color == 'blue'

    def test_custom_linetype(self):
        """Test custom line style."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq_line(linetype='solid')
        fig = plot.draw()
        assert fig.data[0].line.dash == 'solid'

    def test_custom_size(self):
        """Test custom line width."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq_line(size=3)
        fig = plot.draw()
        assert fig.data[0].line.width == 3

    def test_custom_line_p(self):
        """Test custom quantile positions for line fit."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(sample='x')) + geom_qq_line(line_p=(0.10, 0.90))
        fig = plot.draw()
        assert len(fig.data) >= 1


class TestQQIntegration:
    """Integration tests for Q-Q plots."""

    def test_full_qq_plot(self):
        """Test complete Q-Q plot with points and line."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = (ggplot(df, aes(sample='x'))
                + geom_qq()
                + geom_qq_line())
        fig = plot.draw()

        # Should have both points and line
        assert len(fig.data) == 2
        modes = [t.mode for t in fig.data]
        assert 'markers' in modes
        assert 'lines' in modes

    def test_qq_t_distribution(self):
        """Test Q-Q plot comparing data to t-distribution."""
        from scipy.stats import t

        np.random.seed(42)
        df = pd.DataFrame({'x': t.rvs(df=5, size=100)})

        plot = (ggplot(df, aes(sample='x'))
                + geom_qq(distribution=t, dparams={'df': 5})
                + geom_qq_line(distribution=t, dparams={'df': 5}))
        fig = plot.draw()

        assert len(fig.data) == 2

    def test_qq_normality_check(self):
        """Test Q-Q plot for checking normality."""
        np.random.seed(42)
        # Generate normal data
        normal_data = np.random.randn(100)
        df = pd.DataFrame({'x': normal_data})

        plot = (ggplot(df, aes(sample='x'))
                + geom_qq()
                + geom_qq_line())
        fig = plot.draw()

        # Points should roughly follow the line for normal data
        points = fig.data[0] if fig.data[0].mode == 'markers' else fig.data[1]
        line = fig.data[0] if fig.data[0].mode == 'lines' else fig.data[1]

        assert len(points.x) == 100
        assert len(line.x) == 2
