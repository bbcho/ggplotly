"""
Data normalization utilities for ggplotly.

This module provides automatic handling of DataFrame/Series indices as axis values.

Features:
    - Use x='index' to explicitly reference the DataFrame index
    - If x is not specified but y is, x defaults to the index
    - Series are automatically converted to DataFrames (values become y, index becomes x)
    - Named indices are used as axis labels

Examples:
    >>> import pandas as pd
    >>> from ggplotly import ggplot, aes, geom_point

    # Explicit index reference
    >>> df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
    >>> ggplot(df, aes(x='index', y='y')) + geom_point()

    # Auto-populate x from index
    >>> ggplot(df, aes(y='y')) + geom_point()

    # Series: y=values, x=index automatically
    >>> s = pd.Series([1, 2, 3], index=['a', 'b', 'c'], name='values')
    >>> ggplot(s) + geom_point()

    # Named index becomes axis label
    >>> df.index.name = 'time'
    >>> ggplot(df, aes(y='y')) + geom_point()  # x-axis labeled 'time'
"""
from __future__ import annotations

from typing import Any

import pandas as pd

# Reserved column name for index data
INDEX_COLUMN = '_ggplotly_index'


def normalize_data(data, mapping: dict[str, Any]) -> tuple[pd.DataFrame | None, dict[str, Any], str | None]:
    """
    Normalize input data and mapping for ggplotly consumption.

    This function handles:
        1. Converting Series to DataFrame (values as y column, index as x)
        2. Replacing 'index' keyword in mappings with the actual index column
        3. Auto-populating x aesthetic from index when only y is specified

    Parameters:
        data: DataFrame, Series, or None
        mapping: Dictionary of aesthetic mappings (e.g., {'x': 'col1', 'y': 'col2'})

    Returns:
        Tuple of (normalized_dataframe, updated_mapping, index_name):
            - normalized_dataframe: DataFrame with index converted to column if needed
            - updated_mapping: Mapping with 'index' replaced by INDEX_COLUMN
            - index_name: Original index name for axis labeling ('index' if unnamed)

    Raises:
        ValueError: If data has a MultiIndex (not supported)

    Examples:
        >>> df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
        >>> norm_df, norm_map, idx_name = normalize_data(df, {'y': 'y'})
        >>> norm_map['x']  # Auto-populated
        '_ggplotly_index'
    """
    if data is None:
        return None, mapping.copy() if mapping else {}, None

    mapping = mapping.copy() if mapping else {}
    index_name = None

    # Convert dict to DataFrame
    if isinstance(data, dict):
        data = pd.DataFrame(data)

    # Check for MultiIndex (not supported)
    if isinstance(data.index, pd.MultiIndex):
        raise ValueError(
            "MultiIndex is not supported for automatic index handling. "
            "Please reset the index first: df.reset_index()"
        )

    # Handle Series input
    if isinstance(data, pd.Series):
        data, mapping, index_name = _normalize_series(data, mapping)
    else:
        data = data.copy()
        # Get index name from DataFrame
        index_name = data.index.name if data.index.name else 'index'

    # Handle 'index' references in mapping
    data, mapping = _handle_index_references(data, mapping)

    # Auto-populate x if not specified and y is present
    data, mapping = _auto_populate_x(data, mapping)

    return data, mapping, index_name


def _normalize_series(series: pd.Series, mapping: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any], str]:
    """
    Convert a Series to a DataFrame for plotting.

    The Series is converted as follows:
        - Values become a column named after series.name (or 'value' if unnamed)
        - Index becomes a column named INDEX_COLUMN
        - If y is not in mapping, it's set to the values column
        - DatetimeIndex is preserved

    Parameters:
        series: The pandas Series to convert
        mapping: Current aesthetic mapping dictionary

    Returns:
        Tuple of (dataframe, updated_mapping, index_name)
    """
    series_name = series.name if series.name is not None else 'value'
    index_name = series.index.name if series.index.name else 'index'

    # Create DataFrame from Series
    df = pd.DataFrame({
        series_name: series.values,
        INDEX_COLUMN: series.index.values
    })

    # Preserve index dtype info for DatetimeIndex handling
    if isinstance(series.index, pd.DatetimeIndex):
        df[INDEX_COLUMN] = pd.to_datetime(df[INDEX_COLUMN])

    # Update mapping - set y to series values if not specified
    if 'y' not in mapping:
        mapping['y'] = series_name

    return df, mapping, index_name


def _handle_index_references(data: pd.DataFrame, mapping: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Handle 'index' keyword in aesthetic mappings.

    When any aesthetic value is the string 'index', this function:
        1. Adds the DataFrame's index as a new column (INDEX_COLUMN)
        2. Replaces 'index' in the mapping with INDEX_COLUMN
        3. Preserves DatetimeIndex dtype

    Parameters:
        data: DataFrame to modify
        mapping: Aesthetic mapping dictionary

    Returns:
        Tuple of (modified_dataframe, updated_mapping)
    """
    # Check if any aesthetic references 'index'
    needs_index_column = any(
        aes_value == 'index'
        for aes_value in mapping.values()
        if isinstance(aes_value, str)
    )

    if needs_index_column and INDEX_COLUMN not in data.columns:
        # Add index as column
        data[INDEX_COLUMN] = data.index.values

        # Preserve DatetimeIndex dtype
        if isinstance(data.index, pd.DatetimeIndex):
            data[INDEX_COLUMN] = pd.to_datetime(data[INDEX_COLUMN])

    # Replace 'index' references with INDEX_COLUMN
    for aes_name, aes_value in list(mapping.items()):
        if aes_value == 'index':
            mapping[aes_name] = INDEX_COLUMN

    return data, mapping


def _auto_populate_x(data: pd.DataFrame, mapping: dict[str, Any]) -> tuple[pd.DataFrame, dict[str, Any]]:
    """
    Auto-populate x aesthetic from index when not specified.

    If x is not in the mapping but y is specified, this function:
        1. Adds the DataFrame's index as INDEX_COLUMN (if not already present)
        2. Sets mapping['x'] to INDEX_COLUMN
        3. Preserves DatetimeIndex dtype

    This enables the common pattern of plotting a single column against its index
    without explicitly specifying x.

    Parameters:
        data: DataFrame to modify
        mapping: Aesthetic mapping dictionary

    Returns:
        Tuple of (modified_dataframe, updated_mapping)
    """
    if 'x' not in mapping and 'y' in mapping:
        # Add index column if not already present
        if INDEX_COLUMN not in data.columns:
            data[INDEX_COLUMN] = data.index.values

            # Preserve DatetimeIndex dtype
            if isinstance(data.index, pd.DatetimeIndex):
                data[INDEX_COLUMN] = pd.to_datetime(data[INDEX_COLUMN])

        mapping['x'] = INDEX_COLUMN

    return data, mapping


def get_index_label(index_name: str | None) -> str:
    """
    Get the appropriate label for the index axis.

    Parameters:
        index_name: The original index name from the DataFrame/Series

    Returns:
        The index name if it's a meaningful name, otherwise 'index'
    """
    return index_name if index_name and index_name != 'index' else 'index'
