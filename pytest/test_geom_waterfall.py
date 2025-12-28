import pandas as pd

import pytest
from ggplotly import aes, geom_waterfall, ggplot


class TestGeomWaterfall:
    """Tests for geom_waterfall."""

    def test_basic_waterfall(self):
        """Test basic waterfall chart returns correct trace type and values."""
        df = pd.DataFrame({
            'category': ['Q1', 'Q2', 'Q3', 'Q4'],
            'value': [100, 50, -30, 20]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        # Verify trace type
        assert len(fig.data) == 1
        assert fig.data[0].type == 'waterfall'

        # Verify x and y values are correctly passed
        assert list(fig.data[0].x) == ['Q1', 'Q2', 'Q3', 'Q4']
        assert list(fig.data[0].y) == [100, 50, -30, 20]

    def test_waterfall_with_measures(self):
        """Test waterfall with explicit measure types."""
        df = pd.DataFrame({
            'category': ['Start', 'Sales', 'Returns', 'End'],
            'value': [100, 50, -20, 0],
            'measure': ['absolute', 'relative', 'relative', 'total']
        })

        plot = (ggplot(df, aes(x='category', y='value', measure='measure'))
                + geom_waterfall())
        fig = plot.draw()

        assert fig.data[0].type == 'waterfall'
        assert fig.data[0].measure == ('absolute', 'relative', 'relative', 'total')

        # Verify values
        assert list(fig.data[0].y) == [100, 50, -20, 0]

    def test_financial_waterfall(self):
        """Test financial statement waterfall with mixed measure types."""
        df = pd.DataFrame({
            'item': ['Revenue', 'COGS', 'Gross Profit', 'OpEx', 'Net Income'],
            'amount': [1000, -400, 0, -200, 0],
            'type': ['absolute', 'relative', 'total', 'relative', 'total']
        })

        plot = (ggplot(df, aes(x='item', y='amount', measure='type'))
                + geom_waterfall())
        fig = plot.draw()

        assert fig.data[0].type == 'waterfall'

        # Verify items and values
        assert list(fig.data[0].x) == ['Revenue', 'COGS', 'Gross Profit', 'OpEx', 'Net Income']
        assert list(fig.data[0].y) == [1000, -400, 0, -200, 0]
        assert fig.data[0].measure == ('absolute', 'relative', 'total', 'relative', 'total')

    def test_custom_colors(self):
        """Test custom bar colors are applied correctly."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(
                    increasing_color='blue',
                    decreasing_color='orange',
                    total_color='purple'
                ))
        fig = plot.draw()

        assert fig.data[0].increasing.marker.color == 'blue'
        assert fig.data[0].decreasing.marker.color == 'orange'
        assert fig.data[0].totals.marker.color == 'purple'

    def test_default_colors(self):
        """Test default bar colors are applied."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        # Default colors
        assert fig.data[0].increasing.marker.color == '#2ca02c'  # Green
        assert fig.data[0].decreasing.marker.color == '#d62728'  # Red
        assert fig.data[0].totals.marker.color == '#1f77b4'  # Blue

    def test_connector_options(self):
        """Test connector customization."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(
                    connector_color='red',
                    connector_width=2,
                    connector_visible=True
                ))
        fig = plot.draw()

        assert fig.data[0].connector.visible is True
        assert fig.data[0].connector.line.color == 'red'
        assert fig.data[0].connector.line.width == 2

    def test_hide_connectors(self):
        """Test hiding connectors."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(connector_visible=False))
        fig = plot.draw()

        assert fig.data[0].connector.visible is False

    def test_horizontal_orientation(self):
        """Test horizontal orientation is set correctly."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(orientation='h'))
        fig = plot.draw()

        assert fig.data[0].orientation == 'h'

    def test_vertical_orientation_default(self):
        """Test vertical orientation is the default."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        assert fig.data[0].orientation == 'v'

    def test_text_position(self):
        """Test text position options."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(text_position='inside'))
        fig = plot.draw()

        assert fig.data[0].textposition == 'inside'

    def test_text_position_outside_default(self):
        """Test default text position is outside."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        assert fig.data[0].textposition == 'outside'

    def test_text_format(self):
        """Test text formatting with decimal precision."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100.5, 50.25, -30.75]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall(text_format='.1f'))
        fig = plot.draw()

        # Check text is formatted correctly
        text_values = list(fig.data[0].text)
        assert '100.5' in text_values
        assert '50.2' in text_values or '50.3' in text_values  # Rounding
        assert '-30.8' in text_values or '-30.7' in text_values  # Rounding

    def test_text_labels_present(self):
        """Test that text labels are generated from values."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        # Text should be string representations of values
        text_values = list(fig.data[0].text)
        assert '100' in text_values
        assert '50' in text_values
        assert '-30' in text_values

    def test_missing_y_aesthetic_raises(self):
        """Test that missing y aesthetic raises RequiredAestheticError."""
        from ggplotly.exceptions import RequiredAestheticError

        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        # Missing y
        plot = (ggplot(df, aes(x='category'))
                + geom_waterfall())
        with pytest.raises(RequiredAestheticError, match="y"):
            plot.draw()

    def test_missing_x_aesthetic_raises(self):
        """Test that missing x aesthetic raises RequiredAestheticError."""
        from ggplotly.exceptions import RequiredAestheticError

        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        # Create geom with only y mapping (no x)
        plot = (ggplot(df) + geom_waterfall(mapping=aes(y='value')))
        with pytest.raises(RequiredAestheticError, match="x"):
            plot.draw()

    def test_missing_column_raises(self):
        """Test that missing data column raises ColumnNotFoundError."""
        from ggplotly.exceptions import ColumnNotFoundError

        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
        })

        plot = (ggplot(df, aes(x='category', y='nonexistent'))
                + geom_waterfall())
        with pytest.raises(ColumnNotFoundError, match="not found"):
            plot.draw()

    def test_default_measures(self):
        """Test that default measures are all relative when measure not provided."""
        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [100, 50, -30]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        # All should be relative by default
        assert fig.data[0].measure == ('relative', 'relative', 'relative')

    def test_positive_negative_values(self):
        """Test waterfall correctly handles positive and negative values."""
        df = pd.DataFrame({
            'category': ['Start', 'Gain', 'Loss', 'Gain2'],
            'value': [100, 50, -75, 25]
        })

        plot = (ggplot(df, aes(x='category', y='value'))
                + geom_waterfall())
        fig = plot.draw()

        # Verify all values are passed correctly
        assert list(fig.data[0].y) == [100, 50, -75, 25]
        assert fig.data[0].type == 'waterfall'
