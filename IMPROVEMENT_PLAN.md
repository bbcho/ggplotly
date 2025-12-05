# ggplotly Improvement Plan

This document outlines the implementation plan for the following improvements:
1. **Code Documentation** - Add docstrings to all public classes and methods
2. **Consistency Refactoring** - Extract duplicated palette logic, standardize patterns
3. **Helpful Error Messages** - Add validation with clear, actionable error messages
4. **Cache Aesthetic Calculations** - Optimize repeated calculations in AestheticMapper

---

## 1. Code Documentation

### 1.1 Scale Classes (Missing Docstrings)

| File | Class | Current State |
|------|-------|---------------|
| `scales/scale_color_gradient.py` | `scale_color_gradient` | No docstrings |
| `scales/scale_fill_gradient.py` | `scale_fill_gradient` | No docstrings |
| `scales/scale_x_log10.py` | `scale_x_log10` | No docstrings |
| `scales/scale_y_log10.py` | `scale_y_log10` | No docstrings |
| `scales/scale_x_continuous.py` | `scale_x_continuous` | No docstrings |
| `scales/scale_y_continuous.py` | `scale_y_continuous` | No docstrings |
| `scales/scale_size.py` | `scale_size` | No docstrings |
| `scales/scale_shape_manual.py` | `scale_shape_manual` | No docstrings |
| `scales/scale_color_manual.py` | `scale_color_manual` | No docstrings |
| `scales/scale_fill_manual.py` | `scale_fill_manual` | No docstrings |
| `scales/scale_color_brewer.py` | `scale_color_brewer` | No docstrings |
| `scales/scale_fill_brewer.py` | `scale_fill_brewer` | No docstrings |
| `scales/scale_fill_viridis.py` | `scale_fill_viridis_c` | No docstrings |
| `scales/scale_x_date.py` | `scale_x_date` | No docstrings |

**Template for scale docstrings:**
```python
class scale_color_gradient(Scale):
    """
    Create a continuous color gradient scale.

    Maps numeric values to a color gradient between two colors,
    useful for heatmaps and continuous color scales.

    Parameters:
        low (str): Color for low values. Default is 'blue'.
        high (str): Color for high values. Default is 'red'.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + scale_color_gradient(low='white', high='red')
    """
```

### 1.2 Coord Classes (Missing Docstrings)

| File | Class | Current State |
|------|-------|---------------|
| `coords/coord_cartesian.py` | `coord_cartesian` | No docstrings |
| `coords/coord_flip.py` | `coord_flip` | No docstrings |
| `coords/coord_polar.py` | `coord_polar` | No docstrings |
| `coords/coord_base.py` | `Coord` | No docstrings |

### 1.3 Stat Classes (Missing Docstrings)

| File | Class | Current State |
|------|-------|---------------|
| `stats/stat_bin.py` | `stat_bin` | Minimal docstrings |
| `stats/stat_ecdf.py` | `stat_ecdf` | Minimal docstrings |
| `stats/stat_identity.py` | `stat_identity` | No docstrings |
| `stats/stat_count.py` | `stat_count` | Has debug print statement to remove |
| `stats/stat_base.py` | `Stat` | No docstrings |

---

## 2. Consistency Refactoring

### 2.1 Extract Duplicated SHAPE_PALETTE

**Current duplication:**
- `ggplotly/aesthetic_mapper.py:17-33` - Defines `SHAPE_PALETTE`
- `ggplotly/facets.py:8-12` - Defines identical `SHAPE_PALETTE`

**Solution:** Create a shared constants module.

```python
# ggplotly/constants.py
"""Shared constants for ggplotly."""

import plotly.express as px

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

# Default color palette
DEFAULT_COLOR_PALETTE = px.colors.qualitative.Plotly
```

**Files to update:**
- `aesthetic_mapper.py` - Import from constants
- `facets.py` - Import from constants

### 2.2 Extract Duplicated Color Palette Logic

**Current duplication:**
- `aesthetic_mapper.py:65-69` - `get_color_palette()` method
- `facets.py:42-46` - Inline color palette retrieval

**Solution:** Use the `AestheticMapper.get_color_palette()` method in facets, or extract to constants.

```python
# In constants.py, add helper function:
def get_color_palette(theme=None):
    """Get the color palette from theme or use default."""
    if theme and hasattr(theme, 'color_map') and theme.color_map:
        return theme.color_map
    return DEFAULT_COLOR_PALETTE
```

---

## 3. Helpful Error Messages

### 3.1 Column Reference Validation

**Location:** `aesthetic_mapper.py` - `is_column_reference()` and `resolve_aesthetic()`

**Current behavior:** Silently returns None or uses default when column doesn't exist.

**Improvement:** Add validation with helpful messages.

```python
class AestheticMapperError(Exception):
    """Base exception for aesthetic mapping errors."""
    pass

class ColumnNotFoundError(AestheticMapperError):
    """Raised when a mapped column doesn't exist in the data."""
    pass

class InvalidAestheticError(AestheticMapperError):
    """Raised when an aesthetic value is invalid."""
    pass
```

**Validation points:**
1. **Missing column in aes()**: When user maps to a column that doesn't exist
   ```python
   # Instead of silent failure:
   raise ColumnNotFoundError(
       f"Column '{value}' not found in data. "
       f"Available columns: {list(self.data.columns)[:10]}..."
       f"\n\nDid you mean one of these? {get_similar_columns(value, self.data.columns)}"
   )
   ```

2. **Invalid color values**: When a literal color is not recognized
   ```python
   # Add validation in _color_to_rgba()
   raise InvalidAestheticError(
       f"Color '{color}' not recognized. "
       f"Use hex colors (#RRGGBB) or named colors like 'red', 'blue', 'steelblue'."
   )
   ```

3. **Type mismatches**: When numeric aesthetic gets categorical data
   ```python
   raise InvalidAestheticError(
       f"Size aesthetic requires numeric values, but column '{col}' is {dtype}. "
       f"Consider using scale_size_manual() for categorical data."
   )
   ```

### 3.2 Geom-Specific Validation

**Add validation in `geom_base.py` `draw()` method or individual geoms:**

```python
def _validate_required_aesthetics(self, required: list[str]):
    """Validate that required aesthetics are present."""
    missing = [aes for aes in required if aes not in self.mapping]
    if missing:
        raise ValueError(
            f"{self.__class__.__name__} requires aesthetics: {missing}. "
            f"Add them via aes(). Example: aes({', '.join(f'{m}=\"column\"' for m in missing)})"
        )
```

### 3.3 Facet Validation

**Location:** `facets.py` - `facet_wrap` and `facet_grid`

```python
def apply(self, plot):
    # Validate facet column exists
    if self.facet_var not in plot.data.columns:
        raise ValueError(
            f"Facet variable '{self.facet_var}' not found in data. "
            f"Available columns: {list(plot.data.columns)}"
        )

    # Validate facet column is categorical
    if plot.data[self.facet_var].nunique() > 50:
        import warnings
        warnings.warn(
            f"Facet variable '{self.facet_var}' has {plot.data[self.facet_var].nunique()} "
            f"unique values. This will create many subplots. Consider filtering your data."
        )
```

### 3.4 Scale Validation

**Add validation for scale parameters:**

```python
class scale_color_gradient(Scale):
    def __init__(self, low="blue", high="red"):
        # Validate colors
        self._validate_color(low, "low")
        self._validate_color(high, "high")
        self.low = low
        self.high = high

    def _validate_color(self, color, param_name):
        """Validate that a color value is valid."""
        if not isinstance(color, str):
            raise TypeError(
                f"Parameter '{param_name}' must be a string color value, "
                f"got {type(color).__name__}"
            )
```

---

## 4. Cache Aesthetic Calculations

### 4.1 Add Caching to AestheticMapper

**Location:** `aesthetic_mapper.py`

**Methods to cache:**
1. `_color_to_rgba()` - Most frequently called, expensive Plotly conversion
2. `get_style_properties()` - Called per geom, builds large dict
3. `_create_color_map()` and `_create_shape_map()` - Called for each mapped column

**Implementation using `functools.lru_cache`:**

```python
from functools import lru_cache

class AestheticMapper:
    def __init__(self, ...):
        # ... existing code ...
        # Cache for color conversions (shared across all mappers)
        # Use module-level cache for color conversions

    @staticmethod
    @lru_cache(maxsize=256)
    def _cached_color_to_rgba(color: str, alpha: float) -> str:
        """Cached color to RGBA conversion."""
        # Implementation moved here
        ...

    def _color_to_rgba(self, color: str, alpha: float) -> str:
        """Convert color to RGBA string with alpha."""
        return self._cached_color_to_rgba(color, alpha)
```

**Alternative: Instance-level caching with lazy evaluation:**

```python
class AestheticMapper:
    def __init__(self, ...):
        # ... existing code ...
        self._style_props_cache = None
        self._color_map_cache = {}
        self._shape_map_cache = {}

    def get_style_properties(self) -> Dict[str, Any]:
        """Extract all relevant style properties for a geom (cached)."""
        if self._style_props_cache is not None:
            return self._style_props_cache

        # ... compute style properties ...
        self._style_props_cache = result
        return result

    def _create_color_map(self, series: pd.Series) -> Dict[Any, str]:
        """Create color mapping (cached by series name)."""
        cache_key = series.name
        if cache_key in self._color_map_cache:
            return self._color_map_cache[cache_key]

        # ... compute color map ...
        self._color_map_cache[cache_key] = color_map
        return color_map
```

### 4.2 Module-Level Color Conversion Cache

**For `_color_to_rgba()` which is the most expensive operation:**

```python
# At module level in aesthetic_mapper.py
_COLOR_RGBA_CACHE = {}

def _cached_color_to_rgba(color: str, alpha: float) -> str:
    """Convert color to RGBA with caching."""
    cache_key = (color, alpha)
    if cache_key in _COLOR_RGBA_CACHE:
        return _COLOR_RGBA_CACHE[cache_key]

    # ... conversion logic ...

    _COLOR_RGBA_CACHE[cache_key] = result
    return result
```

### 4.3 Cache DataFrame Column Lookups

**Optimization in `is_column_reference()`:**

```python
class AestheticMapper:
    def __init__(self, ...):
        # ... existing code ...
        # Pre-compute column set for O(1) lookups
        self._column_set = frozenset(self.data.columns)

    def is_column_reference(self, aesthetic: str, value: Any) -> bool:
        """Determine if an aesthetic value refers to a column in the data."""
        if value is None or not isinstance(value, str):
            return False
        return value in self._column_set  # O(1) instead of O(n)
```

---

## Implementation Order

### Phase 1: Foundation (Low Risk)
1. Create `ggplotly/constants.py` with shared palettes
2. Update imports in `aesthetic_mapper.py` and `facets.py`
3. Add caching to `_color_to_rgba()` (module-level LRU cache)
4. Add column set optimization to `is_column_reference()`

### Phase 2: Error Handling (Medium Risk)
1. Create `ggplotly/exceptions.py` with custom exception classes
2. Add column validation to `AestheticMapper.resolve_aesthetic()`
3. Add facet column validation to `facet_wrap` and `facet_grid`
4. Add helpful error messages with suggestions

### Phase 3: Documentation (Low Risk)
1. Add docstrings to all scale classes
2. Add docstrings to all coord classes
3. Add docstrings to all stat classes
4. Remove debug print statement in `stat_count.py`

### Phase 4: Additional Caching (Medium Risk)
1. Add instance-level caching for `get_style_properties()`
2. Add caching for `_create_color_map()` and `_create_shape_map()`
3. Add cache invalidation hooks if needed

---

## Files to Modify

| File | Changes |
|------|---------|
| `ggplotly/constants.py` | **NEW** - Shared constants |
| `ggplotly/exceptions.py` | **NEW** - Custom exceptions |
| `ggplotly/aesthetic_mapper.py` | Import constants, add caching, add validation |
| `ggplotly/facets.py` | Import constants, add validation |
| `ggplotly/scales/scale_base.py` | Add base docstring |
| `ggplotly/scales/scale_color_gradient.py` | Add docstrings, validation |
| `ggplotly/scales/scale_fill_gradient.py` | Add docstrings |
| `ggplotly/scales/scale_x_log10.py` | Add docstrings |
| `ggplotly/scales/scale_y_log10.py` | Add docstrings |
| `ggplotly/scales/scale_x_continuous.py` | Add docstrings |
| `ggplotly/scales/scale_y_continuous.py` | Add docstrings |
| `ggplotly/scales/scale_size.py` | Add docstrings |
| `ggplotly/scales/scale_shape_manual.py` | Add docstrings |
| `ggplotly/scales/scale_color_manual.py` | Add docstrings |
| `ggplotly/scales/scale_fill_manual.py` | Add docstrings |
| `ggplotly/scales/scale_color_brewer.py` | Add docstrings |
| `ggplotly/scales/scale_fill_brewer.py` | Add docstrings |
| `ggplotly/scales/scale_fill_viridis.py` | Add docstrings |
| `ggplotly/scales/scale_x_date.py` | Add docstrings |
| `ggplotly/coords/coord_base.py` | Add docstrings |
| `ggplotly/coords/coord_cartesian.py` | Add docstrings |
| `ggplotly/coords/coord_flip.py` | Add docstrings |
| `ggplotly/coords/coord_polar.py` | Add docstrings |
| `ggplotly/stats/stat_base.py` | Add docstrings |
| `ggplotly/stats/stat_bin.py` | Improve docstrings |
| `ggplotly/stats/stat_ecdf.py` | Add docstrings |
| `ggplotly/stats/stat_identity.py` | Add docstrings |
| `ggplotly/stats/stat_count.py` | Remove debug print, improve docstrings |

---

## Testing Plan

1. **Unit tests for error messages:**
   - Test that `ColumnNotFoundError` is raised with helpful message
   - Test that similar column suggestions work
   - Test facet validation

2. **Unit tests for caching:**
   - Test that `_color_to_rgba` cache works
   - Test cache hit rate with repeated calls
   - Test that caching doesn't break functionality

3. **Run existing test suite:**
   ```bash
   pytest pytest/ -v
   ```

4. **Performance benchmark:**
   - Time aesthetic resolution with/without caching
   - Measure memory usage of caches
