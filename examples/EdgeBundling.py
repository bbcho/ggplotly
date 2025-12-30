# %%
%load_ext autoreload
%autoreload 2
import os
import sys

from ggplotly import *
import pandas as pd
import numpy as np

# %%
from ggplotly import ggplot, aes, geom_edgebundle

# Create edge data with flow values
edges_df = pd.DataFrame({
    'x': [0.2, 0.5, 0.9],
    'y': [0.6, 0.3, 0.75],
    'xend': [0.5, 0.85, 0.2],
    'yend': [0.3, 0.2, 0.6],
    'flow': [150, 80, 130]
})

# Create bundled visualization
(
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
    + geom_edgebundle(K=0.1, cycles=6, alpha=0.7)
)

# %%
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
n_edges_target = 100

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

# Plot with edge bundling
print("Applying edge bundling...")
(
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.1, compatibility_threshold=0.3, cycles=8, alpha=0.35, width=0.6)
)

# %%
edges_df

# %%
