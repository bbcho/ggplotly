# aesthetic_mapper.py
"""
Centralized aesthetic mapping system for ggplotly.

This module provides a clean interface for resolving aesthetic mappings
and determining whether aesthetic values are column references or literal values.
"""

import pandas as pd
import plotly.express as px
from typing import Any, Dict, Optional, Union, Tuple


# Default shape palette matching ggplot2's defaults
# Maps to Plotly marker symbols
# See: https://plotly.com/python/marker-style/
SHAPE_PALETTE = [
    'circle',         # 0 - ggplot2 default
    'triangle-up',    # 1
    'square',         # 2
    'cross',          # 3 (plus in ggplot2)
    'diamond',        # 4
    'triangle-down',  # 5
    'star',           # 6
    'hexagon',        # 7
    'circle-open',    # 8
    'triangle-up-open',  # 9
    'square-open',    # 10
    'diamond-open',   # 11
    'x',              # 12
    'star-open',      # 13
    'hexagon-open',   # 14
]


class AestheticMapper:
    """
    Handles the resolution and mapping of aesthetics to visual properties.
    
    This class distinguishes between:
    - Column references (strings that map to DataFrame columns)
    - Literal values (colors, sizes, etc. to be used directly)
    """
    
    def __init__(self, data: pd.DataFrame, mapping: Dict[str, Any], params: Dict[str, Any], theme=None):
        """
        Initialize the aesthetic mapper.
        
        Parameters:
            data: The DataFrame containing the plot data
            mapping: Dictionary of aesthetic mappings from aes()
            params: Dictionary of parameters passed to the geom
            theme: Optional theme object for default color palettes
        """
        self.data = data
        self.mapping = mapping
        self.params = params
        self.theme = theme
        
    def get_color_palette(self) -> list:
        """Get the color palette from theme or use default."""
        if self.theme and hasattr(self.theme, 'color_map') and self.theme.color_map:
            return self.theme.color_map
        return px.colors.qualitative.Plotly
    
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
            
        # Check if it exists as a column in the data
        return value in self.data.columns
    
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
            color_map = self._create_color_map(series)
            return value, series, color_map
        else:
            # It's a literal value
            return value, None, None
    
    def _create_color_map(self, series: pd.Series) -> Dict[Any, str]:
        """
        Create a mapping from unique values to colors.

        Parameters:
            series: The data series to map

        Returns:
            Dictionary mapping each unique value to a color
        """
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

        return {
            'color': color,
            'color_series': color_series,
            'color_map': color_map,
            'fill': fill,
            'fill_series': fill_series,
            'fill_map': fill_map,
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

        Parameters:
            color: Color as hex (#RRGGBB) or named color
            alpha: Alpha value (0-1)

        Returns:
            RGBA string like 'rgba(255, 0, 0, 0.5)'
        """
        import plotly.colors as pc

        # Handle hex colors
        if color.startswith('#'):
            # Convert hex to RGB
            color = color.lstrip('#')
            if len(color) == 6:
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
                return f'rgba({r},{g},{b},{alpha})'

        # Try to use plotly's color conversion
        try:
            # Convert named color to RGB via plotly
            rgb_str = pc.convert_colors_to_same_type([color], colortype='rgb')[0][0]
            # rgb_str is like 'rgb(255, 0, 0)'
            if rgb_str.startswith('rgb('):
                rgb_values = rgb_str[4:-1]  # Remove 'rgb(' and ')'
                return f'rgba({rgb_values},{alpha})'
        except:
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
        }

        if color.lower() in common_colors:
            r, g, b = common_colors[color.lower()]
            return f'rgba({r},{g},{b},{alpha})'

        # Ultimate fallback - assume it's already in right format or use default
        return f'rgba(31, 119, 180, {alpha})'  # Default plotly blue

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
