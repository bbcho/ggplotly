# %% [markdown]
# ## Oil Shipping Network Visualization with Edge Bundling <br>

# Simulates global oil tanker traffic between major oil ports/regions. <br>
# Demonstrates edge weight functionality where heavier shipping routes <br>
# %%
import numpy as np
import pandas as pd
import igraph as ig
from ggplotly import ggplot, aes, geom_edgebundle, geom_map, theme_dark, labs

# Set seed for reproducibility
np.random.seed(42)

# %%
# =============================================================================
# Define number of edges
# =============================================================================

n_edges = 100

# %%
# =============================================================================
# Define major oil ports/terminals (50 nodes)
# =============================================================================


ports = pd.DataFrame([
    # Middle East - Major exporters
    {"name": "Ras Tanura", "lon": 50.03, "lat": 26.64, "region": "Middle East", "type": "export"},
    {"name": "Kharg Island", "lon": 50.32, "lat": 29.23, "region": "Middle East", "type": "export"},
    {"name": "Fujairah", "lon": 56.33, "lat": 25.12, "region": "Middle East", "type": "export"},
    {"name": "Jebel Ali", "lon": 55.03, "lat": 24.98, "region": "Middle East", "type": "export"},
    {"name": "Basra", "lon": 47.78, "lat": 30.51, "region": "Middle East", "type": "export"},
    {"name": "Kuwait City", "lon": 47.98, "lat": 29.38, "region": "Middle East", "type": "export"},
    {"name": "Yanbu", "lon": 38.06, "lat": 24.09, "region": "Middle East", "type": "export"},
    {"name": "Muscat", "lon": 58.54, "lat": 23.61, "region": "Middle East", "type": "export"},

    # Asia - Major importers
    {"name": "Singapore", "lon": 103.85, "lat": 1.29, "region": "Asia", "type": "hub"},
    {"name": "Shanghai", "lon": 121.47, "lat": 31.23, "region": "Asia", "type": "import"},
    {"name": "Ningbo", "lon": 121.55, "lat": 29.87, "region": "Asia", "type": "import"},
    {"name": "Qingdao", "lon": 120.38, "lat": 36.07, "region": "Asia", "type": "import"},
    {"name": "Busan", "lon": 129.03, "lat": 35.10, "region": "Asia", "type": "import"},
    {"name": "Yokohama", "lon": 139.64, "lat": 35.44, "region": "Asia", "type": "import"},
    {"name": "Chiba", "lon": 140.10, "lat": 35.61, "region": "Asia", "type": "import"},
    {"name": "Kaohsiung", "lon": 120.27, "lat": 22.62, "region": "Asia", "type": "import"},
    {"name": "Hong Kong", "lon": 114.17, "lat": 22.32, "region": "Asia", "type": "hub"},
    {"name": "Mumbai", "lon": 72.88, "lat": 19.08, "region": "Asia", "type": "import"},
    {"name": "Chennai", "lon": 80.27, "lat": 13.08, "region": "Asia", "type": "import"},
    {"name": "Visakhapatnam", "lon": 83.30, "lat": 17.69, "region": "Asia", "type": "import"},

    # Europe - Importers and refineries
    {"name": "Rotterdam", "lon": 4.48, "lat": 51.92, "region": "Europe", "type": "hub"},
    {"name": "Antwerp", "lon": 4.40, "lat": 51.22, "region": "Europe", "type": "import"},
    {"name": "Hamburg", "lon": 9.99, "lat": 53.55, "region": "Europe", "type": "import"},
    {"name": "Le Havre", "lon": 0.11, "lat": 49.49, "region": "Europe", "type": "import"},
    {"name": "Marseille", "lon": 5.37, "lat": 43.30, "region": "Europe", "type": "import"},
    {"name": "Genoa", "lon": 8.93, "lat": 44.41, "region": "Europe", "type": "import"},
    {"name": "Trieste", "lon": 13.77, "lat": 45.65, "region": "Europe", "type": "import"},
    {"name": "Algeciras", "lon": -5.45, "lat": 36.13, "region": "Europe", "type": "hub"},
    {"name": "Sines", "lon": -8.87, "lat": 37.95, "region": "Europe", "type": "import"},
    {"name": "Milford Haven", "lon": -5.05, "lat": 51.71, "region": "Europe", "type": "import"},

    # Africa - Exporters
    {"name": "Bonny", "lon": 7.17, "lat": 4.43, "region": "Africa", "type": "export"},
    {"name": "Lagos", "lon": 3.39, "lat": 6.45, "region": "Africa", "type": "export"},
    {"name": "Luanda", "lon": 13.23, "lat": -8.84, "region": "Africa", "type": "export"},
    {"name": "Pointe-Noire", "lon": 11.86, "lat": -4.77, "region": "Africa", "type": "export"},
    {"name": "Durban", "lon": 31.03, "lat": -29.86, "region": "Africa", "type": "import"},
    {"name": "Alexandria", "lon": 29.92, "lat": 31.20, "region": "Africa", "type": "hub"},
    {"name": "Suez", "lon": 32.55, "lat": 29.97, "region": "Africa", "type": "hub"},

    # Americas - Mixed
    {"name": "Houston", "lon": -95.36, "lat": 29.76, "region": "Americas", "type": "hub"},
    {"name": "Louisiana Offshore", "lon": -90.00, "lat": 28.50, "region": "Americas", "type": "export"},
    {"name": "Corpus Christi", "lon": -97.40, "lat": 27.80, "region": "Americas", "type": "export"},
    {"name": "New York", "lon": -74.01, "lat": 40.71, "region": "Americas", "type": "import"},
    {"name": "Philadelphia", "lon": -75.16, "lat": 39.95, "region": "Americas", "type": "import"},
    {"name": "Cartagena", "lon": -75.51, "lat": 10.39, "region": "Americas", "type": "export"},
    {"name": "Maracaibo", "lon": -71.64, "lat": 10.64, "region": "Americas", "type": "export"},
    {"name": "Santos", "lon": -46.33, "lat": -23.95, "region": "Americas", "type": "import"},
    {"name": "Valdez", "lon": -146.35, "lat": 61.13, "region": "Americas", "type": "export"},

    # Russia/CIS
    {"name": "Novorossiysk", "lon": 37.77, "lat": 44.72, "region": "Russia", "type": "export"},
    {"name": "Primorsk", "lon": 29.52, "lat": 60.35, "region": "Russia", "type": "export"},
    {"name": "Kozmino", "lon": 133.08, "lat": 42.73, "region": "Russia", "type": "export"},
])

n_ports = len(ports)
print(f"Created {n_ports} oil ports across {ports['region'].nunique()} regions")

# %%

# =============================================================================
# Generate shipping routes (10,000 edges with weights)
# =============================================================================

# Vessel weight classes (deadweight tonnage in thousands)
vessel_classes = {
    "VLCC": {"min_dwt": 200, "max_dwt": 320, "probability": 0.15},      # Very Large Crude Carrier
    "Suezmax": {"min_dwt": 120, "max_dwt": 200, "probability": 0.25},   # Max size for Suez Canal
    "Aframax": {"min_dwt": 80, "max_dwt": 120, "probability": 0.30},    # Average Freight Rate Assessment
    "Panamax": {"min_dwt": 60, "max_dwt": 80, "probability": 0.20},     # Max size for Panama Canal
    "Handysize": {"min_dwt": 15, "max_dwt": 60, "probability": 0.10},   # Smaller tankers
}

def get_route_probability(source_type, target_type, source_region, target_region):
    """Calculate probability weight for a route based on realistic trade patterns."""
    prob = 1.0

    # Export to import routes are most common
    if source_type == "export" and target_type == "import":
        prob *= 3.0
    elif source_type == "export" and target_type == "hub":
        prob *= 2.5
    elif source_type == "hub" and target_type == "import":
        prob *= 2.0
    elif source_type == "hub" and target_type == "hub":
        prob *= 1.5

    # Major trade flows
    if source_region == "Middle East" and target_region == "Asia":
        prob *= 4.0  # Largest oil trade route in the world
    elif source_region == "Middle East" and target_region == "Europe":
        prob *= 2.5
    elif source_region == "Africa" and target_region == "Europe":
        prob *= 2.0
    elif source_region == "Africa" and target_region == "Asia":
        prob *= 1.8
    elif source_region == "Russia" and target_region == "Europe":
        prob *= 2.0
    elif source_region == "Russia" and target_region == "Asia":
        prob *= 2.5
    elif source_region == "Americas" and target_region == "Europe":
        prob *= 1.5
    elif source_region == "Americas" and target_region == "Asia":
        prob *= 1.8

    return prob

# Build probability matrix for route selection
route_probs = np.zeros((n_ports, n_ports))
for i in range(n_ports):
    for j in range(n_ports):
        if i != j:
            route_probs[i, j] = get_route_probability(
                ports.iloc[i]['type'], ports.iloc[j]['type'],
                ports.iloc[i]['region'], ports.iloc[j]['region']
            )

# Normalize probabilities
route_probs_flat = route_probs.flatten()
route_probs_flat = route_probs_flat / route_probs_flat.sum()

# Generate 10,000 shipping movements
edge_indices = np.random.choice(
    n_ports * n_ports,
    size=n_edges,
    replace=True,
    p=route_probs_flat
)

# Convert flat indices back to (source, target) pairs
sources = edge_indices // n_ports
targets = edge_indices % n_ports

# Assign vessel classes based on route characteristics
def assign_vessel_class(source_idx, target_idx):
    """Assign vessel class based on route - longer routes tend to use larger vessels."""
    source = ports.iloc[source_idx]
    target = ports.iloc[target_idx]

    # Calculate approximate distance (simple Euclidean for weighting)
    dist = np.sqrt((source['lon'] - target['lon'])**2 + (source['lat'] - target['lat'])**2)

    # Long-haul routes favor VLCCs
    if dist > 100:  # ~intercontinental
        class_probs = {"VLCC": 0.4, "Suezmax": 0.35, "Aframax": 0.15, "Panamax": 0.07, "Handysize": 0.03}
    elif dist > 50:  # ~regional
        class_probs = {"VLCC": 0.2, "Suezmax": 0.35, "Aframax": 0.30, "Panamax": 0.10, "Handysize": 0.05}
    else:  # Short haul
        class_probs = {"VLCC": 0.05, "Suezmax": 0.15, "Aframax": 0.35, "Panamax": 0.30, "Handysize": 0.15}

    classes = list(class_probs.keys())
    probs = list(class_probs.values())
    return np.random.choice(classes, p=probs)

# Generate vessel weights (cargo capacity in thousands of DWT)
vessel_weights = []
vessel_types = []
for s, t in zip(sources, targets):
    v_class = assign_vessel_class(s, t)
    vessel_types.append(v_class)
    v_info = vessel_classes[v_class]
    weight = np.random.uniform(v_info['min_dwt'], v_info['max_dwt'])
    vessel_weights.append(weight)

vessel_weights = np.array(vessel_weights)

# Create edges DataFrame
edges_df = pd.DataFrame({
    'source': sources,
    'target': targets,
    'x': ports.iloc[sources]['lon'].values,
    'y': ports.iloc[sources]['lat'].values,
    'xend': ports.iloc[targets]['lon'].values,
    'yend': ports.iloc[targets]['lat'].values,
    'weight': vessel_weights,
    'vessel_class': vessel_types
})

print(f"\nGenerated {len(edges_df)} shipping movements")
print(f"\nVessel class distribution:")
print(edges_df['vessel_class'].value_counts())
print(f"\nWeight statistics (thousand DWT):")
print(edges_df['weight'].describe())

# %%
# =============================================================================
# Create igraph object for visualization
# =============================================================================

g = ig.Graph(directed=True)
g.add_vertices(n_ports)

# Set vertex attributes
g.vs['name'] = ports['name'].tolist()
g.vs['longitude'] = ports['lon'].tolist()
g.vs['latitude'] = ports['lat'].tolist()
g.vs['region'] = ports['region'].tolist()
g.vs['type'] = ports['type'].tolist()

# Add edges with weights
g.add_edges(list(zip(sources, targets)))
g.es['weight'] = vessel_weights.tolist()
g.es['vessel_class'] = vessel_types

print(f"\nCreated igraph with {g.vcount()} vertices and {g.ecount()} edges")

# %%
# =============================================================================
# Visualize with edge bundling
# =============================================================================

print("\n" + "="*60)
print("Creating visualization with weighted edge bundling...")
print("Heavier shipping routes (VLCCs) will attract lighter routes")
print("="*60 + "\n")

# Create the edgebundle geom first (extracts data from igraph)
bundle = geom_edgebundle(
    graph=g,
    # weight is auto-detected from graph's edge 'weight' attribute
    compatibility_threshold=0.6,
    C=6,
    I=50,
    E=1.0,
    color='#ff6b35',
    alpha=0.4,
    linewidth=0.3,
    show_highlight=True,
    highlight_color='#ffd700',
    highlight_alpha=0.15,
    highlight_width=0.1,
    show_nodes=True,
    node_color='#00ff88',
    node_size=4,
    node_alpha=0.9,
    verbose=True
)

# Create the visualization using extracted data
fig = (
    ggplot(bundle.data, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_map(
        map_type='world',
        landcolor='#1a1a2e',
        oceancolor='#0f0f1a',
        countrycolor='#2d2d44',
        coastlinecolor='#3d3d5c',
        bgcolor='#0a0a14'
    )
    + bundle
    + theme_dark()
    + labs(
        title='Global Oil Tanker Shipping Network',
        subtitle='10,000 simulated vessel movements with weighted edge bundling (heavier vessels = stronger bundling attraction)'
    )
)

# Draw and show
figure = fig.draw()

# Update layout for better presentation
figure.update_layout(
    geo=dict(
        projection_type='natural earth',
        showland=True,
        showocean=True,
        showcoastlines=True,
        showcountries=True,
        landcolor='#1a1a2e',
        oceancolor='#0f0f1a',
        countrycolor='#2d2d44',
        coastlinecolor='#3d3d5c',
        bgcolor='#0a0a14',
        lonaxis=dict(range=[-180, 180]),
        lataxis=dict(range=[-60, 75]),
    ),
    paper_bgcolor='#0a0a14',
    title=dict(
        text='<b>Global Oil Tanker Shipping Network</b><br><sup>10,000 simulated movements | Weighted edge bundling (VLCC routes attract lighter traffic)</sup>',
        font=dict(color='white', size=16),
        x=0.5,
        xanchor='center'
    ),
    margin=dict(l=0, r=0, t=60, b=0),
)

figure.show()

# %%

# =============================================================================
# Summary statistics
# =============================================================================

print("\n" + "="*60)
print("SHIPPING NETWORK SUMMARY")
print("="*60)

print(f"\nTop 10 busiest routes:")
route_counts = edges_df.groupby(['source', 'target']).agg({
    'weight': ['count', 'sum', 'mean']
}).reset_index()
route_counts.columns = ['source', 'target', 'n_shipments', 'total_dwt', 'avg_dwt']
route_counts['source_name'] = route_counts['source'].map(lambda x: ports.iloc[x]['name'])
route_counts['target_name'] = route_counts['target'].map(lambda x: ports.iloc[x]['name'])
route_counts = route_counts.sort_values('total_dwt', ascending=False)

for _, row in route_counts.head(10).iterrows():
    print(f"  {row['source_name']:20} → {row['target_name']:20}: "
          f"{int(row['n_shipments']):4} ships, {row['total_dwt']/1000:.1f}M DWT total")

print(f"\nRegional trade flows (million DWT):")
edges_df['source_region'] = edges_df['source'].map(lambda x: ports.iloc[x]['region'])
edges_df['target_region'] = edges_df['target'].map(lambda x: ports.iloc[x]['region'])
regional_flows = edges_df.groupby(['source_region', 'target_region'])['weight'].sum() / 1000
regional_flows = regional_flows.sort_values(ascending=False)
for (src, tgt), flow in regional_flows.head(10).items():
    print(f"  {src:15} → {tgt:15}: {flow:.1f}M DWT")

# %%