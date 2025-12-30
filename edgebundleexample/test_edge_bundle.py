"""
Test for edge bundling implementation
"""

import numpy as np
import networkx as nx
import plotly.graph_objects as go
from edge_bundle import edge_bundle_force, plot_bundled_edges


def test_edge_bundling():
    """
    Test edge bundling with a random graph of 20 nodes and 100+ edges.
    """
    print("=" * 60)
    print("TEST: Edge Bundling with 20 nodes")
    print("=" * 60)

    # Set random seed for reproducibility
    np.random.seed(42)

    # Create a graph with 20 nodes
    n_nodes = 20

    # Generate random coordinates for nodes (in a circle for nice visualization)
    angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
    radius = 10
    node_coords = np.column_stack([
        radius * np.cos(angles),
        radius * np.sin(angles)
    ])

    # Add some randomness to make it more interesting
    node_coords += np.random.randn(n_nodes, 2) * 0.5

    # Create a random graph with high connectivity
    G = nx.Graph()
    G.add_nodes_from(range(n_nodes))

    # Add edges to create a dense graph
    # Method 1: Connect each node to several random other nodes
    edges_added = 0
    for i in range(n_nodes):
        # Each node connects to 5-8 other nodes
        n_connections = np.random.randint(5, 9)
        targets = np.random.choice(
            [j for j in range(n_nodes) if j != i and not G.has_edge(i, j)],
            size=min(n_connections, n_nodes - 1 - G.degree(i)),
            replace=False
        )
        for target in targets:
            if not G.has_edge(i, target):
                G.add_edge(i, target)
                edges_added += 1

    n_edges = G.number_of_edges()
    print(f"\nGraph created:")
    print(f"  Nodes: {n_nodes}")
    print(f"  Edges: {n_edges}")
    print(f"  Average degree: {2 * n_edges / n_nodes:.2f}")

    # Convert edges to coordinate format
    edge_list = list(G.edges())
    edges_xy = np.zeros((n_edges, 4))
    for idx, (i, j) in enumerate(edge_list):
        edges_xy[idx] = [
            node_coords[i, 0], node_coords[i, 1],
            node_coords[j, 0], node_coords[j, 1]
        ]

    print(f"\nEdges converted to coordinate format: {edges_xy.shape}")

    # Run edge bundling with reduced parameters for faster testing
    print("\n" + "=" * 60)
    print("Running edge bundling algorithm...")
    print("=" * 60)

    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,
        C=4,  # Reduced from 6 for faster testing
        P=1,
        S=0.04,
        P_rate=2,
        I=30,  # Reduced from 50 for faster testing
        I_rate=2/3,
        compatibility_threshold=0.6,
        eps=1e-8
    )

    print(f"\nBundled edges dataframe shape: {bundled.shape}")
    print(f"Columns: {list(bundled.columns)}")
    print(f"Number of edge groups: {bundled['group'].nunique()}")
    print(f"Points per edge: {len(bundled[bundled['group'] == 0])}")

    # Verify output structure
    assert 'x' in bundled.columns, "Missing 'x' column"
    assert 'y' in bundled.columns, "Missing 'y' column"
    assert 'index' in bundled.columns, "Missing 'index' column"
    assert 'group' in bundled.columns, "Missing 'group' column"
    assert bundled['group'].nunique() == n_edges, f"Expected {n_edges} groups, got {bundled['group'].nunique()}"

    # Check that index goes from 0 to 1
    for group_id in range(min(5, n_edges)):  # Check first 5 edges
        group_data = bundled[bundled['group'] == group_id]
        indices = group_data['index'].values
        assert np.isclose(indices[0], 0.0), f"Edge {group_id} doesn't start at index 0"
        assert np.isclose(indices[-1], 1.0), f"Edge {group_id} doesn't end at index 1"

    print("\n" + "=" * 60)
    print("Creating visualization...")
    print("=" * 60)

    # Create visualization
    fig = plot_bundled_edges(bundled, node_coords, title="Test: Force Directed Edge Bundling")

    # Save to HTML file
    output_file = "/workspaces/edgebundle/test_bundled_edges.html"
    fig.write_html(output_file)
    print(f"\nVisualization saved to: {output_file}")

    # Also create a comparison plot with unbundled edges
    fig_comparison = go.Figure()

    # Add unbundled edges (gray)
    for i, (node_i, node_j) in enumerate(edge_list):
        if i < 50:  # Limit to first 50 for clarity
            fig_comparison.add_trace(go.Scatter(
                x=[node_coords[node_i, 0], node_coords[node_j, 0]],
                y=[node_coords[node_i, 1], node_coords[node_j, 1]],
                mode='lines',
                line=dict(color='gray', width=0.5),
                showlegend=False,
                hoverinfo='skip'
            ))

    # Add bundled edges (magenta)
    for group_id in bundled['group'].unique():
        if group_id < 50:  # Limit to first 50 for clarity
            group_data = bundled[bundled['group'] == group_id]
            fig_comparison.add_trace(go.Scatter(
                x=group_data['x'],
                y=group_data['y'],
                mode='lines',
                line=dict(color='#9d0191', width=1.5),
                showlegend=False,
                hoverinfo='skip'
            ))

    # Add nodes
    fig_comparison.add_trace(go.Scatter(
        x=node_coords[:, 0],
        y=node_coords[:, 1],
        mode='markers',
        marker=dict(color='white', size=10, line=dict(color='black', width=1)),
        showlegend=False,
        hoverinfo='skip'
    ))

    fig_comparison.update_layout(
        title="Comparison: Gray = Original, Magenta = Bundled",
        plot_bgcolor='white',
        xaxis=dict(showgrid=True, zeroline=False),
        yaxis=dict(showgrid=True, zeroline=False, scaleanchor='x', scaleratio=1),
        margin=dict(l=20, r=20, t=40, b=20)
    )

    comparison_file = "/workspaces/edgebundle/test_comparison.html"
    fig_comparison.write_html(comparison_file)
    print(f"Comparison visualization saved to: {comparison_file}")

    print("\n" + "=" * 60)
    print("TEST PASSED!")
    print("=" * 60)
    print("\nSummary:")
    print(f"  ✓ Bundled {n_edges} edges successfully")
    print(f"  ✓ Output structure is correct")
    print(f"  ✓ Visualizations created")
    print(f"\nOpen the HTML files in a browser to view the results:")
    print(f"  - {output_file}")
    print(f"  - {comparison_file}")


if __name__ == "__main__":
    test_edge_bundling()
