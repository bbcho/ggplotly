#!/usr/bin/env python
"""Test script to check 1 standard deviation confidence band"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_point, geom_smooth
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

# Test with default level (0.68 - 1 stdev)
print("Testing confidence band with default level (0.68 - 1 standard deviation)...")
smoother = stat_smooth(method='loess', span=2/3, se=True)  # Use default level
smoothed_data = smoother.compute_stat(data.copy(), x_col='displ', y_col='hwy')

# Sort by x for viewing
smoothed_sorted = smoothed_data.sort_values('displ')

# Check band width
smoothed_sorted['band_width'] = smoothed_sorted['ymax'] - smoothed_sorted['ymin']
print("\nBand width statistics:")
print(f"Mean band width: {smoothed_sorted['band_width'].mean():.2f}")
print(f"Min band width:  {smoothed_sorted['band_width'].min():.2f}")
print(f"Max band width:  {smoothed_sorted['band_width'].max():.2f}")

# Check if bands cover the original data reasonably
coverage = ((data['hwy'] >= smoothed_data['ymin']) & (data['hwy'] <= smoothed_data['ymax'])).sum()
coverage_pct = 100 * coverage / len(data)
print(f"\nCoverage: {coverage}/{len(data)} points ({coverage_pct:.1f}%) within confidence band")
print("(Should be around 68% for 1 standard deviation)")

# Create plot with default confidence band
print("\nCreating plot with default 1-stdev confidence band...")
p = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth()  # Use all defaults including level=0.68
)
fig = p.draw()
fig.write_html('test_1stdev_band.html')
print("Saved: test_1stdev_band.html")

print("\n✓ 1 standard deviation confidence band test complete")
