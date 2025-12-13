"""Tests for automatic index handling in ggplotly."""
import os
import sys

import pandas as pd

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")

from ggplotly import aes, geom_line, geom_point, ggplot, labs
from ggplotly.data_utils import INDEX_COLUMN, normalize_data


class TestIndexKeyword:
    """Test x='index' keyword behavior."""

    def test_x_equals_index_uses_dataframe_index(self):
        """Test x='index' explicitly uses DataFrame index."""
        df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
        p = ggplot(df, aes(x='index', y='y')) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [10, 20, 30]

    def test_x_equals_index_with_string_index(self):
        """Test x='index' works with string index."""
        df = pd.DataFrame({'y': [1, 2, 3]}, index=['a', 'b', 'c'])
        p = ggplot(df, aes(x='index', y='y')) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == ['a', 'b', 'c']


class TestAutoPopulateX:
    """Test automatic x population from index."""

    def test_auto_x_when_only_y_specified(self):
        """Test x defaults to index when only y is specified."""
        df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
        p = ggplot(df, aes(y='y')) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [10, 20, 30]
        assert list(fig.data[0].y) == [1, 2, 3]

    def test_explicit_x_takes_precedence(self):
        """Test explicit x column overrides index default."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]}, index=[10, 20, 30])
        p = ggplot(df, aes(x='x', y='y')) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [1, 2, 3]
        assert list(fig.data[0].y) == [4, 5, 6]


class TestSeriesHandling:
    """Test Series input handling."""

    def test_series_default_mapping(self):
        """Test Series values become y, index becomes x."""
        s = pd.Series([1, 2, 3], index=[10, 20, 30], name='values')
        p = ggplot(s, aes()) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [10, 20, 30]
        assert list(fig.data[0].y) == [1, 2, 3]

    def test_series_without_name(self):
        """Test Series without name uses 'value' as column name."""
        s = pd.Series([1, 2, 3], index=[10, 20, 30])
        p = ggplot(s, aes()) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [10, 20, 30]
        assert list(fig.data[0].y) == [1, 2, 3]

    def test_series_with_explicit_y(self):
        """Test Series with explicit y matching series name."""
        s = pd.Series([1, 2, 3], index=[10, 20, 30], name='values')
        p = ggplot(s, aes(y='values')) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == [10, 20, 30]
        assert list(fig.data[0].y) == [1, 2, 3]

    def test_series_with_string_index(self):
        """Test Series with string index."""
        s = pd.Series([4, 5, 6], index=['a', 'b', 'c'], name='val')
        p = ggplot(s, aes()) + geom_point()
        fig = p.draw()
        assert list(fig.data[0].x) == ['a', 'b', 'c']
        assert list(fig.data[0].y) == [4, 5, 6]


class TestIndexLabeling:
    """Test axis labeling when using index."""

    def test_named_index_label(self):
        """Test named index provides x-axis label."""
        df = pd.DataFrame({'y': [1, 2, 3]})
        df.index.name = 'time'
        p = ggplot(df, aes(y='y')) + geom_point()
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'time'

    def test_unnamed_index_label(self):
        """Test unnamed index uses 'index' as label."""
        df = pd.DataFrame({'y': [1, 2, 3]})
        p = ggplot(df, aes(y='y')) + geom_point()
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'index'

    def test_labs_overrides_index_label(self):
        """Test that explicit labs() overrides index label."""
        df = pd.DataFrame({'y': [1, 2, 3]})
        df.index.name = 'time'
        p = ggplot(df, aes(y='y')) + geom_point() + labs(x='Custom X')
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'Custom X'

    def test_series_named_index_label(self):
        """Test Series with named index provides x-axis label."""
        s = pd.Series([1, 2, 3], name='values')
        s.index.name = 'category'
        p = ggplot(s, aes()) + geom_point()
        fig = p.draw()
        assert fig.layout.xaxis.title.text == 'category'


class TestDatetimeIndex:
    """Test DatetimeIndex handling."""

    def test_datetime_index(self):
        """Test DatetimeIndex is handled correctly."""
        dates = pd.date_range('2023-01-01', periods=3)
        df = pd.DataFrame({'y': [1, 2, 3]}, index=dates)
        p = ggplot(df, aes(y='y')) + geom_line()
        fig = p.draw()
        # Datetime values should be preserved
        assert pd.to_datetime(fig.data[0].x[0]) == dates[0]

    def test_datetime_index_with_series(self):
        """Test Series with DatetimeIndex."""
        dates = pd.date_range('2023-01-01', periods=3)
        s = pd.Series([1, 2, 3], index=dates, name='values')
        p = ggplot(s, aes()) + geom_line()
        fig = p.draw()
        assert pd.to_datetime(fig.data[0].x[0]) == dates[0]


class TestNormalizeDataFunction:
    """Test the normalize_data utility function directly."""

    def test_normalize_dataframe_with_index_keyword(self):
        """Test normalize_data handles 'index' keyword."""
        df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
        mapping = {'x': 'index', 'y': 'y'}
        norm_df, norm_mapping, index_name = normalize_data(df, mapping)

        assert INDEX_COLUMN in norm_df.columns
        assert norm_mapping['x'] == INDEX_COLUMN
        assert list(norm_df[INDEX_COLUMN]) == [10, 20, 30]

    def test_normalize_series(self):
        """Test normalize_data converts Series to DataFrame."""
        s = pd.Series([1, 2, 3], index=[10, 20, 30], name='values')
        mapping = {}
        norm_df, norm_mapping, index_name = normalize_data(s, mapping)

        assert isinstance(norm_df, pd.DataFrame)
        assert 'values' in norm_df.columns
        assert INDEX_COLUMN in norm_df.columns
        assert norm_mapping['y'] == 'values'

    def test_normalize_auto_populate_x(self):
        """Test normalize_data auto-populates x when y is specified."""
        df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
        mapping = {'y': 'y'}
        norm_df, norm_mapping, index_name = normalize_data(df, mapping)

        assert norm_mapping['x'] == INDEX_COLUMN
        assert INDEX_COLUMN in norm_df.columns

    def test_normalize_preserves_explicit_x(self):
        """Test normalize_data doesn't override explicit x."""
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]}, index=[10, 20, 30])
        mapping = {'x': 'x', 'y': 'y'}
        norm_df, norm_mapping, index_name = normalize_data(df, mapping)

        assert norm_mapping['x'] == 'x'

    def test_multiindex_raises_error(self):
        """Test that MultiIndex raises a helpful error."""
        arrays = [[1, 1, 2, 2], ['a', 'b', 'a', 'b']]
        index = pd.MultiIndex.from_arrays(arrays, names=['first', 'second'])
        df = pd.DataFrame({'y': [1, 2, 3, 4]}, index=index)
        mapping = {'y': 'y'}

        try:
            normalize_data(df, mapping)
            assert False, "Should have raised ValueError"
        except ValueError as e:
            assert "MultiIndex" in str(e)


class TestGeomLine:
    """Test index handling with geom_line."""

    def test_line_with_index(self):
        """Test geom_line works with index as x."""
        df = pd.DataFrame({'y': [1, 3, 2]}, index=[0, 1, 2])
        p = ggplot(df, aes(y='y')) + geom_line()
        fig = p.draw()
        assert list(fig.data[0].x) == [0, 1, 2]
        assert list(fig.data[0].y) == [1, 3, 2]
