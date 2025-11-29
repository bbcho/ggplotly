"""
Tests for ggplotly annotate function.
"""
import pytest
import pandas as pd
import numpy as np
from plotly.graph_objects import Figure

import sys
sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import (
    ggplot, aes,
    geom_point, geom_line, geom_bar, geom_col,
    annotate, labs
)


@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': range(10),
        'y': np.random.randn(10) * 10 + 50,
        'group': ['A'] * 5 + ['B'] * 5
    })


class TestAnnotateText:
    """Tests for text annotations."""

    def test_basic_text(self, sample_data):
        """Test basic text annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Test Label'))
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have at least one annotation
        assert len(fig.layout.annotations) >= 1

    def test_text_with_color(self, sample_data):
        """Test text annotation with color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Red Text', color='red'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_text_with_size(self, sample_data):
        """Test text annotation with custom size."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Large Text', size=20))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_text_with_hjust(self, sample_data):
        """Test text annotation with horizontal justification."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Left Aligned', hjust=0))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_text_with_vjust(self, sample_data):
        """Test text annotation with vertical justification."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Top Aligned', vjust=1))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_text_with_alpha(self, sample_data):
        """Test text annotation with transparency."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Transparent', alpha=0.5))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_multiple_text_annotations(self, sample_data):
        """Test multiple text annotations."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=2, y=45, label='Point A')
             + annotate('text', x=7, y=55, label='Point B'))
        fig = p.draw()
        assert isinstance(fig, Figure)
        assert len(fig.layout.annotations) >= 2


class TestAnnotateLabel:
    """Tests for label annotations (text with background box)."""

    def test_basic_label(self, sample_data):
        """Test basic label annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('label', x=5, y=50, label='Boxed Label'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_label_with_fill(self, sample_data):
        """Test label with background fill color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('label', x=5, y=50, label='Yellow Box', fill='yellow'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_label_with_color(self, sample_data):
        """Test label with border color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('label', x=5, y=50, label='Blue Border', color='blue'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateSegment:
    """Tests for segment annotations."""

    def test_basic_segment(self, sample_data):
        """Test basic segment (line) annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('segment', x=2, y=40, xend=7, yend=60))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_segment_with_arrow(self, sample_data):
        """Test segment with arrow."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('segment', x=2, y=40, xend=7, yend=60, arrow=True))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_segment_with_color(self, sample_data):
        """Test segment with custom color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('segment', x=2, y=40, xend=7, yend=60, color='red'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_segment_with_size(self, sample_data):
        """Test segment with custom line width."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('segment', x=2, y=40, xend=7, yend=60, size=3))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateRect:
    """Tests for rectangle annotations."""

    def test_basic_rect(self, sample_data):
        """Test basic rectangle annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('rect', xmin=3, xmax=7, ymin=45, ymax=55))
        fig = p.draw()
        assert isinstance(fig, Figure)
        # Should have at least one shape
        assert len(fig.layout.shapes) >= 1

    def test_rect_with_fill(self, sample_data):
        """Test rectangle with fill color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('rect', xmin=3, xmax=7, ymin=45, ymax=55, fill='yellow'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_rect_with_alpha(self, sample_data):
        """Test rectangle with transparency."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('rect', xmin=3, xmax=7, ymin=45, ymax=55, fill='blue', alpha=0.2))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_rect_with_border(self, sample_data):
        """Test rectangle with border color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('rect', xmin=3, xmax=7, ymin=45, ymax=55, color='red', fill='yellow'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotatePoint:
    """Tests for point annotations."""

    def test_basic_point(self, sample_data):
        """Test basic point annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('point', x=5, y=50))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_point_with_size(self, sample_data):
        """Test point with custom size."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('point', x=5, y=50, size=20))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_point_with_color(self, sample_data):
        """Test point with color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('point', x=5, y=50, color='red', size=15))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateCurve:
    """Tests for curved annotations."""

    def test_basic_curve(self, sample_data):
        """Test basic curve annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('curve', x=2, y=40, xend=7, yend=60))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_curve_with_arrow(self, sample_data):
        """Test curve with arrow."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('curve', x=2, y=40, xend=7, yend=60, arrow=True))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateLines:
    """Tests for horizontal and vertical line annotations."""

    def test_hline(self, sample_data):
        """Test horizontal line annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('hline', y=50))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_hline_with_color(self, sample_data):
        """Test horizontal line with color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('hline', y=50, color='red'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_vline(self, sample_data):
        """Test vertical line annotation."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('vline', x=5))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_vline_with_color(self, sample_data):
        """Test vertical line with color."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('vline', x=5, color='blue'))
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateCombinations:
    """Tests for combining multiple annotation types."""

    def test_multiple_annotation_types(self, sample_data):
        """Test combining different annotation types."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=60, label='Peak')
             + annotate('rect', xmin=4, xmax=6, ymin=55, ymax=65, fill='yellow', alpha=0.3)
             + annotate('segment', x=0, y=50, xend=9, yend=50, color='gray'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_annotations_with_labs(self, sample_data):
        """Test annotations combined with labels."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='Important')
             + labs(title='Annotated Plot', x='X Values', y='Y Values'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_many_annotations(self, sample_data):
        """Test plot with many annotations."""
        p = ggplot(sample_data, aes(x='x', y='y')) + geom_point()
        for i in range(5):
            p = p + annotate('point', x=i*2, y=50, color='red', size=8)
            p = p + annotate('text', x=i*2, y=45, label=f'P{i}')
        fig = p.draw()
        assert isinstance(fig, Figure)


class TestAnnotateEdgeCases:
    """Tests for edge cases in annotations."""

    def test_annotate_empty_label(self, sample_data):
        """Test text annotation with empty label."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label=''))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_annotate_special_characters(self, sample_data):
        """Test text annotation with special characters."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=5, y=50, label='<Special> & "chars"'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_annotate_at_data_bounds(self, sample_data):
        """Test annotations at data boundaries."""
        x_min, x_max = sample_data['x'].min(), sample_data['x'].max()
        y_min, y_max = sample_data['y'].min(), sample_data['y'].max()

        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=x_min, y=y_min, label='Min')
             + annotate('text', x=x_max, y=y_max, label='Max'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_annotate_outside_data_range(self, sample_data):
        """Test annotations outside the data range."""
        p = (ggplot(sample_data, aes(x='x', y='y'))
             + geom_point()
             + annotate('text', x=-5, y=100, label='Outside'))
        fig = p.draw()
        assert isinstance(fig, Figure)

    def test_invalid_geom_type(self, sample_data):
        """Test that invalid annotation type raises error."""
        with pytest.raises(ValueError):
            p = (ggplot(sample_data, aes(x='x', y='y'))
                 + geom_point()
                 + annotate('invalid_type', x=5, y=50))
            fig = p.draw()
