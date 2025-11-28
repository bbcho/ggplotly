#!/usr/bin/env python
"""Test script to examine actual smoothed values"""

import pandas as pd
import numpy as np
from ggplotly.stats.stat_smooth import stat_smooth

# Create sample data similar to mpg dataset
data = pd.DataFrame({
    'displ': [1.8, 1.8, 2.0, 2.0, 2.8, 2.8, 3.1, 1.8, 1.8, 2.0, 2.0, 2.8,
              2.8, 3.1, 3.1, 2.8, 3.1, 4.2, 5.3, 5.3, 5.3, 5.7, 6.0, 5.7,
              5.7, 6.2, 6.2, 7.0, 5.3, 5.3, 5.7, 6.5, 2.4, 2.4, 3.1, 2.0,
              2.0, 2.0, 2.0, 2.0, 2.7, 2.7, 2.7, 3.0, 3.7, 4.0, 4.7, 5.7,
              6.1, 2.2, 2.2, 2.4, 2.4, 3.3, 3.3, 3.3, 3.3, 3.8, 3.8, 4.0],
    'hwy': [29, 29, 31, 30, 26, 26, 27, 26, 25, 28, 27, 25, 25, 25,
            24, 27, 25, 23, 20, 15, 20, 17, 17, 26, 23, 26, 25, 24,
            19, 14, 15, 17, 27, 30, 26, 29, 26, 29, 24, 24, 22, 22,
            24, 24, 17, 22, 21, 23, 23, 19, 18, 17, 17, 19, 19, 12,
            17, 15, 17, 17]
})

# Test LOESS with default span
print("Testing LOESS with span=0.75...")
smoother = stat_smooth(method='loess', span=0.75, se=True, level=0.95)
smoothed_data = smoother.compute_stat(data.copy(), x_col='displ', y_col='hwy')

# Sort by x for better viewing
smoothed_sorted = smoothed_data.sort_values('displ')

print("\nFirst 10 rows (sorted by displ):")
print(smoothed_sorted[['displ', 'hwy', 'ymin', 'ymax']].head(10))

print("\nLast 10 rows (sorted by displ):")
print(smoothed_sorted[['displ', 'hwy', 'ymin', 'ymax']].tail(10))

# Check for U-shape: values should be high at low displ,
# decrease in the middle, then potentially level off or increase slightly
print("\n\nChecking for U-shape pattern:")
low_displ = smoothed_sorted[smoothed_sorted['displ'] < 2.5]['hwy'].mean()
mid_displ = smoothed_sorted[(smoothed_sorted['displ'] >= 2.5) & (smoothed_sorted['displ'] < 4.5)]['hwy'].mean()
high_displ = smoothed_sorted[smoothed_sorted['displ'] >= 4.5]['hwy'].mean()

print(f"Average smoothed hwy for displ < 2.5:     {low_displ:.2f}")
print(f"Average smoothed hwy for 2.5 <= displ < 4.5: {mid_displ:.2f}")
print(f"Average smoothed hwy for displ >= 4.5:    {high_displ:.2f}")

# Check smoothness - consecutive values shouldn't jump around too much
print("\n\nChecking smoothness (first differences):")
diffs = smoothed_sorted['hwy'].diff().dropna()
print(f"Mean absolute difference: {abs(diffs).mean():.3f}")
print(f"Max absolute difference:  {abs(diffs).max():.3f}")
print(f"Std of differences:       {diffs.std():.3f}")

# Show the differences to spot any jumps
print("\nLargest jumps (absolute differences > 0.5):")
large_jumps = smoothed_sorted.copy()
large_jumps['diff'] = large_jumps['hwy'].diff()
large_jumps = large_jumps[abs(large_jumps['diff']) > 0.5]
if len(large_jumps) > 0:
    print(large_jumps[['displ', 'hwy', 'diff']])
else:
    print("No large jumps found - smooth!")

print("\n✓ Smoothed values examination complete")
