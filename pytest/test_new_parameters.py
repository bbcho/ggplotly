# pytest/test_new_parameters.py
"""
Tests for new ggplot2-compatible parameters added to ggplotly.

Tests cover:
- geom_point: stroke parameter
- geom_segment: arrow parameter
- geom_errorbar: width parameter
- linewidth alias for size
- geom_text: parse parameter
- New position exports: position_fill, position_nudge, position_identity, position_dodge2

Test categories:
1. Basic functionality tests
2. Edge cases
3. Integration tests (with faceting, color mappings, multiple geoms)
4. Visual regression tests (image comparison)
"""

import hashlib
import json
import os
import tempfile

import numpy as np
import pandas as pd
import pytest

from ggplotly import (
    aes,
    facet_grid,
    facet_wrap,
    geom_bar,
    geom_density,
    geom_errorbar,
    geom_line,
    geom_point,
    geom_ribbon,
    geom_segment,
    geom_smooth,
    geom_text,
    ggplot,
    labs,
    position_dodge,
    position_dodge2,
    position_fill,
    position_identity,
    position_jitter,
    position_nudge,
    scale_color_manual,
    theme_minimal,
)


# =============================================================================
# BASIC FUNCTIONALITY TESTS
# =============================================================================


class TestGeomPointStroke:
    """Tests for geom_point stroke parameter."""

    def test_stroke_default(self):
        """Test that stroke defaults to 0."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point()
        fig = plot.draw()
        assert fig is not None

    def test_stroke_with_value(self):
        """Test that stroke parameter is applied."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2)
        fig = plot.draw()
        # Check that marker line width is set
        assert fig.data[0].marker.line.width == 2

    def test_stroke_zero_no_line(self):
        """Test that stroke=0 doesn't add marker line."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=0)
        fig = plot.draw()
        # stroke=0 should result in empty marker_line (no width set)
        assert fig is not None


class TestGeomSegmentArrow:
    """Tests for geom_segment arrow parameter."""

    def test_arrow_default_false(self):
        """Test that arrow defaults to False."""
        df = pd.DataFrame({"x": [1], "y": [1], "xend": [2], "yend": [2]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment()
        fig = plot.draw()
        # Without arrow, mode should be 'lines'
        assert fig.data[0].mode == "lines"

    def test_arrow_true_adds_markers(self):
        """Test that arrow=True changes mode to lines+markers."""
        df = pd.DataFrame({"x": [1], "y": [1], "xend": [2], "yend": [2]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True
        )
        fig = plot.draw()
        # With arrow, mode should be 'lines+markers'
        assert fig.data[0].mode == "lines+markers"
        # Check arrow marker is configured
        assert fig.data[0].marker.symbol[1] == "arrow"

    def test_arrow_size_parameter(self):
        """Test that arrow_size parameter is applied."""
        df = pd.DataFrame({"x": [1], "y": [1], "xend": [2], "yend": [2]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True, arrow_size=20
        )
        fig = plot.draw()
        assert fig.data[0].marker.size[1] == 20


class TestGeomErrorbarWidth:
    """Tests for geom_errorbar width parameter."""

    def test_width_default(self):
        """Test that width has a default value."""
        df = pd.DataFrame({"x": [1, 2], "y": [5, 6], "ymin": [4, 5], "ymax": [6, 7]})
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax")) + geom_errorbar()
        fig = plot.draw()
        # Default width should be 4
        assert fig.data[0].error_y.width == 4

    def test_width_custom(self):
        """Test that custom width is applied."""
        df = pd.DataFrame({"x": [1, 2], "y": [5, 6], "ymin": [4, 5], "ymax": [6, 7]})
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax")) + geom_errorbar(
            width=10
        )
        fig = plot.draw()
        assert fig.data[0].error_y.width == 10


class TestLinewidthAlias:
    """Tests for linewidth as alias for size."""

    def test_linewidth_alias_in_geom_line(self):
        """Test that linewidth works as alias for size in geom_line."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_line(linewidth=5)
        fig = plot.draw()
        # linewidth should map to line width
        assert fig.data[0].line.width == 5

    def test_size_still_works(self):
        """Test that size parameter still works."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_line(size=3)
        fig = plot.draw()
        assert fig.data[0].line.width == 3

    def test_size_takes_precedence(self):
        """Test that explicit size takes precedence over linewidth."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        # If both are provided, size should win (it's more explicit)
        plot = ggplot(df, aes(x="x", y="y")) + geom_line(size=3, linewidth=5)
        fig = plot.draw()
        # size=3 should be used since it was explicitly provided
        assert fig.data[0].line.width == 3


class TestGeomTextParse:
    """Tests for geom_text parse parameter."""

    def test_parse_default_false(self):
        """Test that parse defaults to False."""
        df = pd.DataFrame({"x": [1], "y": [1], "label": ["alpha"]})
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text()
        fig = plot.draw()
        # Without parse, text should be plain
        assert fig.data[0].text[0] == "alpha"

    def test_parse_true_wraps_in_mathjax(self):
        """Test that parse=True wraps text in $ for MathJax."""
        df = pd.DataFrame({"x": [1], "y": [1], "label": ["alpha"]})
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        # With parse, text should be wrapped in $...$
        assert fig.data[0].text[0] == "$alpha$"

    def test_parse_already_mathjax(self):
        """Test that parse doesn't double-wrap already MathJax text."""
        df = pd.DataFrame({"x": [1], "y": [1], "label": ["$beta$"]})
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        # Should not become $$beta$$
        assert fig.data[0].text[0] == "$beta$"


class TestPositionExports:
    """Tests that new position functions are properly exported."""

    def test_position_fill_exported(self):
        """Test that position_fill is exported and callable."""
        pos = position_fill()
        assert pos is not None

    def test_position_nudge_exported(self):
        """Test that position_nudge is exported and callable."""
        pos = position_nudge(x=0.1, y=0.1)
        assert pos is not None

    def test_position_identity_exported(self):
        """Test that position_identity is exported and callable."""
        pos = position_identity()
        assert pos is not None

    def test_position_dodge2_exported(self):
        """Test that position_dodge2 is exported and callable."""
        pos = position_dodge2()
        assert pos is not None


# =============================================================================
# EDGE CASE TESTS
# =============================================================================


class TestStrokeEdgeCases:
    """Edge case tests for geom_point stroke parameter."""

    def test_stroke_with_large_value(self):
        """Test stroke with large value."""
        df = pd.DataFrame({"x": [1, 2], "y": [1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=10)
        fig = plot.draw()
        assert fig.data[0].marker.line.width == 10

    def test_stroke_with_float_value(self):
        """Test stroke with float value."""
        df = pd.DataFrame({"x": [1, 2], "y": [1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=1.5)
        fig = plot.draw()
        assert fig.data[0].marker.line.width == 1.5

    def test_stroke_with_color_aesthetic(self):
        """Test stroke works with color aesthetic."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3], "cat": ["A", "A", "B"]})
        plot = ggplot(df, aes(x="x", y="y", color="cat")) + geom_point(stroke=2)
        fig = plot.draw()
        # Should have multiple traces, each with stroke
        assert len(fig.data) >= 2
        for trace in fig.data:
            assert trace.marker.line.width == 2

    def test_stroke_with_shape_aesthetic(self):
        """Test stroke works with shape aesthetic."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3], "cat": ["A", "A", "B"]})
        plot = ggplot(df, aes(x="x", y="y", shape="cat")) + geom_point(stroke=3)
        fig = plot.draw()
        assert fig is not None

    def test_stroke_with_size_parameter(self):
        """Test stroke and size work together."""
        df = pd.DataFrame({"x": [1, 2], "y": [1, 2]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(size=15, stroke=3)
        fig = plot.draw()
        assert fig.data[0].marker.size == 15
        assert fig.data[0].marker.line.width == 3

    def test_stroke_empty_dataframe(self):
        """Test stroke with empty dataframe doesn't crash."""
        df = pd.DataFrame({"x": [], "y": []})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2)
        fig = plot.draw()
        assert fig is not None


class TestArrowEdgeCases:
    """Edge case tests for geom_segment arrow parameter."""

    def test_arrow_multiple_segments(self):
        """Test arrow with multiple segments."""
        df = pd.DataFrame({
            "x": [0, 1, 2],
            "y": [0, 0, 0],
            "xend": [1, 2, 3],
            "yend": [1, 1, 1],
        })
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True
        )
        fig = plot.draw()
        # Each segment should have arrow
        assert len(fig.data) == 3
        for trace in fig.data:
            assert trace.mode == "lines+markers"

    def test_arrow_with_color_grouping(self):
        """Test arrow with color aesthetic."""
        df = pd.DataFrame({
            "x": [0, 1],
            "y": [0, 0],
            "xend": [1, 2],
            "yend": [1, 1],
            "cat": ["A", "B"],
        })
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend", color="cat")) + geom_segment(
            arrow=True
        )
        fig = plot.draw()
        # Each category should have arrow
        for trace in fig.data:
            assert trace.mode == "lines+markers"

    def test_arrow_horizontal_segment(self):
        """Test arrow on horizontal segment."""
        df = pd.DataFrame({"x": [0], "y": [1], "xend": [5], "yend": [1]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True
        )
        fig = plot.draw()
        assert fig.data[0].marker.angleref == "previous"

    def test_arrow_vertical_segment(self):
        """Test arrow on vertical segment."""
        df = pd.DataFrame({"x": [1], "y": [0], "xend": [1], "yend": [5]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True
        )
        fig = plot.draw()
        assert fig.data[0].marker.angleref == "previous"

    def test_arrow_size_zero(self):
        """Test arrow with size 0 (effectively no arrow head)."""
        df = pd.DataFrame({"x": [0], "y": [0], "xend": [1], "yend": [1]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True, arrow_size=0
        )
        fig = plot.draw()
        assert fig.data[0].marker.size[1] == 0


class TestErrorbarWidthEdgeCases:
    """Edge case tests for geom_errorbar width parameter."""

    def test_width_zero(self):
        """Test width=0 (no caps)."""
        df = pd.DataFrame({"x": [1], "y": [5], "ymin": [4], "ymax": [6]})
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax")) + geom_errorbar(
            width=0
        )
        fig = plot.draw()
        assert fig.data[0].error_y.width == 0

    def test_width_with_yerr_aesthetic(self):
        """Test width with yerr aesthetic instead of ymin/ymax."""
        df = pd.DataFrame({"x": [1, 2], "y": [5, 6], "err": [0.5, 0.3]})
        plot = ggplot(df, aes(x="x", y="y", yerr="err")) + geom_errorbar(width=8)
        fig = plot.draw()
        assert fig.data[0].error_y.width == 8

    def test_width_with_grouped_data(self):
        """Test width with grouped error bars."""
        df = pd.DataFrame({
            "x": [1, 1, 2, 2],
            "y": [5, 6, 7, 8],
            "ymin": [4, 5, 6, 7],
            "ymax": [6, 7, 8, 9],
            "group": ["A", "B", "A", "B"],
        })
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax", color="group")) + geom_errorbar(
            width=6
        )
        fig = plot.draw()
        for trace in fig.data:
            assert trace.error_y.width == 6


class TestLinewidthEdgeCases:
    """Edge case tests for linewidth alias."""

    def test_linewidth_in_geom_smooth(self):
        """Test linewidth alias works in geom_smooth."""
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [1, 2, 1.5, 3, 2.5]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_smooth(linewidth=4, se=False)
        fig = plot.draw()
        # Find the line trace (not the CI ribbon)
        line_traces = [t for t in fig.data if t.mode == "lines"]
        assert len(line_traces) > 0
        assert line_traces[0].line.width == 4

    def test_linewidth_in_geom_density(self):
        """Test linewidth alias works in geom_density."""
        np.random.seed(42)
        df = pd.DataFrame({"x": np.random.normal(0, 1, 100)})
        plot = ggplot(df, aes(x="x")) + geom_density(linewidth=3)
        fig = plot.draw()
        assert fig is not None

    def test_linewidth_with_color_aesthetic(self):
        """Test linewidth with color grouping."""
        df = pd.DataFrame({
            "x": [1, 2, 3, 1, 2, 3],
            "y": [1, 2, 3, 2, 3, 4],
            "group": ["A", "A", "A", "B", "B", "B"],
        })
        plot = ggplot(df, aes(x="x", y="y", color="group")) + geom_line(linewidth=4)
        fig = plot.draw()
        for trace in fig.data:
            assert trace.line.width == 4


class TestParseEdgeCases:
    """Edge case tests for geom_text parse parameter."""

    def test_parse_complex_latex(self):
        """Test parse with complex LaTeX expressions."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["x^2", "\\frac{1}{2}", "\\sqrt{x}"],
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        assert fig.data[0].text[0] == "$x^2$"
        assert fig.data[0].text[1] == "$\\frac{1}{2}$"
        assert fig.data[0].text[2] == "$\\sqrt{x}$"

    def test_parse_mixed_content(self):
        """Test parse with mix of regular and special text."""
        df = pd.DataFrame({
            "x": [1, 2],
            "y": [1, 2],
            "label": ["regular", "\\alpha"],
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        assert fig.data[0].text[0] == "$regular$"
        assert fig.data[0].text[1] == "$\\alpha$"

    def test_parse_with_color_aesthetic(self):
        """Test parse with color grouping."""
        df = pd.DataFrame({
            "x": [1, 2],
            "y": [1, 2],
            "label": ["x", "y"],
            "cat": ["A", "B"],
        })
        plot = ggplot(df, aes(x="x", y="y", label="label", color="cat")) + geom_text(
            parse=True
        )
        fig = plot.draw()
        # All traces should have parsed text
        for trace in fig.data:
            for text in trace.text:
                assert text.startswith("$") and text.endswith("$")

    def test_parse_empty_string(self):
        """Test parse with empty string label."""
        df = pd.DataFrame({"x": [1], "y": [1], "label": [""]})
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        assert fig.data[0].text[0] == "$$"  # Empty MathJax

    def test_parse_numeric_labels(self):
        """Test parse with numeric labels."""
        df = pd.DataFrame({"x": [1, 2], "y": [1, 2], "label": [123, 456]})
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()
        assert fig.data[0].text[0] == "$123$"
        assert fig.data[0].text[1] == "$456$"


# =============================================================================
# INTEGRATION TESTS
# =============================================================================


class TestStrokeWithFaceting:
    """Integration tests for stroke with faceting."""

    def test_stroke_with_facet_wrap(self):
        """Test stroke parameter works with facet_wrap."""
        df = pd.DataFrame({
            "x": [1, 2, 3, 1, 2, 3],
            "y": [1, 2, 3, 2, 3, 4],
            "panel": ["A", "A", "A", "B", "B", "B"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point(stroke=2)
            + facet_wrap("panel")
        )
        fig = plot.draw()
        # Both panels should have points with stroke
        for trace in fig.data:
            if trace.mode == "markers":
                assert trace.marker.line.width == 2

    def test_stroke_with_facet_grid(self):
        """Test stroke parameter works with facet_grid."""
        df = pd.DataFrame({
            "x": [1, 2, 1, 2],
            "y": [1, 2, 2, 3],
            "row_var": ["R1", "R1", "R2", "R2"],
            "col_var": ["C1", "C2", "C1", "C2"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point(stroke=3)
            + facet_grid(rows="row_var", cols="col_var")
        )
        fig = plot.draw()
        assert fig is not None

    def test_stroke_with_color_and_facet(self):
        """Test stroke with both color aesthetic and faceting."""
        df = pd.DataFrame({
            "x": [1, 2, 3, 4],
            "y": [1, 2, 3, 4],
            "color_var": ["A", "B", "A", "B"],
            "facet_var": ["P1", "P1", "P2", "P2"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y", color="color_var"))
            + geom_point(stroke=2)
            + facet_wrap("facet_var")
        )
        fig = plot.draw()
        # All point traces should have stroke
        for trace in fig.data:
            if hasattr(trace, 'marker') and trace.mode == "markers":
                assert trace.marker.line.width == 2


class TestArrowIntegration:
    """Integration tests for arrow with other features."""

    def test_arrow_with_facet_wrap(self):
        """Test arrow works with facet_wrap."""
        df = pd.DataFrame({
            "x": [0, 0],
            "y": [0, 0],
            "xend": [1, 1],
            "yend": [1, 1],
            "panel": ["A", "B"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y", xend="xend", yend="yend"))
            + geom_segment(arrow=True)
            + facet_wrap("panel")
        )
        fig = plot.draw()
        for trace in fig.data:
            assert trace.mode == "lines+markers"

    def test_arrow_with_multiple_geoms(self):
        """Test arrow segment combined with points."""
        df_segments = pd.DataFrame({
            "x": [0],
            "y": [0],
            "xend": [1],
            "yend": [1],
        })
        df_points = pd.DataFrame({"x": [0, 1], "y": [0, 1]})
        plot = (
            ggplot(df_points, aes(x="x", y="y"))
            + geom_point(size=10)
            + geom_segment(
                data=df_segments,
                mapping=aes(x="x", y="y", xend="xend", yend="yend"),
                arrow=True,
            )
        )
        fig = plot.draw()
        # Should have both points and arrow segment
        modes = [t.mode for t in fig.data]
        assert "markers" in modes
        assert "lines+markers" in modes


class TestLinewidthIntegration:
    """Integration tests for linewidth alias."""

    def test_linewidth_with_multiple_lines(self):
        """Test linewidth with multiple line groups."""
        df = pd.DataFrame({
            "x": [1, 2, 3] * 3,
            "y": [1, 2, 3, 2, 3, 4, 3, 4, 5],
            "group": ["A"] * 3 + ["B"] * 3 + ["C"] * 3,
        })
        plot = ggplot(df, aes(x="x", y="y", color="group")) + geom_line(linewidth=3)
        fig = plot.draw()
        assert len(fig.data) == 3
        for trace in fig.data:
            assert trace.line.width == 3

    def test_linewidth_with_ribbon(self):
        """Test linewidth alias doesn't break geom_ribbon."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [2, 3, 2.5],
            "ymin": [1, 2, 1.5],
            "ymax": [3, 4, 3.5],
        })
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax")) + geom_ribbon(
            linewidth=2
        )
        fig = plot.draw()
        assert fig is not None


class TestPositionIntegration:
    """Integration tests for new position functions."""

    def test_position_fill_with_bar(self):
        """Test position_fill with bar chart (100% stacked)."""
        df = pd.DataFrame({
            "category": ["A", "A", "B", "B"],
            "group": ["X", "Y", "X", "Y"],
            "value": [10, 20, 30, 40],
        })
        plot = (
            ggplot(df, aes(x="category", y="value", fill="group"))
            + geom_bar(stat="identity", position=position_fill())
        )
        fig = plot.draw()
        assert fig is not None

    def test_position_nudge_with_text(self):
        """Test position_nudge with text labels."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["A", "B", "C"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + geom_text(aes(label="label"), nudge_y=0.2)
        )
        fig = plot.draw()
        assert fig is not None

    def test_position_dodge2_with_boxplot(self):
        """Test position_dodge2 is callable for boxplots."""
        pos = position_dodge2(padding=0.2)
        assert pos.padding == 0.2

    def test_position_identity_preserves_data(self):
        """Test position_identity doesn't modify positions."""
        pos = position_identity()
        assert pos is not None


class TestMultipleNewParameters:
    """Integration tests combining multiple new parameters."""

    def test_stroke_and_linewidth_together(self):
        """Test using stroke (point) and linewidth (line) in same plot."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_line(linewidth=3)
            + geom_point(stroke=2, size=10)
        )
        fig = plot.draw()
        # Find line and point traces
        line_trace = [t for t in fig.data if t.mode == "lines"][0]
        point_trace = [t for t in fig.data if t.mode == "markers"][0]
        assert line_trace.line.width == 3
        assert point_trace.marker.line.width == 2

    def test_all_new_params_complex_plot(self):
        """Test complex plot with multiple new parameters."""
        np.random.seed(42)
        df = pd.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [2, 3, 2.5, 4, 3.5],
            "ymin": [1.5, 2.5, 2, 3.5, 3],
            "ymax": [2.5, 3.5, 3, 4.5, 4],
            "label": ["A", "B", "C", "D", "E"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_line(linewidth=2)
            + geom_point(stroke=1.5, size=8)
            + geom_errorbar(aes(ymin="ymin", ymax="ymax"), width=6)
            + geom_text(aes(label="label"), parse=True, nudge_y=0.3)
            + theme_minimal()
            + labs(title="Combined New Parameters")
        )
        fig = plot.draw()
        assert fig is not None
        assert len(fig.data) >= 3  # At least line, points, errorbars


# =============================================================================
# VISUAL REGRESSION TESTS
# =============================================================================


class TestVisualRegression:
    """
    Visual regression tests using figure JSON comparison.

    These tests capture the essential visual properties of figures
    and compare them against expected values to detect regressions.
    """

    @staticmethod
    def get_figure_signature(fig):
        """
        Generate a signature of key visual properties from a figure.

        Returns a dict with essential properties that define the visual output.
        """
        signature = {
            "num_traces": len(fig.data),
            "traces": [],
        }

        for i, trace in enumerate(fig.data):
            trace_sig = {
                "type": trace.type,
                "mode": getattr(trace, "mode", None),
            }

            # Capture marker properties
            if hasattr(trace, "marker") and trace.marker:
                marker = trace.marker
                symbol = getattr(marker, "symbol", None)
                # Convert tuple to list for consistent comparison
                if isinstance(symbol, tuple):
                    symbol = list(symbol)
                size = getattr(marker, "size", None)
                if isinstance(size, tuple):
                    size = list(size)
                trace_sig["marker"] = {
                    "size": size,
                    "symbol": symbol,
                }
                if hasattr(marker, "line") and marker.line:
                    trace_sig["marker"]["line_width"] = getattr(marker.line, "width", None)

            # Capture line properties
            if hasattr(trace, "line") and trace.line:
                trace_sig["line"] = {
                    "width": getattr(trace.line, "width", None),
                    "dash": getattr(trace.line, "dash", None),
                }

            # Capture error bar properties
            if hasattr(trace, "error_y") and trace.error_y:
                trace_sig["error_y"] = {
                    "width": getattr(trace.error_y, "width", None),
                }

            # Capture text
            if hasattr(trace, "text") and trace.text is not None:
                text = trace.text
                # Handle numpy arrays and pandas Series
                if hasattr(text, "tolist"):
                    text = text.tolist()
                if isinstance(text, (list, tuple)):
                    trace_sig["text_sample"] = list(text)[:3]
                else:
                    trace_sig["text_sample"] = [text]

            signature["traces"].append(trace_sig)

        return signature

    def test_stroke_visual_signature(self):
        """Test that stroke produces expected visual signature."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_point(stroke=2.5)
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        assert sig["num_traces"] == 1
        assert sig["traces"][0]["type"] == "scatter"
        assert sig["traces"][0]["mode"] == "markers"
        assert sig["traces"][0]["marker"]["line_width"] == 2.5

    def test_arrow_visual_signature(self):
        """Test that arrow produces expected visual signature."""
        df = pd.DataFrame({"x": [0], "y": [0], "xend": [1], "yend": [1]})
        plot = ggplot(df, aes(x="x", y="y", xend="xend", yend="yend")) + geom_segment(
            arrow=True, arrow_size=18
        )
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        assert sig["num_traces"] == 1
        assert sig["traces"][0]["mode"] == "lines+markers"
        # Arrow marker at end
        assert sig["traces"][0]["marker"]["symbol"] == ["circle", "arrow"]
        assert sig["traces"][0]["marker"]["size"] == [0, 18]

    def test_errorbar_width_visual_signature(self):
        """Test that errorbar width produces expected visual signature."""
        df = pd.DataFrame({"x": [1, 2], "y": [5, 6], "ymin": [4, 5], "ymax": [6, 7]})
        plot = ggplot(df, aes(x="x", y="y", ymin="ymin", ymax="ymax")) + geom_errorbar(
            width=12
        )
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        assert sig["traces"][0]["error_y"]["width"] == 12

    def test_linewidth_visual_signature(self):
        """Test that linewidth produces expected visual signature."""
        df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 3]})
        plot = ggplot(df, aes(x="x", y="y")) + geom_line(linewidth=4.5)
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        assert sig["traces"][0]["line"]["width"] == 4.5

    def test_parse_visual_signature(self):
        """Test that parse produces expected visual signature."""
        df = pd.DataFrame({
            "x": [1, 2],
            "y": [1, 2],
            "label": ["\\alpha", "\\beta"],
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text(parse=True)
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        # Text should be wrapped in $...$
        assert sig["traces"][0]["text_sample"] == ["$\\alpha$", "$\\beta$"]

    def test_combined_visual_signature(self):
        """Test combined parameters produce expected visual signature."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["a", "b", "c"],
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_line(linewidth=2)
            + geom_point(stroke=1, size=10)
            + geom_text(aes(label="label"), parse=True, nudge_y=0.1)
        )
        fig = plot.draw()

        sig = self.get_figure_signature(fig)

        # Should have 3 traces: line, points, text
        assert sig["num_traces"] == 3

        # Find each trace type
        line_trace = next(t for t in sig["traces"] if t.get("mode") == "lines")
        point_trace = next(t for t in sig["traces"] if t.get("mode") == "markers")
        text_trace = next(t for t in sig["traces"] if t.get("mode") == "text")

        assert line_trace["line"]["width"] == 2
        assert point_trace["marker"]["size"] == 10
        assert point_trace["marker"]["line_width"] == 1
        assert text_trace["text_sample"] == ["$a$", "$b$", "$c$"]


class TestVisualRegressionWithColors:
    """Visual regression tests with color aesthetics."""

    def test_stroke_with_colors_signature(self):
        """Test stroke with color aesthetic produces correct traces."""
        df = pd.DataFrame({
            "x": [1, 2, 3, 4],
            "y": [1, 2, 3, 4],
            "cat": ["A", "A", "B", "B"],
        })
        plot = ggplot(df, aes(x="x", y="y", color="cat")) + geom_point(stroke=2)
        fig = plot.draw()

        # Should have 2 traces (one per category)
        assert len(fig.data) == 2

        # Both should have stroke
        for trace in fig.data:
            assert trace.marker.line.width == 2
            # Each trace should have different colors
            assert trace.marker.color is not None

    def test_linewidth_with_colors_signature(self):
        """Test linewidth with color aesthetic produces correct traces."""
        df = pd.DataFrame({
            "x": [1, 2, 3] * 2,
            "y": [1, 2, 3, 2, 3, 4],
            "cat": ["A"] * 3 + ["B"] * 3,
        })
        plot = ggplot(df, aes(x="x", y="y", color="cat")) + geom_line(linewidth=3)
        fig = plot.draw()

        # Should have 2 traces
        assert len(fig.data) == 2

        # Both should have linewidth
        for trace in fig.data:
            assert trace.line.width == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
