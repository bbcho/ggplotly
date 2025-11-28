# Aesthetic Mapping System Refactoring

## Overview

The aesthetic mapping system in ggplotly has been refactored to provide clearer, more maintainable code for handling colors, fills, sizes, and other visual properties.

## Problem with Old System

The previous implementation had several issues:

1. **Fragile column detection**: Used try-except blocks to guess whether a value was a column name
2. **Complex logic**: The `handle_style()` method in `geom_base.py` was doing too much (275 lines)
3. **No validation**: Confusing errors when both color and fill were mapped to columns
4. **Debug code**: Print statements left in production code
5. **Duplicate code**: Each geom had similar logic for handling aesthetics
6. **Hard to test**: Tightly coupled logic made unit testing difficult

## New Architecture

### Core Component: `AestheticMapper`

Located in `ggplotly/aesthetic_mapper.py`, this class centralizes all aesthetic resolution logic:

```python
from ggplotly.aesthetic_mapper import AestheticMapper

# In a geom's draw method:
mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
style_props = mapper.get_style_properties()
```

### Key Features

#### 1. Clear Column Detection

```python
def is_column_reference(self, aesthetic: str, value: Any) -> bool:
    """Determine if an aesthetic value refers to a column."""
    if value is None or not isinstance(value, str):
        return False
    return value in self.data.columns
```

No more try-except guessing!

#### 2. Explicit Aesthetic Resolution

```python
def resolve_aesthetic(self, aesthetic: str) -> Tuple[Any, Optional[pd.Series], Optional[Dict]]:
    """
    Returns:
        - The aesthetic value (column name or literal)
        - Series of data if it's a column reference, None otherwise
        - Dictionary mapping unique values to colors, None otherwise
    """
```

#### 3. Flexible Aesthetic Handling

```python
# Both color and fill can be mapped to columns simultaneously
# Individual geoms will prioritize the appropriate aesthetic:
# - Point/line geoms use 'color'
# - Fill-based geoms (area, ribbon) use 'fill'
```

Each geom layer can use different aesthetics as needed.

#### 4. Centralized Color Mapping

```python
def _create_color_map(self, series: pd.Series) -> Dict[Any, str]:
    """Create a mapping from unique values to colors."""
    palette = self.get_color_palette()
    unique_values = series.dropna().unique()
    
    color_map = {}
    for i, val in enumerate(unique_values):
        color_map[val] = palette[i % len(palette)]
    
    return color_map
```

## Changes to `geom_base.py`

### Removed

- `handle_style()` method (replaced by `AestheticMapper.get_style_properties()`)
- `_format_color_targets()` (replaced by `_apply_color_targets()`)
- Debug print statements
- Duplicate import of `aes`
- Complex try-except logic for column detection

### Added

- Import of `AestheticMapper`
- New `_apply_color_targets()` method for cleaner trace property application
- Clearer three-case structure in `_transform_fig()`:
  1. Grouped by 'group' aesthetic
  2. Colored/filled by categorical variable
  3. Single trace with no grouping

### Simplified Logic

**Before:**
```python
# Complex nested conditionals
if group_values is not None:
    # ... 20 lines
elif (color_values is not None) | (fill_values is not None):
    if (color_values is not None) & (fill_values is not None):
        raise ValueError(...)
    if color_values is not None:
        values = color_values
        value_col = color
    else:
        values = fill_values
        value_col = fill
    for key in values.keys():
        # ... 30 lines of complex logic
else:
    # ... 15 lines
```

**After:**
```python
# Clear, maintainable structure
mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
style_props = mapper.get_style_properties()

if style_props['group_series'] is not None:
    # Handle grouped data
elif style_props['color_series'] is not None or style_props['fill_series'] is not None:
    # Handle categorical coloring
else:
    # Single trace
```

## Usage Examples

### Mapping color to a column

```python
ggplot(df, aes(x='x', y='y', color='category')) + geom_point()
```

### Using literal color

```python
ggplot(df, aes(x='x', y='y')) + geom_point(color='red')
```

### Mixing mapped and literal

```python
# Valid: color mapped, fill literal
ggplot(df, aes(x='x', y='y', color='category')) + geom_point(fill='lightblue')

# Also valid: both mapped (different layers use different aesthetics)
ggplot(df, aes(x='x', y='y', color='category')) + \
    geom_point() + \
    geom_area(aes(fill='fill_value'), alpha=0.3)
```

## Benefits

1. **Testability**: `AestheticMapper` can be unit tested independently
2. **Maintainability**: All aesthetic logic in one place
3. **Extensibility**: Easy to add new aesthetics (shape, linetype, etc.)
4. **Debuggability**: Clear separation of concerns
5. **User Experience**: Better error messages
6. **Performance**: No unnecessary try-except blocks
7. **Readability**: Self-documenting code with clear method names

## Migration Guide

For users: No API changes! Everything works the same.

For contributors:
- Import `AestheticMapper` instead of using `handle_style()`
- Use `mapper.get_style_properties()` to get all resolved aesthetics
- Use `_apply_color_targets()` for applying colors to traces

## Testing

Run the demonstration:
```bash
python examples/aesthetic_mapper_demo.py
```

Run existing tests to verify backward compatibility:
```bash
pytest pytest/test_main.py
```

## Future Enhancements

The new architecture makes it easy to add:
- Shape aesthetic for different point shapes
- Linetype aesthetic for line patterns
- Custom color scales
- Gradient fills for continuous variables
- Better integration with position adjustments
