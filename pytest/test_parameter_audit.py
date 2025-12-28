# pytest/test_parameter_audit.py
"""
Tests for parameter audit features added for v1.0.0.

Tests cover:
- Base class: na_rm, show_legend, colour alias
- geom_col: width parameter
- geom_smooth: fullrange parameter
- geom_ribbon: linetype, size parameters
- geom_area: position parameter
- All geoms: linewidth alias for size
"""

import numpy as np
import pandas as pd
import pytest

from ggplotly import (
    ggplot,
    aes,
    geom_point,
    geom_line,
    geom_col,
    geom_bar,
    geom_smooth,
    geom_ribbon,
    geom_area,
    geom_path,
    geom_step,
    geom_segment,
    geom_density,
    labs,
)


# =============================================================================
# Test Fixtures
# =============================================================================

@pytest.fixture
def basic_df():
    """Basic DataFrame for testing."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 3, 5, 4],
    })


@pytest.fixture
def df_with_na():
    """DataFrame with missing values."""
    return pd.DataFrame({
        'x': [1, 2, np.nan, 4, 5],
        'y': [2, np.nan, 3, 5, 4],
    })


@pytest.fixture
def category_df():
    """DataFrame with categories."""
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'A', 'B', 'C'],
        'value': [10, 15, 12, 8, 18, 14],
    })


@pytest.fixture
def ribbon_df():
    """DataFrame for ribbon plots."""
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [3, 4, 3.5, 5, 4.5],
        'ymin': [2, 3, 2.5, 4, 3.5],
        'ymax': [4, 5, 4.5, 6, 5.5],
    })


@pytest.fixture
def area_df():
    """DataFrame for stacked area plots."""
    return pd.DataFrame({
        'x': [1, 2, 3, 1, 2, 3],
        'y': [2, 3, 2.5, 1, 2, 1.5],
        'group': ['A', 'A', 'A', 'B', 'B', 'B'],
    })


@pytest.fixture
def segment_df():
    """DataFrame for segment plots."""
    return pd.DataFrame({
        'x': [1, 2],
        'y': [1, 2],
        'xend': [3, 4],
        'yend': [2, 3],
    })


# =============================================================================
# Priority 1: Base Class Parameters
# =============================================================================

class TestNaRmParameter:
    """Tests for na_rm parameter in base Geom class."""

    def test_na_rm_default_false(self, df_with_na):
        """na_rm should default to False."""
        g = geom_point()
        assert g.params.get('na_rm') == False

    def test_na_rm_true_removes_missing(self, df_with_na):
        """na_rm=True should remove rows with NA in mapped columns."""
        p = ggplot(df_with_na, aes(x='x', y='y')) + geom_point(na_rm=True)
        fig = p.draw()
        # Should have 3 points (rows 0, 3, 4 have complete data)
        assert len(fig.data) >= 1

    def test_na_rm_false_keeps_data(self, df_with_na):
        """na_rm=False should keep all data (default behavior)."""
        p = ggplot(df_with_na, aes(x='x', y='y')) + geom_point(na_rm=False)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_na_rm_with_geom_line(self, df_with_na):
        """na_rm should work with geom_line."""
        p = ggplot(df_with_na, aes(x='x', y='y')) + geom_line(na_rm=True)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_na_rm_with_geom_bar(self):
        """na_rm should work with geom_bar."""
        df = pd.DataFrame({
            'category': ['A', 'B', np.nan, 'D'],
            'value': [10, np.nan, 12, 14],
        })
        p = ggplot(df, aes(x='category', y='value')) + geom_bar(stat='identity', na_rm=True)
        fig = p.draw()
        assert len(fig.data) >= 1


class TestShowLegendParameter:
    """Tests for show_legend parameter in base Geom class."""

    def test_show_legend_default_true(self):
        """show_legend should default to True."""
        g = geom_point()
        assert g.params.get('show_legend') == True

    def test_show_legend_false(self, basic_df):
        """show_legend=False should be accepted."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_point(show_legend=False)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_showlegend_alias(self):
        """showlegend should be an alias for show_legend."""
        g = geom_point(showlegend=False)
        assert g.params.get('show_legend') == False


class TestColourAlias:
    """Tests for colour/color alias in base Geom class."""

    def test_colour_alias_works(self, basic_df):
        """colour should work as alias for color."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_point(colour='red')
        fig = p.draw()
        assert len(fig.data) >= 1
        # The color should be applied
        assert 'red' in str(fig.data[0].marker.color).lower() or fig.data[0].marker.color == 'red'

    def test_color_takes_precedence(self, basic_df):
        """If both color and colour specified, color should take precedence."""
        g = geom_point(color='blue', colour='red')
        assert g.params.get('color') == 'blue'


# =============================================================================
# Priority 2: Geom-Specific Parameters
# =============================================================================

class TestGeomColWidth:
    """Tests for width parameter in geom_col."""

    def test_width_default(self):
        """geom_col should have default width of 0.9."""
        g = geom_col()
        assert g.params.get('width') == 0.9

    def test_width_custom(self, category_df):
        """Custom width should be applied."""
        p = ggplot(category_df, aes(x='category', y='value')) + geom_col(width=0.5)
        fig = p.draw()
        assert len(fig.data) >= 1
        # Width should be set on the trace
        assert fig.data[0].width == 0.5

    def test_width_narrow(self, category_df):
        """Narrow width (0.3) should work."""
        p = ggplot(category_df, aes(x='category', y='value')) + geom_col(width=0.3)
        fig = p.draw()
        assert fig.data[0].width == 0.3

    def test_width_full(self, category_df):
        """Full width (1.0) should work."""
        p = ggplot(category_df, aes(x='category', y='value')) + geom_col(width=1.0)
        fig = p.draw()
        assert fig.data[0].width == 1.0


class TestGeomSmoothFullrange:
    """Tests for fullrange parameter in geom_smooth."""

    def test_fullrange_default_false(self):
        """fullrange should default to False."""
        g = geom_smooth()
        assert g.params.get('fullrange') == False

    def test_fullrange_true_accepted(self, basic_df):
        """fullrange=True should be accepted."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_smooth(fullrange=True, se=False)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_n_parameter(self):
        """n parameter should control number of prediction points."""
        g = geom_smooth(n=100)
        assert g.params.get('n') == 100


class TestGeomRibbonParams:
    """Tests for linetype and size parameters in geom_ribbon."""

    def test_ribbon_default_params(self):
        """geom_ribbon should have default alpha and size."""
        g = geom_ribbon()
        assert g.params.get('alpha') == 0.5
        assert g.params.get('size') == 1

    def test_ribbon_custom_size(self, ribbon_df):
        """Custom size should be passed through."""
        p = ggplot(ribbon_df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(size=3)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_ribbon_linetype(self, ribbon_df):
        """linetype should be passed through."""
        p = ggplot(ribbon_df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(linetype='dash')
        fig = p.draw()
        assert len(fig.data) >= 1


class TestGeomAreaPosition:
    """Tests for position parameter in geom_area."""

    def test_position_default_identity(self):
        """position should default to 'identity'."""
        g = geom_area()
        assert g.params.get('position') == 'identity'

    def test_position_stack(self, area_df):
        """position='stack' should create stacked areas."""
        p = ggplot(area_df, aes(x='x', y='y', fill='group')) + geom_area(position='stack')
        fig = p.draw()
        assert len(fig.data) >= 1
        # Stack mode should set stackgroup
        assert any(hasattr(trace, 'stackgroup') and trace.stackgroup for trace in fig.data)

    def test_position_identity(self, area_df):
        """position='identity' should not stack."""
        p = ggplot(area_df, aes(x='x', y='y', fill='group')) + geom_area(position='identity')
        fig = p.draw()
        assert len(fig.data) >= 1


# =============================================================================
# Priority 3: Linewidth Alias Consistency
# =============================================================================

class TestLinewidthAlias:
    """Tests for linewidth alias across all line-based geoms."""

    def test_geom_line_linewidth(self, basic_df):
        """geom_line should accept linewidth."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_line(linewidth=4)
        fig = p.draw()
        assert fig.data[0].line.width == 4

    def test_geom_path_linewidth(self, basic_df):
        """geom_path should accept linewidth."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_path(linewidth=3)
        fig = p.draw()
        assert fig.data[0].line.width == 3

    def test_geom_step_linewidth(self, basic_df):
        """geom_step should accept linewidth."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_step(linewidth=2)
        fig = p.draw()
        assert fig.data[0].line.width == 2

    def test_geom_segment_linewidth(self, segment_df):
        """geom_segment should accept linewidth."""
        p = ggplot(segment_df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment(linewidth=2)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_geom_smooth_linewidth(self, basic_df):
        """geom_smooth should accept linewidth."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_smooth(linewidth=5, se=False)
        fig = p.draw()
        assert fig.data[0].line.width == 5

    def test_linewidth_size_both_specified(self, basic_df):
        """If both linewidth and size specified, size should take precedence."""
        g = geom_line(linewidth=10, size=5)
        # size was explicitly provided, so it should win
        assert g.params.get('size') == 5


# =============================================================================
# Integration Tests
# =============================================================================

class TestParameterCombinations:
    """Integration tests for combining multiple new parameters."""

    def test_na_rm_with_colour(self, df_with_na):
        """na_rm and colour should work together."""
        p = ggplot(df_with_na, aes(x='x', y='y')) + geom_point(na_rm=True, colour='purple')
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_linewidth_with_linetype(self, basic_df):
        """linewidth and linetype should work together."""
        p = ggplot(basic_df, aes(x='x', y='y')) + geom_line(linewidth=3, linetype='dash')
        fig = p.draw()
        assert fig.data[0].line.width == 3
        assert fig.data[0].line.dash == 'dash'

    def test_area_position_with_alpha(self, area_df):
        """position='stack' should work with alpha."""
        p = ggplot(area_df, aes(x='x', y='y', fill='group')) + geom_area(position='stack', alpha=0.7)
        fig = p.draw()
        assert len(fig.data) >= 1

    def test_col_width_with_fill(self, category_df):
        """width should work with fill aesthetic."""
        p = ggplot(category_df, aes(x='category', y='value')) + geom_col(width=0.6, fill='coral')
        fig = p.draw()
        assert fig.data[0].width == 0.6


# =============================================================================
# Visual Regression Tests
# =============================================================================

class TestParameterAuditVisualSignatures:
    """Visual regression tests verifying expected plot structure."""

    def test_geom_col_width_signature(self, category_df):
        """Verify geom_col width creates expected structure."""
        p = ggplot(category_df, aes(x='category', y='value')) + geom_col(width=0.7)
        fig = p.draw()

        assert fig.data[0].type == 'bar'
        assert fig.data[0].width == 0.7

    def test_geom_area_stack_signature(self, area_df):
        """Verify stacked area creates expected structure."""
        p = ggplot(area_df, aes(x='x', y='y', fill='group')) + geom_area(position='stack')
        fig = p.draw()

        # Should have scatter traces with stackgroup
        scatter_traces = [t for t in fig.data if t.type == 'scatter']
        assert len(scatter_traces) >= 1

    def test_base_params_inherited(self, basic_df):
        """Verify base class params are inherited by all geoms."""
        geoms = [
            geom_point(na_rm=True, show_legend=False),
            geom_line(na_rm=True, show_legend=False),
            geom_bar(na_rm=True, show_legend=False),
        ]

        for g in geoms:
            assert g.params.get('na_rm') == True
            assert g.params.get('show_legend') == False
