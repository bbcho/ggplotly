import numpy as np
import pandas as pd

import pytest
from ggplotly import aes, geom_stl, ggplot


class TestGeomStl:
    """Tests for geom_stl."""

    def test_basic_usage(self):
        """Test basic STL decomposition plot."""
        np.random.seed(42)
        n = 60
        t = np.arange(n)
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=n, freq='ME'),
            'value': 10 * np.sin(2 * np.pi * t / 12) + 0.1 * t + np.random.randn(n)
        })

        plot = ggplot(df, aes(x='date', y='value')) + geom_stl(period=12)
        fig = plot.draw()

        # Should have 4 traces (one per component)
        assert len(fig.data) == 4

    def test_creates_four_subplots(self):
        """Test that 4 subplots are created."""
        np.random.seed(42)
        n = 60
        t = np.arange(n)
        df = pd.DataFrame({
            'date': pd.date_range('2020-01-01', periods=n, freq='ME'),
            'value': 10 * np.sin(2 * np.pi * t / 12) + np.random.randn(n)
        })

        plot = ggplot(df, aes(x='date', y='value')) + geom_stl(period=12)
        fig = plot.draw()

        # Check subplot axes exist
        assert hasattr(fig.layout, 'xaxis')
        assert hasattr(fig.layout, 'xaxis2')
        assert hasattr(fig.layout, 'xaxis3')
        assert hasattr(fig.layout, 'xaxis4')

    def test_robust_decomposition(self):
        """Test robust STL for data with outliers."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n)) + np.random.randn(n) * 0.1
        })
        df.loc[10, 'y'] = 100  # Add outlier

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12, robust=True)
        fig = plot.draw()

        assert len(fig.data) == 4

    def test_custom_color(self):
        """Test custom line color."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12, color='coral')
        fig = plot.draw()

        # Check first trace has coral color
        assert fig.data[0].line.color == 'coral'

    def test_custom_line_width(self):
        """Test custom line width."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12, line_width=3)
        fig = plot.draw()

        assert fig.data[0].line.width == 3

    def test_rangeslider_enabled_by_default(self):
        """Test that rangeslider is enabled by default."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12)
        fig = plot.draw()

        # xaxis4 should have rangeslider
        assert fig.layout.xaxis4.rangeslider.visible is True

    def test_rangeslider_can_be_disabled(self):
        """Test that rangeslider can be disabled."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12, rangeslider=False)
        fig = plot.draw()

        # xaxis4 should not have visible rangeslider
        assert fig.layout.xaxis4.rangeslider.visible is not True

    def test_custom_seasonal(self):
        """Test custom seasonal smoother."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12, seasonal=13)
        fig = plot.draw()

        assert len(fig.data) == 4

    def test_missing_period_raises(self):
        """Test that missing period raises error."""
        df = pd.DataFrame({'x': range(60), 'y': np.random.randn(60)})

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl()

        with pytest.raises(ValueError, match="period must be specified"):
            plot.draw()

    def test_trace_names(self):
        """Test that traces have correct component names."""
        np.random.seed(42)
        n = 60
        df = pd.DataFrame({
            'x': range(n),
            'y': np.sin(np.linspace(0, 10 * np.pi, n))
        })

        plot = ggplot(df, aes(x='x', y='y')) + geom_stl(period=12)
        fig = plot.draw()

        trace_names = [trace.name for trace in fig.data]
        assert trace_names == ['Observed', 'Trend', 'Seasonal', 'Residual']
