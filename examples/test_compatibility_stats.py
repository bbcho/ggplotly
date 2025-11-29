#!/usr/bin/env python
"""Test how many edges are compatible at different thresholds"""

import pandas as pd
import numpy as np
from ggplotly.stats.stat_edgebundle import stat_edgebundle

np.random.seed(42)

# Create 20 nodes in a circle
n_nodes = 20
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
radius = 1.0

nodes = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

# Create 200 edges
edges = []
n_edges_target = 200
while len(edges) < n_edges_target:
    i = np.random.randint(0, n_nodes)
    j = np.random.randint(0, n_nodes)
    if i != j:
        edges.append({
            'x': nodes[i][0],
            'y': nodes[i][1],
            'xend': nodes[j][0],
            'yend': nodes[j][1],
            'edge_id': len(edges)
        })

edges_df = pd.DataFrame(edges)
print(f"Created {len(edges_df)} edges")
print()

# Test different compatibility thresholds
for threshold in [0.1, 0.3, 0.6]:
    stat = stat_edgebundle(K=0.1, compatibility_threshold=threshold, cycles=1, iterations_per_cycle=1)

    # Access the internal method to compute compatibility
    edges_list = []
    for idx, row in edges_df.iterrows():
        edges_list.append({
            'edge_id': row['edge_id'],
            'p0': np.array([row['x'], row['y']]),
            'p1': np.array([row['xend'], row['yend']]),
            'initial_length': np.linalg.norm(np.array([row['xend'], row['y']]) - np.array([row['x'], row['y']]))
        })

    compatibility = stat._compute_compatibility_matrix(edges_list)

    n_compatible_pairs = np.sum(compatibility > 0) // 2
    avg_neighbors = np.sum(compatibility > 0, axis=1).mean()

    print(f"Threshold {threshold}:")
    print(f"  Compatible pairs: {n_compatible_pairs}")
    print(f"  Avg compatible neighbors per edge: {avg_neighbors:.1f}")
    print()

print("INSIGHT: Higher threshold dramatically reduces interactions!")
print("With threshold=0.6, most edges have very few neighbors.")
print("With threshold=0.1, edges have MANY neighbors = force explosion.")
