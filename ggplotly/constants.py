"""
Shared constants for ggplotly.

This module contains palettes, defaults, and other constants used across
the library to avoid duplication and ensure consistency.
"""

import plotly.express as px


# Default shape palette matching ggplot2's defaults
# Maps to Plotly marker symbols
# See: https://plotly.com/python/marker-style/
SHAPE_PALETTE = [
    'circle',            # 0 - ggplot2 default
    'triangle-up',       # 1
    'square',            # 2
    'cross',             # 3 (plus in ggplot2)
    'diamond',           # 4
    'triangle-down',     # 5
    'star',              # 6
    'hexagon',           # 7
    'circle-open',       # 8
    'triangle-up-open',  # 9
    'square-open',       # 10
    'diamond-open',      # 11
    'x',                 # 12
    'star-open',         # 13
    'hexagon-open',      # 14
]

# Default color palette (Plotly's qualitative palette)
DEFAULT_COLOR_PALETTE = px.colors.qualitative.Plotly


def get_color_palette(theme=None):
    """
    Get the color palette from theme or use default.

    Parameters:
        theme: Optional theme object with a color_map attribute.

    Returns:
        list: A list of color strings.
    """
    if theme and hasattr(theme, 'color_map') and theme.color_map:
        return theme.color_map
    return DEFAULT_COLOR_PALETTE
