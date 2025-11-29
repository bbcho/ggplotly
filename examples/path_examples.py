# geom_path examples - connecting points in data order
# Key difference from geom_line: NO sorting by x-axis

import pandas as pd
import math
from ggplotly import ggplot, aes, geom_path, geom_line, geom_point, ggsave, labs

# =============================================================================
# Example 1: Spiral - demonstrates why geom_path matters
# =============================================================================
# X values are NOT monotonic (they go back and forth)
t_vals = [i * 4 * math.pi / 100 for i in range(100)]
spiral = pd.DataFrame({
    'x': [t * math.cos(t) for t in t_vals],
    'y': [t * math.sin(t) for t in t_vals],
    't': t_vals
})

# geom_path: connects in data order - draws the spiral correctly
plot_spiral = (
    ggplot(spiral, aes(x='x', y='y'))
    + geom_path(color='steelblue', size=2)
    + labs(title='Spiral with geom_path (correct)')
)
ggsave(plot_spiral, 'examples/path_spiral.html')
print("Created: examples/path_spiral.html")

# geom_line: sorts by x first - WRONG for spirals!
plot_spiral_wrong = (
    ggplot(spiral, aes(x='x', y='y'))
    + geom_line(color='red', size=2)
    + labs(title='Spiral with geom_line (wrong - sorted by x)')
)
ggsave(plot_spiral_wrong, 'examples/path_spiral_wrong.html')
print("Created: examples/path_spiral_wrong.html")

# =============================================================================
# Example 2: Connected scatterplot (Gapminder-style)
# =============================================================================
# GDP vs Life Expectancy over time for a few countries
gapminder_sample = pd.DataFrame({
    'country': ['USA']*5 + ['China']*5 + ['Brazil']*5,
    'year': [1960, 1980, 2000, 2010, 2020] * 3,
    'gdp_per_capita': [
        # USA
        3007, 12575, 36330, 48468, 63028,
        # China
        90, 195, 959, 4550, 10500,
        # Brazil
        210, 1947, 3749, 11286, 6797
    ],
    'life_exp': [
        # USA
        69.8, 73.7, 76.6, 78.5, 77.0,
        # China
        43.7, 66.8, 71.4, 75.0, 77.1,
        # Brazil
        54.7, 62.7, 70.3, 73.1, 75.9
    ]
})

# Connected scatterplot - trace each country's trajectory over time
plot_gapminder = (
    ggplot(gapminder_sample, aes(x='gdp_per_capita', y='life_exp', color='country'))
    + geom_path(size=2)
    + geom_point(size=8)
    + labs(
        title='GDP vs Life Expectancy Over Time',
        x='GDP per Capita (USD)',
        y='Life Expectancy (years)'
    )
)
ggsave(plot_gapminder, 'examples/path_gapminder.html')
print("Created: examples/path_gapminder.html")

# =============================================================================
# Example 3: Movement trajectory / GPS track
# =============================================================================
# Simulated random walk (like GPS coordinates)
import random
random.seed(42)

x, y = 0, 0
track_x, track_y, track_time = [0], [0], [0]
for t in range(1, 50):
    x += random.uniform(-1, 1)
    y += random.uniform(-1, 1)
    track_x.append(x)
    track_y.append(y)
    track_time.append(t)

trajectory = pd.DataFrame({
    'x': track_x,
    'y': track_y,
    'time': track_time
})

plot_trajectory = (
    ggplot(trajectory, aes(x='x', y='y'))
    + geom_path(color='darkgreen', size=1.5, alpha=0.7)
    + geom_point(size=4, color='darkgreen')
    + labs(title='Random Walk Trajectory')
)
ggsave(plot_trajectory, 'examples/path_trajectory.html')
print("Created: examples/path_trajectory.html")

# =============================================================================
# Example 4: Drawing a shape (polygon without fill)
# =============================================================================
# Draw a star
points = 5
outer_r, inner_r = 1, 0.4
star_x, star_y = [], []
for i in range(points * 2 + 1):  # +1 to close the shape
    angle = i * math.pi / points - math.pi / 2
    r = outer_r if i % 2 == 0 else inner_r
    star_x.append(r * math.cos(angle))
    star_y.append(r * math.sin(angle))

star = pd.DataFrame({'x': star_x, 'y': star_y})

plot_star = (
    ggplot(star, aes(x='x', y='y'))
    + geom_path(color='gold', size=3)
    + labs(title='Star drawn with geom_path')
)
ggsave(plot_star, 'examples/path_star.html')
print("Created: examples/path_star.html")

print("\nAll examples created successfully!")
print("\nKey takeaway:")
print("  - geom_path: connects points in DATA ORDER")
print("  - geom_line: connects points sorted by X-AXIS")
