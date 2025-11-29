#!/usr/bin/env python
"""
Circular graph demo with 20 nodes and 200 edges.
"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle

np.random.seed(42)

# Create 20 nodes in a circle
n_nodes = 20
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
radius = 1.0

nodes = []
for i, angle in enumerate(angles):
    nodes.append({
        'id': i,
        'x': radius * np.cos(angle),
        'y': radius * np.sin(angle)
    })

nodes_df = pd.DataFrame(nodes)

# Create 200 edges
edges = []
n_edges_target = 200

# Create random edges between nodes
while len(edges) < n_edges_target:
    i = np.random.randint(0, n_nodes)
    j = np.random.randint(0, n_nodes)

    if i != j:
        edges.append({
            'x': nodes[i]['x'],
            'y': nodes[i]['y'],
            'xend': nodes[j]['x'],
            'yend': nodes[j]['y']
        })

edges_df = pd.DataFrame(edges)
print(f"Created {len(edges_df)} edges between {n_nodes} nodes")

# Plot with edge bundling (test 1 cycle with corrected formulas)
print("Applying edge bundling...")
p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.1, compatibility_threshold=0.6, cycles=1, alpha=0.35, width=0.6)
)

fig = p.draw()

# Add nodes
import plotly.graph_objects as go
fig.add_trace(
    go.Scatter(
        x=nodes_df['x'],
        y=nodes_df['y'],
        mode='markers',
        marker=dict(size=8, color='darkred', opacity=0.8, line=dict(width=1, color='white')),
        showlegend=False,
        hoverinfo='skip'
    )
)

fig.update_layout(
    title=f"Circular Graph: {n_nodes} nodes, {len(edges_df)} edges",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
    width=1000,
    height=1000
)

fig.write_html('circular_demo_20_200.html')
print("Created: circular_demo_20_200.html")
print("✓ Done!")
