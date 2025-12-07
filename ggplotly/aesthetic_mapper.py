# aesthetic_mapper.py
"""
Centralized aesthetic mapping system for ggplotly.

This module provides a clean interface for resolving aesthetic mappings
and determining whether aesthetic values are column references or literal values.
"""

import pandas as pd
import plotly.express as px
from functools import lru_cache
from typing import Any, Dict, Optional, Union, Tuple

from .constants import SHAPE_PALETTE, get_color_palette as _get_color_palette
from .exceptions import ColumnNotFoundError, InvalidColorError


# Module-level cache for color conversions (expensive Plotly operations)
@lru_cache(maxsize=512)
def _cached_color_to_rgba(color: str, alpha: float) -> str:
    """
    Convert color to RGBA string with alpha (cached).

    This is a module-level cached function to avoid repeated expensive
    color conversions across multiple AestheticMapper instances.

    Parameters:
        color: Color as hex (#RRGGBB) or named color
        alpha: Alpha value (0-1)

    Returns:
        RGBA string like 'rgba(255, 0, 0, 0.5)'
    """
    import plotly.colors as pc

    # Handle hex colors
    if color.startswith('#'):
        color_hex = color.lstrip('#')
        if len(color_hex) == 6:
            r, g, b = int(color_hex[0:2], 16), int(color_hex[2:4], 16), int(color_hex[4:6], 16)
            return f'rgba({r},{g},{b},{alpha})'

    # Handle existing rgba/rgb strings
    if color.startswith('rgba('):
        # Already has alpha, replace it
        parts = color[5:-1].split(',')
        if len(parts) >= 3:
            return f'rgba({parts[0]},{parts[1]},{parts[2]},{alpha})'
    if color.startswith('rgb('):
        rgb_values = color[4:-1]
        return f'rgba({rgb_values},{alpha})'

    # Try to use plotly's color conversion
    try:
        rgb_str = pc.convert_colors_to_same_type([color], colortype='rgb')[0][0]
        if rgb_str.startswith('rgb('):
            rgb_values = rgb_str[4:-1]
            return f'rgba({rgb_values},{alpha})'
    except Exception:
        pass

    # Fallback: common color names
    common_colors = {
        'red': (255, 0, 0),
        'blue': (0, 0, 255),
        'green': (0, 128, 0),
        'yellow': (255, 255, 0),
        'orange': (255, 165, 0),
        'purple': (128, 0, 128),
        'black': (0, 0, 0),
        'white': (255, 255, 255),
        'gray': (128, 128, 128),
        'grey': (128, 128, 128),
        'steelblue': (70, 130, 180),
        'forestgreen': (34, 139, 34),
        'coral': (255, 127, 80),
        'tomato': (255, 99, 71),
        'gold': (255, 215, 0),
        'navy': (0, 0, 128),
        'teal': (0, 128, 128),
        'maroon': (128, 0, 0),
        'olive': (128, 128, 0),
        'aqua': (0, 255, 255),
        'fuchsia': (255, 0, 255),
        'silver': (192, 192, 192),
        'lime': (0, 255, 0),
    }

    if color.lower() in common_colors:
        r, g, b = common_colors[color.lower()]
        return f'rgba({r},{g},{b},{alpha})'

    # Ultimate fallback - use default plotly blue
    return f'rgba(31, 119, 180, {alpha})'


class AestheticMapper:
    """
    Handles the resolution and mapping of aesthetics to visual properties.

    This class distinguishes between:
    - Column references (strings that map to DataFrame columns)
    - Literal values (colors, sizes, etc. to be used directly)
    """

    def __init__(self, data: pd.DataFrame, mapping: Dict[str, Any], params: Dict[str, Any], theme=None,
                 global_color_map: Dict[Any, str] = None, global_shape_map: Dict[Any, str] = None,
                 validate: bool = True):
        """
        Initialize the aesthetic mapper.

        Parameters:
            data: The DataFrame containing the plot data
            mapping: Dictionary of aesthetic mappings from aes()
            params: Dictionary of parameters passed to the geom
            theme: Optional theme object for default color palettes
            global_color_map: Optional pre-computed color map (for faceting)
            global_shape_map: Optional pre-computed shape map (for faceting)
            validate: If True, validate column references and raise helpful errors
        """
        self.data = data
        self.mapping = mapping
        self.params = params
        self.theme = theme
        self.global_color_map = global_color_map
        self.global_shape_map = global_shape_map
        self.validate = validate

        # Cache column names as frozenset for O(1) lookups
        self._column_set = frozenset(data.columns) if data is not None else frozenset()

        # Instance-level cache for style properties
        self._style_props_cache = None

    def get_color_palette(self) -> list:
        """Get the color palette from theme or use default."""
        return _get_color_palette(self.theme)

    def is_column_reference(self, aesthetic: str, value: Any) -> bool:
        """
        Determine if an aesthetic value refers to a column in the data.

        Parameters:
            aesthetic: Name of the aesthetic (e.g., 'color', 'fill')
            value: The value to check

        Returns:
            True if value is a column reference, False otherwise
        """
        # None is not a column reference
        if value is None:
            return False

        # Must be a string to be a column name
        if not isinstance(value, str):
            return False

        # O(1) lookup using cached frozenset
        return value in self._column_set

    def validate_column(self, column: str, aesthetic: str = None) -> None:
        """
        Validate that a column exists in the data, raising a helpful error if not.

        Parameters:
            column: The column name to validate
            aesthetic: Optional aesthetic name for better error messages

        Raises:
            ColumnNotFoundError: If the column doesn't exist, with suggestions
        """
        if column not in self._column_set:
            raise ColumnNotFoundError(column, list(self.data.columns), aesthetic)
    
    def resolve_aesthetic(self, aesthetic: str) -> Tuple[Any, Optional[pd.Series], Optional[Dict]]:
        """
        Resolve an aesthetic from both mapping and params.

        Returns a tuple of:
        - The aesthetic value (column name or literal)
        - Series of data if it's a column reference, None otherwise
        - Dictionary mapping unique values to colors (for categorical), None otherwise

        Parameters:
            aesthetic: Name of the aesthetic to resolve (e.g., 'color', 'fill', 'size')
        """
        # First check mapping (aes), then params
        value = self.mapping.get(aesthetic) or self.params.get(aesthetic)

        if value is None:
            return None, None, None

        # Check if this is a column reference
        if self.is_column_reference(aesthetic, value):
            series = self.data[value]
            # Use global color map if provided (for faceting), otherwise create from local data
            if aesthetic in ('color', 'fill') and self.global_color_map is not None:
                color_map = self.global_color_map
            else:
                color_map = self._create_color_map(series)
            return value, series, color_map
        else:
            # It's a literal value
            return value, None, None
    
    def _is_continuous(self, series: pd.Series) -> bool:
        """
        Determine if a series should be treated as continuous (numeric) or categorical.

        Parameters:
            series: The data series to check

        Returns:
            True if the series should use continuous color mapping
        """
        # Must be numeric dtype
        if not pd.api.types.is_numeric_dtype(series):
            return False

        # If it has many unique values relative to its size, treat as continuous
        # This helps distinguish between e.g. [1, 2, 3] (categorical) and [0.1, 0.2, ..., 0.99] (continuous)
        n_unique = series.nunique()
        n_total = len(series)

        # Heuristics:
        # - More than 20 unique values is likely continuous
        # - More than 50% unique values is likely continuous (for smaller datasets)
        # - Float dtype with non-integer values is likely continuous
        if n_unique > 20:
            return True
        if n_total > 0 and n_unique / n_total > 0.5:
            return True
        if pd.api.types.is_float_dtype(series):
            # Check if values are actually floats (not integers stored as float)
            if not series.dropna().apply(lambda x: float(x).is_integer()).all():
                return True

        return False

    def _create_color_map(self, series: pd.Series) -> Dict[Any, str]:
        """
        Create a mapping from unique values to colors.

        Parameters:
            series: The data series to map

        Returns:
            Dictionary mapping each unique value to a color, or None for continuous data
        """
        # Check if this should be treated as continuous
        if self._is_continuous(series):
            # Return None to signal continuous color mapping
            return None

        palette = self.get_color_palette()
        unique_values = series.dropna().unique()

        color_map = {}
        for i, val in enumerate(unique_values):
            color_map[val] = palette[i % len(palette)]

        return color_map

    def _create_shape_map(self, series: pd.Series) -> Dict[Any, str]:
        """
        Create a mapping from unique values to marker shapes.

        Parameters:
            series: The data series to map

        Returns:
            Dictionary mapping each unique value to a Plotly marker symbol
        """
        unique_values = series.dropna().unique()

        shape_map = {}
        for i, val in enumerate(unique_values):
            shape_map[val] = SHAPE_PALETTE[i % len(SHAPE_PALETTE)]

        return shape_map
    
    def get_style_properties(self) -> Dict[str, Any]:
        """
        Extract all relevant style properties for a geom.

        Results are cached for the lifetime of this AestheticMapper instance.

        Returns a dictionary with resolved properties:
        - color: The color aesthetic (column name or literal)
        - color_series: Series if color is a column, None otherwise
        - color_map: Dict mapping values to colors, None otherwise
        - fill: The fill aesthetic
        - fill_series: Series if fill is a column, None otherwise
        - fill_map: Dict mapping values to colors, None otherwise
        - size: The size value (literal or series if mapped to column)
        - size_series: Series if size is a column, None otherwise
        - shape: The shape aesthetic (column name or literal Plotly symbol)
        - shape_series: Series if shape is a column, None otherwise
        - shape_map: Dict mapping values to Plotly symbols, None otherwise
        - alpha: The transparency value
        - linetype: The line type
        - group: The grouping variable
        - group_series: Series if group is a column, None otherwise
        """
        # Return cached result if available
        if self._style_props_cache is not None:
            return self._style_props_cache

        # Resolve each aesthetic
        color, color_series, color_map = self.resolve_aesthetic('color')
        fill, fill_series, fill_map = self.resolve_aesthetic('fill')
        size, size_series, _ = self.resolve_aesthetic('size')
        alpha = self.params.get('alpha', 1.0)
        linetype = self.params.get('linetype', 'solid')

        # Resolve shape aesthetic
        shape_value = self.mapping.get('shape') or self.params.get('shape')
        shape_series = None
        shape_map = None
        if shape_value is not None and self.is_column_reference('shape', shape_value):
            shape_series = self.data[shape_value]
            # Use global shape map if provided (for faceting), otherwise create from local data
            if self.global_shape_map is not None:
                shape_map = self.global_shape_map
            else:
                shape_map = self._create_shape_map(shape_series)
            shape = shape_value  # column name
        else:
            shape = shape_value  # literal value (Plotly symbol name) or None

        # Group is special - it's always a column reference if provided
        group = self.mapping.get('group')
        group_series = self.data[group] if group and group in self.data.columns else None

        # Get default color if neither color nor fill is mapped
        default_color = self.params.get('color', '#1f77b4')

        # Note: If both color and fill are mapped to columns, priority is given to:
        # - 'fill' for fill-based geoms (area, ribbon, etc.)
        # - 'color' for line/point-based geoms
        # Individual geoms can handle this as needed

        # Determine if color/fill is continuous (color_map will be None)
        color_is_continuous = color_series is not None and color_map is None
        fill_is_continuous = fill_series is not None and fill_map is None

        result = {
            'color': color,
            'color_series': color_series,
            'color_map': color_map,
            'color_is_continuous': color_is_continuous,
            'fill': fill,
            'fill_series': fill_series,
            'fill_map': fill_map,
            'fill_is_continuous': fill_is_continuous,
            'size': size if size is not None else 10,
            'size_series': size_series,
            'shape': shape,
            'shape_series': shape_series,
            'shape_map': shape_map,
            'alpha': alpha,
            'linetype': linetype,
            'group': group,
            'group_series': group_series,
            'default_color': default_color,
        }

        # Cache the result for subsequent calls
        self._style_props_cache = result
        return result
    
    def get_color_for_value(self, value_key: Any, style_props: Dict[str, Any] = None,
                            prefer_fill: bool = False) -> str:
        """
        Get the resolved color for a specific value/group.

        This is the unified method for color resolution across all geoms.

        Parameters:
            value_key: The group/category value to get color for
            style_props: Style properties dict (if None, will call get_style_properties())
            prefer_fill: If True, prefer fill over color when both are mapped

        Returns:
            Color string (hex or named color)
        """
        if style_props is None:
            style_props = self.get_style_properties()

        # Determine which aesthetic to use for color
        if prefer_fill:
            # Prefer fill for area/ribbon/bar geoms
            if style_props['fill_series'] is not None:
                return style_props['fill_map'].get(value_key, style_props['default_color'])
            elif style_props['color_series'] is not None:
                return style_props['color_map'].get(value_key, style_props['default_color'])
            elif style_props['fill'] is not None:
                return style_props['fill']
            elif style_props['color'] is not None:
                return style_props['color']
        else:
            # Prefer color for line/point geoms
            if style_props['color_series'] is not None:
                return style_props['color_map'].get(value_key, style_props['default_color'])
            elif style_props['fill_series'] is not None:
                return style_props['fill_map'].get(value_key, style_props['default_color'])
            elif style_props['color'] is not None:
                return style_props['color']
            elif style_props['fill'] is not None:
                return style_props['fill']

        return style_props['default_color']

    def get_color_with_alpha(self, value_key: Any = None, style_props: Dict[str, Any] = None,
                            prefer_fill: bool = False, alpha_override: float = None) -> str:
        """
        Get color with alpha channel as RGBA string.

        Parameters:
            value_key: The group/category value to get color for (None for literal colors)
            style_props: Style properties dict (if None, will call get_style_properties())
            prefer_fill: If True, prefer fill over color when both are mapped
            alpha_override: Override alpha value (if None, uses style_props['alpha'])

        Returns:
            RGBA color string like 'rgba(255, 0, 0, 0.5)'
        """
        if style_props is None:
            style_props = self.get_style_properties()

        if value_key is not None:
            color = self.get_color_for_value(value_key, style_props, prefer_fill)
        else:
            # No specific value - use literal or default
            if prefer_fill:
                color = style_props.get('fill') or style_props.get('color') or style_props['default_color']
            else:
                color = style_props.get('color') or style_props.get('fill') or style_props['default_color']

        alpha = alpha_override if alpha_override is not None else style_props['alpha']

        return self._color_to_rgba(color, alpha)

    def _color_to_rgba(self, color: str, alpha: float) -> str:
        """
        Convert color to RGBA string with alpha.

        Uses module-level LRU cache for performance.

        Parameters:
            color: Color as hex (#RRGGBB) or named color
            alpha: Alpha value (0-1)

        Returns:
            RGBA string like 'rgba(255, 0, 0, 0.5)'
        """
        return _cached_color_to_rgba(color, alpha)

    def apply_style_to_trace(self, trace_kwargs: dict, style_props: dict,
                            target_mapping: dict, value_key: Optional[Any] = None) -> dict:
        """
        Apply style properties to a trace dictionary based on target mapping.

        Parameters:
            trace_kwargs: Dictionary of trace keyword arguments to update
            style_props: Style properties from get_style_properties()
            target_mapping: Maps aesthetic names to trace property paths
                           e.g., {'color': 'marker_color', 'size': 'marker_size'}
            value_key: If provided, use this key to look up color/fill from color_map

        Returns:
            Updated trace_kwargs dictionary
        """
        # Determine which color/fill to use
        if value_key is not None:
            # We're drawing a specific group - look up its color
            if style_props['color_series'] is not None:
                color_value = style_props['color_map'].get(value_key)
            elif style_props['fill_series'] is not None:
                color_value = style_props['fill_map'].get(value_key)
            else:
                color_value = style_props.get('color') or style_props.get('fill') or style_props['default_color']
        else:
            # Use literal color/fill or default
            color_value = style_props.get('color') or style_props.get('fill') or style_props['default_color']

        # Apply to trace based on target mapping
        for aesthetic, target_path in target_mapping.items():
            if aesthetic == 'color' or aesthetic == 'fill':
                trace_kwargs[target_path] = color_value
            elif aesthetic == 'size':
                trace_kwargs[target_path] = style_props['size']
            elif aesthetic == 'alpha':
                trace_kwargs['opacity'] = style_props['alpha']

        return trace_kwargs


def create_aesthetic_mapper(data: pd.DataFrame, mapping: Dict[str, Any], 
                           params: Dict[str, Any], theme=None) -> AestheticMapper:
    """
    Factory function to create an AestheticMapper instance.
    
    Parameters:
        data: The DataFrame containing the plot data
        mapping: Dictionary of aesthetic mappings from aes()
        params: Dictionary of parameters passed to the geom
        theme: Optional theme object
        
    Returns:
        AestheticMapper instance
    """
    return AestheticMapper(data, mapping, params, theme)
