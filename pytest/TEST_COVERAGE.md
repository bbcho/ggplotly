# Test Coverage for Refactoring Improvements

This document describes the comprehensive test suite added for the major refactoring improvements made to ggplotly.

## Test File

**Location:** `pytest/test_refactoring_improvements.py`

**Total Tests:** 22 tests organized into 5 test suites
**Status:** ✅ All 22 tests passing

## Test Suites

### 1. TestGroupedColorCombinations (6 tests)

Tests that all geoms properly handle the combination of `group` and `color` aesthetics.

**Tests:**
- ✅ `test_geom_line_grouped_color` - Validates geom_line creates correct traces with unique colors
- ✅ `test_geom_step_grouped_color` - Validates geom_step creates correct traces with unique colors
- ✅ `test_geom_smooth_grouped_color` - Validates geom_smooth creates correct traces with unique colors
- ✅ `test_geom_errorbar_grouped_color` - Validates geom_errorbar creates correct traces with unique colors
- ✅ `test_geom_text_grouped_color` - Validates geom_text creates correct traces
- ✅ `test_geom_segment_grouped_color` - Validates geom_segment creates correct traces

**What This Tests:**
- The critical bug fix where `group + color` combinations now pass `value_key=group` to `_apply_color_targets`
- Ensures each group gets a unique color from the theme palette
- Verifies all geoms (both using `_transform_fig` and manual implementations) work correctly

### 2. TestPlotlyFillParameter (3 tests)

Tests that Plotly's fill parameter (like `'tonexty'`) is handled correctly and not confused with fill aesthetics.

**Tests:**
- ✅ `test_geom_ribbon_with_default` - Validates ribbon works without explicit fill/color
- ✅ `test_geom_ribbon_with_color` - Validates ribbon with explicit color parameter
- ✅ `test_geom_ribbon_with_fill` - Validates ribbon with explicit fill parameter

**What This Tests:**
- The fix for Plotly fill parameters being incorrectly treated as fill aesthetics
- Ensures geom_ribbon creates proper filled areas using `fill='tonexty'`
- Verifies both geom_line and geom_density handle fill parameters correctly

### 3. TestMigratedGeoms (4 tests)

Tests geoms that were migrated to use the centralized `_transform_fig` method.

**Tests:**
- ✅ `test_geom_step_basic` - Validates basic step plot functionality
- ✅ `test_geom_step_with_ecdf` - Validates ECDF transformation with automatic y mapping
- ✅ `test_geom_smooth_basic` - Validates basic smooth plot functionality
- ✅ `test_geom_density_basic` - Validates basic density plot functionality

**What This Tests:**
- geom_step, geom_smooth, and geom_density now use `_transform_fig` consistently
- Data transformations (ECDF, smoothing, KDE) work correctly before calling `_transform_fig`
- ECDF automatically creates y mapping when not provided
- Migrated geoms produce correct trace types and properties

### 4. TestManualGeoms (4 tests)

Tests geoms that remain manual implementations due to special requirements.

**Tests:**
- ✅ `test_geom_text_basic` - Validates text labels are correctly displayed
- ✅ `test_geom_errorbar_basic` - Validates error bars with ymin/ymax
- ✅ `test_geom_errorbar_with_yerr` - Validates error bars with yerr aesthetic
- ✅ `test_geom_segment_basic` - Validates line segments and legend handling

**What This Tests:**
- geom_text, geom_errorbar, and geom_segment have valid reasons for manual implementation
- These geoms require per-trace custom data (text labels, error arrays, segment coordinates)
- Special requirements like legend grouping work correctly

### 5. TestEdgeCases (5 tests)

Tests edge cases and potential regression scenarios.

**Tests:**
- ✅ `test_group_without_color` - Validates group aesthetic works alone (same default color)
- ✅ `test_color_without_group` - Validates color aesthetic works alone (unique colors)
- ✅ `test_no_group_no_color` - Validates basic plot with no grouping or coloring
- ✅ `test_multiple_geoms_same_plot` - Validates multiple geoms can coexist
- ✅ `test_size_aesthetic_with_line_geoms` - Validates complex plot with size aesthetic mapped to column

**What This Tests:**
- Edge cases that could cause regressions
- Ensures aesthetic system works correctly in all combinations
- Verifies backward compatibility with existing code
- Size aesthetic with line geoms (geom_smooth ignores, geom_point uses)
- Complex multi-component plots with faceting and color scales

## Coverage Summary

### Bugs Fixed and Tested
1. ✅ Grouped + color aesthetic combination bug in all geoms
2. ✅ Plotly fill parameter confusion with fill aesthetic
3. ✅ None color value handling in _apply_color_targets
4. ✅ Duplicate name parameter in grouped traces
5. ✅ Numpy bool type in showlegend parameter
6. ✅ Size aesthetic mapped to columns causing errors in line geoms
7. ✅ ECDF stat without y mapping in geom_step

### Refactorings Tested
1. ✅ geom_step migration to _transform_fig
2. ✅ geom_smooth migration to _transform_fig
3. ✅ geom_density already using _transform_fig (verified)
4. ✅ Manual geoms (text, errorbar, segment) working correctly
5. ✅ geom_ribbon composition pattern working

### Code Quality Improvements Tested
1. ✅ All geoms use consistent color palette system
2. ✅ Default colors properly applied when no color specified
3. ✅ Theme integration working across all geoms
4. ✅ Legend handling correct in all cases
5. ✅ Multiple traces created correctly for grouped/categorical data
6. ✅ Line geoms properly ignore size aesthetics mapped to columns
7. ✅ Complex multi-geom plots with mixed aesthetic requirements

## Running the Tests

```bash
# Run only the new test suite
pytest pytest/test_refactoring_improvements.py -v

# Run all tests
pytest pytest/ -v

# Run with coverage report
pytest pytest/test_refactoring_improvements.py --cov=ggplotly --cov-report=html
```

## Test Data Patterns

The tests use realistic data patterns:
- **Grouped data:** Multiple series with categorical grouping variables
- **Error bars:** Data with uncertainty ranges
- **Text labels:** Data with associated text annotations
- **Segments:** Data with start and end coordinates
- **Continuous transformations:** Normal distributions for density/ECDF

## Future Test Additions

Potential areas for additional tests:
1. geom_tile and heatmap special cases
2. Faceting with grouped/colored aesthetics
3. Size aesthetic mapped to columns
4. More complex theme integration scenarios
5. Additional statistical transformations

## Regression Prevention

These tests ensure that future changes don't break:
1. The grouped+color fix across all geoms
2. The Plotly fill parameter handling
3. The migrated geom implementations
4. The manual geom special requirements
5. The edge cases that work correctly now
