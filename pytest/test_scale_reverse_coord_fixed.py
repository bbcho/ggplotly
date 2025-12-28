"""
Tests for scale_x_reverse, scale_y_reverse, and coord_fixed.

Covers all four test categories:
1. Basic functionality tests
2. Edge case tests
3. Integration tests (with other scales/coords, faceting)
4. Visual regression tests
"""

import numpy as np
import pandas as pd
import pytest

from ggplotly import (
    aes,
    coord_fixed,
    facet_wrap,
    geom_line,
    geom_path,
    geom_point,
    ggplot,
    scale_x_reverse,
    scale_y_reverse,
)


# =============================================================================
# SCALE_X_REVERSE TESTS
# =============================================================================


class TestScaleXReverseBasic:
    """Basic functionality tests for scale_x_reverse."""

    def test_scale_x_reverse_basic(self):
        """Test basic x-axis reversal."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_x_reverse()
        fig = plot.draw()
        # Check that autorange is set to reversed
        assert fig.layout.xaxis.autorange == "reversed"

    def test_scale_x_reverse_with_name(self):
        """Test reversed x-axis with custom name."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_x_reverse(name="Reversed X")
        fig = plot.draw()
        assert fig.layout.xaxis.title.text == "Reversed X"

    def test_scale_x_reverse_with_limits(self):
        """Test reversed x-axis with explicit limits."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_x_reverse(limits=(0, 10))
        fig = plot.draw()
        # Limits should be reversed (high to low)
        xrange = fig.layout.xaxis.range
        assert xrange[0] > xrange[1]  # First value greater than second (reversed)

    def test_scale_x_reverse_with_breaks(self):
        """Test reversed x-axis with custom breaks."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse(breaks=[1, 2, 3])
        )
        fig = plot.draw()
        assert fig.layout.xaxis.tickmode == "array"
        assert list(fig.layout.xaxis.tickvals) == [1, 2, 3]

    def test_scale_x_reverse_with_labels(self):
        """Test reversed x-axis with custom labels."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse(breaks=[1, 2, 3], labels=["A", "B", "C"])
        )
        fig = plot.draw()
        assert list(fig.layout.xaxis.ticktext) == ["A", "B", "C"]


class TestScaleYReverseBasic:
    """Basic functionality tests for scale_y_reverse."""

    def test_scale_y_reverse_basic(self):
        """Test basic y-axis reversal."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_y_reverse()
        fig = plot.draw()
        assert fig.layout.yaxis.autorange == "reversed"

    def test_scale_y_reverse_with_name(self):
        """Test reversed y-axis with custom name."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_y_reverse(name="Depth")
        fig = plot.draw()
        assert fig.layout.yaxis.title.text == "Depth"

    def test_scale_y_reverse_with_limits(self):
        """Test reversed y-axis with explicit limits."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_y_reverse(limits=(0, 100))
        fig = plot.draw()
        # Limits should be reversed
        yrange = fig.layout.yaxis.range
        assert yrange[0] > yrange[1]


# =============================================================================
# COORD_FIXED TESTS
# =============================================================================


class TestCoordFixedBasic:
    """Basic functionality tests for coord_fixed."""

    def test_coord_fixed_basic(self):
        """Test basic fixed aspect ratio (1:1)."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed()
        fig = plot.draw()
        # Y-axis should be anchored to x-axis with ratio 1
        assert fig.layout.yaxis.scaleanchor == "x"
        assert fig.layout.yaxis.scaleratio == 1

    def test_coord_fixed_custom_ratio(self):
        """Test fixed aspect ratio with custom ratio."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ratio=2)
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 2

    def test_coord_fixed_ratio_half(self):
        """Test fixed aspect ratio with ratio < 1."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ratio=0.5)
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 0.5

    def test_coord_fixed_with_xlim(self):
        """Test fixed aspect ratio with x-axis limits."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(xlim=(0, 5))
        fig = plot.draw()
        assert fig.layout.xaxis.range is not None

    def test_coord_fixed_with_ylim(self):
        """Test fixed aspect ratio with y-axis limits."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ylim=(0, 5))
        fig = plot.draw()
        assert fig.layout.yaxis.range is not None

    def test_coord_fixed_constrained(self):
        """Test that coord_fixed sets constrain to domain."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed()
        fig = plot.draw()
        assert fig.layout.xaxis.constrain == "domain"
        assert fig.layout.yaxis.constrain == "domain"


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestReverseScaleEdgeCases:
    """Edge case tests for reverse scales."""

    def test_scale_x_reverse_empty_data(self):
        """Test reverse scale with empty data."""
        df = pd.DataFrame({"x": [], "y": []})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_x_reverse()
        fig = plot.draw()  # Should not crash
        assert fig.layout.xaxis.autorange == "reversed"

    def test_scale_y_reverse_single_point(self):
        """Test reverse scale with single data point."""
        df = pd.DataFrame({"x": [5], "y": [5]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_y_reverse()
        fig = plot.draw()
        assert fig.layout.yaxis.autorange == "reversed"

    def test_scale_x_reverse_negative_values(self):
        """Test reverse scale with negative values."""
        df = pd.DataFrame({"x": [-10, -5, 0, 5], "y": [1, 2, 3, 4]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + scale_x_reverse()
        fig = plot.draw()
        assert fig.layout.xaxis.autorange == "reversed"

    def test_scale_reverse_callable_labels(self):
        """Test reverse scale with callable labels."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse(breaks=[1, 2, 3], labels=lambda x: [f"Val {v}" for v in x])
        )
        fig = plot.draw()
        assert list(fig.layout.xaxis.ticktext) == ["Val 1", "Val 2", "Val 3"]

    def test_both_axes_reversed(self):
        """Test both x and y axes reversed."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse()
            + scale_y_reverse()
        )
        fig = plot.draw()
        assert fig.layout.xaxis.autorange == "reversed"
        assert fig.layout.yaxis.autorange == "reversed"


class TestCoordFixedEdgeCases:
    """Edge case tests for coord_fixed."""

    def test_coord_fixed_empty_data(self):
        """Test coord_fixed with empty data."""
        df = pd.DataFrame({"x": [], "y": []})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed()
        fig = plot.draw()  # Should not crash
        assert fig.layout.yaxis.scaleanchor == "x"

    def test_coord_fixed_very_small_ratio(self):
        """Test coord_fixed with very small ratio."""
        df = pd.DataFrame({"x": [0, 1], "y": [0, 1]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ratio=0.01)
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 0.01

    def test_coord_fixed_very_large_ratio(self):
        """Test coord_fixed with very large ratio."""
        df = pd.DataFrame({"x": [0, 1], "y": [0, 1]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ratio=100)
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 100

    def test_coord_fixed_both_limits(self):
        """Test coord_fixed with both x and y limits."""
        df = pd.DataFrame({"x": [0, 1], "y": [0, 1]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + coord_fixed(xlim=(0, 10), ylim=(0, 10))
        )
        fig = plot.draw()
        assert fig.layout.xaxis.range is not None
        assert fig.layout.yaxis.range is not None

    def test_coord_fixed_no_expand(self):
        """Test coord_fixed with expand=False."""
        df = pd.DataFrame({"x": [0, 1], "y": [0, 1]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + coord_fixed(xlim=(0, 1), ylim=(0, 1), expand=False)
        )
        fig = plot.draw()
        # Without expansion, limits should be exact
        xrange = fig.layout.xaxis.range
        assert list(xrange) == [0, 1]


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestReverseScaleIntegration:
    """Integration tests for reverse scales."""

    def test_scale_x_reverse_with_line(self):
        """Test reversed x-axis with line geom."""
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 4, 2, 5, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_line() + scale_x_reverse()
        fig = plot.draw()
        assert fig.layout.xaxis.autorange == "reversed"
        assert len(fig.data) >= 1

    def test_scale_y_reverse_with_facet(self):
        """Test reversed y-axis with faceting."""
        df = pd.DataFrame({
            "x": [1, 2, 1, 2],
            "y": [1, 2, 3, 4],
            "group": ["A", "A", "B", "B"]
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_y_reverse()
            + facet_wrap("group")
        )
        fig = plot.draw()
        # At least one y-axis should be reversed
        assert any(
            getattr(fig.layout[f"yaxis{'' if i == 0 else i+1}"], "autorange", None) == "reversed"
            for i in range(4)
            if hasattr(fig.layout, f"yaxis{'' if i == 0 else i+1}")
        )

    def test_reverse_scale_with_multiple_geoms(self):
        """Test reversed scale with multiple geoms."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + geom_line()
            + scale_x_reverse()
        )
        fig = plot.draw()
        assert fig.layout.xaxis.autorange == "reversed"
        assert len(fig.data) >= 2


class TestCoordFixedIntegration:
    """Integration tests for coord_fixed."""

    def test_coord_fixed_with_circle(self):
        """Test that coord_fixed makes a circle look circular."""
        # Create circle data
        theta = np.linspace(0, 2 * np.pi, 100)
        circle_df = pd.DataFrame({
            "x": np.cos(theta),
            "y": np.sin(theta)
        })
        plot = ggplot(circle_df, aes(x="x", y="y")) + geom_path() + coord_fixed()
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 1

    def test_coord_fixed_with_facet(self):
        """Test coord_fixed with faceting."""
        df = pd.DataFrame({
            "x": [1, 2, 1, 2],
            "y": [1, 2, 3, 4],
            "group": ["A", "A", "B", "B"]
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + coord_fixed(ratio=1)
            + facet_wrap("group")
        )
        fig = plot.draw()
        # The first y-axis should have scaleanchor set
        assert fig.layout.yaxis.scaleanchor == "x"

    def test_coord_fixed_with_multiple_geoms(self):
        """Test coord_fixed with multiple geoms."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + geom_line()
            + coord_fixed()
        )
        fig = plot.draw()
        assert fig.layout.yaxis.scaleratio == 1
        assert len(fig.data) >= 2


# =============================================================================
# VISUAL REGRESSION TESTS
# =============================================================================


class TestVisualRegressionScales:
    """Visual regression tests for reverse scales."""

    def get_axis_signature(self, fig):
        """Extract key axis properties."""
        return {
            "xaxis": {
                "autorange": getattr(fig.layout.xaxis, "autorange", None),
                "range": getattr(fig.layout.xaxis, "range", None),
                "title": getattr(fig.layout.xaxis.title, "text", None) if fig.layout.xaxis.title else None,
                "tickmode": getattr(fig.layout.xaxis, "tickmode", None),
            },
            "yaxis": {
                "autorange": getattr(fig.layout.yaxis, "autorange", None),
                "range": getattr(fig.layout.yaxis, "range", None),
                "title": getattr(fig.layout.yaxis.title, "text", None) if fig.layout.yaxis.title else None,
                "scaleanchor": getattr(fig.layout.yaxis, "scaleanchor", None),
                "scaleratio": getattr(fig.layout.yaxis, "scaleratio", None),
            }
        }

    def test_scale_x_reverse_signature(self):
        """Test scale_x_reverse visual signature."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse(name="Reversed", breaks=[1, 2, 3])
        )
        fig = plot.draw()
        sig = self.get_axis_signature(fig)

        assert sig["xaxis"]["autorange"] == "reversed"
        assert sig["xaxis"]["title"] == "Reversed"
        assert sig["xaxis"]["tickmode"] == "array"

    def test_scale_y_reverse_signature(self):
        """Test scale_y_reverse visual signature."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_y_reverse(name="Depth")
        )
        fig = plot.draw()
        sig = self.get_axis_signature(fig)

        assert sig["yaxis"]["autorange"] == "reversed"
        assert sig["yaxis"]["title"] == "Depth"

    def test_coord_fixed_signature(self):
        """Test coord_fixed visual signature."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point() + coord_fixed(ratio=1.5)
        fig = plot.draw()
        sig = self.get_axis_signature(fig)

        assert sig["yaxis"]["scaleanchor"] == "x"
        assert sig["yaxis"]["scaleratio"] == 1.5

    def test_combined_reverse_and_fixed(self):
        """Test combining reversed scale with coord_fixed."""
        df = pd.DataFrame({"x": [0, 1, 2], "y": [0, 1, 2]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + scale_x_reverse()
            + coord_fixed()
        )
        fig = plot.draw()
        sig = self.get_axis_signature(fig)

        assert sig["xaxis"]["autorange"] == "reversed"
        assert sig["yaxis"]["scaleanchor"] == "x"
        assert sig["yaxis"]["scaleratio"] == 1
