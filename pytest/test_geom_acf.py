import numpy as np
import pandas as pd

import pytest
from ggplotly import aes, geom_acf, ggplot


class TestGeomAcf:
    """Tests for geom_acf."""

    def test_basic_usage(self):
        """Test basic ACF plot."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf()
        fig = plot.draw()

        # Should have 3 traces: confidence band, zero line, bars
        assert len(fig.data) == 3

    def test_custom_nlags(self):
        """Test custom number of lags."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf(nlags=20)
        fig = plot.draw()

        # Bar trace should have 20 bars (lag 1 to lag 20, excluding lag 0)
        bar_trace = [t for t in fig.data if t.type == 'bar'][0]
        assert len(bar_trace.x) == 20

    def test_custom_color(self):
        """Test custom bar color."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf(color='coral')
        fig = plot.draw()

        bar_trace = [t for t in fig.data if t.type == 'bar'][0]
        assert bar_trace.marker.color == 'coral'

    def test_missing_y_raises(self):
        """Test that missing y aesthetic raises error."""
        df = pd.DataFrame({'x': range(100), 'value': np.random.randn(100)})

        plot = ggplot(df, aes(x='x')) + geom_acf()
        with pytest.raises(ValueError, match="requires y aesthetic"):
            plot.draw()

    def test_starts_at_lag_one(self):
        """Test that ACF starts at lag 1 (lag 0 excluded)."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf(nlags=10)
        fig = plot.draw()

        bar_trace = [t for t in fig.data if t.type == 'bar'][0]
        # First lag should be 1, not 0
        assert bar_trace.x[0] == 1

    def test_has_confidence_band(self):
        """Test that confidence band is present."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf()
        fig = plot.draw()

        # First trace should be the filled confidence band
        ci_trace = fig.data[0]
        assert ci_trace.fill == 'toself'

    def test_has_zero_line(self):
        """Test that zero reference line is present."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf()
        fig = plot.draw()

        # Second trace should be the zero line
        zero_line = fig.data[1]
        assert list(zero_line.y) == [0, 0]

    def test_bar_width(self):
        """Test custom bar width."""
        np.random.seed(42)
        df = pd.DataFrame({'value': np.random.randn(100).cumsum()})

        plot = ggplot(df, aes(y='value')) + geom_acf(bar_width=0.5)
        fig = plot.draw()

        bar_trace = [t for t in fig.data if t.type == 'bar'][0]
        assert bar_trace.width == 0.5
