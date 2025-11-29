#!/usr/bin/env python
"""Test K scaling with different coordinate systems."""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle

np.random.seed(42)

def create_graph_at_scale(scale_factor, n_nodes=20, n_edges=50):
    """Create a circular graph at a specific coordinate scale."""
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = scale_factor

    nodes = [
        (radius * np.cos(a), radius * np.sin(a))
        for a in angles
    ]

    edges = []
    while len(edges) < n_edges:
        i = np.random.randint(0, n_nodes)
        j = np.random.randint(0, n_nodes)
        if i != j:
            edges.append({
                'x': nodes[i][0], 'y': nodes[i][1],
                'xend': nodes[j][0], 'yend': nodes[j][1]
            })

    return pd.DataFrame(edges)

# Test 1: Small coordinates (unit scale: -1 to +1)
print("=" * 70)
print("Test 1: Unit scale (coordinates: -1 to +1)")
print("=" * 70)
edges_small = create_graph_at_scale(1.0)
print(f"Created {len(edges_small)} edges")

p1 = (
    ggplot(edges_small, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.5, cycles=1, alpha=0.5, width=0.8)
)
fig1 = p1.draw()
fig1.update_layout(title="Unit Scale (r=1, K=0.5, 1 cycle)")
fig1.write_html('test_scale_unit.html')
print("Created: test_scale_unit.html\n")

# Test 2: Medium coordinates (10x scale: -10 to +10)
print("=" * 70)
print("Test 2: Medium scale (coordinates: -10 to +10)")
print("=" * 70)
edges_medium = create_graph_at_scale(10.0)
print(f"Created {len(edges_medium)} edges")

p2 = (
    ggplot(edges_medium, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.5, cycles=1, alpha=0.5, width=0.8)
)
fig2 = p2.draw()
fig2.update_layout(title="Medium Scale (r=10, K=0.5, 1 cycle)")
fig2.write_html('test_scale_medium.html')
print("Created: test_scale_medium.html\n")

# Test 3: Large coordinates (100x scale: -100 to +100)
print("=" * 70)
print("Test 3: Large scale (coordinates: -100 to +100)")
print("=" * 70)
edges_large = create_graph_at_scale(100.0)
print(f"Created {len(edges_large)} edges")

p3 = (
    ggplot(edges_large, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.5, cycles=1, alpha=0.5, width=0.8)
)
fig3 = p3.draw()
fig3.update_layout(title="Large Scale (r=100, K=0.5, 1 cycle)")
fig3.write_html('test_scale_large.html')
print("Created: test_scale_large.html\n")

print("=" * 70)
print("✓ Scale invariance test complete!")
print("=" * 70)
print("\nWith automatic K scaling, all three graphs should show similar")
print("bundling behavior despite having coordinates that differ by 100x.")
print("\nThe scaled K values should be proportional to the average edge length:")
print("  - Unit scale (r=1):   K scaled to ~0.5 * 1.4 = 0.7")
print("  - Medium scale (r=10): K scaled to ~0.5 * 14 = 7")
print("  - Large scale (r=100): K scaled to ~0.5 * 140 = 70")
