# Smoothing Methods in ggplotly

## Overview

ggplotly now provides three smoothing methods for `geom_smooth()`:

### 1. `loess` (Default) - Custom LOESS Implementation

**Best for**: Maximum R compatibility, capturing non-linear patterns

- **Polynomial degree**: 2 (quadratic) by default
- **Algorithm**: Custom implementation using local weighted regression
- **Weighting**: Tricube kernel
- **Advantage**: Can capture U-shaped and other non-linear patterns better than degree-1 methods
- **Default parameters**: `span=2/3`, `degree=2`

```python
from ggplotly import ggplot, aes, geom_point, geom_smooth

p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(method='loess')  # Default
)
```

### 2. `lowess` - statsmodels Implementation

**Best for**: Speed and computational efficiency

- **Polynomial degree**: 1 (linear)
- **Algorithm**: statsmodels' `lowess` function
- **Robustness iterations**: 3 (matches R's default)
- **Delta parameter**: `0.01 * range(x)` for computational optimization
- **Advantage**: Faster, well-tested library implementation
- **Default parameters**: `span=2/3`, `it=3`, `delta=0.01*range(x)`

```python
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(method='lowess')
)
```

### 3. `lm` - Linear Regression

**Best for**: Linear relationships, simple models

- **Algorithm**: sklearn's `LinearRegression`
- **Advantage**: Simplest, fastest, interpretable
- **No span parameter** (uses all data)

```python
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(method='lm')
)
```

## Parameters

All methods support these parameters:

- **`span`** (float): Fraction of data used for local fits (LOESS/LOWESS only)
  - Default: `2/3` (~0.667)
  - Range: 0 to 1
  - Larger values → smoother curves

- **`se`** (bool): Show confidence interval ribbon
  - Default: `True`

- **`level`** (float): Confidence level for interval
  - Default: `0.68` (1 standard deviation, ~68% confidence)

## Confidence Intervals

All methods compute varying-width confidence bands that are:
- Narrower in the center of the data
- Wider at the edges (where there's more uncertainty)
- Based on residual standard deviation and t-distribution

The confidence bands use an edge multiplier: `1.0 + 0.5 * distance_from_center`

## Examples

### Basic LOESS Smoothing
```python
p = (
    ggplot(mpg, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth()  # Uses loess by default
)
```

### Adjust Smoothness
```python
# More responsive (less smooth)
p = ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + geom_smooth(span=0.3)

# Very smooth
p = ggplot(mpg, aes(x='displ', y='hwy')) + geom_point() + geom_smooth(span=0.9)
```

### Grouped Smoothing
```python
p = (
    ggplot(mpg, aes(x='displ', y='hwy', color='class'))
    + geom_point(alpha=0.5)
    + geom_smooth()  # Separate smooth line for each class
)
```

### Compare Methods
```python
# LOESS (degree-2, default)
p1 = ggplot(data, aes(x='x', y='y')) + geom_point() + geom_smooth(method='loess')

# LOWESS (degree-1, faster)
p2 = ggplot(data, aes(x='x', y='y')) + geom_point() + geom_smooth(method='lowess')

# Linear regression
p3 = ggplot(data, aes(x='x', y='y')) + geom_point() + geom_smooth(method='lm')
```

### Disable Confidence Band
```python
p = (
    ggplot(mpg, aes(x='displ', y='hwy'))
    + geom_point()
    + geom_smooth(se=False)
)
```

## Technical Details

### LOESS Algorithm (method='loess')

For each evaluation point:
1. Find `n_local = ceil(span * n)` nearest neighbors
2. Compute tricube weights: `w = (1 - (d/d_max)^3)^3`
3. Fit weighted polynomial (degree 1 or 2)
4. Evaluate at target point

Design matrix for degree=2:
```
X = [1, x_norm, x_norm^2]
```

Weighted least squares with ridge regularization:
```
β = (X'WX + λI)^(-1) X'Wy
```

### LOWESS Algorithm (method='lowess')

Uses statsmodels implementation with:
- `frac = span`
- `it = 3` (robustness iterations)
- `delta = 0.01 * range(x)` (computational optimization)

### Confidence Intervals

For both LOESS and LOWESS:
```
margin[i] = t_value * residual_std * edge_multiplier[i]
edge_multiplier[i] = 1.0 + 0.5 * |x[i] - x_center| / (x_range/2)
```

## Comparison with R

### Default Behavior
✅ Default `span = 2/3` (matches R's `loess`)
✅ Default `se = TRUE` (matches R's ggplot2)
✅ Confidence intervals shown by default
✅ Varying-width confidence bands (wider at edges)

### Differences
- R's `loess()` uses proprietary algorithm with exact variance calculation
- ggplotly uses simplified edge-based variance approximation
- Results should be visually very similar but not numerically identical

## Performance

Typical performance on 100 data points:

| Method | Time | Notes |
|--------|------|-------|
| `lm` | ~1ms | Fastest, no local fitting |
| `lowess` | ~5ms | Fast, uses optimized C code |
| `loess` | ~10ms | Slower due to Python loops |

For datasets > 500 points, consider `lowess` for better performance.

## See Also

- `geom_smooth()` documentation
- R's `stats::loess()` documentation
- Cleveland, W.S. (1979) "Robust Locally Weighted Regression and Smoothing Scatterplots"
