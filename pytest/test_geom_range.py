"""
Tests for geom_range - 5-year range plots with historical context.
"""
import sys

import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest

sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import aes, geom_range, ggplot, labs


@pytest.fixture
def daily_data():
    """Create 6 years of daily data for testing."""
    np.random.seed(42)
    dates = pd.date_range('2019-01-01', '2024-12-31', freq='D')

    # Create seasonal pattern with some noise
    values = []
    for date in dates:
        # Base seasonal pattern (higher in summer)
        seasonal = 50 + 30 * np.sin(2 * np.pi * date.dayofyear / 365)
        # Year-over-year trend
        trend = (date.year - 2019) * 5
        # Random noise
        noise = np.random.randn() * 10
        values.append(seasonal + trend + noise)

    return pd.DataFrame({
        'date': dates,
        'value': values
    })


@pytest.fixture
def weekly_data():
    """Create 6 years of weekly data."""
    np.random.seed(42)
    dates = pd.date_range('2019-01-01', '2024-12-31', freq='W')
    values = np.random.randn(len(dates)).cumsum() + 100
    return pd.DataFrame({
        'date': dates,
        'value': values
    })


@pytest.fixture
def monthly_data():
    """Create 6 years of monthly data."""
    np.random.seed(42)
    dates = pd.date_range('2019-01-01', '2024-12-31', freq='ME')
    values = np.random.randn(len(dates)).cumsum() + 100
    return pd.DataFrame({
        'date': dates,
        'value': values
    })


@pytest.fixture
def quarterly_data():
    """Create 6 years of quarterly data."""
    np.random.seed(42)
    dates = pd.date_range('2019-01-01', '2024-12-31', freq='QE')
    values = np.random.randn(len(dates)).cumsum() + 100
    return pd.DataFrame({
        'date': dates,
        'value': values
    })


class TestGeomRangeBasic:
    """Basic tests for geom_range."""

    def test_basic_range_plot(self, daily_data):
        """Test basic 5-year range plot."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have multiple traces: ribbon (2), avg, prior year, current year
        assert len(fig.data) >= 4

    def test_with_weekly_data(self, weekly_data):
        """Test with weekly frequency data."""
        p = ggplot(weekly_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_with_monthly_data(self, monthly_data):
        """Test with monthly frequency data."""
        p = ggplot(monthly_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_with_quarterly_data(self, quarterly_data):
        """Test with quarterly frequency data."""
        p = ggplot(quarterly_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomRangeFrequency:
    """Tests for frequency handling."""

    def test_auto_detect_daily(self, daily_data):
        """Test auto-detection of daily frequency."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_force_weekly_freq(self, daily_data):
        """Test forcing weekly frequency on daily data."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(freq='W')
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_force_monthly_freq(self, daily_data):
        """Test forcing monthly frequency on daily data."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(freq='M')
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_force_quarterly_freq(self, daily_data):
        """Test forcing quarterly frequency on daily data."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(freq='Q')
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_freq_string_variants(self, daily_data):
        """Test various frequency string formats."""
        for freq in ['daily', 'D', 'd', 'weekly', 'W', 'monthly', 'M', 'quarterly', 'Q']:
            p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(freq=freq)
            fig = p.draw()
            assert isinstance(fig, Figure)


class TestGeomRangeYears:
    """Tests for year handling."""

    def test_custom_current_year(self, daily_data):
        """Test specifying a different current year."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(current_year=2023)
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_show_additional_years(self, daily_data):
        """Test showing additional specific years."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(show_years=[2020, 2021])
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have extra traces for additional years
        assert len(fig.data) >= 6

    def test_show_years_with_overlap(self, daily_data):
        """Test show_years when it includes current/prior year (should skip)."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(show_years=[2023, 2024])
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_custom_years_count(self, daily_data):
        """Test using different number of historical years."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(years=3)
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomRangeCustomization:
    """Tests for customization options."""

    def test_custom_colors(self, daily_data):
        """Test custom color settings."""
        p = (ggplot(daily_data, aes(x='date', y='value'))
             + geom_range(
                 current_color='green',
                 prior_color='orange',
                 avg_color='purple',
                 ribbon_color='lightblue'
             ))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_custom_ribbon_alpha(self, daily_data):
        """Test custom ribbon transparency."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(ribbon_alpha=0.5)
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_custom_avg_linetype(self, daily_data):
        """Test custom average line style."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(avg_linetype='dash')
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_hide_legend(self, daily_data):
        """Test hiding legend."""
        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range(show_legend=False)
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomRangeWithLabs:
    """Tests for geom_range combined with labels."""

    def test_with_title(self, daily_data):
        """Test with plot title."""
        p = (ggplot(daily_data, aes(x='date', y='value'))
             + geom_range()
             + labs(title='5-Year Range Plot'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_with_full_labs(self, daily_data):
        """Test with complete labels."""
        p = (ggplot(daily_data, aes(x='date', y='value'))
             + geom_range()
             + labs(
                 title='Temperature Analysis',
                 subtitle='Historical Range Comparison',
                 x='Date',
                 y='Temperature (°F)',
                 caption='Source: Weather Station'
             ))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestGeomRangeEdgeCases:
    """Tests for edge cases."""

    def test_limited_data(self):
        """Test with limited historical data (less than 5 years)."""
        dates = pd.date_range('2023-01-01', '2024-12-31', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(len(dates)) + 50
        })
        p = ggplot(df, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_single_year_data(self):
        """Test with only one year of data."""
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        df = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(len(dates)) + 50
        })
        p = ggplot(df, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_sparse_data(self):
        """Test with sparse/irregular data."""
        np.random.seed(42)
        # Random dates over 3 years
        dates = pd.to_datetime(['2022-01-15', '2022-03-20', '2022-07-10',
                                '2023-02-14', '2023-05-22', '2023-09-30',
                                '2024-01-05', '2024-04-18', '2024-08-25'])
        df = pd.DataFrame({
            'date': dates,
            'value': np.random.randn(len(dates)) + 50
        })
        p = ggplot(df, aes(x='date', y='value')) + geom_range()
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_missing_aesthetic(self):
        """Test error when missing required aesthetic."""
        from ggplotly.exceptions import RequiredAestheticError

        df = pd.DataFrame({'date': [1, 2, 3], 'value': [1, 2, 3]})
        with pytest.raises(RequiredAestheticError):
            p = ggplot(df, aes(x='date')) + geom_range()
            fig = p.draw()

    def test_data_preserves_original(self, daily_data):
        """Test that geom_range doesn't modify original data."""
        original_shape = daily_data.shape
        original_cols = daily_data.columns.tolist()

        p = ggplot(daily_data, aes(x='date', y='value')) + geom_range()
        fig = p.draw()

        assert daily_data.shape == original_shape
        assert daily_data.columns.tolist() == original_cols
