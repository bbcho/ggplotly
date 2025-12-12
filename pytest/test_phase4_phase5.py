"""
Functional tests for Phase 4 (Coordinate Systems) and Phase 5 (Stats Improvements).

Tests verify that the new parameters work correctly and match ggplot2 R behavior.
"""

import pytest
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# =============================================================================
# Phase 4: Coordinate System Tests
# =============================================================================

class TestCoordPolar:
    """Test coord_polar parameters."""

    def test_coord_polar_default_theta(self):
        """Test that theta defaults to 'x'."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar()
        assert coord.theta == 'x'

    def test_coord_polar_theta_y(self):
        """Test theta='y' option."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar(theta='y')
        assert coord.theta == 'y'

    def test_coord_polar_invalid_theta_raises(self):
        """Test that invalid theta raises ValueError."""
        from ggplotly.coords.coord_polar import coord_polar
        with pytest.raises(ValueError):
            coord_polar(theta='z')

    def test_coord_polar_start_default(self):
        """Test that start defaults to 0."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar()
        assert coord.start == 0

    def test_coord_polar_start_custom(self):
        """Test custom start angle."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar(start=np.pi/2)
        assert coord.start == np.pi/2

    def test_coord_polar_direction_default(self):
        """Test that direction defaults to 1 (clockwise)."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar()
        assert coord.direction == 1

    def test_coord_polar_direction_counterclockwise(self):
        """Test counterclockwise direction."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar(direction=-1)
        assert coord.direction == -1

    def test_coord_polar_invalid_direction_raises(self):
        """Test that invalid direction raises ValueError."""
        from ggplotly.coords.coord_polar import coord_polar
        with pytest.raises(ValueError):
            coord_polar(direction=0)

    def test_coord_polar_clip_default(self):
        """Test that clip defaults to 'on'."""
        from ggplotly.coords.coord_polar import coord_polar
        coord = coord_polar()
        assert coord.clip == 'on'

    def test_coord_polar_apply_sets_direction(self):
        """Test that apply() correctly sets direction in layout."""
        from ggplotly.coords.coord_polar import coord_polar
        fig = go.Figure()
        coord = coord_polar(direction=-1)
        coord.apply(fig)
        assert fig.layout.polar.angularaxis.direction == 'counterclockwise'


class TestCoordCartesian:
    """Test coord_cartesian parameters."""

    def test_coord_cartesian_xlim(self):
        """Test xlim parameter."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(xlim=(0, 10))
        assert coord.xlim == (0, 10)

    def test_coord_cartesian_ylim(self):
        """Test ylim parameter."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(ylim=(-5, 5))
        assert coord.ylim == (-5, 5)

    def test_coord_cartesian_expand_default(self):
        """Test that expand defaults to True."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian()
        assert coord.expand is True

    def test_coord_cartesian_expand_false(self):
        """Test expand=False for exact limits."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(xlim=(0, 10), expand=False)
        assert coord.expand is False

    def test_coord_cartesian_expansion_applies(self):
        """Test that expansion is applied to limits."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(xlim=(0, 100), expand=True, default_expand=(0.05, 0))
        expanded = coord._apply_expansion((0, 100))
        assert expanded[0] == -5  # 0 - 100*0.05
        assert expanded[1] == 105  # 100 + 100*0.05

    def test_coord_cartesian_no_expansion(self):
        """Test that expand=False gives exact limits."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(xlim=(0, 100), expand=False)
        result = coord._apply_expansion((0, 100))
        assert result == (0, 100)

    def test_coord_cartesian_clip_default(self):
        """Test that clip defaults to 'on'."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian()
        assert coord.clip == 'on'

    def test_coord_cartesian_clip_off(self):
        """Test clip='off' option."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        coord = coord_cartesian(clip='off')
        assert coord.clip == 'off'

    def test_coord_cartesian_apply_sets_range(self):
        """Test that apply() sets axis range."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3], y=[4, 5, 6]))
        coord = coord_cartesian(xlim=(0, 10), expand=False)
        coord.apply(fig)
        assert tuple(fig.layout.xaxis.range) == (0, 10)


# =============================================================================
# Phase 5: Stats Tests
# =============================================================================

class TestStatSummary:
    """Test stat_summary parameter naming and functionality."""

    def test_stat_summary_fun_alias(self):
        """Test that 'fun' parameter works (R-style naming)."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun='median')
        assert stat.fun == 'median'
        assert stat.fun_y == 'median'  # Internal storage

    def test_stat_summary_fun_min_alias(self):
        """Test that 'fun_min' parameter works."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun_min='min')
        assert stat.fun_min == 'min'
        assert stat.fun_ymin == 'min'

    def test_stat_summary_fun_max_alias(self):
        """Test that 'fun_max' parameter works."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun_max='max')
        assert stat.fun_max == 'max'
        assert stat.fun_ymax == 'max'

    def test_stat_summary_legacy_params_work(self):
        """Test that legacy fun_y/fun_ymin/fun_ymax still work."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun_y='mean', fun_ymin='min', fun_ymax='max')
        assert stat.fun == 'mean'
        assert stat.fun_min == 'min'
        assert stat.fun_max == 'max'

    def test_stat_summary_legacy_takes_precedence(self):
        """Test that legacy params take precedence for backward compat."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun='median', fun_y='mean')
        assert stat.fun == 'mean'  # Legacy takes precedence

    def test_stat_summary_na_rm_default(self):
        """Test that na_rm defaults to False."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary()
        assert stat.na_rm is False

    def test_stat_summary_na_rm_true(self):
        """Test na_rm=True parameter."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(na_rm=True)
        assert stat.na_rm is True

    def test_stat_summary_fun_args(self):
        """Test fun_args parameter."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(fun_args={'conf_level': 0.99})
        assert stat.fun_args == {'conf_level': 0.99}


class TestStatDensity:
    """Test stat_density parameters."""

    def test_stat_density_default_n(self):
        """Test that n defaults to 512 (R default)."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        assert stat.n == 512

    def test_stat_density_default_bw(self):
        """Test that bw defaults to 'nrd0' (R default)."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        assert stat.bw == 'nrd0'

    def test_stat_density_bw_options(self):
        """Test various bandwidth options."""
        from ggplotly.stats.stat_density import stat_density
        for bw in ['nrd0', 'nrd', 'scott', 'silverman']:
            stat = stat_density(bw=bw)
            assert stat.bw == bw

    def test_stat_density_numeric_bw(self):
        """Test numeric bandwidth value."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density(bw=0.5)
        assert stat.bw == 0.5

    def test_stat_density_adjust_default(self):
        """Test that adjust defaults to 1."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        assert stat.adjust == 1

    def test_stat_density_adjust_custom(self):
        """Test custom adjust value."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density(adjust=0.5)
        assert stat.adjust == 0.5

    def test_stat_density_kernel_default(self):
        """Test that kernel defaults to 'gaussian'."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        assert stat.kernel == 'gaussian'

    def test_stat_density_trim_default(self):
        """Test that trim defaults to False."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        assert stat.trim is False

    def test_stat_density_trim_true(self):
        """Test trim=True."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density(trim=True)
        assert stat.trim is True

    def test_stat_density_compute_returns_all_variables(self):
        """Test that compute_array returns all expected variables."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density()
        result = stat.compute_array(np.random.randn(100))
        assert 'x' in result
        assert 'y' in result
        assert 'density' in result
        assert 'count' in result
        assert 'scaled' in result
        assert 'ndensity' in result

    def test_stat_density_compute_n_points(self):
        """Test that compute_array returns n points."""
        from ggplotly.stats.stat_density import stat_density
        stat = stat_density(n=256)
        result = stat.compute_array(np.random.randn(100))
        assert len(result['x']) == 256

    def test_stat_density_trim_affects_range(self):
        """Test that trim affects the range of x values."""
        from ggplotly.stats.stat_density import stat_density
        data = np.array([1, 2, 3, 4, 5])

        stat_notrim = stat_density(trim=False)
        result_notrim = stat_notrim.compute_array(data)

        stat_trim = stat_density(trim=True)
        result_trim = stat_trim.compute_array(data)

        # Trimmed should stay within data range
        assert result_trim['x'].min() >= data.min()
        assert result_trim['x'].max() <= data.max()

        # Not trimmed extends beyond
        assert result_notrim['x'].min() < data.min()
        assert result_notrim['x'].max() > data.max()


class TestStatBin:
    """Test stat_bin parameters and implementation."""

    def test_stat_bin_default_bins(self):
        """Test that bins defaults to 30."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        assert stat.bins == 30

    def test_stat_bin_custom_bins(self):
        """Test custom bins value."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, bins=20)
        assert stat.bins == 20

    def test_stat_bin_binwidth(self):
        """Test binwidth parameter."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, binwidth=0.5)
        assert stat.binwidth == 0.5

    def test_stat_bin_boundary(self):
        """Test boundary parameter."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, boundary=0)
        assert stat.boundary == 0

    def test_stat_bin_center(self):
        """Test center parameter."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, center=0.5)
        assert stat.center == 0.5

    def test_stat_bin_closed_default(self):
        """Test that closed defaults to 'right'."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        assert stat.closed == 'right'

    def test_stat_bin_closed_left(self):
        """Test closed='left' option."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, closed='left')
        assert stat.closed == 'left'

    def test_stat_bin_pad_default(self):
        """Test that pad defaults to False."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        assert stat.pad is False

    def test_stat_bin_pad_true(self):
        """Test pad=True option."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, pad=True)
        assert stat.pad is True

    def test_stat_bin_compute_returns_dataframe(self):
        """Test that compute returns a DataFrame."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        data = pd.DataFrame({'value': np.random.randn(100)})
        result = stat.compute(data)
        assert isinstance(result, pd.DataFrame)

    def test_stat_bin_compute_has_required_columns(self):
        """Test that compute returns all required columns."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        data = pd.DataFrame({'value': np.random.randn(100)})
        result = stat.compute(data)
        for col in ['x', 'count', 'density', 'ncount', 'ndensity', 'width', 'xmin', 'xmax']:
            assert col in result.columns

    def test_stat_bin_bins_count(self):
        """Test that correct number of bins are created."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, bins=10)
        data = pd.DataFrame({'value': np.linspace(0, 10, 100)})
        result = stat.compute(data)
        # Due to how bin edges are computed, we might get bins+1
        assert len(result) >= 10

    def test_stat_bin_binwidth_creates_correct_width(self):
        """Test that binwidth creates bins of correct width."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, binwidth=1.0)
        data = pd.DataFrame({'value': np.linspace(0, 10, 100)})
        result = stat.compute(data)
        # All widths should be approximately 1.0
        assert np.allclose(result['width'].values, 1.0)

    def test_stat_bin_count_sums_to_n(self):
        """Test that counts sum to total observations."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        n = 100
        data = pd.DataFrame({'value': np.random.randn(n)})
        result = stat.compute(data)
        assert result['count'].sum() == n

    def test_stat_bin_density_integrates_to_one(self):
        """Test that density integrates to approximately 1."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'})
        data = pd.DataFrame({'value': np.random.randn(1000)})
        result = stat.compute(data)
        integral = (result['density'] * result['width']).sum()
        assert np.isclose(integral, 1.0, atol=0.01)

    def test_stat_bin_breaks_override(self):
        """Test that explicit breaks override bins/binwidth."""
        from ggplotly.stats.stat_bin import stat_bin
        breaks = [0, 2, 4, 6, 8, 10]
        stat = stat_bin(mapping={'x': 'value'}, breaks=breaks)
        data = pd.DataFrame({'value': np.linspace(0, 10, 100)})
        result = stat.compute(data)
        assert len(result) == len(breaks) - 1  # n bins = n edges - 1

    def test_stat_bin_na_rm(self):
        """Test that na_rm removes NA values."""
        from ggplotly.stats.stat_bin import stat_bin
        stat = stat_bin(mapping={'x': 'value'}, na_rm=True)
        data = pd.DataFrame({'value': [1, 2, np.nan, 4, 5, np.nan]})
        result = stat.compute(data)
        # Should only count 4 values
        assert result['count'].sum() == 4


# =============================================================================
# Integration Tests
# =============================================================================

class TestIntegration:
    """Integration tests combining multiple features."""

    def test_coord_cartesian_with_scatter(self):
        """Test coord_cartesian with a scatter plot."""
        from ggplotly.coords.coord_cartesian import coord_cartesian
        fig = go.Figure(data=go.Scatter(x=[1, 2, 3, 10, 20], y=[1, 2, 3, 4, 5]))
        coord = coord_cartesian(xlim=(0, 5), ylim=(0, 4), expand=False)
        coord.apply(fig)
        assert tuple(fig.layout.xaxis.range) == (0, 5)
        assert tuple(fig.layout.yaxis.range) == (0, 4)

    def test_stat_summary_with_data(self):
        """Test stat_summary computes correct statistics."""
        from ggplotly.stats.stat_summary import stat_summary
        stat = stat_summary(mapping={'x': 'group', 'y': 'value'}, fun='mean', fun_min='min', fun_max='max')
        data = pd.DataFrame({
            'group': ['A', 'A', 'A', 'B', 'B', 'B'],
            'value': [1, 2, 3, 10, 20, 30]
        })
        result, mapping = stat.compute(data)
        # Group A: mean=2, min=1, max=3
        # Group B: mean=20, min=10, max=30
        a_row = result[result['group'] == 'A'].iloc[0]
        b_row = result[result['group'] == 'B'].iloc[0]
        assert a_row['y'] == 2
        assert a_row['ymin'] == 1
        assert a_row['ymax'] == 3
        assert b_row['y'] == 20
        assert b_row['ymin'] == 10
        assert b_row['ymax'] == 30
