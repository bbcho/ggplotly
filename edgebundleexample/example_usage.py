"""
Example usage of the edge bundling implementation.
This demonstrates how to use the Python equivalent of R's edge_bundle_force.
"""

import numpy as np
import networkx as nx
from edge_bundle import edge_bundle_force, plot_bundled_edges


def example_basic_usage():
    """
    Basic example showing how to use edge_bundle_force.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Basic Usage")
    print("=" * 60)

    # Step 1: Create a graph using NetworkX
    G = nx.karate_club_graph()  # Classic karate club network
    print(f"\nCreated graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    # Step 2: Create node coordinates (layout)
    # You can use any layout algorithm
    pos = nx.spring_layout(G, seed=42, k=2)
    node_coords = np.array([pos[i] for i in range(G.number_of_nodes())])

    # Step 3: Convert edges to coordinate format
    edges = list(G.edges())
    edges_xy = np.zeros((len(edges), 4))
    for idx, (i, j) in enumerate(edges):
        edges_xy[idx] = [
            node_coords[i, 0], node_coords[i, 1],
            node_coords[j, 0], node_coords[j, 1]
        ]

    # Step 4: Run edge bundling
    bundled = edge_bundle_force(
        edges_xy,
        K=1.0,                      # Spring constant
        C=6,                        # Number of cycles
        P=1,                        # Initial subdivisions
        S=0.04,                     # Initial step size
        P_rate=2,                   # Subdivision increase rate
        I=50,                       # Initial iterations
        I_rate=2/3,                 # Iteration decrease rate
        compatibility_threshold=0.6, # Compatibility threshold
        eps=1e-8                    # Numerical stability
    )

    print(f"\nBundled edges shape: {bundled.shape}")
    print(f"Columns: {list(bundled.columns)}")

    # Step 5: Visualize
    fig = plot_bundled_edges(bundled, node_coords, title="Karate Club Network")

    output_file = "/workspaces/edgebundle/example_karate.html"
    fig.write_html(output_file)
    print(f"\nVisualization saved to: {output_file}")

    return bundled, node_coords


def example_compare_with_r():
    """
    Example that mimics the R code structure from test.R.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: R-style Usage")
    print("=" * 60)

    # Create a simple graph (like the R example)
    edges = [
        (0, 11), (1, 10), (2, 9),
        (3, 8), (4, 7), (5, 6)
    ]

    G = nx.Graph()
    G.add_edges_from(edges)

    # Create coordinates (mimic R example with two columns of points)
    xy = np.column_stack([
        np.concatenate([np.zeros(6), np.ones(6)]),  # x: 0 for first 6, 1 for second 6
        np.concatenate([np.arange(1, 7), np.arange(1, 7)])  # y: 1-6 for both groups
    ])

    print(f"\nNode coordinates shape: {xy.shape}")
    print("First few coordinates:")
    print(xy[:3])

    # Convert to edge coordinate format
    edges_xy = np.zeros((len(edges), 4))
    for idx, (i, j) in enumerate(edges):
        edges_xy[idx] = [xy[i, 0], xy[i, 1], xy[j, 0], xy[j, 1]]

    # Run bundling (equivalent to R's edge_bundle_force)
    fbundle = edge_bundle_force(
        edges_xy,
        compatibility_threshold=0.6
    )

    print(f"\nBundled result shape: {fbundle.shape}")
    print("\nFirst few rows of bundled data:")
    print(fbundle.head())

    # Create visualization
    fig = plot_bundled_edges(fbundle, xy, title="R-style Example")

    output_file = "/workspaces/edgebundle/example_r_style.html"
    fig.write_html(output_file)
    print(f"\nVisualization saved to: {output_file}")

    return fbundle


def example_from_edge_list():
    """
    Example showing direct usage with just edge coordinates (no graph object needed).
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Direct Edge Coordinate Usage")
    print("=" * 60)

    # You can also directly provide edge coordinates without creating a graph
    # This is useful if you have spatial data or custom layouts

    # Create some random edges
    np.random.seed(789)
    n_edges = 30

    # Random edges in a unit square
    edges_xy = np.random.rand(n_edges, 4)

    print(f"Created {n_edges} random edges")

    # Bundle them
    bundled = edge_bundle_force(
        edges_xy,
        C=4,  # Fewer cycles for speed
        I=30,
        compatibility_threshold=0.5
    )

    # Extract unique node coordinates from edges for visualization
    unique_points = set()
    for edge in edges_xy:
        unique_points.add((edge[0], edge[1]))
        unique_points.add((edge[2], edge[3]))

    node_coords = np.array(list(unique_points))

    # Visualize
    fig = plot_bundled_edges(bundled, node_coords, title="Random Edges")

    output_file = "/workspaces/edgebundle/example_random.html"
    fig.write_html(output_file)
    print(f"\nVisualization saved to: {output_file}")

    return bundled


def run_all_examples():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("RUNNING EDGE BUNDLING EXAMPLES")
    print("=" * 70)

    # Example 1: Basic usage
    example_basic_usage()

    # Example 2: R-style usage
    example_compare_with_r()

    # Example 3: Direct edge coordinates
    example_from_edge_list()

    print("\n" + "=" * 70)
    print("ALL EXAMPLES COMPLETED!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - /workspaces/edgebundle/example_karate.html")
    print("  - /workspaces/edgebundle/example_r_style.html")
    print("  - /workspaces/edgebundle/example_random.html")
    print("\nOpen these HTML files in a browser to view the visualizations.")


if __name__ == "__main__":
    run_all_examples()
