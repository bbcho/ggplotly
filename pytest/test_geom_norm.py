import numpy as np
import pandas as pd

import pytest
from ggplotly import aes, geom_histogram, geom_norm, ggplot


class TestGeomNorm:
    """Tests for geom_norm."""

    def test_basic_usage(self):
        """Test basic normal overlay on histogram."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(1000)})

        plot = (ggplot(df, aes(x='x'))
                + geom_histogram(aes(y='..density..'), bins=30)
                + geom_norm())
        fig = plot.draw()
        # Should have histogram bars + normal curve
        assert len(fig.data) >= 2

    def test_explicit_parameters(self):
        """Test with explicit mean and sd."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = (ggplot(df, aes(x='x'))
                + geom_histogram(aes(y='..density..'), bins=30)
                + geom_norm(mean=0, sd=1))
        fig = plot.draw()
        assert len(fig.data) >= 2

    def test_custom_color(self):
        """Test custom color."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(x='x')) + geom_norm(color='blue')
        fig = plot.draw()
        norm_trace = [t for t in fig.data if t.mode == 'lines'][0]
        assert norm_trace.line.color == 'blue'

    def test_custom_size(self):
        """Test custom line width."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(x='x')) + geom_norm(size=4)
        fig = plot.draw()
        norm_trace = [t for t in fig.data if t.mode == 'lines'][0]
        assert norm_trace.line.width == 4

    def test_auto_fit(self):
        """Test that auto-fit uses data mean and std."""
        np.random.seed(42)
        # Data with known mean/std
        x = np.random.randn(1000) * 2 + 5  # mean=5, std~2
        df = pd.DataFrame({'x': x})

        plot = ggplot(df, aes(x='x')) + geom_norm()
        fig = plot.draw()
        # Check legend name contains approximate mean/std
        norm_trace = fig.data[0]
        assert '\u03bc=' in norm_trace.name
        assert '\u03c3=' in norm_trace.name

    def test_missing_x_raises(self):
        """Test that missing x aesthetic raises error."""
        from ggplotly.exceptions import ColumnNotFoundError

        df = pd.DataFrame({'value': np.random.randn(100)})

        # x mapped to non-existent column
        plot = ggplot(df, aes(x='nonexistent')) + geom_norm()
        with pytest.raises(ColumnNotFoundError, match="nonexistent.*not found"):
            plot.draw()

    def test_linetype(self):
        """Test custom linetype."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(100)})

        plot = ggplot(df, aes(x='x')) + geom_norm(linetype='dashed')
        fig = plot.draw()
        norm_trace = [t for t in fig.data if t.mode == 'lines'][0]
        assert norm_trace.line.dash == 'dash'

    def test_scale_count(self):
        """Test scale='count' matches histogram scale."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(1000)})

        plot = ggplot(df, aes(x='x')) + geom_histogram(bins=30) + geom_norm(scale='count')
        fig = plot.draw()

        hist_max = max([max(t.y) for t in fig.data if t.type == 'bar'])
        norm_max = max([max(t.y) for t in fig.data if t.type == 'scatter'])

        # Normal curve max should be similar to histogram max (within 50%)
        assert 0.5 < norm_max / hist_max < 1.5

    def test_scale_count_with_binwidth(self):
        """Test scale='count' with explicit binwidth."""
        np.random.seed(42)
        df = pd.DataFrame({'x': np.random.randn(1000)})

        plot = (ggplot(df, aes(x='x'))
                + geom_histogram(binwidth=0.5)
                + geom_norm(scale='count', binwidth=0.5))
        fig = plot.draw()

        hist_max = max([max(t.y) for t in fig.data if t.type == 'bar'])
        norm_max = max([max(t.y) for t in fig.data if t.type == 'scatter'])

        # Should be well matched with explicit binwidth
        assert 0.7 < norm_max / hist_max < 1.3
