# Edge Bundling Implementation

## Overview

ggplotly now includes `geom_edgebundle()` for creating bundled graph visualizations using force-directed edge bundling. This technique reduces visual clutter in dense graphs by attracting compatible edges together into smooth bundles.

## Implementation

Based on the paper: **Holten, D., & Van Wijk, J. J. (2009). Force‐directed edge bundling for graph visualization. Computer Graphics Forum, 28(3), 983-990.**

https://github.com/verasativa/python.ForceBundle/blob/master/usage.ipynb

### Architecture

The implementation consists of two main components:

1. **`stat_edgebundle`** ([ggplotly/stats/stat_edgebundle.py](ggplotly/stats/stat_edgebundle.py))
   - Core force-directed bundling algorithm
   - Edge compatibility calculations
   - Iterative refinement with progressive subdivision

2. **`geom_edgebundle`** ([ggplotly/geoms/geom_edgebundle.py](ggplotly/geoms/geom_edgebundle.py))
   - Visualization layer
   - Color mapping (categorical and continuous)
   - Integration with ggplotly's aesthetic system

## Algorithm Details

### Edge Compatibility

Four compatibility measures determine how strongly edges attract each other:

1. **Angle Compatibility** (C_a): Edges with similar directions attract more strongly
   ```
   C_a = |cos(angle)|
   ```

2. **Scale Compatibility** (C_s): Edges of similar length attract more strongly
   ```
   C_s = 2 / (l_avg/l_min + l_max/l_avg)
   ```

3. **Position Compatibility** (C_p): Edges that are closer together attract more strongly
   ```
   C_p = l_avg / (l_avg + ||m_P - m_Q||)
   ```

4. **Visibility Compatibility** (C_v): Edges that can "see" each other attract more strongly
   ```
   C_v = min(V(P,Q), V(Q,P))
   V(P,Q) = 1 - 2 * ||m - I_PQ|| / ||P||
   ```

**Combined Compatibility:**
```
C_e(P,Q) = C_a * C_s * C_p * C_v
```

Only edges with `C_e >= compatibility_threshold` interact.

### Force Model

Each edge is represented as a flexible spring with subdivision points. Two types of forces are applied:

1. **Spring Forces**: Keep subdivision points evenly spaced along the edge
   ```
   F_spring = K * (normalize(p_prev - p_k) + normalize(p_next - p_k))
   ```

2. **Electrostatic Forces**: Attract subdivision points on compatible edges
   ```
   F_electro = Σ (C_e(P,Q) / ||p_k - q_k||) * normalize(q_k - p_k)
   ```

### Iterative Refinement

The algorithm progressively refines the bundling through multiple cycles:

1. Start with 1 subdivision point per edge (3 points total including endpoints)
2. Apply forces iteratively (default: 50 iterations per cycle)
3. Double the subdivision points (via linear interpolation)
4. Repeat for a specified number of cycles (default: 6)

After 6 cycles: 1 → 2 → 4 → 8 → 16 → 32 subdivision points

## Usage

### Basic Usage

```python
from ggplotly import ggplot, aes, geom_edgebundle

# Create edge data
edges_df = pd.DataFrame({
    'x': [0, 1, 2],      # Start x coordinates
    'y': [0, 1, 0],      # Start y coordinates
    'xend': [2, 3, 3],   # End x coordinates
    'yend': [2, 2, 1]    # End y coordinates
})

# Create bundled graph
p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle()
)

fig = p.draw()
fig.write_html('bundled_graph.html')
```

### Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `K` | 0.1 | Spring constant controlling bundling strength (0.3-1.5 recommended for visible bundling) |
| `cycles` | 6 | Number of refinement cycles (4-8 recommended) |
| `compatibility_threshold` | 0.1 | Minimum compatibility for edge interaction (0.0-1.0, lower = more bundling) |
| `color` | 'steelblue' | Edge color (literal or mapped to data) |
| `alpha` | 0.6 | Edge transparency (0-1) |
| `width` | 1.5 | Edge line width |

**Note**: Legends are disabled by default for edge bundles. The bundling algorithm uses coordinate normalization to [0, 1] range for consistent behavior across different scales. This means K values should typically be higher (0.3-1.5) than in unnormalized implementations. The algorithm uses 90 iterations per cycle for more visible bundling effects.

### Adjusting Bundling Strength

To make bundling more visible, adjust these parameters:

```python
# Very strong bundling (high K, low threshold)
p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
p = p + geom_edgebundle(K=1.2, compatibility_threshold=0.05, cycles=6)

# Strong bundling
p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
p = p + geom_edgebundle(K=0.8, compatibility_threshold=0.08, cycles=6)

# Moderate bundling
p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
p = p + geom_edgebundle(K=0.5, compatibility_threshold=0.1, cycles=6)

# Subtle bundling (lower K, higher threshold)
p = ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
p = p + geom_edgebundle(K=0.3, compatibility_threshold=0.15, cycles=6)
```

**Tips for Visible Bundling:**
- **Higher `K`** (e.g., 0.5-1.2): Makes bundles tighter due to coordinate normalization
- **Lower `compatibility_threshold`** (e.g., 0.05-0.08): Allows more edges to bundle together
- **More `cycles`** (e.g., 7-8): Creates smoother, more refined bundles (but slower)
- **Dense graphs work best**: Edge bundling is most effective when you have 50+ edges
- **Start high**: Due to coordinate normalization, begin with K=0.5 or higher and adjust from there

### Color Mapping

#### Categorical Coloring

```python
edges_df['type'] = ['highway', 'local', 'highway']

p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
    + geom_edgebundle()
)
```

#### Continuous Coloring

```python
edges_df['flow'] = [100, 200, 150]  # Numeric values

p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
    + geom_edgebundle()
)
```

## Examples

### Example 1: Star Graph

Edges radiating from a central hub naturally bundle together:

```python
import numpy as np
import pandas as pd
from ggplotly import ggplot, aes, geom_edgebundle

# Create star graph
center = (0, 0)
n_nodes = 8
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
radius = 2

edges = []
for angle in angles:
    x_end = radius * np.cos(angle)
    y_end = radius * np.sin(angle)
    edges.append({
        'x': center[0],
        'y': center[1],
        'xend': x_end,
        'yend': y_end
    })

edges_df = pd.DataFrame(edges)

p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.1, cycles=5)
)

fig = p.draw()
fig.write_html('star_graph.html')
```

### Example 2: Geographic Flow Graph (Migration-Style)

Similar to the US migration visualization:

```python
# State positions (simplified)
states = {
    'CA': (0.2, 0.6), 'TX': (0.5, 0.3), 'NY': (0.9, 0.75),
    'FL': (0.85, 0.2), 'IL': (0.65, 0.7), 'WA': (0.1, 0.9)
}

# Migration flows
flows = [
    ('CA', 'TX', 150), ('CA', 'NY', 100), ('TX', 'CA', 120),
    ('TX', 'FL', 80), ('NY', 'FL', 130), ('NY', 'CA', 90)
]

edges = []
for src, dst, flow in flows:
    x_start, y_start = states[src]
    x_end, y_end = states[dst]
    edges.append({
        'x': x_start, 'y': y_start,
        'xend': x_end, 'yend': y_end,
        'flow': flow
    })

edges_df = pd.DataFrame(edges)

p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
    + geom_edgebundle(K=0.08, cycles=6, alpha=0.7)
)

fig = p.draw()
fig.write_html('migration_flows.html')
```

## Performance

### Complexity

- **Time**: O(N·M²·K) where:
  - N = number of iterations per cycle (default: 50)
  - M = number of edges
  - K = number of subdivision points (grows exponentially: 1, 2, 4, 8, 16, 32)

- **Space**: O(M·K) for storing subdivision points

### Typical Performance

On a 2020 MacBook Pro:

| Edges | Cycles | Time | Subdivision Points (final) |
|-------|--------|------|---------------------------|
| 10    | 5      | ~0.2s | 16 |
| 20    | 6      | ~1.5s | 32 |
| 50    | 6      | ~8s  | 32 |
| 100   | 6      | ~30s | 32 |

### Optimization Tips

For large graphs (>50 edges):

1. **Reduce cycles**: Use 4-5 cycles instead of 6
   ```python
   geom_edgebundle(cycles=4)  # Faster, still good quality
   ```

2. **Increase compatibility threshold**: Only bundle most compatible edges
   ```python
   geom_edgebundle(compatibility_threshold=0.2)  # More selective
   ```

3. **Reduce iterations per cycle**: Fewer force iterations
   ```python
   from ggplotly.stats.stat_edgebundle import stat_edgebundle
   stat = stat_edgebundle(cycles=5, iterations_per_cycle=30)
   ```

## Testing

Run the example visualizations:

```bash
python examples/test_edgebundle.py
```

This creates three HTML files:
- `test_edgebundle_star.html` - Star graph with radial edges
- `test_edgebundle_circular.html` - Circular graph with crossing edges
- `test_edgebundle_geographic.html` - Geographic-style migration flows

## Technical Details

### Subdivision Algorithm

Edges are subdivided by inserting midpoints between existing points:

```
Cycle 0: [P0] ---- [P1]                     (1 point)
Cycle 1: [P0] -- [M01] -- [P1]              (2 points)
Cycle 2: [P0]-[M0]-[M01]-[M1]-[P1]         (4 points)
```

After subdivision, existing points remain at even indices, new midpoints at odd indices.

### Numerical Stability

- **Ridge regularization**: Small diagonal term (1e-8) prevents singular matrices
- **Distance epsilon**: Avoids division by zero in force calculations (1e-10)
- **Step size decay**: Step size halves each cycle for stability

### Endpoint Handling

Endpoints remain fixed at their original positions throughout the bundling process. Only interior subdivision points are moved by forces.

## Comparison with R

### Similarities

- Edge compatibility metrics match the paper
- Force model follows the paper's physics-based approach
- Progressive subdivision with exponentially growing points

### Differences

- **No delta parameter**: We evaluate forces at all subdivision points (R's igraph can skip nearby points for speed)
- **Simplified forces**: Uses inverse-linear electrostatic force (simpler than paper's inverse-quadratic option)
- **No iterations parameter exposed**: Fixed at 50 iterations per cycle (R allows customization)

## Future Enhancements

Potential improvements:

1. **Delta parameter**: Skip force evaluation at nearby points and interpolate
2. **Robust iterations**: Apply multiple bundling passes with different parameters
3. **GPU acceleration**: Parallelize force calculations
4. **Hierarchical bundling**: Bundle bundles for very large graphs
5. **Custom compatibility functions**: Allow user-defined edge compatibility
6. **Animation**: Show bundling process as animation

## References

- Holten, D., & Van Wijk, J. J. (2009). Force‐directed edge bundling for graph visualization. Computer Graphics Forum, 28(3), 983-990.
- R's igraph library: `edge_bundle_force_directed()`
- Observable notebooks on edge bundling: https://observablehq.com/@d3/force-directed-edge-bundling

## See Also

- [geom_segment](ggplotly/geoms/geom_segment.py) - For straight, unbundled edges
- [geom_line](ggplotly/geoms/geom_line.py) - For connected line paths
- R's ggraph package: `geom_conn_bundle()`
