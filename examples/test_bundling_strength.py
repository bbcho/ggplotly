#!/usr/bin/env python
"""Quick test to verify bundling is visible."""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle

np.random.seed(42)

# Create a simple star pattern - should show clear bundling
center_x, center_y = 0.5, 0.5
n_outer = 20
angles = np.linspace(0, 2*np.pi, n_outer, endpoint=False)
radius = 0.4

edges = []
for i, angle in enumerate(angles):
    x_outer = center_x + radius * np.cos(angle)
    y_outer = center_y + radius * np.sin(angle)

    # Each outer node connects to center
    edges.append({
        'x': x_outer,
        'y': y_outer,
        'xend': center_x,
        'yend': center_y,
        'type': 'radial'
    })

    # Also connect to opposite node (crossing edges - should bundle)
    opposite_idx = (i + n_outer // 2) % n_outer
    x_opposite = center_x + radius * np.cos(angles[opposite_idx])
    y_opposite = center_y + radius * np.sin(angles[opposite_idx])

    edges.append({
        'x': x_outer,
        'y': y_outer,
        'xend': x_opposite,
        'yend': y_opposite,
        'type': 'crossing'
    })

edges_df = pd.DataFrame(edges)
print(f"Created {len(edges_df)} edges")

# Test with moderate bundling (test 1 cycle only)
p = (
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_edgebundle(K=0.5, cycles=1, alpha=0.5, width=1.0)
)

fig = p.draw()
fig.update_layout(
    title="Bundling Test - Moderate Strength (K=0.5)",
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    width=800,
    height=800
)
fig.write_html('bundling_test.html')
print("Created: bundling_test.html")
print("✓ If bundling is working, crossing edges should form visible bundles!")
