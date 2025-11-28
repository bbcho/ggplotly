#!/usr/bin/env python
"""Test the new LOESS method with degree-2 polynomials"""

import pandas as pd
from ggplotly import ggplot, aes, geom_point, geom_smooth

# Create sample data
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

print("Testing new LOESS method (degree=2, default)...")
p1 = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='loess', se=True)
)
fig1 = p1.draw()
fig1.write_html('test_loess_degree2.html')
print("Saved: test_loess_degree2.html")

print("\nTesting LOWESS method (statsmodels, degree=1)...")
p2 = (
    ggplot(data, aes(x='displ', y='hwy'))
    + geom_point(alpha=0.5)
    + geom_smooth(method='lowess', se=True)
)
fig2 = p2.draw()
fig2.write_html('test_lowess_degree1.html')
print("Saved: test_lowess_degree1.html")

print("\n✓ Both methods tested successfully!")
print("  - loess (default): Custom implementation with degree-2 polynomials")
print("  - lowess: statsmodels implementation with degree-1 polynomials")
