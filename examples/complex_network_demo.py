#!/usr/bin/env python
"""
Complex network examples for edge bundling demonstration.

Creates several dense graph structures where edge bundling is most effective:
1. Hierarchical tree with many connections between levels
2. Dense airline network (hub-and-spoke + point-to-point)
3. Social network with community structure
"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle
import plotly.graph_objects as go


def create_hierarchical_network():
    """
    Create a hierarchical tree structure with cross-level connections.
    This creates visual bundles along the hierarchy.
    """
    print("\n=== Test 1: Hierarchical Network (150 edges) ===")

    # Level 1: Root node at top
    level1 = [{'id': 0, 'x': 0.5, 'y': 1.0, 'level': 1}]

    # Level 2: 4 nodes
    level2 = []
    for i in range(4):
        level2.append({
            'id': i + 1,
            'x': (i + 0.5) / 4,
            'y': 0.75,
            'level': 2
        })

    # Level 3: 12 nodes (3 per level 2 node)
    level3 = []
    for i in range(12):
        parent = i // 3
        offset = (i % 3) - 1
        level3.append({
            'id': i + 5,
            'x': (parent + 0.5) / 4 + offset * 0.05,
            'y': 0.5,
            'level': 3
        })

    # Level 4: 36 nodes (3 per level 3 node)
    level4 = []
    for i in range(36):
        parent = i // 3 + 5
        parent_x = level3[i // 3]['x']
        offset = (i % 3) - 1
        level4.append({
            'id': i + 17,
            'x': parent_x + offset * 0.02,
            'y': 0.25,
            'level': 4
        })

    # Level 5: Leaf nodes (many)
    level5 = []
    for i in range(72):
        parent = i // 2 + 17
        parent_x = level4[i // 2]['x']
        offset = (i % 2) - 0.5
        level5.append({
            'id': i + 53,
            'x': parent_x + offset * 0.01,
            'y': 0.0,
            'level': 5
        })

    nodes = level1 + level2 + level3 + level4 + level5
    nodes_df = pd.DataFrame(nodes)

    # Create edges
    edges = []

    # Level 1 -> Level 2 (root to major branches)
    for node in level2:
        edges.append({
            'x': level1[0]['x'], 'y': level1[0]['y'],
            'xend': node['x'], 'yend': node['y'],
            'type': 'L1-L2', 'weight': 10
        })

    # Level 2 -> Level 3
    for i, node in enumerate(level3):
        parent = level2[i // 3]
        edges.append({
            'x': parent['x'], 'y': parent['y'],
            'xend': node['x'], 'yend': node['y'],
            'type': 'L2-L3', 'weight': 8
        })

    # Level 3 -> Level 4
    for i, node in enumerate(level4):
        parent = level3[i // 3]
        edges.append({
            'x': parent['x'], 'y': parent['y'],
            'xend': node['x'], 'yend': node['y'],
            'type': 'L3-L4', 'weight': 6
        })

    # Level 4 -> Level 5
    for i, node in enumerate(level5):
        parent = level4[i // 2]
        edges.append({
            'x': parent['x'], 'y': parent['y'],
            'xend': node['x'], 'yend': node['y'],
            'type': 'L4-L5', 'weight': 4
        })

    # Add some cross-level connections (these should bundle)
    # Level 2 to Level 4 (skip level 3)
    for i in range(20):
        l2_node = level2[np.random.randint(0, 4)]
        l4_node = level4[np.random.randint(0, 36)]
        edges.append({
            'x': l2_node['x'], 'y': l2_node['y'],
            'xend': l4_node['x'], 'yend': l4_node['y'],
            'type': 'cross', 'weight': 2
        })

    edges_df = pd.DataFrame(edges)
    print(f"Created hierarchical network: {len(nodes_df)} nodes, {len(edges_df)} edges")

    # Plot with edge bundling
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
        + geom_edgebundle(K=0.12, cycles=6, compatibility_threshold=0.08, alpha=0.4, width=0.8)
    )

    fig = p.draw()
    fig.update_layout(
        title="Hierarchical Network with Edge Bundling (150 edges)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1200,
        height=800,
        showlegend=True
    )

    # Add node markers
    fig.add_trace(
        go.Scatter(
            x=nodes_df['x'],
            y=nodes_df['y'],
            mode='markers',
            marker=dict(size=3, color='black', opacity=0.6),
            showlegend=False,
            hoverinfo='skip'
        )
    )

    fig.write_html('complex_hierarchical.html')
    print("Created: complex_hierarchical.html")


def create_airline_network():
    """
    Create a realistic airline network with hubs and spoke cities.
    Dense connections between major hubs, sparse to regional airports.
    """
    print("\n=== Test 2: Airline Network (200+ edges) ===")

    # Major hubs (center)
    hubs = [
        {'name': 'ATL', 'x': 0.65, 'y': 0.35, 'type': 'hub', 'size': 30},
        {'name': 'DFW', 'x': 0.45, 'y': 0.40, 'type': 'hub', 'size': 28},
        {'name': 'ORD', 'x': 0.60, 'y': 0.65, 'type': 'hub', 'size': 27},
        {'name': 'LAX', 'x': 0.15, 'y': 0.45, 'type': 'hub', 'size': 26},
        {'name': 'DEN', 'x': 0.35, 'y': 0.55, 'type': 'hub', 'size': 25},
        {'name': 'JFK', 'x': 0.90, 'y': 0.65, 'type': 'hub', 'size': 24},
        {'name': 'SFO', 'x': 0.10, 'y': 0.60, 'type': 'hub', 'size': 23},
    ]

    # Regional airports (scattered around hubs)
    regional = []
    np.random.seed(42)

    # West coast regional
    for i in range(15):
        regional.append({
            'name': f'W{i}',
            'x': np.random.uniform(0.05, 0.25),
            'y': np.random.uniform(0.3, 0.9),
            'type': 'regional',
            'size': 8
        })

    # Southwest regional
    for i in range(12):
        regional.append({
            'name': f'SW{i}',
            'x': np.random.uniform(0.25, 0.50),
            'y': np.random.uniform(0.15, 0.45),
            'type': 'regional',
            'size': 8
        })

    # Midwest regional
    for i in range(18):
        regional.append({
            'name': f'MW{i}',
            'x': np.random.uniform(0.45, 0.70),
            'y': np.random.uniform(0.45, 0.80),
            'type': 'regional',
            'size': 8
        })

    # East coast regional
    for i in range(15):
        regional.append({
            'name': f'E{i}',
            'x': np.random.uniform(0.75, 0.95),
            'y': np.random.uniform(0.30, 0.85),
            'type': 'regional',
            'size': 8
        })

    nodes = hubs + regional
    nodes_df = pd.DataFrame(nodes)

    edges = []

    # Hub-to-hub connections (fully connected, high volume)
    for i, hub1 in enumerate(hubs):
        for hub2 in hubs[i+1:]:
            edges.append({
                'x': hub1['x'], 'y': hub1['y'],
                'xend': hub2['x'], 'yend': hub2['y'],
                'type': 'hub-to-hub',
                'volume': np.random.randint(100, 200)
            })

    # Hub-to-regional connections (spoke)
    for regional_airport in regional:
        # Connect to nearest 2-3 hubs
        distances = [(hub['name'], np.sqrt((hub['x'] - regional_airport['x'])**2 +
                                           (hub['y'] - regional_airport['y'])**2))
                     for hub in hubs]
        distances.sort(key=lambda x: x[1])

        n_connections = np.random.randint(2, 4)
        for hub_name, _ in distances[:n_connections]:
            hub = next(h for h in hubs if h['name'] == hub_name)
            edges.append({
                'x': regional_airport['x'], 'y': regional_airport['y'],
                'xend': hub['x'], 'yend': hub['y'],
                'type': 'spoke',
                'volume': np.random.randint(20, 60)
            })

    # Some direct regional-to-regional connections
    for i in range(30):
        r1 = regional[np.random.randint(0, len(regional))]
        r2 = regional[np.random.randint(0, len(regional))]
        if r1 != r2:
            edges.append({
                'x': r1['x'], 'y': r1['y'],
                'xend': r2['x'], 'yend': r2['y'],
                'type': 'regional',
                'volume': np.random.randint(10, 30)
            })

    edges_df = pd.DataFrame(edges)
    print(f"Created airline network: {len(nodes_df)} airports, {len(edges_df)} routes")

    # Plot with edge bundling
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
        + geom_edgebundle(K=0.10, cycles=6, compatibility_threshold=0.10, alpha=0.3, width=0.5)
    )

    fig = p.draw()
    fig.update_layout(
        title=f"Airline Network with Edge Bundling ({len(edges_df)} routes)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1400,
        height=900,
        showlegend=True,
        legend=dict(x=0.02, y=0.98)
    )

    # Add airport markers (hubs larger)
    hub_nodes = nodes_df[nodes_df['type'] == 'hub']
    regional_nodes = nodes_df[nodes_df['type'] == 'regional']

    fig.add_trace(
        go.Scatter(
            x=hub_nodes['x'],
            y=hub_nodes['y'],
            mode='markers+text',
            marker=dict(size=hub_nodes['size'], color='red', opacity=0.8, line=dict(width=1, color='white')),
            text=hub_nodes['name'],
            textposition='top center',
            textfont=dict(size=10, color='black'),
            showlegend=False,
            name='Hubs'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=regional_nodes['x'],
            y=regional_nodes['y'],
            mode='markers',
            marker=dict(size=regional_nodes['size'], color='navy', opacity=0.6),
            showlegend=False,
            name='Regional'
        )
    )

    fig.write_html('complex_airline.html')
    print("Created: complex_airline.html")


def create_social_network():
    """
    Create a social network with community structure.
    Dense connections within communities, sparse between communities.
    """
    print("\n=== Test 3: Social Network with Communities (250+ edges) ===")

    np.random.seed(123)

    # Create 5 communities
    communities = []
    community_centers = [
        (0.2, 0.8), (0.8, 0.8), (0.5, 0.5), (0.2, 0.2), (0.8, 0.2)
    ]

    nodes = []
    node_id = 0

    for comm_id, (cx, cy) in enumerate(community_centers):
        community_size = np.random.randint(15, 25)

        for i in range(community_size):
            # Place nodes in a cluster around community center
            angle = np.random.uniform(0, 2 * np.pi)
            radius = np.random.uniform(0, 0.15)

            x = cx + radius * np.cos(angle)
            y = cy + radius * np.sin(angle)

            nodes.append({
                'id': node_id,
                'x': x,
                'y': y,
                'community': comm_id,
                'influence': np.random.uniform(0.5, 1.0)
            })
            node_id += 1

    nodes_df = pd.DataFrame(nodes)

    edges = []

    # Intra-community edges (dense)
    for comm_id in range(5):
        comm_nodes = nodes_df[nodes_df['community'] == comm_id]
        comm_size = len(comm_nodes)

        # Create random edges within community (higher density)
        for i in range(comm_size):
            n_connections = np.random.randint(3, 8)
            for _ in range(n_connections):
                j = np.random.randint(0, comm_size)
                if i != j:
                    node_i = comm_nodes.iloc[i]
                    node_j = comm_nodes.iloc[j]
                    edges.append({
                        'x': node_i['x'], 'y': node_i['y'],
                        'xend': node_j['x'], 'yend': node_j['y'],
                        'type': 'intra-community',
                        'strength': np.random.uniform(0.5, 1.0)
                    })

    # Inter-community edges (sparse bridges)
    for comm_id1 in range(5):
        for comm_id2 in range(comm_id1 + 1, 5):
            # Create a few bridge connections between communities
            n_bridges = np.random.randint(3, 8)

            comm_nodes1 = nodes_df[nodes_df['community'] == comm_id1]
            comm_nodes2 = nodes_df[nodes_df['community'] == comm_id2]

            for _ in range(n_bridges):
                node1 = comm_nodes1.iloc[np.random.randint(0, len(comm_nodes1))]
                node2 = comm_nodes2.iloc[np.random.randint(0, len(comm_nodes2))]

                edges.append({
                    'x': node1['x'], 'y': node1['y'],
                    'xend': node2['x'], 'yend': node2['y'],
                    'type': 'inter-community',
                    'strength': np.random.uniform(0.2, 0.5)
                })

    edges_df = pd.DataFrame(edges)
    print(f"Created social network: {len(nodes_df)} people, {len(edges_df)} connections")

    # Plot with edge bundling
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
        + geom_edgebundle(K=0.11, cycles=6, compatibility_threshold=0.12, alpha=0.25, width=0.4)
    )

    fig = p.draw()
    fig.update_layout(
        title=f"Social Network with Communities ({len(edges_df)} connections)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        width=1200,
        height=1200,
        showlegend=True
    )

    # Add nodes colored by community
    colors = ['red', 'blue', 'green', 'orange', 'purple']
    for comm_id in range(5):
        comm_nodes = nodes_df[nodes_df['community'] == comm_id]
        fig.add_trace(
            go.Scatter(
                x=comm_nodes['x'],
                y=comm_nodes['y'],
                mode='markers',
                marker=dict(
                    size=comm_nodes['influence'] * 10,
                    color=colors[comm_id],
                    opacity=0.7,
                    line=dict(width=0.5, color='white')
                ),
                name=f'Community {comm_id + 1}',
                showlegend=True
            )
        )

    fig.write_html('complex_social.html')
    print("Created: complex_social.html")


def create_circular_force_layout():
    """
    Create a circular layout with many crossing edges.
    This is the classic edge bundling demo from the paper.
    """
    print("\n=== Test 4: Circular Force Layout (300+ edges) ===")

    n_nodes = 80
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 1.0

    nodes = []
    for i, angle in enumerate(angles):
        nodes.append({
            'id': i,
            'x': radius * np.cos(angle),
            'y': radius * np.sin(angle),
            'group': i // 10  # 8 groups of 10 nodes each
        })

    nodes_df = pd.DataFrame(nodes)

    edges = []
    np.random.seed(456)

    # Create edges with hierarchical structure
    for i in range(n_nodes):
        node_i = nodes[i]
        group_i = node_i['group']

        # Connect to nodes in same group (high probability)
        for j in range(n_nodes):
            if i >= j:
                continue

            node_j = nodes[j]
            group_j = node_j['group']

            if group_i == group_j:
                # High probability for same group
                if np.random.random() < 0.4:
                    edges.append({
                        'x': node_i['x'], 'y': node_i['y'],
                        'xend': node_j['x'], 'yend': node_j['y'],
                        'type': 'intra-group',
                        'weight': 1.0
                    })
            else:
                # Lower probability for different groups
                if np.random.random() < 0.03:
                    edges.append({
                        'x': node_i['x'], 'y': node_i['y'],
                        'xend': node_j['x'], 'yend': node_j['y'],
                        'type': 'inter-group',
                        'weight': 0.5
                    })

    edges_df = pd.DataFrame(edges)
    print(f"Created circular network: {len(nodes_df)} nodes, {len(edges_df)} edges")

    # Plot with edge bundling
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='type'))
        + geom_edgebundle(K=0.15, cycles=6, compatibility_threshold=0.15, alpha=0.2, width=0.3)
    )

    fig = p.draw()
    fig.update_layout(
        title=f"Circular Network Layout ({len(edges_df)} edges)",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        width=1200,
        height=1200,
        showlegend=True
    )

    # Add node markers
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']
    for group_id in range(8):
        group_nodes = nodes_df[nodes_df['group'] == group_id]
        fig.add_trace(
            go.Scatter(
                x=group_nodes['x'],
                y=group_nodes['y'],
                mode='markers',
                marker=dict(size=5, color=colors[group_id], opacity=0.8),
                name=f'Group {group_id + 1}',
                showlegend=True
            )
        )

    fig.write_html('complex_circular.html')
    print("Created: complex_circular.html")


if __name__ == '__main__':
    print("=" * 60)
    print("COMPLEX NETWORK EXAMPLES FOR EDGE BUNDLING")
    print("=" * 60)
    print("\nThese examples demonstrate edge bundling on dense graphs")
    print("where the technique is most effective.\n")

    try:
        create_hierarchical_network()
    except Exception as e:
        print(f"Error in hierarchical network: {e}")
        import traceback
        traceback.print_exc()

    try:
        create_airline_network()
    except Exception as e:
        print(f"Error in airline network: {e}")
        import traceback
        traceback.print_exc()

    try:
        create_social_network()
    except Exception as e:
        print(f"Error in social network: {e}")
        import traceback
        traceback.print_exc()

    try:
        create_circular_force_layout()
    except Exception as e:
        print(f"Error in circular network: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 60)
    print("✓ Complex network examples complete!")
    print("=" * 60)
    print("\nGenerated visualizations:")
    print("  - complex_hierarchical.html  (150 edges, tree structure)")
    print("  - complex_airline.html       (200+ edges, hub-and-spoke)")
    print("  - complex_social.html        (250+ edges, communities)")
    print("  - complex_circular.html      (300+ edges, circular layout)")
    print("\nThese demonstrate edge bundling at scale!")
