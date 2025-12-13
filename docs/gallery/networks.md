# Network Graphs

ggplotly provides specialized geoms for network visualization, including force-directed edge bundling for reducing visual clutter in dense graphs.

## Edge Bundling

Edge bundling groups edges that travel in similar directions, making network structure more visible.

### Basic Circular Network

```python
import numpy as np
import pandas as pd
from ggplotly import *

# Create nodes in a circular layout
n_nodes = 20
angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
radius = 10
node_x = radius * np.cos(angles)
node_y = radius * np.sin(angles)

# Create edges across the circle
edges = []
for i in range(n_nodes):
    for offset in [5, 7, 10]:
        j = (i + offset) % n_nodes
        edges.append({
            'x': node_x[i], 'y': node_y[i],
            'xend': node_x[j], 'yend': node_y[j]
        })

edges_df = pd.DataFrame(edges)
nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})

(ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_edgebundle(compatibility_threshold=0.6)
 + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='white', size=4)
 + theme_dark()
 + labs(title='Circular Network with Edge Bundling'))
```

### Random Network

```python
np.random.seed(42)
n_nodes = 30
n_edges = 80

node_x = np.random.uniform(0, 100, n_nodes)
node_y = np.random.uniform(0, 100, n_nodes)

edges = []
for _ in range(n_edges):
    i, j = np.random.choice(n_nodes, 2, replace=False)
    edges.append({
        'x': node_x[i], 'y': node_y[i],
        'xend': node_x[j], 'yend': node_y[j]
    })

edges_df = pd.DataFrame(edges)
nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})

(ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_edgebundle(C=5, compatibility_threshold=0.5)
 + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='#00ff00', size=5)
 + theme_dark()
 + labs(title='Random Network with Edge Bundling'))
```

### Edge Bundling Parameters

`geom_edgebundle` has several parameters to control the bundling behavior:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `K` | 1.0 | Spring constant - higher values resist bundling |
| `E` | 1.0 | Electrostatic constant - higher values increase bundling |
| `C` | 6 | Number of cycles - more cycles = smoother curves |
| `P` | 1 | Initial edge subdivisions |
| `S` | 0.04 | Initial step size |
| `compatibility_threshold` | 0.6 | Minimum edge compatibility (0-1) |
| `color` | '#9d0191' | Edge color |
| `alpha` | 0.8 | Edge transparency |
| `linewidth` | 0.5 | Edge line width |
| `show_highlight` | True | Add highlight effect on edges |
| `highlight_color` | 'white' | Highlight line color |
| `verbose` | True | Print progress messages |

### Weighted Edge Bundling

Edges can have weights that affect how strongly they attract other edges during bundling:

```python
# Edges with weights - heavier edges attract lighter ones
edges_df = pd.DataFrame({
    'x': [0, 0, 0],
    'y': [0, 1, 2],
    'xend': [10, 10, 10],
    'yend': [0, 1, 2],
    'traffic': [100, 10, 10]  # First edge is 10x heavier
})

(ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', weight='traffic'))
 + geom_edgebundle(C=4, compatibility_threshold=0.5)
 + theme_dark())
```

### Using igraph Graphs

`geom_edgebundle` can directly accept igraph Graph objects:

```python
import igraph as ig
from ggplotly import data

# Load built-in US flights network
g = data('us_flights')

(ggplot()
 + geom_map(map_type='usa')
 + geom_edgebundle(graph=g, show_nodes=True, node_color='white', node_size=3)
 + theme_dark()
 + labs(title='US Flight Network'))
```

The graph vertices must have coordinate attributes (`longitude`/`lon`/`x` and `latitude`/`lat`/`y`). Edge weights are automatically detected from the `weight` attribute.

## Edge Bundling on Maps

When `geom_map` is present in the plot, `geom_edgebundle` automatically uses geographic coordinates:

```python
airports = pd.DataFrame({
    'lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4],
    'lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6],
    'name': ['SFO', 'JFK', 'ORD', 'LAX', 'IAH', 'ATL']
})

flights = pd.DataFrame({
    'src_lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -73.8],
    'src_lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 40.6],
    'dst_lon': [-73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -84.4, -118.4],
    'dst_lat': [40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 33.6, 34.0]
})

(ggplot(flights, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
 + geom_map(map_type='usa')
 + geom_point(data=airports, mapping=aes(x='lon', y='lat'), color='white', size=8)
 + geom_edgebundle(C=4, compatibility_threshold=0.5, verbose=False)
 + theme_dark()
 + labs(title='US Flights with Edge Bundling'))
```

## Sea Routes

`geom_searoute` calculates realistic maritime shipping routes that avoid land masses.

!!! note "Requires searoute package"
    Install with: `pip install searoute`

### Basic Sea Routes

```python
shipping_routes = pd.DataFrame({
    'origin': ['Rotterdam', 'Shanghai', 'Los Angeles'],
    'x': [4.48, 121.47, -118.24],       # origin longitude
    'y': [51.92, 31.23, 33.73],         # origin latitude
    'xend': [121.47, -74.01, 4.48],     # destination longitude
    'yend': [31.23, 40.71, 51.92]       # destination latitude
})

(ggplot(shipping_routes, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_map(map_type='world')
 + geom_searoute(color='steelblue', linewidth=1.0)
 + theme_dark()
 + labs(title='Maritime Shipping Routes'))
```

### Routes with Restrictions

Force routes to avoid certain passages (e.g., for geopolitical or capacity reasons):

```python
(ggplot(shipping_routes, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_map(map_type='world')
 + geom_searoute(
     restrictions=['suez'],  # Routes go around Cape of Good Hope
     color='#ff6b35',
     show_highlight=True,
     show_ports=True,
     port_color='#00ff88',
     verbose=True  # Shows route distances
 )
 + theme_dark()
 + labs(title='Shipping Routes Avoiding Suez Canal'))
```

### Sea Route Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `restrictions` | [] | Passages to avoid: 'suez', 'panama', 'northwest', 'northeast' |
| `color` | '#9d0191' | Route line color |
| `linewidth` | 0.5 | Line width |
| `show_highlight` | True | Add glow effect |
| `show_ports` | False | Show origin/destination markers |
| `port_color` | 'white' | Port marker color |
| `port_size` | 5 | Port marker size |
| `verbose` | False | Print route distances |

## Caching

Edge bundling is computationally expensive. Results are automatically cached at the module level, so repeated plots with the same data and parameters are instant:

```python
from ggplotly.stats.stat_edgebundle import clear_bundling_cache

# Clear cache if needed (e.g., memory constraints)
clear_bundling_cache()
```

The cache key includes:
- Edge coordinates (x, y, xend, yend)
- Edge weights (if provided)
- All algorithm parameters (K, E, C, P, S, etc.)
