"""
Tests for stat_summary, geom_tile, position adjustments, limits, and brewer scales.
These tests verify actual functionality, not just that functions run.
"""
import sys

import numpy as np
import pandas as pd
from plotly.graph_objects import Figure

import pytest

sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    aes,
    geom_col,
    geom_point,
    geom_tile,
    ggplot,
    scale_color_brewer,
    scale_fill_brewer,
)
from ggplotly.limits import lims, xlim, ylim
from ggplotly.positions import position_dodge, position_jitter, position_stack
from ggplotly.stats.stat_summary import (
    mean_cl_normal,
    mean_sdl,
    mean_se,
    median_hilow,
    stat_summary,
)

# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def grouped_data():
    """Data with groups for summary statistics."""
    np.random.seed(42)
    return pd.DataFrame({
        'group': ['A'] * 20 + ['B'] * 20 + ['C'] * 20,
        'value': np.concatenate([
            np.random.normal(10, 2, 20),  # Group A: mean ~10
            np.random.normal(20, 3, 20),  # Group B: mean ~20
            np.random.normal(15, 1, 20),  # Group C: mean ~15
        ])
    })


@pytest.fixture
def simple_data():
    """Simple numeric data for basic tests."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [10, 20, 30, 40, 50]
    })


@pytest.fixture
def tile_data():
    """Data for heatmap/tile tests."""
    x = np.repeat([1, 2, 3, 4, 5], 5)
    y = np.tile([1, 2, 3, 4, 5], 5)
    z = x * y  # Values from 1 to 25
    return pd.DataFrame({'x': x, 'y': y, 'z': z})


@pytest.fixture
def categorical_tile_data():
    """Categorical data for tile tests."""
    return pd.DataFrame({
        'x': ['A', 'A', 'B', 'B'],
        'y': ['X', 'Y', 'X', 'Y'],
        'category': ['low', 'high', 'high', 'low']
    })


@pytest.fixture
def bar_data():
    """Data for bar chart position tests."""
    return pd.DataFrame({
        'category': ['A', 'A', 'B', 'B', 'C', 'C'],
        'group': ['G1', 'G2', 'G1', 'G2', 'G1', 'G2'],
        'value': [10, 15, 20, 25, 30, 35]
    })


# ============================================================================
# stat_summary Helper Functions Tests
# ============================================================================

class TestMeanSe:
    """Tests for mean_se function."""

    def test_mean_se_returns_correct_keys(self):
        """Test that mean_se returns y, ymin, ymax."""
        data = pd.Series([1, 2, 3, 4, 5])
        result = mean_se(data)

        assert 'y' in result
        assert 'ymin' in result
        assert 'ymax' in result

    def test_mean_se_computes_correct_mean(self):
        """Test that mean_se computes the correct mean."""
        data = pd.Series([10, 20, 30, 40, 50])
        result = mean_se(data)

        assert result['y'] == 30.0  # Mean of 10-50

    def test_mean_se_computes_correct_standard_error(self):
        """Test that mean_se computes correct SE bounds."""
        data = pd.Series([10, 20, 30, 40, 50])
        result = mean_se(data)

        expected_mean = 30.0
        expected_se = data.std() / np.sqrt(len(data))

        assert result['ymin'] == pytest.approx(expected_mean - expected_se)
        assert result['ymax'] == pytest.approx(expected_mean + expected_se)

    def test_mean_se_single_value_returns_zero_se(self):
        """Test that single value returns zero standard error."""
        data = pd.Series([42])
        result = mean_se(data)

        assert result['y'] == 42
        assert result['ymin'] == 42  # No error when n=1
        assert result['ymax'] == 42


class TestMeanClNormal:
    """Tests for mean_cl_normal function."""

    def test_mean_cl_normal_returns_correct_keys(self):
        """Test that mean_cl_normal returns y, ymin, ymax."""
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = mean_cl_normal(data)

        assert 'y' in result
        assert 'ymin' in result
        assert 'ymax' in result

    def test_mean_cl_normal_symmetric_bounds(self):
        """Test that confidence interval bounds are symmetric around mean."""
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result = mean_cl_normal(data)

        mean = result['y']
        lower_diff = mean - result['ymin']
        upper_diff = result['ymax'] - mean

        assert lower_diff == pytest.approx(upper_diff, rel=1e-10)

    def test_mean_cl_normal_wider_at_lower_confidence(self):
        """Test that 99% CI is wider than 95% CI."""
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        result_95 = mean_cl_normal(data, conf_level=0.95)
        result_99 = mean_cl_normal(data, conf_level=0.99)

        width_95 = result_95['ymax'] - result_95['ymin']
        width_99 = result_99['ymax'] - result_99['ymin']

        assert width_99 > width_95


class TestMeanSdl:
    """Tests for mean_sdl function."""

    def test_mean_sdl_default_mult(self):
        """Test mean_sdl with default multiplier (1)."""
        data = pd.Series([10, 20, 30, 40, 50])
        result = mean_sdl(data)

        expected_mean = 30.0
        expected_sd = data.std()

        assert result['y'] == expected_mean
        assert result['ymin'] == pytest.approx(expected_mean - expected_sd)
        assert result['ymax'] == pytest.approx(expected_mean + expected_sd)

    def test_mean_sdl_custom_mult(self):
        """Test mean_sdl with custom multiplier."""
        data = pd.Series([10, 20, 30, 40, 50])
        result = mean_sdl(data, mult=2)

        expected_mean = 30.0
        expected_sd = data.std()

        assert result['ymin'] == pytest.approx(expected_mean - 2 * expected_sd)
        assert result['ymax'] == pytest.approx(expected_mean + 2 * expected_sd)


class TestMedianHilow:
    """Tests for median_hilow function."""

    def test_median_hilow_returns_correct_median(self):
        """Test that median_hilow returns correct median."""
        data = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9])
        result = median_hilow(data)

        assert result['y'] == 5.0  # Median of 1-9

    def test_median_hilow_returns_correct_quantiles(self):
        """Test that median_hilow returns correct quantile bounds."""
        data = pd.Series(range(1, 101))  # 1 to 100
        result = median_hilow(data, conf_level=0.95)

        assert result['ymin'] == pytest.approx(data.quantile(0.025))
        assert result['ymax'] == pytest.approx(data.quantile(0.975))


# ============================================================================
# stat_summary Class Tests
# ============================================================================

class TestStatSummary:
    """Tests for stat_summary class."""

    def test_stat_summary_computes_mean_by_group(self, grouped_data):
        """Test that stat_summary correctly computes mean for each group."""
        stat = stat_summary(mapping={'x': 'group', 'y': 'value'}, fun_y='mean')
        result, mapping = stat.compute(grouped_data)

        # Should have 3 rows (one per group)
        assert len(result) == 3

        # Check that means are approximately correct
        group_a_mean = grouped_data[grouped_data['group'] == 'A']['value'].mean()
        group_b_mean = grouped_data[grouped_data['group'] == 'B']['value'].mean()

        result_a = result[result['group'] == 'A']['y'].values[0]
        result_b = result[result['group'] == 'B']['y'].values[0]

        assert result_a == pytest.approx(group_a_mean)
        assert result_b == pytest.approx(group_b_mean)

    def test_stat_summary_computes_median(self, grouped_data):
        """Test that stat_summary correctly computes median."""
        stat = stat_summary(mapping={'x': 'group', 'y': 'value'}, fun_y='median')
        result, mapping = stat.compute(grouped_data)

        group_a_median = grouped_data[grouped_data['group'] == 'A']['value'].median()
        result_a = result[result['group'] == 'A']['y'].values[0]

        assert result_a == pytest.approx(group_a_median)

    def test_stat_summary_computes_min_max(self, grouped_data):
        """Test that stat_summary correctly computes min and max."""
        stat = stat_summary(
            mapping={'x': 'group', 'y': 'value'},
            fun_y='mean',
            fun_ymin='min',
            fun_ymax='max'
        )
        result, mapping = stat.compute(grouped_data)

        # Check that ymin and ymax columns exist
        assert 'ymin' in result.columns
        assert 'ymax' in result.columns

        # Check values for group A
        group_a = grouped_data[grouped_data['group'] == 'A']['value']
        result_row = result[result['group'] == 'A'].iloc[0]

        assert result_row['ymin'] == pytest.approx(group_a.min())
        assert result_row['ymax'] == pytest.approx(group_a.max())

    def test_stat_summary_with_fun_data_mean_se(self, grouped_data):
        """Test stat_summary with fun_data='mean_se'."""
        stat = stat_summary(
            mapping={'x': 'group', 'y': 'value'},
            fun_data='mean_se'
        )
        result, mapping = stat.compute(grouped_data)

        # Result format from apply() is long format with level_1 column containing metric names
        # Each group has rows for 'y', 'ymin', 'ymax'
        assert 'group' in result.columns

        # Check that each group has y, ymin, ymax values
        for group in ['A', 'B', 'C']:
            group_data = result[result['group'] == group]
            metrics = group_data['level_1'].tolist()
            assert 'y' in metrics
            assert 'ymin' in metrics
            assert 'ymax' in metrics

            # Get values for this group
            y_val = group_data[group_data['level_1'] == 'y']['value'].values[0]
            ymin_val = group_data[group_data['level_1'] == 'ymin']['value'].values[0]
            ymax_val = group_data[group_data['level_1'] == 'ymax']['value'].values[0]

            # ymin < y < ymax
            assert ymin_val < y_val
            assert ymax_val > y_val

    def test_stat_summary_with_custom_function(self, grouped_data):
        """Test stat_summary with custom aggregation function."""
        # Custom function: 75th percentile
        stat = stat_summary(
            mapping={'x': 'group', 'y': 'value'},
            fun_y=lambda x: x.quantile(0.75)
        )
        result, mapping = stat.compute(grouped_data)

        group_a_q75 = grouped_data[grouped_data['group'] == 'A']['value'].quantile(0.75)
        result_a = result[result['group'] == 'A']['y'].values[0]

        assert result_a == pytest.approx(group_a_q75)

    def test_stat_summary_raises_without_x_y(self):
        """Test that stat_summary raises error without x and y mappings."""
        stat = stat_summary(mapping={'x': 'group'})  # Missing 'y'

        with pytest.raises(ValueError, match="requires both 'x' and 'y'"):
            stat.compute(pd.DataFrame({'group': ['A', 'B'], 'value': [1, 2]}))

    def test_stat_summary_all_agg_functions(self, grouped_data):
        """Test all built-in aggregation functions."""
        functions = ['mean', 'median', 'min', 'max', 'sum', 'sd', 'var', 'se']

        for func in functions:
            stat = stat_summary(mapping={'x': 'group', 'y': 'value'}, fun_y=func)
            result, mapping = stat.compute(grouped_data)

            assert len(result) == 3, f"Function {func} should return 3 groups"
            assert 'y' in result.columns, f"Function {func} should create 'y' column"


# ============================================================================
# geom_tile Tests
# ============================================================================

class TestGeomTile:
    """Tests for geom_tile (heatmap)."""

    def test_tile_creates_heatmap_trace(self, tile_data):
        """Test that geom_tile creates a heatmap trace."""
        p = ggplot(tile_data, aes(x='x', y='y', fill='z')) + geom_tile()
        fig = p.draw()

        assert isinstance(fig, Figure)
        assert len(fig.data) == 1
        assert fig.data[0].type == 'heatmap'

    def test_tile_data_matches_input(self, tile_data):
        """Test that heatmap data matches input."""
        p = ggplot(tile_data, aes(x='x', y='y', fill='z')) + geom_tile()
        fig = p.draw()

        trace = fig.data[0]
        # X and Y should contain the unique values
        assert set(trace.x) == {1, 2, 3, 4, 5}
        assert set(trace.y) == {1, 2, 3, 4, 5}

    def test_tile_with_custom_colorscale(self, tile_data):
        """Test that custom palette is applied."""
        p = ggplot(tile_data, aes(x='x', y='y', fill='z')) + geom_tile(palette='Plasma')
        fig = p.draw()

        assert fig.data[0].colorscale is not None

    def test_tile_with_alpha(self, tile_data):
        """Test that alpha is applied to heatmap."""
        p = ggplot(tile_data, aes(x='x', y='y', fill='z')) + geom_tile(alpha=0.5)
        fig = p.draw()

        assert fig.data[0].opacity == 0.5

    def test_tile_colorbar_name(self, tile_data):
        """Test that colorbar name is applied."""
        p = ggplot(tile_data, aes(x='x', y='y', fill='z')) + geom_tile(name='Intensity')
        fig = p.draw()

        assert fig.data[0].colorbar.title.text == 'Intensity'


# ============================================================================
# Position Adjustment Tests
# ============================================================================

class TestPositionDodge:
    """Tests for position_dodge.

    position_dodge separates overlapping objects at the same x position
    based on a grouping variable. Points with the same x but different
    groups are spread apart.
    """

    def test_dodge_separates_groups_at_same_x(self):
        """Test that dodge separates different groups at the same x position."""
        pos = position_dodge()
        x = np.array([1.0, 1.0, 1.0, 2.0, 2.0, 2.0])
        group = np.array(['A', 'B', 'C', 'A', 'B', 'C'])

        adjusted = pos.adjust(x, group=group, width=0.9)

        # At x=1, groups A, B, C should be at different positions
        x1_positions = adjusted[:3]
        assert len(np.unique(x1_positions)) == 3  # All 3 should be different

        # At x=2, same pattern
        x2_positions = adjusted[3:]
        assert len(np.unique(x2_positions)) == 3

        # Groups should be spread symmetrically around original x
        assert np.mean(x1_positions) == pytest.approx(1.0)
        assert np.mean(x2_positions) == pytest.approx(2.0)

    def test_dodge_two_groups(self):
        """Test dodging with exactly two groups."""
        pos = position_dodge()
        x = np.array([1.0, 1.0, 2.0, 2.0])
        group = np.array(['G1', 'G2', 'G1', 'G2'])

        adjusted = pos.adjust(x, group=group, width=0.8)

        # G1 should be left of center, G2 right of center
        # With width=0.8 and 2 groups, each element is 0.4 wide
        # G1 at -0.2 offset, G2 at +0.2 offset
        assert adjusted[0] == pytest.approx(0.8)   # x=1, G1: 1.0 - 0.2
        assert adjusted[1] == pytest.approx(1.2)   # x=1, G2: 1.0 + 0.2
        assert adjusted[2] == pytest.approx(1.8)   # x=2, G1: 2.0 - 0.2
        assert adjusted[3] == pytest.approx(2.2)   # x=2, G2: 2.0 + 0.2

    def test_dodge_width_controls_spread(self):
        """Test that width controls the total spread of dodged groups."""
        pos = position_dodge()
        x = np.array([1.0, 1.0])
        group = np.array(['A', 'B'])

        narrow = pos.adjust(x.copy(), group=group, width=0.4)
        wide = pos.adjust(x.copy(), group=group, width=0.8)

        narrow_spread = np.max(narrow) - np.min(narrow)
        wide_spread = np.max(wide) - np.min(wide)

        assert wide_spread > narrow_spread
        assert narrow_spread == pytest.approx(0.2)  # 0.4 / 2 groups
        assert wide_spread == pytest.approx(0.4)    # 0.8 / 2 groups

    def test_dodge_without_group_returns_unchanged(self):
        """Test that dodge without group parameter returns x unchanged."""
        pos = position_dodge()
        x = np.array([1.0, 1.0, 2.0, 2.0])

        adjusted = pos.adjust(x, width=0.8)

        np.testing.assert_array_equal(adjusted, x)

    def test_dodge_single_group_returns_unchanged(self):
        """Test that dodge with single group returns x unchanged."""
        pos = position_dodge()
        x = np.array([1.0, 1.0, 2.0, 2.0])
        group = np.array(['A', 'A', 'A', 'A'])

        adjusted = pos.adjust(x, group=group, width=0.8)

        np.testing.assert_array_equal(adjusted, x)

    def test_dodge_preserves_group_order(self):
        """Test that dodge preserves order of first appearance for groups."""
        pos = position_dodge()
        x = np.array([1.0, 1.0, 1.0])
        group = np.array(['B', 'A', 'C'])  # B appears first

        adjusted = pos.adjust(x, group=group, width=0.9)

        # B should be leftmost (appeared first), then A, then C
        assert adjusted[0] < adjusted[1]  # B < A
        assert adjusted[1] < adjusted[2]  # A < C

    def test_dodge_with_dataframe_method(self):
        """Test the compute_dodged_positions convenience method."""
        pos = position_dodge()
        df = pd.DataFrame({
            'x': [1, 1, 2, 2],
            'group': ['A', 'B', 'A', 'B'],
            'y': [10, 20, 30, 40]
        })

        adjusted = pos.compute_dodged_positions(df, 'x', 'group', width=0.8)

        # A at x=1 should be left of B at x=1
        assert adjusted[0] < adjusted[1]


class TestPositionJitter:
    """Tests for position_jitter."""

    def test_jitter_adds_noise(self):
        """Test that jitter adds random noise to positions."""
        pos = position_jitter(width=0.2)
        x = np.array([1.0, 1.0, 1.0, 1.0, 1.0])

        adjusted = pos.adjust(x)

        # Should no longer all be exactly 1.0
        assert not np.all(adjusted == 1.0)

        # Should be within jitter range
        assert np.all(adjusted >= 0.9)
        assert np.all(adjusted <= 1.1)

    def test_jitter_width_controls_spread(self):
        """Test that width controls jitter spread."""
        x = np.ones(100)

        narrow_pos = position_jitter(width=0.1, seed=42)
        wide_pos = position_jitter(width=0.5, seed=42)

        narrow = narrow_pos.adjust(x.copy())
        wide = wide_pos.adjust(x.copy())

        # Wide should have more spread
        assert np.std(wide) > np.std(narrow) * 2

    def test_jitter_with_seed_is_reproducible(self):
        """Test that jitter with seed produces reproducible results."""
        x = np.array([1.0, 2.0, 3.0])

        pos1 = position_jitter(width=0.5, seed=123)
        pos2 = position_jitter(width=0.5, seed=123)

        result1 = pos1.adjust(x.copy())
        result2 = pos2.adjust(x.copy())

        np.testing.assert_array_equal(result1, result2)

    def test_jitter_x_and_y(self):
        """Test that jitter can adjust both x and y."""
        pos = position_jitter(width=0.2, height=0.3, seed=42)
        x = np.array([1.0, 2.0, 3.0])
        y = np.array([10.0, 20.0, 30.0])

        x_adj, y_adj = pos.adjust(x, y)

        # X should be jittered within ±0.1
        assert np.all(np.abs(x_adj - x) <= 0.1)

        # Y should be jittered within ±0.15
        assert np.all(np.abs(y_adj - y) <= 0.15)


class TestPositionStack:
    """Tests for position_stack."""

    def test_stack_cumulative_sum(self):
        """Test that stack returns cumulative sum."""
        pos = position_stack()
        y = np.array([10, 20, 30])

        adjusted = pos.adjust(y)

        expected = np.array([10, 30, 60])  # Cumulative sum
        np.testing.assert_array_equal(adjusted, expected)

    def test_stack_preserves_first_value(self):
        """Test that first value is unchanged."""
        pos = position_stack()
        y = np.array([5, 10, 15])

        adjusted = pos.adjust(y)

        assert adjusted[0] == 5

    def test_stack_with_dataframe(self):
        """Test stack compute_stacked_positions method."""
        pos = position_stack()
        df = pd.DataFrame({
            'x': ['A', 'A', 'B', 'B'],
            'y': [10, 20, 30, 40],
            'group': ['G1', 'G2', 'G1', 'G2']
        })

        y_bottom, y_top = pos.compute_stacked_positions(df, 'x', 'y', 'group')

        # At x='A': G1 bottom=0 top=10, G2 bottom=10 top=30
        # At x='B': G1 bottom=0 top=30, G2 bottom=30 top=70
        assert len(y_bottom) == 4
        assert len(y_top) == 4


class TestPositionFill:
    """Tests for position_fill (normalized stacking)."""

    def test_fill_normalizes_to_one(self):
        """Test that fill normalizes stacks to sum to 1."""
        from ggplotly.positions import position_fill

        pos = position_fill()
        df = pd.DataFrame({
            'x': ['A', 'A', 'A'],
            'y': [10, 20, 30],  # Sum = 60
            'group': ['G1', 'G2', 'G3']
        })

        y_bottom, y_top = pos.compute_stacked_positions(df, 'x', 'y', 'group')

        # Top of last bar should be 1.0
        assert y_top[-1] == pytest.approx(1.0)

        # Each proportion should be correct
        assert y_top[0] == pytest.approx(10/60)
        assert y_top[1] == pytest.approx(30/60)  # 10+20
        assert y_top[2] == pytest.approx(1.0)    # 10+20+30


class TestPositionIdentity:
    """Tests for position_identity (no adjustment)."""

    def test_identity_returns_unchanged(self):
        """Test that identity returns positions unchanged."""
        from ggplotly.positions import position_identity

        pos = position_identity()
        x = np.array([1.0, 2.0, 3.0])

        adjusted = pos.adjust(x)

        np.testing.assert_array_equal(adjusted, x)


class TestPositionNudge:
    """Tests for position_nudge (fixed offset)."""

    def test_nudge_x_only(self):
        """Test nudging x positions only."""
        from ggplotly.positions import position_nudge

        pos = position_nudge(x=0.5)
        x = np.array([1.0, 2.0, 3.0])

        adjusted = pos.adjust(x)

        expected = np.array([1.5, 2.5, 3.5])
        np.testing.assert_array_equal(adjusted, expected)

    def test_nudge_x_and_y(self):
        """Test nudging both x and y positions."""
        from ggplotly.positions import position_nudge

        pos = position_nudge(x=0.1, y=0.2)
        x = np.array([1.0, 2.0])
        y = np.array([10.0, 20.0])

        x_adj, y_adj = pos.adjust(x, y)

        np.testing.assert_array_equal(x_adj, [1.1, 2.1])
        np.testing.assert_array_equal(y_adj, [10.2, 20.2])

    def test_nudge_negative(self):
        """Test nudging with negative values."""
        from ggplotly.positions import position_nudge

        pos = position_nudge(x=-0.5, y=-1.0)
        x = np.array([5.0])
        y = np.array([10.0])

        x_adj, y_adj = pos.adjust(x, y)

        assert x_adj[0] == 4.5
        assert y_adj[0] == 9.0


# ============================================================================
# Limits Tests
# ============================================================================

class TestXlim:
    """Tests for xlim."""

    def test_xlim_sets_x_range(self, simple_data):
        """Test that xlim sets x-axis range."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + xlim(0, 10)
        fig = p.draw()

        # Range is stored as tuple
        assert fig.layout.xaxis.range == (0, 10)

    def test_xlim_with_tuple(self, simple_data):
        """Test that xlim works with tuple input."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + xlim((0, 10))
        fig = p.draw()

        assert fig.layout.xaxis.range == (0, 10)

    def test_xlim_negative_values(self, simple_data):
        """Test xlim with negative values."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + xlim(-5, 5)
        fig = p.draw()

        assert fig.layout.xaxis.range == (-5, 5)

    def test_xlim_raises_on_invalid_args(self):
        """Test that xlim raises error on invalid arguments."""
        with pytest.raises(ValueError, match="requires two values"):
            xlim(1)  # Only one value

        with pytest.raises(ValueError, match="requires two values"):
            xlim(1, 2, 3)  # Three values


class TestYlim:
    """Tests for ylim."""

    def test_ylim_sets_y_range(self, simple_data):
        """Test that ylim sets y-axis range."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + ylim(0, 100)
        fig = p.draw()

        assert fig.layout.yaxis.range == (0, 100)

    def test_ylim_with_tuple(self, simple_data):
        """Test that ylim works with tuple input."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + ylim((0, 100))
        fig = p.draw()

        assert fig.layout.yaxis.range == (0, 100)

    def test_ylim_raises_on_invalid_args(self):
        """Test that ylim raises error on invalid arguments."""
        with pytest.raises(ValueError, match="requires two values"):
            ylim(1)


class TestLims:
    """Tests for lims (combined limits)."""

    def test_lims_sets_both_axes(self, simple_data):
        """Test that lims sets both x and y ranges."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + lims(x=(0, 10), y=(0, 100))
        fig = p.draw()

        assert fig.layout.xaxis.range == (0, 10)
        assert fig.layout.yaxis.range == (0, 100)

    def test_lims_x_only(self, simple_data):
        """Test lims with only x specified."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + lims(x=(0, 10))
        fig = p.draw()

        assert fig.layout.xaxis.range == (0, 10)

    def test_lims_y_only(self, simple_data):
        """Test lims with only y specified."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + lims(y=(0, 100))
        fig = p.draw()

        assert fig.layout.yaxis.range == (0, 100)


# ============================================================================
# Brewer Scale Tests
# ============================================================================

class TestScaleColorBrewer:
    """Tests for scale_color_brewer."""

    def test_brewer_qual_applies_colors(self):
        """Test that qualitative brewer scale applies colors to figure traces."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4],
            'y': [10, 20, 30, 40],
            'group': ['A', 'B', 'C', 'D']
        })

        p = ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + scale_color_brewer(type='qual', palette='Set1')
        fig = p.draw()

        # All traces should have different colors
        colors = [t.marker.color for t in fig.data]
        assert len(set(colors)) == 4

    def test_brewer_seq_applies_colors(self):
        """Test that sequential brewer scale applies colors."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [10, 20, 30],
            'intensity': ['low', 'medium', 'high']
        })

        p = ggplot(df, aes(x='x', y='y', color='intensity')) + geom_point() + scale_color_brewer(type='seq', palette='Blues')
        fig = p.draw()

        colors = [t.marker.color for t in fig.data]
        assert len(set(colors)) == 3

    def test_brewer_div_applies_colors(self):
        """Test that diverging brewer scale applies colors."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [10, 20, 30],
            'direction': ['negative', 'neutral', 'positive']
        })

        p = ggplot(df, aes(x='x', y='y', color='direction')) + geom_point() + scale_color_brewer(type='div', palette='RdBu')
        fig = p.draw()

        colors = [t.marker.color for t in fig.data]
        assert len(set(colors)) == 3

    def test_brewer_invalid_type_raises(self):
        """Test that invalid type raises error."""
        df = pd.DataFrame({'x': [1], 'y': [1], 'g': ['A']})
        p = ggplot(df, aes(x='x', y='y', color='g')) + geom_point() + scale_color_brewer(type='invalid', palette='Set1')

        with pytest.raises(ValueError, match="Unsupported type"):
            p.draw()

    def test_brewer_applies_to_traces_by_name(self):
        """Test that brewer scale applies colors based on trace names."""
        df = pd.DataFrame({'x': [1, 2], 'y': [10, 20], 'group': ['A', 'B']})

        p = ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + scale_color_brewer(type='qual', palette='Set1')
        fig = p.draw()

        # Should have two traces with different colors
        assert len(fig.data) == 2
        assert fig.data[0].marker.color != fig.data[1].marker.color

    def test_brewer_get_legend_info(self):
        """Test that get_legend_info returns palette info."""
        scale = scale_color_brewer(palette='Set2')
        info = scale.get_legend_info()

        assert info['name'] == 'Set2'


class TestScaleFillBrewer:
    """Tests for scale_fill_brewer."""

    def test_fill_brewer_applies_colors(self):
        """Test that fill brewer scale applies colors to figure traces."""
        df = pd.DataFrame({
            'x': ['A', 'B', 'C'],
            'y': [10, 20, 30],
            'category': ['cat1', 'cat2', 'cat3']
        })

        p = ggplot(df, aes(x='x', y='y', fill='category')) + geom_col() + scale_fill_brewer(type='qual', palette='Pastel1')
        fig = p.draw()

        # All traces should have different colors
        colors = [t.marker.color for t in fig.data]
        assert len(set(colors)) == 3


class TestBrewerIntegration:
    """Integration tests for brewer scales with plots."""

    def test_brewer_with_geom_point(self):
        """Test brewer scale integration with geom_point."""
        df = pd.DataFrame({
            'x': [1, 2, 3, 4, 5],
            'y': [10, 20, 15, 25, 30],
            'group': ['A', 'A', 'B', 'B', 'C']
        })

        p = (ggplot(df, aes(x='x', y='y', color='group'))
             + geom_point()
             + scale_color_brewer(palette='Dark2'))
        fig = p.draw()

        assert isinstance(fig, Figure)
        # Should have traces for each group
        assert len(fig.data) >= 1

    def test_brewer_with_geom_bar(self):
        """Test brewer scale integration with geom_bar."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 30]
        })

        p = (ggplot(df, aes(x='category', y='value', fill='category'))
             + geom_col()
             + scale_fill_brewer(palette='Set3'))
        fig = p.draw()

        assert isinstance(fig, Figure)


# ============================================================================
# Edge Cases and Error Handling
# ============================================================================

class TestEdgeCases:
    """Edge case tests."""

    def test_stat_summary_empty_group(self):
        """Test stat_summary handles data correctly even with few points."""
        df = pd.DataFrame({
            'group': ['A', 'A', 'B'],
            'value': [1, 2, 3]
        })

        stat = stat_summary(mapping={'x': 'group', 'y': 'value'}, fun_y='mean')
        result, mapping = stat.compute(df)

        assert len(result) == 2

    def test_xlim_with_list(self, simple_data):
        """Test xlim works with list input."""
        p = ggplot(simple_data, aes(x='x', y='y')) + geom_point() + xlim([0, 10])
        fig = p.draw()

        assert fig.layout.xaxis.range == (0, 10)

    def test_position_dodge_no_group(self):
        """Test position_dodge without group returns unchanged."""
        pos = position_dodge()
        x = np.array([1.0, 2.0, 3.0])

        adjusted = pos.adjust(x, width=0.8)

        # Without group, should be unchanged
        np.testing.assert_array_equal(adjusted, x)

    def test_mean_se_large_sample(self):
        """Test mean_se with large sample has small SE."""
        np.random.seed(42)
        data = pd.Series(np.random.normal(100, 10, 1000))
        result = mean_se(data)

        # SE should be much smaller than SD for large samples
        se_width = result['ymax'] - result['ymin']
        assert se_width < 2  # Should be approximately 2*SE ≈ 2*(10/sqrt(1000)) ≈ 0.63
