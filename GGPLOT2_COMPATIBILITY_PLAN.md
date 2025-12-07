# ggplotly API Compatibility Audit Plan

## Overview
Comprehensive audit and fix of ggplotly to match ggplot2 R behavior. This is a large undertaking with 100+ discrepancies identified across geoms, stats, scales, coords, facets, and themes.

## Scope
- 33 geom files
- 11 stat files
- 17 scale files
- 7 coord files
- 1 facets file
- 1 themes file
- Core functions (aes, ggplot, labs, guides)

---

## Phase 1: Critical Fixes (Breaking Behavior) ✅ COMPLETE

### 1.1 Fix coord_flip (BROKEN) ✅
**File**: `ggplotly/coords/coord_flip.py`
- **Bug**: Currently reverses x-axis instead of swapping x/y coordinates
- **Fix**: Swap x and y data/aesthetics, not just reverse axis
- Add `xlim`, `ylim`, `expand`, `clip` parameters

### 1.2 Fix stat_smooth confidence level ✅
**File**: `ggplotly/stats/stat_smooth.py`
- **Bug**: Default `level=0.68` (1 SD) instead of R's `level=0.95` (95% CI)
- **Fix**: Change default to 0.95

### 1.3 Fix scale_brewer default type ✅
**Files**: `ggplotly/scales/scale_color_brewer.py`, `scale_fill_brewer.py`
- **Bug**: Default `type="qual"` instead of R's `type="seq"`
- **Fix**: Change default to "seq"

### 1.4 ~~Fix default sizes/linewidths~~ - NOT A BUG
Plotly and ggplot2 use different units for sizes/linewidths, so the current defaults are appropriate for Plotly rendering. No changes needed.

---

## Phase 2: Missing Parameters (High Priority) - PARTIALLY COMPLETE

### 2.1 Add universal parameters to all geoms
Add to base Geom class or each geom:
- `na_rm` (default: False) - remove NA values
- `show_legend` (default: None/auto) - control legend visibility
- `inherit_aes` (default: True) - inherit aesthetics from ggplot

### 2.2 geom_boxplot missing outlier control ✅
**File**: `ggplotly/geoms/geom_boxplot.py`
Add parameters:
- `outlier_colour`, `outlier_fill`, `outlier_shape`, `outlier_size`
- `notch` (default: False) - draw notched boxplot
- `varwidth` (default: False) - variable width by sample size
- `coef` (default: 1.5) - whisker length as IQR multiple

### 2.3 geom_text missing alignment ✅
**File**: `ggplotly/geoms/geom_text.py`
Add parameters:
- `hjust` (0-1, default: 0.5) - horizontal justification
- `vjust` (0-1, default: 0.5) - vertical justification
- `angle` (default: 0) - rotation angle
- `check_overlap` (default: False)
- `na_rm` (default: False)

### 2.4 geom_bar/histogram missing width ✅
**Files**: `geom_bar.py`, `geom_histogram.py`
- Add `width` parameter (default: 0.9 for bar)
- Add `binwidth` as alternative to `bins` for histogram
- Add `position` parameter support (stack, dodge, fill, identity)

### 2.5 geom_density missing bandwidth control ✅
**File**: `ggplotly/geoms/geom_density.py`
Add parameters:
- `bw` (default: "nrd0") - bandwidth method
- `adjust` (default: 1) - bandwidth multiplier
- `kernel` (default: "gaussian")
- `n` (default: 512) - number of points (currently 1000)

---

## Phase 3: Scale Improvements ✅ COMPLETE

### 3.1 Fix scale API inconsistencies ✅
- `scale_fill_manual`: Add missing `breaks`, `labels` parameters
- `scale_color_gradient`: Add missing `name` parameter
- Standardize on `apply(fig)` method across all scales

### 3.2 Add missing scale parameters ✅
All continuous scales missing:
- `minor_breaks` - for minor grid lines
- `n_breaks` - auto-calculate break count
- `expand` - padding around limits (default: (0.05, 0))
- `oob` - out-of-bounds handling
- `na_value` - color for NA values
- `position` - axis position (top/bottom/left/right)

### 3.3 Expand transformation support ✅
**File**: `ggplotly/scales/scale_x_continuous.py`
Currently only: "log", "sqrt"
Add: "log2", "reverse", "sqrt", "date", "time", "hms"

### 3.4 Add parameters to scale_x_log10/scale_y_log10 ✅
Currently no parameters at all. Add: name, breaks, labels, limits, expand

---

## Phase 4: Coordinate Systems ✅ COMPLETE

### 4.1 coord_polar - add all parameters ✅
**File**: `ggplotly/coords/coord_polar.py`
Add:
- `theta` (default: "x") - which var maps to angle
- `start` (default: 0) - starting angle in radians
- `direction` (default: 1) - 1=clockwise, -1=counterclockwise

### 4.2 coord_cartesian - add missing parameters ✅
**File**: `ggplotly/coords/coord_cartesian.py`
Add:
- `expand` (default: True)
- `clip` (default: "on")

---

## Phase 5: Stats Improvements ✅ COMPLETE

### 5.1 stat_summary parameter naming ✅
**File**: `ggplotly/stats/stat_summary.py`
- Added `fun`, `fun_min`, `fun_max` as R-style aliases
- Legacy `fun_y`, `fun_ymin`, `fun_ymax` still work for backward compatibility
- Added `na_rm` and `fun_args` parameters

### 5.2 stat_density improvements ✅
**File**: `ggplotly/stats/stat_density.py`
- Added `bw`, `adjust`, `kernel`, `trim` parameters
- Changed n from 100 to 512 (R default)
- Added computed variables: `count`, `scaled`, `ndensity`

### 5.3 stat_bin completion ✅
**File**: `ggplotly/stats/stat_bin.py`
- Fully implemented binning with proper histogram computation
- Added `binwidth`, `breaks`, `center`, `boundary`, `closed`, `pad`, `na_rm`
- Returns proper computed variables: count, density, ncount, ndensity, width, xmin, xmax

---

## Phase 6: Facets & Themes

### 6.1 facet_wrap improvements
**File**: `ggplotly/facets.py`
Add:
- `strip_position` (default: "top")
- `drop` (default: True) - drop unused levels
- `as_table` (default: True)

### 6.2 facet_grid improvements
Add:
- `margins` (default: False)
- `drop` (default: True)
- `switch` (default: None)

### 6.3 theme() expansion
**File**: `ggplotly/themes.py`
Current theme() only has `legend_position`, `legend_show`.
Add support for major theme elements:
- `axis_title`, `axis_text`, `axis_line`, `axis_ticks`
- `panel_background`, `panel_grid`, `panel_border`
- `plot_title`, `plot_subtitle`, `plot_caption`, `plot_background`
- `legend_title`, `legend_text`, `legend_background`
- `strip_text`, `strip_background`

### 6.4 Preset themes - add base parameters
All preset themes (theme_minimal, theme_classic, etc.) should accept:
- `base_size` (default: 11)
- `base_family` (default: "")

---

## Phase 7: Core Functions

### 7.1 Implement guides() function
**File**: `ggplotly/guides.py`
Currently missing! Add:
- `guides(color=..., fill=..., shape=..., size=...)`
- Support `"none"` to hide legend
- Support `guide_legend()` and `guide_colorbar()`

### 7.2 Enhance aes() function
**File**: `ggplotly/aes.py`
Add support for:
- `after_stat()` computed aesthetics
- `after_scale()` for scale-dependent mappings

### 7.3 labs() improvements
**File**: `ggplotly/ggtitle.py`
Add support for arbitrary aesthetic labels:
- `labs(shape="Shape Label", size="Size Label", alpha="Alpha")`

---

## Files to Modify (Summary)

### Critical (Phase 1)
1. `ggplotly/coords/coord_flip.py` - FIX broken swap behavior
2. `ggplotly/stats/stat_smooth.py` - FIX confidence level default
3. `ggplotly/scales/scale_color_brewer.py` - FIX default type
4. `ggplotly/scales/scale_fill_brewer.py` - FIX default type

### High Priority (Phase 2-3)
5. `ggplotly/geoms/geom_base.py` - Add universal parameters
6. `ggplotly/geoms/geom_boxplot.py` - Add outlier control
7. `ggplotly/geoms/geom_text.py` - Add hjust/vjust/angle
8. `ggplotly/geoms/geom_bar.py` - Add width parameter
9. `ggplotly/geoms/geom_histogram.py` - Add binwidth
10. `ggplotly/geoms/geom_density.py` - Add bandwidth control
11. `ggplotly/scales/scale_fill_manual.py` - Add missing params
12. `ggplotly/scales/scale_x_continuous.py` - Add expand, minor_breaks
13. `ggplotly/scales/scale_x_log10.py` - Add all parameters

### Medium Priority (Phase 4-5)
14. `ggplotly/coords/coord_polar.py` - Add theta, start, direction
15. `ggplotly/coords/coord_cartesian.py` - Add expand, clip
16. `ggplotly/stats/stat_summary.py` - Fix parameter naming
17. `ggplotly/stats/stat_density.py` - Add bandwidth params
18. `ggplotly/stats/stat_bin.py` - Complete implementation

### Lower Priority (Phase 6-7)
19. `ggplotly/facets.py` - Add strip_position, drop, margins
20. `ggplotly/themes.py` - Expand theme() parameters
21. `ggplotly/guides.py` - Implement guides() function
22. `ggplotly/aes.py` - Add computed aesthetics

---

## Testing Strategy
For each fix:
1. Add/update tests in `pytest/test_*.py` with strong assertions
2. Verify behavior matches ggplot2 R documentation
3. Ensure backward compatibility where possible

---

## Estimated Effort
- Phase 1 (Critical): ~2-3 hours
- Phase 2 (High Priority): ~4-5 hours
- Phase 3 (Scales): ~2-3 hours
- Phase 4 (Coords): ~1-2 hours
- Phase 5 (Stats): ~2-3 hours
- Phase 6-7 (Facets/Themes/Core): ~3-4 hours

**Total: ~15-20 hours of work**
