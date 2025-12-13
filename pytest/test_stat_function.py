import numpy as np
import pandas as pd

import pytest
from ggplotly import aes, geom_line, ggplot, stat_function


class TestStatFunction:
    """Tests for stat_function."""

    def test_basic_usage(self):
        """Test basic function overlay."""
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = (ggplot(df, aes(x='x'))
                + stat_function(fun=lambda x: x**2)
                + geom_line())
        fig = plot.draw()
        assert len(fig.data) >= 1

    def test_scipy_function(self):
        """Test with scipy stats function."""
        from scipy.stats import norm
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = (ggplot(df, aes(x='x'))
                + stat_function(fun=lambda x: norm.pdf(x, 0, 1))
                + geom_line())
        fig = plot.draw()
        assert len(fig.data) >= 1

    def test_custom_n(self):
        """Test custom number of points."""
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_function(mapping={'x': 'x'}, fun=lambda x: x, n=50)
        result, _ = stat.compute(df)
        assert len(result) == 50

    def test_custom_xlim(self):
        """Test custom x limits."""
        df = pd.DataFrame({'x': np.random.randn(100)})

        stat = stat_function(mapping={'x': 'x'}, fun=lambda x: x, xlim=(-5, 5))
        result, _ = stat.compute(df)
        assert result['x'].min() < -4.5
        assert result['x'].max() > 4.5

    def test_missing_fun_raises(self):
        """Test that missing fun raises error."""
        with pytest.raises(ValueError, match="requires 'fun'"):
            stat_function()

    def test_no_data_with_xlim(self):
        """Test stat_function works without data when xlim is provided."""
        from scipy.stats import norm

        plot = (ggplot()
                + stat_function(fun=lambda x: norm.pdf(x), xlim=(-4, 4))
                + geom_line())
        fig = plot.draw()
        assert len(fig.data) >= 1
