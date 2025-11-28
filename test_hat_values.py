#!/usr/bin/env python
"""Debug hat matrix values"""

import pandas as pd
import numpy as np
from ggplotly.stats.stat_smooth import stat_smooth

# Create sample data
data = pd.DataFrame({
    'displ': [1.8, 2.0, 2.8, 3.1, 4.2, 5.3, 5.7, 6.0, 6.5, 7.0],
    'hwy': [29, 31, 26, 27, 23, 20, 17, 17, 17, 24]
})

# Test with hat matrix
smoother = stat_smooth(method='loess', span=2/3, se=True)
smoothed_y, hat_diag = smoother.apply_smoothing(data['displ'], data['hwy'], return_hat_diag=True)

print("Hat matrix diagonal values:")
print(f"Min: {hat_diag.min():.6f}")
print(f"Max: {hat_diag.max():.6f}")
print(f"Mean: {hat_diag.mean():.6f}")
print(f"\nValues: {hat_diag}")

# Compute residuals
residuals = data['hwy'] - smoothed_y
residual_std = np.std(residuals, ddof=1)
print(f"\nResidual std: {residual_std:.3f}")

# Show pointwise SE
print("\nPointwise standard errors:")
for i in range(len(data)):
    se_i = residual_std * np.sqrt(hat_diag[i])
    print(f"Point {i}: hat={hat_diag[i]:.4f}, SE={se_i:.3f}")
