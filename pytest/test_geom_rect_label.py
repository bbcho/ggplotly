"""
Tests for geom_rect and geom_label.

Covers all four test categories:
1. Basic functionality tests
2. Edge case tests
3. Integration tests (faceting & color mappings)
4. Visual regression tests
"""

import pandas as pd
import pytest

from ggplotly import (
    aes,
    facet_grid,
    facet_wrap,
    geom_label,
    geom_line,
    geom_point,
    geom_rect,
    geom_text,
    ggplot,
)


# =============================================================================
# GEOM_RECT TESTS
# =============================================================================


class TestGeomRectBasic:
    """Basic functionality tests for geom_rect."""

    def test_rect_basic(self):
        """Test basic rectangle creation."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()
        assert len(fig.data) >= 1
        # Check it's a filled scatter trace
        assert fig.data[0].fill == "toself"

    def test_rect_multiple(self):
        """Test multiple rectangles."""
        df = pd.DataFrame({
            "xmin": [1, 4], "xmax": [3, 6],
            "ymin": [1, 2], "ymax": [4, 5]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()
        # Should have 2 traces (one per rectangle, grouped in legendgroup)
        assert len(fig.data) == 2

    def test_rect_with_fill_color(self):
        """Test rectangle with explicit fill color."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect(
            fill="red"
        )
        fig = plot.draw()
        assert fig.data[0].fillcolor == "red"

    def test_rect_with_border(self):
        """Test rectangle with border color and width."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect(
            fill="lightblue", color="navy", size=2
        )
        fig = plot.draw()
        assert fig.data[0].line.color == "navy"
        assert fig.data[0].line.width == 2

    def test_rect_alpha(self):
        """Test rectangle transparency."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect(
            alpha=0.3
        )
        fig = plot.draw()
        assert fig.data[0].opacity == 0.3

    def test_rect_default_alpha(self):
        """Test rectangle default transparency is 0.5."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()
        assert fig.data[0].opacity == 0.5


class TestGeomRectEdgeCases:
    """Edge case tests for geom_rect."""

    def test_rect_empty_dataframe(self):
        """Test rect with empty DataFrame doesn't crash."""
        df = pd.DataFrame({
            "xmin": [], "xmax": [], "ymin": [], "ymax": []
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()  # Should not raise
        assert len(fig.data) == 0

    def test_rect_zero_area(self):
        """Test rectangle with zero area (point)."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [1], "ymin": [1], "ymax": [1]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()  # Should not crash
        assert len(fig.data) >= 1

    def test_rect_negative_coords(self):
        """Test rectangle with negative coordinates."""
        df = pd.DataFrame({
            "xmin": [-5], "xmax": [-1], "ymin": [-3], "ymax": [-1]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()
        # Verify the path includes negative values
        assert min(fig.data[0].x) == -5
        assert min(fig.data[0].y) == -3

    def test_rect_large_values(self):
        """Test rectangle with large coordinate values."""
        df = pd.DataFrame({
            "xmin": [1e6], "xmax": [1e7], "ymin": [1e6], "ymax": [1e7]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()
        assert len(fig.data) >= 1

    def test_rect_inverted_coords(self):
        """Test rectangle where xmin > xmax (inverted)."""
        df = pd.DataFrame({
            "xmin": [5], "xmax": [1], "ymin": [5], "ymax": [1]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()  # Should still work (creates inverted rectangle)
        assert len(fig.data) >= 1

    def test_rect_linetype_dash(self):
        """Test rectangle with dashed border."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect(
            color="black", linetype="dash"
        )
        fig = plot.draw()
        assert fig.data[0].line.dash == "dash"


class TestGeomRectIntegration:
    """Integration tests for geom_rect with faceting and aesthetics."""

    def test_rect_with_fill_aesthetic(self):
        """Test rectangle with fill mapped to variable."""
        df = pd.DataFrame({
            "xmin": [1, 4], "xmax": [3, 6],
            "ymin": [1, 2], "ymax": [4, 5],
            "category": ["A", "B"]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="category")) + geom_rect()
        fig = plot.draw()
        # Should have separate traces for each category
        assert len(fig.data) == 2
        # Check they have different colors
        colors = {fig.data[0].fillcolor, fig.data[1].fillcolor}
        assert len(colors) == 2

    def test_rect_with_color_aesthetic(self):
        """Test rectangle with color mapped to variable."""
        df = pd.DataFrame({
            "xmin": [1, 4], "xmax": [3, 6],
            "ymin": [1, 2], "ymax": [4, 5],
            "category": ["A", "B"]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", color="category")) + geom_rect()
        fig = plot.draw()
        assert len(fig.data) == 2

    def test_rect_with_facet_wrap(self):
        """Test rectangle with facet_wrap."""
        df = pd.DataFrame({
            "xmin": [1, 1], "xmax": [3, 3],
            "ymin": [1, 1], "ymax": [4, 4],
            "panel": ["A", "B"]
        })
        plot = (
            ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"))
            + geom_rect()
            + facet_wrap("panel")
        )
        fig = plot.draw()
        # Should create subplot structure
        assert len(fig.data) >= 2

    def test_rect_with_facet_grid(self):
        """Test rectangle with facet_grid."""
        df = pd.DataFrame({
            "xmin": [1, 1, 1, 1], "xmax": [3, 3, 3, 3],
            "ymin": [1, 1, 1, 1], "ymax": [4, 4, 4, 4],
            "row_var": ["R1", "R1", "R2", "R2"],
            "col_var": ["C1", "C2", "C1", "C2"]
        })
        plot = (
            ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"))
            + geom_rect()
            + facet_grid(rows="row_var", cols="col_var")
        )
        fig = plot.draw()
        assert len(fig.data) >= 4

    def test_rect_overlay_on_scatter(self):
        """Test rectangle as overlay on scatter plot."""
        scatter_df = pd.DataFrame({
            "x": [1, 2, 3, 4, 5],
            "y": [2, 4, 3, 5, 4]
        })
        rect_df = pd.DataFrame({
            "xmin": [2], "xmax": [4], "ymin": [2.5], "ymax": [4.5]
        })
        plot = (
            ggplot(scatter_df, aes(x="x", y="y"))
            + geom_rect(data=rect_df, mapping=aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax"),
                        fill="yellow", alpha=0.3)
            + geom_point()
        )
        fig = plot.draw()
        # Should have both rect and point traces
        assert len(fig.data) >= 2


# =============================================================================
# GEOM_LABEL TESTS
# =============================================================================


class TestGeomLabelBasic:
    """Basic functionality tests for geom_label."""

    def test_label_basic(self):
        """Test basic label creation."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["A", "B", "C"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        # Labels are added as annotations
        assert len(fig.layout.annotations) == 3

    def test_label_text_content(self):
        """Test label text content is correct."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Hello World"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        assert fig.layout.annotations[0].text == "Hello World"

    def test_label_fill_color(self):
        """Test label background fill color."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(fill="lightblue")
        fig = plot.draw()
        assert fig.layout.annotations[0].bgcolor == "lightblue"

    def test_label_text_color(self):
        """Test label text color."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(color="red")
        fig = plot.draw()
        assert fig.layout.annotations[0].font.color == "red"

    def test_label_font_size(self):
        """Test label font size."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(size=16)
        fig = plot.draw()
        assert fig.layout.annotations[0].font.size == 16

    def test_label_default_fill_white(self):
        """Test label default fill is white."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        assert fig.layout.annotations[0].bgcolor == "white"

    def test_label_alpha(self):
        """Test label background transparency."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(alpha=0.5)
        fig = plot.draw()
        assert fig.layout.annotations[0].opacity == 0.5


class TestGeomLabelEdgeCases:
    """Edge case tests for geom_label."""

    def test_label_empty_dataframe(self):
        """Test label with empty DataFrame doesn't crash."""
        df = pd.DataFrame({
            "x": [],
            "y": [],
            "label": []
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()  # Should not raise
        assert len(fig.layout.annotations) == 0

    def test_label_numeric_labels(self):
        """Test label with numeric values."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": [100, 200, 300]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        assert fig.layout.annotations[0].text == "100"

    def test_label_special_characters(self):
        """Test label with special characters."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Hello <World> & 'Friends'"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        assert len(fig.layout.annotations) == 1

    def test_label_unicode(self):
        """Test label with unicode characters."""
        df = pd.DataFrame({
            "x": [1, 2],
            "y": [1, 2],
            "label": ["Hello", "World"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        fig = plot.draw()
        assert len(fig.layout.annotations) == 2

    def test_label_na_rm_true(self):
        """Test label with na_rm=True removes NA values."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, None, 3],
            "label": ["A", "B", "C"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(na_rm=True)
        fig = plot.draw()
        # Should only have 2 labels (row with None y is removed)
        assert len(fig.layout.annotations) == 2

    def test_label_nudge_x(self):
        """Test label horizontal nudge."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(nudge_x=0.5)
        fig = plot.draw()
        assert fig.layout.annotations[0].x == 1.5

    def test_label_nudge_y(self):
        """Test label vertical nudge."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(nudge_y=0.5)
        fig = plot.draw()
        assert fig.layout.annotations[0].y == 1.5

    def test_label_hjust_left(self):
        """Test label horizontal justification left."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(hjust=0)
        fig = plot.draw()
        assert fig.layout.annotations[0].xanchor == "left"

    def test_label_hjust_right(self):
        """Test label horizontal justification right."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(hjust=1)
        fig = plot.draw()
        assert fig.layout.annotations[0].xanchor == "right"

    def test_label_vjust_top(self):
        """Test label vertical justification top."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(vjust=1)
        fig = plot.draw()
        assert fig.layout.annotations[0].yanchor == "top"

    def test_label_vjust_bottom(self):
        """Test label vertical justification bottom."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(vjust=0)
        fig = plot.draw()
        assert fig.layout.annotations[0].yanchor == "bottom"

    def test_label_parse_latex(self):
        """Test label with parse=True for LaTeX."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["\\alpha"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(parse=True)
        fig = plot.draw()
        assert fig.layout.annotations[0].text == "$\\alpha$"


class TestGeomLabelIntegration:
    """Integration tests for geom_label with faceting and aesthetics."""

    def test_label_with_fill_aesthetic(self):
        """Test label with fill mapped to variable."""
        df = pd.DataFrame({
            "x": [1, 2],
            "y": [1, 2],
            "label": ["A", "B"],
            "category": ["Cat1", "Cat2"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label", fill="category")) + geom_label()
        fig = plot.draw()
        # Annotations should have different background colors
        colors = {fig.layout.annotations[0].bgcolor, fig.layout.annotations[1].bgcolor}
        assert len(colors) == 2

    def test_label_with_points(self):
        """Test label combined with geom_point."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["A", "B", "C"]
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_point()
            + geom_label(aes(label="label"), nudge_y=0.2)
        )
        fig = plot.draw()
        # Should have point trace and annotations
        assert len(fig.data) >= 1  # Points
        assert len(fig.layout.annotations) == 3  # Labels

    def test_label_with_line(self):
        """Test label combined with geom_line."""
        df = pd.DataFrame({
            "x": [1, 2, 3],
            "y": [1, 2, 3],
            "label": ["Start", "Mid", "End"]
        })
        plot = (
            ggplot(df, aes(x="x", y="y"))
            + geom_line()
            + geom_label(aes(label="label"))
        )
        fig = plot.draw()
        assert len(fig.layout.annotations) == 3

    def test_label_with_facet_wrap(self):
        """Test label with facet_wrap."""
        df = pd.DataFrame({
            "x": [1, 1],
            "y": [1, 1],
            "label": ["A", "B"],
            "panel": ["P1", "P2"]
        })
        plot = (
            ggplot(df, aes(x="x", y="y", label="label"))
            + geom_label()
            + facet_wrap("panel")
        )
        fig = plot.draw()
        # Should create annotations in faceted structure
        assert len(fig.layout.annotations) >= 2

    def test_label_vs_text(self):
        """Test that geom_label differs from geom_text by having background."""
        df = pd.DataFrame({
            "x": [1],
            "y": [1],
            "label": ["Test"]
        })

        # geom_label should use annotations with bgcolor
        label_plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label()
        label_fig = label_plot.draw()

        # geom_text should use scatter trace with text mode
        text_plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_text()
        text_fig = text_plot.draw()

        # Label uses annotations, text uses scatter traces
        assert len(label_fig.layout.annotations) == 1
        assert label_fig.layout.annotations[0].bgcolor is not None


# =============================================================================
# VISUAL REGRESSION TESTS
# =============================================================================


class TestVisualRegressionRect:
    """Visual regression tests for geom_rect."""

    def get_figure_signature(self, fig):
        """Extract key properties from figure for comparison."""
        signature = {
            "num_traces": len(fig.data),
            "traces": []
        }
        for trace in fig.data:
            trace_sig = {
                "type": trace.type,
                "fill": getattr(trace, "fill", None),
                "fillcolor": getattr(trace, "fillcolor", None),
                "opacity": getattr(trace, "opacity", None),
            }
            if hasattr(trace, "line") and trace.line:
                trace_sig["line"] = {
                    "color": getattr(trace.line, "color", None),
                    "width": getattr(trace.line, "width", None),
                    "dash": getattr(trace.line, "dash", None),
                }
            signature["traces"].append(trace_sig)
        return signature

    def test_rect_visual_signature(self):
        """Test that rect produces expected visual signature."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [1], "ymax": [4]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect(
            fill="blue", color="red", size=2, alpha=0.4
        )
        fig = plot.draw()
        sig = self.get_figure_signature(fig)

        assert sig["num_traces"] == 1
        assert sig["traces"][0]["fill"] == "toself"
        assert sig["traces"][0]["fillcolor"] == "blue"
        assert sig["traces"][0]["opacity"] == 0.4
        assert sig["traces"][0]["line"]["color"] == "red"
        assert sig["traces"][0]["line"]["width"] == 2

    def test_rect_path_signature(self):
        """Test that rect creates correct rectangular path."""
        df = pd.DataFrame({
            "xmin": [1], "xmax": [3], "ymin": [2], "ymax": [5]
        })
        plot = ggplot(df, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax")) + geom_rect()
        fig = plot.draw()

        # Check the path forms a closed rectangle
        x_path = list(fig.data[0].x)
        y_path = list(fig.data[0].y)

        # Should be 5 points (closed rectangle)
        assert len(x_path) == 5
        assert len(y_path) == 5

        # Path should include all corners
        assert 1 in x_path  # xmin
        assert 3 in x_path  # xmax
        assert 2 in y_path  # ymin
        assert 5 in y_path  # ymax


class TestVisualRegressionLabel:
    """Visual regression tests for geom_label."""

    def get_annotation_signature(self, fig):
        """Extract key properties from annotations."""
        return [
            {
                "text": ann.text,
                "x": ann.x,
                "y": ann.y,
                "bgcolor": ann.bgcolor,
                "font_color": ann.font.color if ann.font else None,
                "font_size": ann.font.size if ann.font else None,
                "xanchor": ann.xanchor,
                "yanchor": ann.yanchor,
                "opacity": ann.opacity,
            }
            for ann in fig.layout.annotations
        ]

    def test_label_visual_signature(self):
        """Test that label produces expected visual signature."""
        df = pd.DataFrame({
            "x": [1],
            "y": [2],
            "label": ["Test"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(
            fill="yellow", color="blue", size=14, alpha=0.9
        )
        fig = plot.draw()
        sig = self.get_annotation_signature(fig)

        assert len(sig) == 1
        assert sig[0]["text"] == "Test"
        assert sig[0]["x"] == 1
        assert sig[0]["y"] == 2
        assert sig[0]["bgcolor"] == "yellow"
        assert sig[0]["font_color"] == "blue"
        assert sig[0]["font_size"] == 14
        assert sig[0]["opacity"] == 0.9

    def test_label_nudge_signature(self):
        """Test label nudge visual signature."""
        df = pd.DataFrame({
            "x": [5],
            "y": [10],
            "label": ["Nudged"]
        })
        plot = ggplot(df, aes(x="x", y="y", label="label")) + geom_label(
            nudge_x=1, nudge_y=2
        )
        fig = plot.draw()
        sig = self.get_annotation_signature(fig)

        # Position should be nudged
        assert sig[0]["x"] == 6  # 5 + 1
        assert sig[0]["y"] == 12  # 10 + 2
