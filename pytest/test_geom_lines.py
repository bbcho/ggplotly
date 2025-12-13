import numpy as np
import pandas as pd

from ggplotly import aes, geom_lines, ggplot


class TestGeomLines:
    """Tests for geom_lines."""

    def test_basic_usage(self):
        """Test simplest case: ggplot(df) + geom_lines()"""
        df = pd.DataFrame(np.random.randn(100, 10))
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        assert len(fig.data) == 1  # Single trace

    def test_with_index_as_x(self):
        """Test that index is used as x by default."""
        df = pd.DataFrame(np.random.randn(50, 5), index=range(0, 100, 2))
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        # Check x values include index values
        assert 0 in fig.data[0].x
        assert 98 in fig.data[0].x

    def test_explicit_x_column(self):
        """Test explicit x aesthetic."""
        df = pd.DataFrame({
            'time': np.linspace(0, 10, 100),
            'a': np.random.randn(100),
            'b': np.random.randn(100),
        })
        plot = ggplot(df) + geom_lines(aes(x='time'))
        fig = plot.draw()
        assert len(fig.data) == 1

    def test_showlegend_false_by_default(self):
        """Test legend is hidden by default."""
        df = pd.DataFrame(np.random.randn(10, 5))
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        assert fig.data[0].showlegend is False

    def test_showlegend_true(self):
        """Test legend can be enabled."""
        df = pd.DataFrame(np.random.randn(10, 5))
        plot = ggplot(df) + geom_lines(showlegend=True)
        fig = plot.draw()
        assert fig.data[0].showlegend is True

    def test_styling_params(self):
        """Test alpha, size, color params."""
        df = pd.DataFrame(np.random.randn(10, 5))
        plot = ggplot(df) + geom_lines(alpha=0.3, size=2, color='red')
        fig = plot.draw()
        assert fig.data[0].opacity == 0.3
        assert fig.data[0].line.width == 2
        assert fig.data[0].line.color == 'red'

    def test_select_columns(self):
        """Test selecting specific columns."""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 8, 9],
        })
        plot = ggplot(df) + geom_lines(columns=['a', 'b'])
        fig = plot.draw()
        # Should only include data from 2 columns
        # Each column has 3 points + 1 None separator = 4
        # 2 columns = 8 values, but we count non-None values = 6
        assert len([v for v in fig.data[0].y if v is not None]) == 6

    def test_large_matrix_performance(self):
        """Test with large matrix (performance check)."""
        # 1000 time points, 1000 series
        df = pd.DataFrame(np.random.randn(1000, 1000))
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        # Should still be single trace
        assert len(fig.data) == 1

    def test_non_numeric_columns_excluded(self):
        """Test that non-numeric columns are automatically excluded."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'y': [4, 5, 6],
            'label': ['a', 'b', 'c'],  # Non-numeric
        })
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        # Should only plot x and y, not label
        assert len([v for v in fig.data[0].y if v is not None]) == 6

    def test_datetime_index(self):
        """Test with DatetimeIndex as x."""
        dates = pd.date_range('2024-01-01', periods=30)
        df = pd.DataFrame(np.random.randn(30, 5), index=dates)
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        assert len(fig.data) == 1
        # X values should be from datetime index (converted to nanoseconds)
        first_timestamp_ns = pd.Timestamp('2024-01-01').value
        assert first_timestamp_ns in fig.data[0].x

    def test_empty_columns_list(self):
        """Test with empty columns parameter."""
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        plot = ggplot(df) + geom_lines(columns=[])
        fig = plot.draw()
        # Should have trace but no data
        assert len(fig.data) == 1
        assert len([v for v in fig.data[0].y if v is not None]) == 0

    def test_missing_column_ignored(self):
        """Test that missing columns in columns param are ignored."""
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        plot = ggplot(df) + geom_lines(columns=['a', 'nonexistent'])
        fig = plot.draw()
        # Should only plot 'a' column
        assert len([v for v in fig.data[0].y if v is not None]) == 3

    def test_custom_name(self):
        """Test custom trace name."""
        df = pd.DataFrame(np.random.randn(10, 3))
        plot = ggplot(df) + geom_lines(name='My Series')
        fig = plot.draw()
        assert fig.data[0].name == 'My Series'

    def test_x_excluded_from_y_columns(self):
        """Test that x column is not plotted as y."""
        df = pd.DataFrame({
            'x': [1, 2, 3],
            'a': [4, 5, 6],
            'b': [7, 8, 9],
        })
        plot = ggplot(df) + geom_lines(aes(x='x'))
        fig = plot.draw()
        # Should plot a and b (6 values), not x
        assert len([v for v in fig.data[0].y if v is not None]) == 6

    def test_hover_disabled(self):
        """Test that hover is disabled for performance."""
        df = pd.DataFrame(np.random.randn(10, 5))
        plot = ggplot(df) + geom_lines()
        fig = plot.draw()
        assert fig.data[0].hoverinfo == 'skip'

    def test_with_facets(self):
        """Test geom_lines works with faceting."""
        df = pd.DataFrame({
            'group': ['A'] * 10 + ['B'] * 10,
            'x': list(range(10)) * 2,
            'y1': np.random.randn(20),
            'y2': np.random.randn(20),
        })
        # Note: faceting with geom_lines requires columns param
        # since faceted data won't have all numeric columns
        from ggplotly import facet_wrap
        plot = ggplot(df) + geom_lines(aes(x='x'), columns=['y1', 'y2']) + facet_wrap('group')
        fig = plot.draw()
        # Should have 2 subplots
        assert len(fig.data) >= 2

    def test_multicolor_creates_multiple_traces(self):
        """Test multicolor=True creates one trace per series."""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 8, 9],
        })
        plot = ggplot(df) + geom_lines(multicolor=True)
        fig = plot.draw()
        # Should have 3 traces (one per column)
        assert len(fig.data) == 3

    def test_multicolor_different_colors(self):
        """Test multicolor assigns different colors to each series."""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
            'c': [7, 8, 9],
        })
        plot = ggplot(df) + geom_lines(multicolor=True)
        fig = plot.draw()
        colors = [trace.line.color for trace in fig.data]
        # All colors should be different
        assert len(set(colors)) == 3

    def test_multicolor_with_palette(self):
        """Test multicolor with custom palette."""
        df = pd.DataFrame(np.random.randn(10, 5))
        plot = ggplot(df) + geom_lines(multicolor=True, palette='Viridis')
        fig = plot.draw()
        assert len(fig.data) == 5

    def test_multicolor_with_custom_color_list(self):
        """Test multicolor with a list of colors."""
        df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': [4, 5, 6],
        })
        custom_colors = ['red', 'blue']
        plot = ggplot(df) + geom_lines(multicolor=True, palette=custom_colors)
        fig = plot.draw()
        assert fig.data[0].line.color == 'red'
        assert fig.data[1].line.color == 'blue'

    def test_multicolor_trace_names(self):
        """Test multicolor traces have column names."""
        df = pd.DataFrame({
            'series_a': [1, 2, 3],
            'series_b': [4, 5, 6],
        })
        plot = ggplot(df) + geom_lines(multicolor=True)
        fig = plot.draw()
        names = [trace.name for trace in fig.data]
        assert 'series_a' in names
        assert 'series_b' in names
