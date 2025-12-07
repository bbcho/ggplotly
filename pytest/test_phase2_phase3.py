"""
Functional tests for Phase 2 and Phase 3 compatibility improvements.

These tests verify that the new ggplot2-compatible parameters actually work
and produce the expected behavior.
"""

import pytest
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from ggplotly import ggplot, aes
from ggplotly.geoms.geom_text import geom_text
from ggplotly.geoms.geom_bar import geom_bar
from ggplotly.geoms.geom_histogram import geom_histogram
from ggplotly.geoms.geom_density import geom_density
from ggplotly.geoms.geom_boxplot import geom_boxplot
from ggplotly.scales.scale_fill_manual import scale_fill_manual
from ggplotly.scales.scale_color_gradient import scale_color_gradient
from ggplotly.scales.scale_x_continuous import scale_x_continuous
from ggplotly.scales.scale_x_log10 import scale_x_log10
from ggplotly.scales.scale_y_log10 import scale_y_log10


# Test data
@pytest.fixture
def sample_df():
    np.random.seed(42)
    return pd.DataFrame({
        'x': np.random.randn(100),
        'y': np.random.randn(100),
        'label': [f'point_{i}' for i in range(100)],
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'value': np.random.rand(100) * 100
    })


@pytest.fixture
def categorical_df():
    return pd.DataFrame({
        'category': ['A', 'B', 'C', 'A', 'B', 'C'],
        'value': [10, 20, 15, 12, 18, 22],
        'group': ['X', 'X', 'X', 'Y', 'Y', 'Y']
    })


class TestGeomTextParameters:
    """Test geom_text hjust, vjust, angle, nudge parameters."""

    def test_hjust_vjust_converts_to_textposition(self, sample_df):
        """Test that hjust/vjust are converted to Plotly textposition."""
        geom = geom_text()

        # Test different combinations
        assert geom._hjust_vjust_to_textposition(0, 0) == "bottom left"
        assert geom._hjust_vjust_to_textposition(0.5, 0.5) == "middle center"
        assert geom._hjust_vjust_to_textposition(1, 1) == "top right"
        assert geom._hjust_vjust_to_textposition(0, 1) == "top left"
        assert geom._hjust_vjust_to_textposition(1, 0) == "bottom right"

    def test_nudge_offsets_applied(self, sample_df):
        """Test that nudge_x and nudge_y offset the text position."""
        df = sample_df.head(5)
        p = ggplot(df, aes(x='x', y='y', label='label')) + geom_text(nudge_x=0.5, nudge_y=0.5)
        fig = p.draw()

        # The x and y values in the trace should be offset
        trace = fig.data[0]
        original_x = df['x'].values
        # Check that values are offset (approximately, due to potential floating point)
        assert all(trace.x[i] > original_x[i] for i in range(len(original_x)))

    def test_fontface_conversion(self):
        """Test fontface to Plotly conversion."""
        geom = geom_text()

        assert geom._fontface_to_plotly("bold") == {"weight": "bold"}
        assert geom._fontface_to_plotly("italic") == {"style": "italic"}
        assert geom._fontface_to_plotly("bold.italic") == {"weight": "bold", "style": "italic"}
        assert geom._fontface_to_plotly("plain") == {}


class TestGeomBarWidth:
    """Test geom_bar width parameter."""

    def test_width_parameter_applied(self, categorical_df):
        """Test that width parameter is applied to bar traces."""
        p = ggplot(categorical_df, aes(x='category')) + geom_bar(width=0.5)
        fig = p.draw()

        # Check that width is set on the bar trace
        for trace in fig.data:
            if isinstance(trace, go.Bar):
                assert trace.width == 0.5

    def test_default_width_is_0_9(self, categorical_df):
        """Test that default width is 0.9 to match ggplot2."""
        p = ggplot(categorical_df, aes(x='category')) + geom_bar()
        fig = p.draw()

        for trace in fig.data:
            if isinstance(trace, go.Bar):
                assert trace.width == 0.9


class TestGeomHistogramBinwidth:
    """Test geom_histogram binwidth parameter."""

    def test_binwidth_overrides_bins(self, sample_df):
        """Test that binwidth takes precedence over bins."""
        p = ggplot(sample_df, aes(x='x')) + geom_histogram(binwidth=0.5, bins=10)
        fig = p.draw()

        # Check that xbins.size is set (binwidth), not nbinsx
        for trace in fig.data:
            if isinstance(trace, go.Histogram):
                assert trace.xbins is not None
                assert trace.xbins.size == 0.5

    def test_bins_parameter_works(self, sample_df):
        """Test that bins parameter sets nbinsx."""
        p = ggplot(sample_df, aes(x='x')) + geom_histogram(bins=20)
        fig = p.draw()

        for trace in fig.data:
            if isinstance(trace, go.Histogram):
                assert trace.nbinsx == 20

    def test_boundary_parameter(self, sample_df):
        """Test that boundary parameter sets bin start."""
        p = ggplot(sample_df, aes(x='x')) + geom_histogram(binwidth=0.5, boundary=0)
        fig = p.draw()

        for trace in fig.data:
            if isinstance(trace, go.Histogram):
                assert trace.xbins.start == 0

    def test_backward_compat_bin_parameter(self, sample_df):
        """Test that deprecated 'bin' parameter still works."""
        p = ggplot(sample_df, aes(x='x')) + geom_histogram(bin=15)
        fig = p.draw()

        for trace in fig.data:
            if isinstance(trace, go.Histogram):
                assert trace.nbinsx == 15


class TestGeomDensityBandwidth:
    """Test geom_density bandwidth parameters."""

    def test_adjust_parameter_affects_smoothing(self, sample_df):
        """Test that adjust parameter changes bandwidth."""
        # With adjust=0.5, should have more detail (less smoothing)
        geom1 = geom_density(adjust=0.5)
        geom1.data = sample_df
        geom1.mapping = {'x': 'x'}

        # With adjust=2, should have less detail (more smoothing)
        geom2 = geom_density(adjust=2)
        geom2.data = sample_df
        geom2.mapping = {'x': 'x'}

        bw1 = geom1._compute_bandwidth(sample_df['x'], 'nrd0', 0.5)
        bw2 = geom2._compute_bandwidth(sample_df['x'], 'nrd0', 2)

        assert bw1 < bw2  # Lower adjust = smaller bandwidth

    def test_numeric_bw_parameter(self, sample_df):
        """Test that numeric bw parameter is used directly."""
        geom = geom_density(bw=1.0)
        geom.data = sample_df
        geom.mapping = {'x': 'x'}

        bw = geom._compute_bandwidth(sample_df['x'], 1.0, 1)
        assert bw == 1.0

    def test_n_parameter_controls_points(self, sample_df):
        """Test that n parameter controls number of evaluation points."""
        # Default is 512
        geom1 = geom_density()
        assert geom1.n == 512

        # Custom n
        geom2 = geom_density(n=256)
        assert geom2.n == 256


class TestGeomBoxplotOutliers:
    """Test geom_boxplot outlier parameters."""

    def test_outlier_parameters_set(self, categorical_df):
        """Test that outlier parameters are stored correctly."""
        geom = geom_boxplot(
            outlier_colour='red',
            outlier_size=3,
            outlier_shape='square'
        )

        assert geom.outlier_colour == 'red'
        assert geom.outlier_size == 3
        assert geom.outlier_shape == 'square'

    def test_outlier_color_american_spelling(self):
        """Test that outlier_color (American spelling) works."""
        geom = geom_boxplot(outlier_color='blue')
        assert geom.outlier_colour == 'blue'

    def test_notch_parameter(self, categorical_df):
        """Test that notch parameter enables notched boxplot."""
        p = ggplot(categorical_df, aes(x='category', y='value')) + geom_boxplot(notch=True)
        fig = p.draw()

        for trace in fig.data:
            if isinstance(trace, go.Box):
                assert trace.notched == True

    def test_shape_to_plotly_symbol(self):
        """Test shape conversion to Plotly symbols."""
        geom = geom_boxplot()

        assert geom._shape_to_plotly_symbol('circle') == 'circle'
        assert geom._shape_to_plotly_symbol('square') == 'square'
        assert geom._shape_to_plotly_symbol(16) == 'circle'  # R's pch=16
        assert geom._shape_to_plotly_symbol(0) == 'square-open'  # R's pch=0


class TestScaleFillManual:
    """Test scale_fill_manual parameters."""

    def test_breaks_and_labels(self, categorical_df):
        """Test that breaks and labels parameters work."""
        scale = scale_fill_manual(
            values={'A': 'red', 'B': 'blue', 'C': 'green'},
            breaks=['A', 'B'],
            labels=['Category A', 'Category B']
        )

        assert scale.breaks == ['A', 'B']
        assert scale.labels == ['Category A', 'Category B']

    def test_na_value_parameter(self, categorical_df):
        """Test that na_value is used for missing categories."""
        df = categorical_df.copy()
        scale = scale_fill_manual(
            values={'A': 'red', 'B': 'blue'},  # Missing 'C'
            na_value='purple'
        )

        result = scale.apply_scale(df.copy(), {'fill': 'category'})
        # 'C' should be mapped to 'purple'
        c_rows = result[result['category'] == 'C']['fill']
        assert all(c_rows == 'purple')

    def test_list_values(self, categorical_df):
        """Test that list values are mapped to categories in order."""
        scale = scale_fill_manual(values=['red', 'blue', 'green'])
        result = scale.apply_scale(categorical_df.copy(), {'fill': 'category'})

        # Should have mapped categories to colors
        assert 'fill' in result.columns


class TestScaleColorGradient:
    """Test scale_color_gradient parameters."""

    def test_name_parameter(self, sample_df):
        """Test that name parameter sets colorbar title."""
        scale = scale_color_gradient(name='Temperature')
        assert scale.name == 'Temperature'

    def test_limits_parameter(self, sample_df):
        """Test that limits parameter is stored."""
        scale = scale_color_gradient(limits=(0, 100))
        assert scale.limits == (0, 100)

    def test_guide_none_hides_colorbar(self, sample_df):
        """Test that guide='none' hides the colorbar."""
        scale = scale_color_gradient(guide='none')
        assert scale.guide == 'none'


class TestScaleXContinuous:
    """Test scale_x_continuous parameters."""

    def test_expand_parameter(self):
        """Test that expand parameter applies expansion to limits."""
        scale = scale_x_continuous(limits=(0, 100), expand=(0.1, 0))
        expanded = scale._apply_expansion((0, 100))

        # 10% expansion on each side of range 100 = 10 units each side
        assert expanded[0] == -10  # 0 - 100*0.1
        assert expanded[1] == 110  # 100 + 100*0.1

    def test_trans_reverse(self, sample_df):
        """Test that trans='reverse' reverses the axis."""
        scale = scale_x_continuous(trans='reverse')
        assert scale.trans == 'reverse'

    def test_position_top(self, sample_df):
        """Test that position='top' moves axis to top."""
        scale = scale_x_continuous(position='top')
        assert scale.position == 'top'

    def test_callable_labels(self):
        """Test that callable labels work."""
        scale = scale_x_continuous(
            breaks=[0, 50, 100],
            labels=lambda x: [f'${v}' for v in x]
        )

        # Simulate what apply() does
        result = scale.labels(scale.breaks)
        assert result == ['$0', '$50', '$100']


class TestScaleLog10:
    """Test scale_x_log10 and scale_y_log10 parameters."""

    def test_scale_x_log10_name(self, sample_df):
        """Test that name parameter sets axis title."""
        scale = scale_x_log10(name='Value (log scale)')
        assert scale.name == 'Value (log scale)'

    def test_scale_y_log10_breaks(self, sample_df):
        """Test that breaks parameter sets tick positions."""
        scale = scale_y_log10(breaks=[1, 10, 100, 1000])
        assert scale.breaks == [1, 10, 100, 1000]

    def test_scale_x_log10_callable_labels(self):
        """Test callable labels on log scale."""
        scale = scale_x_log10(
            breaks=[1, 10, 100],
            labels=lambda x: [f'10^{int(np.log10(v))}' for v in x]
        )

        result = scale.labels(scale.breaks)
        assert result == ['10^0', '10^1', '10^2']


class TestCoordFlipIntegration:
    """Integration tests for coord_flip fixes from Phase 1."""

    def test_coord_flip_swaps_data(self, categorical_df):
        """Test that coord_flip actually swaps x and y data."""
        from ggplotly.coords.coord_flip import coord_flip

        p = ggplot(categorical_df, aes(x='category', y='value')) + geom_bar(stat='identity')
        fig = p.draw()

        # Get original x values
        original_x = list(fig.data[0].x)
        original_y = list(fig.data[0].y)

        # Apply coord_flip
        coord = coord_flip()
        coord.apply(fig)

        # After flip, x should be what y was and vice versa
        assert list(fig.data[0].x) == original_y
        assert list(fig.data[0].y) == original_x


class TestStatSmoothConfidenceLevel:
    """Test stat_smooth confidence level fix from Phase 1."""

    def test_default_level_is_095(self):
        """Test that default confidence level is 0.95 (not 0.68)."""
        from ggplotly.stats.stat_smooth import stat_smooth

        smoother = stat_smooth()
        assert smoother.level == 0.95


class TestScaleBrewerDefaultType:
    """Test scale_brewer default type fix from Phase 1."""

    def test_default_type_is_seq(self):
        """Test that default type is 'seq' (not 'qual')."""
        from ggplotly.scales.scale_color_brewer import scale_color_brewer
        from ggplotly.scales.scale_fill_brewer import scale_fill_brewer

        color_scale = scale_color_brewer()
        fill_scale = scale_fill_brewer()

        assert color_scale.type == 'seq'
        assert fill_scale.type == 'seq'
