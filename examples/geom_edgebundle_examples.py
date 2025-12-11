# notebooks/geom_edgebundle_examples.py
# %% [markdown]
"""
# Force-Directed Edge Bundling Examples

This notebook demonstrates how to use `geom_edgebundle` for creating
bundled graph visualizations that reduce visual clutter.

Based on Holten & Van Wijk (2009) algorithm.
"""

# %% Imports
import numpy as np
import pandas as pd
import os
from ggplotly import (
    ggplot, aes, geom_edgebundle, geom_point, geom_map,
    theme_dark, theme_minimal, theme_classic,
    labs, ggsize
)

# %% [markdown]
"""
## Example 1: Basic Edge Bundling - Parallel Lines

Simple example showing how parallel edges bundle together.
"""

# %% Example 1: Parallel Lines
edges_parallel = pd.DataFrame({
    'x': [0, 0, 0, 0],
    'y': [0, 1, 2, 3],
    'xend': [10, 10, 10, 10],
    'yend': [0, 1, 2, 3]
})

example_01 = (
    ggplot(edges_parallel, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle()
    + labs(title='Parallel Edges Bundle Together')
    + theme_dark()
)
example_01

# %% [markdown]
"""
## Example 2: Circular Layout Network

Edge bundling on a circular layout - common for network visualization.
"""

# %% Example 2: Circular Layout
n_nodes = 20
angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
radius = 10

node_x = radius * np.cos(angles)
node_y = radius * np.sin(angles)

# Create edges connecting nodes to nodes across the circle
edges_circular = []
for i in range(n_nodes):
    for offset in [5, 7, 10]:  # Connect to multiple nodes across
        j = (i + offset) % n_nodes
        edges_circular.append({
            'x': node_x[i],
            'y': node_y[i],
            'xend': node_x[j],
            'yend': node_y[j]
        })

edges_circular_df = pd.DataFrame(edges_circular)
nodes_circular_df = pd.DataFrame({'x': node_x, 'y': node_y})

example_02 = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(compatibility_threshold=0.6)
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='white', size=4)
    + labs(title='Circular Layout with Edge Bundling')
    + theme_dark()
    + ggsize(width=600, height=600)
)
example_02.show()

# %% [markdown]
"""
## Example 3: Random Network Graph

Edge bundling on a random network shows how it reduces clutter.
"""

# %% Example 3: Random Network
np.random.seed(42)
n_nodes_rand = 30
n_edges_rand = 80

# Random node positions using force-directed-like layout
node_x_rand = np.random.uniform(0, 100, n_nodes_rand)
node_y_rand = np.random.uniform(0, 100, n_nodes_rand)

# Random edges
edges_random = []
for _ in range(n_edges_rand):
    i, j = np.random.choice(n_nodes_rand, 2, replace=False)
    edges_random.append({
        'x': node_x_rand[i],
        'y': node_y_rand[i],
        'xend': node_x_rand[j],
        'yend': node_y_rand[j]
    })

edges_random_df = pd.DataFrame(edges_random)
nodes_random_df = pd.DataFrame({'x': node_x_rand, 'y': node_y_rand})

example_03 = (
    ggplot(edges_random_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=5, compatibility_threshold=0.5)
    + geom_point(data=nodes_random_df, mapping=aes(x='x', y='y'),
                 color='#00ff00', size=5)
    + labs(title='Random Network with Edge Bundling')
    + theme_dark()
)
example_03.show()

# %% [markdown]
"""
## Example 4: Grid Layout

Edge bundling on a grid layout - shows bundling of diagonal edges.
"""

# %% Example 4: Grid Layout
grid_size = 5
grid_x = []
grid_y = []
for i in range(grid_size):
    for j in range(grid_size):
        grid_x.append(i * 10)
        grid_y.append(j * 10)

grid_x = np.array(grid_x)
grid_y = np.array(grid_y)

# Create diagonal edges
edges_grid = []
for i in range(len(grid_x)):
    for j in range(i + 1, len(grid_x)):
        # Only create longer edges
        dist = np.sqrt((grid_x[i] - grid_x[j])**2 + (grid_y[i] - grid_y[j])**2)
        if dist > 20:
            edges_grid.append({
                'x': grid_x[i],
                'y': grid_y[i],
                'xend': grid_x[j],
                'yend': grid_y[j]
            })

edges_grid_df = pd.DataFrame(edges_grid)
nodes_grid_df = pd.DataFrame({'x': grid_x, 'y': grid_y})

example_04 = (
    ggplot(edges_grid_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=4, compatibility_threshold=0.6)
    + geom_point(data=nodes_grid_df, mapping=aes(x='x', y='y'),
                 color='white', size=6)
    + labs(title='Grid Layout with Diagonal Edge Bundling')
    + theme_dark()
)
example_04.show()

# %% [markdown]
"""
## Example 5: Custom Colors and Line Width

Customizing the appearance of bundled edges.
"""

# %% Example 5: Custom Colors
example_05 = (
    ggplot(edges_parallel, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(
        color='#00bfff',  # Deep sky blue
        alpha=0.9,
        linewidth=1.5,
        show_highlight=True,
        highlight_width=0.3
    )
    + labs(title='Custom Blue Edge Bundles')
    + theme_dark()
)
example_05.show()

# %% [markdown]
"""
## Example 6: No Highlight Lines

Clean look without white highlight lines.
"""

# %% Example 6: No Highlights
example_06 = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(
        color='#ff6b6b',
        alpha=0.7,
        show_highlight=False
    )
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='white', size=3)
    + labs(title='Red Edge Bundles (No Highlights)')
    + theme_dark()
)
example_06.show()

# %% [markdown]
"""
## Example 7: Different Bundling Strengths

Comparing different compatibility thresholds.
- Low threshold = more edges considered compatible = more bundling
- High threshold = fewer edges compatible = less bundling
"""

# %% Example 7a: Low Threshold
example_07a = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(compatibility_threshold=0.3)
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='white', size=3)
    + labs(title='Low Threshold (0.3) - More Bundling')
    + theme_dark()
)
example_07a.show()

# %% Example 7b: High Threshold
example_07b = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(compatibility_threshold=0.8)
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='white', size=3)
    + labs(title='High Threshold (0.8) - Less Bundling')
    + theme_dark()
)
example_07b.show()

# %% [markdown]
"""
## Example 8: Bipartite Graph

Edge bundling on a bipartite graph layout.
"""

# %% Example 8: Bipartite Graph
n_left = 8
n_right = 8

left_x = np.zeros(n_left)
left_y = np.linspace(0, 70, n_left)
right_x = np.ones(n_right) * 50
right_y = np.linspace(0, 70, n_right)

# Create edges from left to right
edges_bipartite = []
for i in range(n_left):
    for j in range(n_right):
        if (i + j) % 3 == 0:  # Sparse connections
            edges_bipartite.append({
                'x': left_x[i],
                'y': left_y[i],
                'xend': right_x[j],
                'yend': right_y[j]
            })

edges_bipartite_df = pd.DataFrame(edges_bipartite)

left_nodes = pd.DataFrame({'x': left_x, 'y': left_y})
right_nodes = pd.DataFrame({'x': right_x, 'y': right_y})
all_nodes = pd.concat([left_nodes, right_nodes])

example_08 = (
    ggplot(edges_bipartite_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=5, compatibility_threshold=0.6)
    + geom_point(data=all_nodes, mapping=aes(x='x', y='y'),
                 color='white', size=8)
    + labs(title='Bipartite Graph with Edge Bundling')
    + theme_dark()
)
example_08.show()

# %% [markdown]
"""
## Example 9: With Theme Minimal

Edge bundling with light theme.
"""

# %% Example 9: Minimal Theme
example_09 = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(color='#333333', alpha=0.6, show_highlight=False)
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='steelblue', size=4)
    + labs(title='Edge Bundling with Minimal Theme')
    + theme_minimal()
)
example_09.show()

# %% [markdown]
"""
## Example 10: Star Graph

Edge bundling on a star graph (hub-and-spoke pattern).
"""

# %% Example 10: Star Graph
n_spokes = 12
hub_x, hub_y = 0, 0

spoke_angles = np.linspace(0, 2 * np.pi, n_spokes, endpoint=False)
spoke_x = 10 * np.cos(spoke_angles)
spoke_y = 10 * np.sin(spoke_angles)

# Edges from hub to all spokes
edges_star = []
for i in range(n_spokes):
    edges_star.append({
        'x': hub_x, 'y': hub_y,
        'xend': spoke_x[i], 'yend': spoke_y[i]
    })
# Also connect adjacent spokes
for i in range(n_spokes):
    j = (i + 1) % n_spokes
    edges_star.append({
        'x': spoke_x[i], 'y': spoke_y[i],
        'xend': spoke_x[j], 'yend': spoke_y[j]
    })

edges_star_df = pd.DataFrame(edges_star)
nodes_star_df = pd.DataFrame({
    'x': np.concatenate([[hub_x], spoke_x]),
    'y': np.concatenate([[hub_y], spoke_y])
})

example_10 = (
    ggplot(edges_star_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=4, compatibility_threshold=0.5)
    + geom_point(data=nodes_star_df, mapping=aes(x='x', y='y'),
                 color='white', size=6)
    + labs(title='Star Graph with Edge Bundling')
    + theme_dark()
)
example_10.show()

# %% [markdown]
"""
## Example 11: US Flights (Geographic) - Small Sample

Edge bundling on geographic data (auto-detects map context).
Uses a small sample for demonstration.
"""

# %% Example 11: US Flights Sample
airports_df = pd.DataFrame({
    'lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4],
    'lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6],
    'name': ['SFO', 'JFK', 'ORD', 'LAX', 'IAH', 'ATL']
})

flights_sample = pd.DataFrame({
    'src_lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -73.8],
    'src_lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 40.6],
    'dst_lon': [-73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -84.4, -118.4],
    'dst_lat': [40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 33.6, 34.0]
})

example_11 = (
    ggplot(flights_sample, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
    + geom_map(map_type='usa')
    + geom_point(data=airports_df, mapping=aes(x='lon', y='lat'),
                 color='white', size=8)
    + geom_edgebundle(C=4, compatibility_threshold=0.5, verbose=False)
    + labs(title='US Flights with Edge Bundling')
    + theme_dark()
)
example_11.show()

# %% [markdown]
"""
## Example 12: Dense Network

Edge bundling really shines with dense networks.
"""

# %% Example 12: Dense Network
np.random.seed(123)
n_dense = 25
dense_x = np.random.uniform(0, 100, n_dense)
dense_y = np.random.uniform(0, 100, n_dense)

# Create many edges
edges_dense = []
for i in range(n_dense):
    for j in range(i + 1, n_dense):
        dist = np.sqrt((dense_x[i] - dense_x[j])**2 + (dense_y[i] - dense_y[j])**2)
        # Connect if within distance
        if dist < 50:
            edges_dense.append({
                'x': dense_x[i], 'y': dense_y[i],
                'xend': dense_x[j], 'yend': dense_y[j]
            })

edges_dense_df = pd.DataFrame(edges_dense)
nodes_dense_df = pd.DataFrame({'x': dense_x, 'y': dense_y})

example_12 = (
    ggplot(edges_dense_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=5, compatibility_threshold=0.5, alpha=0.6)
    + geom_point(data=nodes_dense_df, mapping=aes(x='x', y='y'),
                 color='#00ff88', size=5)
    + labs(title=f'Dense Network ({len(edges_dense_df)} edges) with Bundling')
    + theme_dark()
)
example_12.show()

# %% [markdown]
"""
## Example 13: Hierarchical Tree Layout

Edge bundling on a tree structure.
"""

# %% Example 13: Tree Layout
tree_nodes = pd.DataFrame({
    'x': [50, 25, 75, 10, 40, 60, 90, 5, 15, 35, 45, 55, 65, 85, 95],
    'y': [100, 70, 70, 40, 40, 40, 40, 10, 10, 10, 10, 10, 10, 10, 10],
    'level': [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]
})

tree_edges = pd.DataFrame({
    'x': [50, 50, 25, 25, 75, 75, 10, 10, 40, 40, 60, 60, 90, 90],
    'y': [100, 100, 70, 70, 70, 70, 40, 40, 40, 40, 40, 40, 40, 40],
    'xend': [25, 75, 10, 40, 60, 90, 5, 15, 35, 45, 55, 65, 85, 95],
    'yend': [70, 70, 40, 40, 40, 40, 10, 10, 10, 10, 10, 10, 10, 10]
})

example_13 = (
    ggplot(tree_edges, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=4, compatibility_threshold=0.4, color='#ff9500')
    + geom_point(data=tree_nodes, mapping=aes(x='x', y='y'),
                 color='white', size=6)
    + labs(title='Hierarchical Tree with Edge Bundling')
    + theme_dark()
)
example_13.show()

# %% [markdown]
"""
## Example 14: Quick Bundling (Reduced Parameters)

For faster bundling, reduce cycles and iterations.
Useful for prototyping or large graphs.
"""

# %% Example 14: Quick Bundling
example_14 = (
    ggplot(edges_dense_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=2, I=20, compatibility_threshold=0.6, verbose=False)
    + geom_point(data=nodes_dense_df, mapping=aes(x='x', y='y'),
                 color='yellow', size=4)
    + labs(title='Quick Bundling (C=2, I=20)')
    + theme_dark()
)
example_14.show()

# %% [markdown]
"""
## Example 15: High Quality Bundling

For publication-quality bundling, increase cycles and iterations.
Takes longer but produces smoother curves.
"""

# %% Example 15: High Quality
example_15 = (
    ggplot(edges_circular_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(C=8, I=80, compatibility_threshold=0.6)
    + geom_point(data=nodes_circular_df, mapping=aes(x='x', y='y'),
                 color='white', size=4)
    + labs(title='High Quality Bundling (C=8, I=80)')
    + theme_dark()
    + ggsize(width=800, height=800)
)
example_15.show()

# %% [markdown]
"""
## Example 16: Full US Flights Dataset (2,682 routes, 276 airports)

Full US flights dataset from the edgebundle R package.
This is the canonical example showing edge bundling at scale.

**NOTE:** This example takes several minutes to compute due to the large
number of edges. Use `verbose=True` to see progress.
"""

# %% Example 16: Load US Flights Data
_data_dir = os.path.join(os.path.dirname(__file__), '..', 'edgebundleexample')
_nodes_path = os.path.join(_data_dir, 'us_flights_nodes.csv')
_edges_path = os.path.join(_data_dir, 'us_flights_edges.csv')

# Only load if files exist
if os.path.exists(_nodes_path) and os.path.exists(_edges_path):
    us_flights_nodes = pd.read_csv(_nodes_path)
    us_flights_edges = pd.read_csv(_edges_path)

    # Get coordinates
    us_coords = us_flights_nodes[['longitude', 'latitude']].values

    # Convert edges to coordinate format
    # Edge file has V1, V2 columns (0-indexed node IDs)
    us_flights_df = pd.DataFrame({
        'x': [us_coords[int(row['V1']), 0] for _, row in us_flights_edges.iterrows()],
        'y': [us_coords[int(row['V1']), 1] for _, row in us_flights_edges.iterrows()],
        'xend': [us_coords[int(row['V2']), 0] for _, row in us_flights_edges.iterrows()],
        'yend': [us_coords[int(row['V2']), 1] for _, row in us_flights_edges.iterrows()]
    })

    us_airports_df = pd.DataFrame({
        'lon': us_flights_nodes['longitude'],
        'lat': us_flights_nodes['latitude'],
        'city': us_flights_nodes['city'],
        'state': us_flights_nodes['state']
    })

    print(f"Loaded US Flights data: {len(us_flights_nodes)} airports, {len(us_flights_df)} routes")
else:
    print("US Flights data not found. Example 16 not available.")
    us_flights_df = None
    us_airports_df = None

# %% Example 16a: US Flights Geographic
if us_flights_df is not None:
    # Full US flights example with geographic projection
    # Uses same parameters as R example: compatibility_threshold=0.6
    K = 1.0
    E = 2.0
    example_16_geo = (
        ggplot(us_flights_df, aes(x='x', y='y', xend='xend', yend='yend'))
        + geom_map(map_type='usa', projection='albers usa')
        + geom_point(
            data=us_airports_df,
            mapping=aes(x='lon', y='lat'),
            color='#9d0191',
            size=3
        )
        + geom_edgebundle(
            K=K,
            E=E,
            C=6,
            P=1,
            S=0.04,
            P_rate=2,
            I=50,
            I_rate=2/3,
            compatibility_threshold=0.6,
            color="#01169d",
            highlight_color='red',
            alpha=0.8,
            highlight_alpha=0.3,
            linewidth=0.5,
            verbose=True  # Show progress for this long computation
        )
        + labs(title=f'US Flights Edge Bundling ({len(us_flights_df)} routes, K = {K})')
        + theme_dark()
        + ggsize(width=1000, height=700)
    )
else:
    example_16_geo = None

example_16_geo

# %% Example 16b: US Flights Simple X-Y
if us_flights_df is not None:
    # Simple X-Y version (non-geographic, faster to render)
    example_16_xy = (
        ggplot(us_flights_df, aes(x='x', y='y', xend='xend', yend='yend'))
        + geom_edgebundle(
            K=1,
            C=6,
            compatibility_threshold=0.6,
            verbose=True
        )
        + geom_point(
            data=us_airports_df,
            mapping=aes(x='lon', y='lat'),
            color='white',
            size=2
        )
        + labs(title=f'US Flights Edge Bundling - Simple X-Y ({len(us_flights_df)} routes)')
        + theme_dark()
        + ggsize(width=1000, height=700)
    )
else:
    example_16_xy = None

example_16_xy

# %% [markdown]
"""
## Summary

To view an example, call `.show()`:
```python
example_01.show()
```

For the full US flights example (takes several minutes):
```python
example_16_geo.show()  # Geographic projection
example_16_xy.show()   # Simple X-Y plot
```
"""

# %% Print Summary
if __name__ == '__main__':
    print("Edge Bundling Examples")
    print("=" * 50)
    print("Example 01: Parallel edges")
    print("Example 02: Circular layout network")
    print("Example 03: Random network graph")
    print("Example 04: Grid layout")
    print("Example 05: Custom colors")
    print("Example 06: No highlights")
    print("Example 07: Different bundling strengths")
    print("Example 08: Bipartite graph")
    print("Example 09: Minimal theme")
    print("Example 10: Star graph")
    print("Example 11: US Flights (Geographic) - Small Sample")
    print("Example 12: Dense network")
    print("Example 13: Tree layout")
    print("Example 14: Quick bundling")
    print("Example 15: High quality bundling")
    print("Example 16: Full US Flights (2,682 routes) - Geographic & X-Y")
    print()
    print("To view an example, call .show():")
    print("  example_01.show()")
    print()
    print("For the full US flights example (takes several minutes):")
    print("  example_16_geo.show()  # Geographic projection")
    print("  example_16_xy.show()   # Simple X-Y plot")
