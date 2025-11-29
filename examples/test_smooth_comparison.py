#!/usr/bin/env python
"""Test script to compare LOESS smoothing results"""

import pandas as pd
import plotly.graph_objects as go
from ggplotly import ggplot, aes, geom_point, geom_smooth

# Create sample data similar to mpg dataset
# Using a pattern that should show U-shape: displ vs hwy
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

# Create plot with default span (0.75)
print("Creating plot with default span=0.75...")
p = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='loess', se=True)
)
fig = p.draw()
fig.write_html('test_smooth_default.html')
print("Saved: test_smooth_default.html")

# Create plot with span=0.3 (more responsive)
print("\nCreating plot with span=0.3...")
p2 = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='loess', span=0.3, se=True)
)
fig2 = p2.draw()
fig2.write_html('test_smooth_span03.html')
print("Saved: test_smooth_span03.html")

# Create plot with span=0.9 (very smooth)
print("\nCreating plot with span=0.9...")
p3 = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='loess', span=0.9, se=True)
)
fig3 = p3.draw()
fig3.write_html('test_smooth_span09.html')
print("Saved: test_smooth_span09.html")

# Create plot with linear method for comparison
print("\nCreating plot with method='lm'...")
p4 = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='lm', se=True)
)
fig4 = p4.draw()
fig4.write_html('test_smooth_lm.html')
print("Saved: test_smooth_lm.html")

print("\n✓ All test plots created successfully!")
print("\nOpen the HTML files to compare:")
print("  - test_smooth_default.html (span=0.75, default)")
print("  - test_smooth_span03.html (span=0.3, more wiggly)")
print("  - test_smooth_span09.html (span=0.9, very smooth)")
print("  - test_smooth_lm.html (linear regression)")
