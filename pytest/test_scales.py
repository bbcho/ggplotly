"""
Tests for ggplotly scales.
"""
import sys
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest

sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    aes,
    geom_col,
    geom_line,
    geom_point,
    ggplot,
    scale_color_brewer,
    scale_color_gradient,
    scale_color_manual,
    scale_fill_brewer,
    scale_fill_gradient,
    scale_fill_manual,
    scale_fill_viridis_c,
    scale_shape_manual,
    scale_size,
    scale_x_continuous,
    scale_x_date,
    scale_x_datetime,
    scale_x_log10,
    scale_y_continuous,
    scale_y_log10,
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': range(10),
        'y': np.random.randn(10) * 10 + 50,
        'group': ['A'] * 5 + ['B'] * 5,
        'size': np.random.rand(10) * 10,
        'value': np.random.rand(10) * 100
    })


@pytest.fixture
def date_data():
    """Create data with dates."""
    base_date = datetime(2023, 1, 1)
    dates = [base_date + timedelta(days=i*30) for i in range(12)]
    return pd.DataFrame({
        'date': dates,
        'value': np.random.randn(12).cumsum() + 100
    })


@pytest.fixture
def datetime_data():
    """Create data with datetimes including time component."""
    base_dt = datetime(2023, 6, 15, 0, 0, 0)
    datetimes = [base_dt + timedelta(hours=i*6) for i in range(24)]
    return pd.DataFrame({
        'datetime': datetimes,
        'value': np.random.randn(24).cumsum()
    })


class TestContinuousScales:
    """Tests for continuous scales."""

    def test_scale_x_continuous_basic(self, sample_data):
        """Test basic x continuous scale."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_x_continuous())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_continuous_limits(self, sample_data):
        """Test x continuous scale with limits."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_x_continuous(limits=(0, 20)))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_continuous_name(self, sample_data):
        """Test x continuous scale with custom name."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_x_continuous(name='Custom X Label'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_y_continuous_basic(self, sample_data):
        """Test basic y continuous scale."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_y_continuous())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_y_continuous_limits(self, sample_data):
        """Test y continuous scale with limits."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_y_continuous(limits=(0, 100)))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestLogScales:
    """Tests for log scales."""

    def test_scale_x_log10(self):
        """Test log10 x scale."""
        df = pd.DataFrame({
            'x': [1, 10, 100, 1000, 10000],
            'y': [1, 2, 3, 4, 5]
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + scale_x_log10())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_y_log10(self):
        """Test log10 y scale."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [1, 10, 100, 1000, 10000]
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + scale_y_log10())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_both_log_scales(self):
        """Test both axes with log scale."""
        df = pd.DataFrame({
            'x': [1, 10, 100, 1000],
            'y': [1, 10, 100, 1000]
        })
        p = (ggplot(df, aes(x='x', y='y'))
             + geom_point()
             + scale_x_log10()
             + scale_y_log10())
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestDateScales:
    """Tests for date and datetime scales."""

    def test_scale_x_date_basic(self, date_data):
        """Test basic date scale."""
        p = (ggplot(date_data, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_with_breaks(self, date_data):
        """Test date scale with date_breaks."""
        p = (ggplot(date_data, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(date_breaks='1 month'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_with_labels(self, date_data):
        """Test date scale with date_labels format."""
        p = (ggplot(date_data, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(date_labels='%b %Y'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_with_breaks_and_labels(self, date_data):
        """Test date scale with both breaks and labels."""
        p = (ggplot(date_data, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(date_breaks='2 months', date_labels='%b'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_yearly_breaks(self):
        """Test date scale with yearly breaks."""
        dates = pd.date_range('2020-01-01', periods=36, freq='ME')
        df = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(36).cumsum()
        })
        p = (ggplot(df, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(date_breaks='1 year', date_labels='%Y'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_weekly_breaks(self):
        """Test date scale with weekly breaks."""
        dates = pd.date_range('2023-01-01', periods=12, freq='W')
        df = pd.DataFrame({
            'date': dates,
            'value': range(12)
        })
        p = (ggplot(df, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(date_breaks='2 weeks', date_labels='%d %b'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_date_with_limits(self, date_data):
        """Test date scale with date limits."""
        p = (ggplot(date_data, aes(x='date', y='value'))
             + geom_line()
             + scale_x_date(limits=('2023-03-01', '2023-10-01')))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_datetime_basic(self, datetime_data):
        """Test basic datetime scale."""
        p = (ggplot(datetime_data, aes(x='datetime', y='value'))
             + geom_line()
             + scale_x_datetime())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_datetime_hourly_breaks(self, datetime_data):
        """Test datetime scale with hourly breaks."""
        p = (ggplot(datetime_data, aes(x='datetime', y='value'))
             + geom_line()
             + scale_x_datetime(date_breaks='6 hours', date_labels='%H:%M'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_x_datetime_with_name(self, datetime_data):
        """Test datetime scale with custom axis name."""
        p = (ggplot(datetime_data, aes(x='datetime', y='value'))
             + geom_line()
             + scale_x_datetime(name='Time of Day'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestColorScales:
    """Tests for color scales."""

    def test_scale_color_manual(self, sample_data):
        """Test manual color scale."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_manual(values=['red', 'blue']))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_color_manual_with_dict(self, sample_data):
        """Test manual color scale with dictionary."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_manual(values={'A': '#FF0000', 'B': '#0000FF'}))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_color_brewer(self, sample_data):
        """Test brewer color scale."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_brewer(palette='Set1'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_color_brewer_different_palettes(self, sample_data):
        """Test brewer color scale with different palettes."""
        for palette in ['Set2', 'Dark2', 'Paired']:
            p = (ggplot(sample_data, aes(x='x', y='y', color='group'))
                 + geom_point()
                 + scale_color_brewer(palette=palette))
            fig = p.draw()
            assert isinstance(fig, Figure)

    def test_scale_color_gradient(self, sample_data):
        """Test continuous color gradient."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='value'))
             + geom_point()
             + scale_color_gradient(low='blue', high='red'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestFillScales:
    """Tests for fill scales."""

    def test_scale_fill_manual(self):
        """Test manual fill scale."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 15]
        })
        p = (ggplot(df, aes(x='category', y='value', fill='category'))
             + geom_col()
             + scale_fill_manual(values=['red', 'green', 'blue']))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_fill_brewer(self):
        """Test brewer fill scale."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 15]
        })
        p = (ggplot(df, aes(x='category', y='value', fill='category'))
             + geom_col()
             + scale_fill_brewer(palette='Pastel1'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_fill_gradient(self):
        """Test continuous fill gradient."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D', 'E'],
            'value': [10, 20, 15, 25, 30]
        })
        p = (ggplot(df, aes(x='category', y='value', fill='value'))
             + geom_col()
             + scale_fill_gradient(low='white', high='darkblue'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_fill_viridis_c(self):
        """Test viridis continuous fill scale."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C', 'D', 'E'],
            'value': [10, 20, 15, 25, 30]
        })
        p = (ggplot(df, aes(x='category', y='value', fill='value'))
             + geom_col()
             + scale_fill_viridis_c())
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestSizeScale:
    """Tests for size scale."""

    def test_scale_size_basic(self, sample_data):
        """Test basic size scale."""
        p = (ggplot(sample_data, aes(x='x', y='y', size='size'))
             + geom_point()
             + scale_size())
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_size_with_range(self, sample_data):
        """Test size scale with custom range."""
        p = (ggplot(sample_data, aes(x='x', y='y', size='size'))
             + geom_point()
             + scale_size(range=(2, 20)))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestShapeScale:
    """Tests for shape scale."""

    def test_scale_shape_manual(self, sample_data):
        """Test manual shape scale."""
        p = (ggplot(sample_data, aes(x='x', y='y', shape='group'))
             + geom_point()
             + scale_shape_manual(values=['circle', 'square']))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestMultipleScales:
    """Tests for combining multiple scales."""

    def test_continuous_and_color(self, sample_data):
        """Test combining continuous and color scales."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_x_continuous(limits=(0, 12))
             + scale_y_continuous(limits=(30, 70))
             + scale_color_manual(values=['purple', 'orange']))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_date_and_color(self, date_data):
        """Test combining date and color scales."""
        date_data['group'] = ['A', 'B'] * 6
        p = (ggplot(date_data, aes(x='date', y='value', color='group'))
             + geom_line()
             + scale_x_date(date_breaks='2 months', date_labels='%b')
             + scale_color_brewer(palette='Set1'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_all_aesthetic_scales(self, sample_data):
        """Test with scales for multiple aesthetics."""
        p = (ggplot(sample_data, aes(x='x', y='y', color='group', size='size'))
             + geom_point()
             + scale_x_continuous()
             + scale_y_continuous()
             + scale_color_manual(values=['red', 'blue'])
             + scale_size(range=(3, 15)))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestScaleEdgeCases:
    """Tests for edge cases in scales."""

    def test_scale_with_single_value(self):
        """Test scales when there's only one unique value."""
        df = pd.DataFrame({
            'x': [1, 1, 1],
            'y': [2, 3, 4],
            'group': ['A', 'A', 'A']
        })
        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_manual(values=['red']))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_scale_inverted_limits(self, sample_data):
        """Test scale with inverted limits (max < min)."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + scale_y_continuous(limits=(100, 0)))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_date_scale_various_break_formats(self):
        """Test date scale parses various break format strings."""
        dates = pd.date_range('2023-01-01', periods=100, freq='D')
        df = pd.DataFrame({
            'date': dates,
            'value': range(100)
        })

        # Test different break format strings
        break_formats = ['1 day', '1 week', '2 weeks', '1 month', '3 months', '1 year']
        for breaks in break_formats:
            p = (ggplot(df, aes(x='date', y='value'))
                 + geom_line()
                 + scale_x_date(date_breaks=breaks))
            fig = p.draw()
            assert isinstance(fig, Figure)


class TestContinuousColorMapping:
    """Tests for continuous color mapping (numeric data mapped to color aesthetic)."""

    def test_continuous_color_creates_single_trace(self):
        """Test that continuous numeric color creates a single trace with colorscale."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(100),
            'y': np.random.randn(100),
            'value': np.random.randn(100)  # Continuous numeric values
        })

        p = ggplot(df, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        # Should create only 1 trace (not 100 traces for each unique value)
        assert len(fig.data) == 1, f"Expected 1 trace, got {len(fig.data)}"

    def test_continuous_color_has_colorscale(self):
        """Test that continuous color mapping applies a colorscale."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(50),
            'y': np.random.randn(50),
            'value': np.random.randn(50)
        })

        p = ggplot(df, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        trace = fig.data[0]
        assert trace.marker.colorscale is not None, "Expected colorscale to be set"
        assert trace.marker.showscale is True, "Expected colorbar to be shown"

    def test_continuous_color_values_are_numeric(self):
        """Test that marker.color contains the actual numeric values."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [1, 2, 3, 4, 5],
            'value': [0.1, 0.5, 1.0, 1.5, 2.0]
        })

        p = ggplot(df, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        trace = fig.data[0]
        # marker.color should be the numeric values, not categorical colors
        assert hasattr(trace.marker.color, '__iter__'), "Expected marker.color to be iterable"
        assert len(trace.marker.color) == 5, "Expected 5 color values"

    def test_continuous_color_with_scale_color_gradient(self):
        """Test that scale_color_gradient overrides the default colorscale."""
        np.random.seed(42)
        df = pd.DataFrame({
            'x': np.random.randn(30),
            'y': np.random.randn(30),
            'value': np.random.randn(30)
        })

        p = (ggplot(df, aes(x='x', y='y', color='value'))
             + geom_point()
             + scale_color_gradient(low='blue', high='red'))
        fig = p.draw()

        assert isinstance(fig, Figure)
        # The scale_color_gradient should have applied its colorscale
        trace = fig.data[0]
        assert trace.marker.colorscale is not None

    def test_categorical_color_still_works(self):
        """Test that categorical color mapping still creates separate traces."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6],
            'y': [1, 2, 3, 4, 5, 6],
            'group': ['A', 'A', 'A', 'B', 'B', 'B']
        })

        p = ggplot(df, aes(x='x', y='y', color='group')) + geom_point()
        fig = p.draw()

        # Should create 2 traces (one for each group)
        assert len(fig.data) == 2, f"Expected 2 traces for categorical, got {len(fig.data)}"

    def test_small_integer_range_is_categorical(self):
        """Test that small integer ranges are treated as categorical."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5, 6],
            'y': [1, 2, 3, 4, 5, 6],
            'category': [1, 1, 2, 2, 3, 3]  # Only 3 unique integers
        })

        p = ggplot(df, aes(x='x', y='y', color='category')) + geom_point()
        fig = p.draw()

        # Should be treated as categorical (3 traces)
        # The heuristic treats small integer ranges as categorical
        assert len(fig.data) == 3, f"Expected 3 traces for small integers, got {len(fig.data)}"

    def test_many_unique_values_is_continuous(self):
        """Test that many unique numeric values trigger continuous mapping."""
        np.random.seed(42)
        # Create data with 50 unique values - should be continuous
        df = pd.DataFrame({
            'x': range(50),
            'y': range(50),
            'value': np.random.rand(50) * 100  # 50 unique float values
        })

        p = ggplot(df, aes(x='x', y='y', color='value')) + geom_point()
        fig = p.draw()

        # Should be 1 trace with colorscale (continuous)
        assert len(fig.data) == 1, f"Expected 1 trace for continuous, got {len(fig.data)}"
        assert fig.data[0].marker.colorscale is not None
