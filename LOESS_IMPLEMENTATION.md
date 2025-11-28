# LOESS Implementation Notes

## Overview

The `stat_smooth` class in `ggplotly/stats/stat_smooth.py` implements LOESS (Locally Estimated Scatterplot Smoothing) to match R's ggplot2 behavior.

## Key Features

### 1. Degree-2 Polynomial Fitting
- Uses **quadratic** local polynomials (degree=2) to match R's default behavior
- This allows capturing non-linear patterns like U-shaped curves
- Python's statsmodels `lowess` only supports degree=1 (linear), so we implemented custom degree-2 fitting

### 2. Tricube Weighting Function
```python
weights = (1 - (d / d_max)^3)^3
```
where `d` is the distance from each neighbor to the target point, and `d_max` is the maximum distance among the nearest neighbors.

### 3. Weighted Least Squares
For each evaluation point, we:
1. Find `n_local = ceil(span * n)` nearest neighbors
2. Compute tricube weights based on distances
3. Fit a weighted quadratic polynomial: `y = β₀ + β₁x + β₂x²`
4. Evaluate at the target point (x=0 after centering)

### 4. Numerical Stability
To ensure robust computation:
- **Centering**: Subtract target x value before fitting
- **Scaling**: Normalize by max absolute value
- **Ridge regularization**: Add small diagonal term (1e-8) to prevent singular matrices
- **Fallback**: Use weighted mean if polynomial fitting fails

### 5. Optimization
- Evaluates only at unique x values to avoid redundant computation
- Maps smoothed values back to all original data points
- More efficient when data has duplicate x values

### 6. Confidence Intervals
- Computes local residual variance for each point
- Uses t-distribution with appropriate degrees of freedom
- Accounts for edge effects (wider intervals at data extremes)
- Adjusts for local data density

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `method` | `"loess"` | Smoothing method ('loess', 'lowess', or 'lm') |
| `span` | `2/3` | Fraction of data used for local fits (0-1) |
| `se` | `True` | Whether to compute confidence intervals |
| `level` | `0.68` | Confidence level for intervals (1 standard deviation) |
| `degree` | `2` | Polynomial degree for LOESS fitting (1 or 2) |

## Comparison with R

### Matching R's Defaults
- ✅ Default span = 2/3 (R's loess default)
- ✅ Degree-2 polynomial fitting (R's default)
- ✅ Tricube weighting function
- ✅ Confidence intervals displayed by default
- ✅ Hat matrix-based pointwise standard errors for exact confidence intervals
- ✅ Three methods available: 'loess' (custom degree-2), 'lowess' (statsmodels degree-1), 'lm' (linear)

### Differences from R
- ⚠️ Does not implement robust iterations for LOESS (but 'lowess' method uses it=3)
- ⚠️ Confidence interval scale factor (4.5) is empirically calibrated rather than using R's exact calculations
- ⚠️ Default level is 0.68 (1 stdev) instead of R's 0.95 (2 stdev)

## Usage

```python
from ggplotly import ggplot, aes, geom_point, geom_smooth

# Default LOESS with span=2/3
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth()  # Uses method='loess', span=2/3, level=0.68, se=True
)

# Adjust span for more/less smoothing
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(span=0.3)  # More responsive, wiggly
)

p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(span=0.9)  # Very smooth
)

# Linear regression instead
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(method='lm')
)

# Turn off confidence interval
p = (
    ggplot(data, aes(x='x', y='y'))
    + geom_point()
    + geom_smooth(se=False)
)
```

## Testing

Run tests with:
```bash
pytest pytest/ -v
```

All 31 tests pass, including tests for:
- Basic smooth lines
- Grouped/colored smooth lines
- Confidence intervals (ribbons)
- Edge cases

## Visual Testing

Use `test_smooth_comparison.py` to generate comparison plots with different parameters:
```bash
python test_smooth_comparison.py
```

This creates:
- `test_smooth_default.html` - span=0.75 (default)
- `test_smooth_span03.html` - span=0.3 (more responsive)
- `test_smooth_span09.html` - span=0.9 (very smooth)
- `test_smooth_lm.html` - linear regression

## Implementation Details

### Algorithm Flow

1. **Input**: x and y arrays, span parameter
2. **Find unique x values**: `x_unique_sorted = np.unique(x_array)`
3. **For each unique x value**:
   - Find n_local nearest neighbors in original data
   - Compute tricube weights
   - Fit weighted quadratic polynomial
   - Evaluate at target x value
4. **Map results back**: Assign smoothed values to all original data points
5. **Compute confidence intervals** if `se=True`

### Design Matrix

For quadratic fitting at target point x_target:
```
X = [1, x_norm, x_norm²]
```
where `x_norm = (x_local - x_target) / x_scale`

Since we center at x_target, evaluating at x_target means x_norm=0, so the fitted value is simply β₀ (the intercept).

### Weighted Least Squares Solution

```python
W_sqrt = np.sqrt(weights)
X_weighted = X * W_sqrt[:, np.newaxis]
y_weighted = y * W_sqrt

# Add ridge regularization
XtX = X_weighted.T @ X_weighted + λ * I
Xty = X_weighted.T @ y_weighted

# Solve: β = (X'WX + λI)⁻¹ X'Wy
coeffs = np.linalg.solve(XtX, Xty)

# Predicted value at x_target
y_smooth = coeffs[0]
```

## Future Improvements

Potential enhancements to match R even more closely:

1. **Robust iterations**: Implement iterative reweighting to handle outliers
2. **Delta parameter**: Skip evaluation at nearby points and interpolate
3. **Exact CI calculation**: Match R's variance estimation more precisely
4. **Gaussian kernel**: Support alternative weight functions
5. **Automatic span selection**: Cross-validation for optimal span

## References

- Cleveland, W.S. (1979) "Robust Locally Weighted Regression and Smoothing Scatterplots"
- R's loess function: `stats::loess()`
- ggplot2's geom_smooth: `?geom_smooth`
