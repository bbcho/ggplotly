#!/usr/bin/env python
"""
Create a realistic migration flow network similar to the example shown.

This creates a very dense graph with 50 US cities and migration flows between them,
demonstrating edge bundling on a realistic geographic network.
"""

import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_edgebundle
import plotly.graph_objects as go


def create_migration_network():
    """
    Create a realistic US migration flow network.
    """
    print("Creating US Migration Flow Network...")

    # Major US cities with approximate normalized positions (0-1 scale)
    cities = {
        # West Coast
        'Seattle': (0.08, 0.88), 'Portland': (0.09, 0.82), 'San Francisco': (0.05, 0.65),
        'Los Angeles': (0.10, 0.55), 'San Diego': (0.12, 0.48), 'Phoenix': (0.21, 0.45),
        'Las Vegas': (0.14, 0.58),

        # Mountain
        'Denver': (0.32, 0.63), 'Salt Lake City': (0.24, 0.68), 'Boise': (0.18, 0.75),
        'Albuquerque': (0.30, 0.50),

        # Southwest
        'Dallas': (0.48, 0.45), 'Houston': (0.50, 0.38), 'Austin': (0.47, 0.42),
        'San Antonio': (0.46, 0.38), 'Oklahoma City': (0.48, 0.55), 'Kansas City': (0.52, 0.63),

        # Midwest
        'Minneapolis': (0.54, 0.80), 'Milwaukee': (0.59, 0.74), 'Chicago': (0.60, 0.70),
        'St. Louis': (0.57, 0.62), 'Indianapolis': (0.63, 0.64), 'Detroit': (0.66, 0.72),
        'Cleveland': (0.69, 0.70), 'Cincinnati': (0.66, 0.63), 'Columbus': (0.68, 0.65),

        # South
        'Memphis': (0.57, 0.53), 'Nashville': (0.61, 0.56), 'New Orleans': (0.57, 0.38),
        'Birmingham': (0.63, 0.48), 'Atlanta': (0.68, 0.48), 'Jacksonville': (0.72, 0.42),
        'Miami': (0.75, 0.30), 'Tampa': (0.71, 0.35), 'Orlando': (0.72, 0.37),

        # East Coast
        'Charlotte': (0.72, 0.53), 'Raleigh': (0.75, 0.55), 'Washington DC': (0.78, 0.62),
        'Baltimore': (0.77, 0.63), 'Philadelphia': (0.80, 0.65), 'New York': (0.82, 0.68),
        'Boston': (0.85, 0.72), 'Buffalo': (0.74, 0.73), 'Pittsburgh': (0.73, 0.66),

        # Additional cities
        'Richmond': (0.77, 0.58), 'Louisville': (0.64, 0.60), 'Omaha': (0.50, 0.70),
        'Des Moines': (0.52, 0.72), 'Little Rock': (0.55, 0.52), 'Providence': (0.86, 0.70),
    }

    nodes_df = pd.DataFrame([
        {'city': name, 'x': x, 'y': y}
        for name, (x, y) in cities.items()
    ])

    n_cities = len(cities)
    print(f"Cities: {n_cities}")

    # Create migration flows
    # More flows between nearby cities and between major hubs
    edges = []
    np.random.seed(789)

    city_names = list(cities.keys())
    city_positions = list(cities.values())

    # Major hubs (higher migration activity)
    major_hubs = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
                  'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Francisco',
                  'Atlanta', 'Miami', 'Seattle', 'Denver', 'Boston']

    # Create flows between all city pairs with distance-based probability
    for i in range(n_cities):
        city1 = city_names[i]
        x1, y1 = city_positions[i]

        # Each city has outflows to 5-15 other cities
        n_outflows = np.random.randint(5, 16)

        # Calculate distances to all other cities
        distances = []
        for j in range(n_cities):
            if i != j:
                x2, y2 = city_positions[j]
                dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                # Higher probability for:
                # 1. Nearby cities (inverse distance)
                # 2. Major hubs
                city2 = city_names[j]
                prob = 1.0 / (dist + 0.1)

                if city1 in major_hubs:
                    prob *= 1.5
                if city2 in major_hubs:
                    prob *= 1.5

                distances.append((j, city2, dist, prob))

        # Sample cities based on probability
        probs = np.array([d[3] for d in distances])
        probs = probs / probs.sum()

        selected_indices = np.random.choice(
            len(distances),
            size=min(n_outflows, len(distances)),
            replace=False,
            p=probs
        )

        for idx in selected_indices:
            j, city2, dist, _ = distances[idx]
            x2, y2 = city_positions[j]

            # Flow magnitude: higher for major hubs, lower for long distances
            base_flow = 50
            if city1 in major_hubs:
                base_flow *= 1.5
            if city2 in major_hubs:
                base_flow *= 1.5

            flow = int(base_flow / (dist + 0.5) + np.random.uniform(10, 30))

            edges.append({
                'x': x1, 'y': y1,
                'xend': x2, 'yend': y2,
                'from': city1,
                'to': city2,
                'flow': flow,
                'distance': dist
            })

    edges_df = pd.DataFrame(edges)
    print(f"Migration flows: {len(edges_df)}")

    # Categorize flows by magnitude for coloring
    edges_df['flow_category'] = pd.cut(
        edges_df['flow'],
        bins=[0, 50, 100, 150, 200, 1000],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )

    print("\nFlow distribution:")
    print(edges_df['flow_category'].value_counts().sort_index())

    # Plot with edge bundling
    print("\nApplying edge bundling...")
    p = (
        ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend', color='flow'))
        + geom_edgebundle(
            K=0.10,                      # Moderate bundling strength
            cycles=6,                     # Full refinement
            compatibility_threshold=0.08, # Selective bundling
            alpha=0.35,                   # Semi-transparent
            width=0.6                     # Thin lines
        )
    )

    fig = p.draw()

    # Customize layout
    fig.update_layout(
        title=dict(
            text=f"US Migration Flow Network with Edge Bundling<br><sub>{len(edges_df)} migration flows between {n_cities} cities</sub>",
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False, range=[-0.05, 1.05]),
        width=1600,
        height=1000,
        showlegend=True,
        legend=dict(
            title="Migration Flow",
            x=0.02,
            y=0.98,
            bgcolor='rgba(255, 255, 255, 0.8)'
        ),
        plot_bgcolor='#f8f9fa'
    )

    # Add city markers
    # Major hubs in red, others in blue
    major_hub_nodes = nodes_df[nodes_df['city'].isin(major_hubs)]
    other_nodes = nodes_df[~nodes_df['city'].isin(major_hubs)]

    fig.add_trace(
        go.Scatter(
            x=major_hub_nodes['x'],
            y=major_hub_nodes['y'],
            mode='markers',
            marker=dict(
                size=12,
                color='darkred',
                opacity=0.9,
                line=dict(width=2, color='white')
            ),
            text=major_hub_nodes['city'],
            hoverinfo='text',
            name='Major Hubs',
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x=other_nodes['x'],
            y=other_nodes['y'],
            mode='markers',
            marker=dict(
                size=6,
                color='navy',
                opacity=0.7,
                line=dict(width=1, color='white')
            ),
            text=other_nodes['city'],
            hoverinfo='text',
            name='Other Cities',
            showlegend=False
        )
    )

    # Add city labels for major hubs
    for _, row in major_hub_nodes.iterrows():
        fig.add_annotation(
            x=row['x'],
            y=row['y'],
            text=row['city'],
            showarrow=False,
            font=dict(size=8, color='black'),
            bgcolor='rgba(255, 255, 255, 0.7)',
            borderpad=2,
            yshift=10
        )

    filename = 'migration_network_us.html'
    fig.write_html(filename)
    print(f"\n✓ Created: {filename}")

    return fig


if __name__ == '__main__':
    print("=" * 70)
    print("US MIGRATION FLOW NETWORK")
    print("=" * 70)
    print("\nDemonstrating edge bundling on a realistic geographic network")
    print("with hundreds of migration flows between major US cities.\n")

    try:
        fig = create_migration_network()

        print("\n" + "=" * 70)
        print("SUCCESS!")
        print("=" * 70)
        print("\nThis visualization demonstrates edge bundling at scale:")
        print("  - 50 US cities")
        print("  - 400+ migration flows")
        print("  - Flows bundled by geographic proximity and compatibility")
        print("  - Color represents migration volume")
        print("\nOpen migration_network_us.html to view the result!")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
