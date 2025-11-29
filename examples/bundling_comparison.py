#!/usr/bin/env python
"""
Compare edge bundling at different parameter settings.

Shows how K, compatibility_threshold, and cycles affect bundling strength.
"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle

np.random.seed(100)


def create_test_graph():
    """Create a circular graph with crossing edges - ideal for showing bundling."""
    n_nodes = 30
    angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
    radius = 1.0

    nodes = [(radius * np.cos(a), radius * np.sin(a)) for a in angles]

    edges = []

    # Create edges between nodes based on groups
    # Nodes in same group connect more (should bundle together)
    groups = 5
    nodes_per_group = n_nodes // groups

    for i in range(n_nodes):
        group_i = i // nodes_per_group

        # Connect to 4-6 other nodes, preferring same group
        n_connections = np.random.randint(4, 7)

        for _ in range(n_connections):
            # 70% chance to connect within group, 30% across groups
            if np.random.random() < 0.7:
                # Same group
                group_start = group_i * nodes_per_group
                group_end = min(group_start + nodes_per_group, n_nodes)
                j = np.random.randint(group_start, group_end)
            else:
                # Different group
                j = np.random.randint(0, n_nodes)

            if i != j:
                edges.append({
                    'x': nodes[i][0], 'y': nodes[i][1],
                    'xend': nodes[j][0], 'yend': nodes[j][1],
                    'group': f'{min(group_i, j // nodes_per_group)}'
                })

    return pd.DataFrame(edges)


def test_parameter(edges_df, name, **kwargs):
    """Test bundling with specific parameters."""
    print(f"\nGenerating: {name}")

    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
        + geom_edgebundle(**kwargs, alpha=0.4, width=0.8)
    )

    fig = p.draw()
    fig.update_layout(
        title=f"Edge Bundling: {name}",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-1.2, 1.2]),
        width=900,
        height=900
    )

    filename = f"bundling_{name.lower().replace(' ', '_').replace(',', '')}.html"
    fig.write_html(filename)
    print(f"Created: {filename}")


if __name__ == '__main__':
    print("=" * 70)
    print("EDGE BUNDLING PARAMETER COMPARISON")
    print("=" * 70)
    print("\nCreating test graph with ~120 edges...")

    edges_df = create_test_graph()
    print(f"Generated {len(edges_df)} edges")

    # Test 1: No bundling (for comparison)
    print("\nNote: For comparison, you can create a non-bundled version")
    print("      using geom_segment instead of geom_edgebundle")

    # Test 2: Default parameters
    test_parameter(edges_df, "Default (K=0.5, threshold=0.1)",
                   K=0.5, compatibility_threshold=0.1, cycles=6)

    # Test 3: Strong bundling
    test_parameter(edges_df, "Strong (K=0.8, threshold=0.05)",
                   K=0.8, compatibility_threshold=0.05, cycles=6)

    # Test 4: Very strong bundling
    test_parameter(edges_df, "Very Strong (K=1.2, threshold=0.03)",
                   K=1.2, compatibility_threshold=0.03, cycles=7)

    # Test 5: Subtle bundling
    test_parameter(edges_df, "Subtle (K=0.3, threshold=0.15)",
                   K=0.3, compatibility_threshold=0.15, cycles=6)

    # Test 6: More cycles (smoother)
    test_parameter(edges_df, "Extra Smooth (K=0.8, cycles=8)",
                   K=0.8, compatibility_threshold=0.08, cycles=8)

    print("\n" + "=" * 70)
    print("✓ Comparison complete!")
    print("=" * 70)
    print("\nGenerated files:")
    print("  - bundling_default_k05_threshold01.html")
    print("  - bundling_strong_k08_threshold005.html")
    print("  - bundling_very_strong_k12_threshold003.html")
    print("  - bundling_subtle_k03_threshold015.html")
    print("  - bundling_extra_smooth_k08_cycles8.html")
    print("\nCompare these to see how parameters affect bundling!")
    print("\nNote: K values are higher than traditional implementations")
    print("      due to coordinate normalization to [0, 1] range.")
