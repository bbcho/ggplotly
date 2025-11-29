#!/usr/bin/env python
"""
Test script for geom_edgebundle with sample graph data.

Creates several example visualizations showing edge bundling:
1. Simple star graph
2. Circular graph with crossing edges
3. Geographic-style graph (similar to migration flows)
"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes
from ggplotly.geoms.geom_edgebundle import geom_edgebundle
from ggplotly.geoms.geom_point import geom_point


def create_star_graph():
    """Create a simple star graph with one central node."""
    print("\n=== Test 1: Star Graph ===")

    # Center node
    center_x, center_y = 0, 0

    # Peripheral nodes in a circle
    n_nodes = 8
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 2

    edges = []
    for i, angle in enumerate(angles):
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)
        edges.append({
            'x': center_x,
            'y': center_y,
            'xend': x,
            'yend': y,
            'flow': np.random.randint(50, 200)
        })

    edges_df = pd.DataFrame(edges)

    # Create nodes dataframe
    nodes = [{'x': center_x, 'y': center_y}]
    for angle in angles:
        nodes.append({
            'x': radius * np.cos(angle),
            'y': radius * np.sin(angle)
        })
    nodes_df = pd.DataFrame(nodes)

    # Plot
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
        + geom_edgebundle(K=0.1, cycles=5, alpha=0.6, width=1.5)
    )

    fig = p.draw()
    fig.update_layout(
        title="Star Graph with Edge Bundling",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        width=600,
        height=600
    )
    fig.write_html('test_edgebundle_star.html')
    print("Created: test_edgebundle_star.html")


def create_circular_graph():
    """Create a circular graph with crossing edges."""
    print("\n=== Test 2: Circular Graph ===")

    # Place nodes in a circle
    n_nodes = 12
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 3

    node_positions = []
    for i, angle in enumerate(angles):
        node_positions.append({
            'id': i,
            'x': radius * np.cos(angle),
            'y': radius * np.sin(angle)
        })

    nodes_df = pd.DataFrame(node_positions)

    # Create edges with various connection patterns
    edges = []

    # Connect opposite nodes
    for i in range(n_nodes // 2):
        j = (i + n_nodes // 2) % n_nodes
        edges.append({
            'x': nodes_df.loc[i, 'x'],
            'y': nodes_df.loc[i, 'y'],
            'xend': nodes_df.loc[j, 'x'],
            'yend': nodes_df.loc[j, 'y'],
            'type': 'opposite'
        })

    # Connect neighbors with distance 2
    for i in range(n_nodes):
        j = (i + 2) % n_nodes
        edges.append({
            'x': nodes_df.loc[i, 'x'],
            'y': nodes_df.loc[i, 'y'],
            'xend': nodes_df.loc[j, 'x'],
            'yend': nodes_df.loc[j, 'y'],
            'type': 'near'
        })

    edges_df = pd.DataFrame(edges)

    # Plot with colored edges
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
        + geom_edgebundle(K=0.12, cycles=6, compatibility_threshold=0.15,
                         alpha=0.5, width=2.0)
    )

    fig = p.draw()
    fig.update_layout(
        title="Circular Graph with Bundled Edges",
        xaxis=dict(showgrid=False, zeroline=False),
        yaxis=dict(showgrid=False, zeroline=False),
        width=700,
        height=700
    )
    fig.write_html('test_edgebundle_circular.html')
    print("Created: test_edgebundle_circular.html")


def create_geographic_graph():
    """Create a geographic-style graph similar to migration flows."""
    print("\n=== Test 3: Geographic Graph (Migration-style) ===")

    # Simulate US state positions (simplified)
    # West coast, central, east coast regions
    states = {
        'CA': (0.2, 0.6), 'OR': (0.15, 0.8), 'WA': (0.1, 0.9),
        'TX': (0.5, 0.3), 'OK': (0.5, 0.5), 'KS': (0.55, 0.6),
        'NY': (0.9, 0.75), 'PA': (0.85, 0.65), 'FL': (0.85, 0.2),
        'IL': (0.65, 0.7), 'OH': (0.75, 0.65), 'MI': (0.7, 0.8),
    }

    nodes = []
    for state, (x, y) in states.items():
        nodes.append({'state': state, 'x': x, 'y': y})
    nodes_df = pd.DataFrame(nodes)

    # Create migration flow edges
    # Higher flows between major states
    flows = [
        ('CA', 'TX', 150),
        ('CA', 'NY', 100),
        ('TX', 'CA', 120),
        ('TX', 'FL', 80),
        ('NY', 'FL', 130),
        ('NY', 'CA', 90),
        ('FL', 'TX', 70),
        ('FL', 'NY', 110),
        ('IL', 'CA', 60),
        ('IL', 'TX', 55),
        ('IL', 'FL', 50),
        ('OH', 'FL', 45),
        ('MI', 'FL', 40),
        ('WA', 'CA', 35),
        ('OR', 'CA', 30),
    ]

    edges = []
    state_to_pos = dict(zip(nodes_df['state'], zip(nodes_df['x'], nodes_df['y'])))

    for src, dst, flow in flows:
        if src in state_to_pos and dst in state_to_pos:
            x_start, y_start = state_to_pos[src]
            x_end, y_end = state_to_pos[dst]
            edges.append({
                'x': x_start,
                'y': y_start,
                'xend': x_end,
                'yend': y_end,
                'flow': flow,
                'route': f'{src}->{dst}'
            })

    edges_df = pd.DataFrame(edges)

    # Plot with flow-based coloring
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
        + geom_edgebundle(K=0.08, cycles=6, compatibility_threshold=0.12,
                         alpha=0.7, width=1.2)
    )

    fig = p.draw()

    # Add state labels
    for _, row in nodes_df.iterrows():
        fig.add_annotation(
            x=row['x'],
            y=row['y'],
            text=row['state'],
            showarrow=False,
            font=dict(size=8, color='white'),
            bgcolor='rgba(0,0,0,0.5)',
            borderpad=2
        )

    fig.update_layout(
        title="Geographic Flow Graph (Migration-style) with Edge Bundling",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=900,
        height=600
    )
    fig.write_html('test_edgebundle_geographic.html')
    print("Created: test_edgebundle_geographic.html")


if __name__ == '__main__':
    print("Testing geom_edgebundle with various graph structures...")

    try:
        create_star_graph()
    except Exception as e:
        print(f"Error in star graph: {e}")

    try:
        create_circular_graph()
    except Exception as e:
        print(f"Error in circular graph: {e}")

    try:
        create_geographic_graph()
    except Exception as e:
        print(f"Error in geographic graph: {e}")

    print("\n✓ Edge bundling tests complete!")
    print("\nOpen the HTML files to view the results:")
    print("  - test_edgebundle_star.html")
    print("  - test_edgebundle_circular.html")
    print("  - test_edgebundle_geographic.html")
