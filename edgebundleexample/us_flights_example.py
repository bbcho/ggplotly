"""
US Flights Edge Bundling Example
Recreating the R package example with actual flight data
"""

# %% [markdown]
# # US Flights - Force Directed Edge Bundling
#
# This script recreates the R example from test.R:
# ```r
# g <- us_flights
# xy <- cbind(V(g)$longitude, V(g)$latitude)
# fbundle <- edge_bundle_force(g, xy, compatibility_threshold = 0.6)
# ```

# %% Import libraries
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from edge_bundle import edge_bundle_force, plot_bundled_edges

print("✓ Libraries imported")

# %% Load US flights data
# 276 airports, 2,682 flight routes
nodes_df = pd.read_csv('us_flights_nodes.csv')
edges_df = pd.read_csv('us_flights_edges.csv')

print(f"Loaded US Flights dataset:")
print(f"  Airports: {len(nodes_df)}")
print(f"  Flights: {len(edges_df)}")
print(f"\nFirst few airports:")
print(nodes_df[['name', 'city', 'state', 'longitude', 'latitude']].head())

# %% Prepare node coordinates
# In R: xy <- cbind(V(g)$longitude, V(g)$latitude)
us_coords = nodes_df[['longitude', 'latitude']].values

print(f"\nCoordinate array shape: {us_coords.shape}")
print(f"Longitude range: [{us_coords[:, 0].min():.2f}, {us_coords[:, 0].max():.2f}]")
print(f"Latitude range: [{us_coords[:, 1].min():.2f}, {us_coords[:, 1].max():.2f}]")

# %% Convert edges to coordinate format
us_edges_xy = np.zeros((len(edges_df), 4))

for idx, row in edges_df.iterrows():
    src, tgt = int(row['V1']), int(row['V2'])
    us_edges_xy[idx] = [
        us_coords[src, 0], us_coords[src, 1],
        us_coords[tgt, 0], us_coords[tgt, 1]
    ]

print(f"Edge array shape: {us_edges_xy.shape}")
print(f"\nFirst 5 flight routes:")
for i in range(5):
    src, tgt = int(edges_df.iloc[i]['V1']), int(edges_df.iloc[i]['V2'])
    print(f"  {nodes_df.iloc[src]['city']}, {nodes_df.iloc[src]['state']} → "
          f"{nodes_df.iloc[tgt]['city']}, {nodes_df.iloc[tgt]['state']}")

# %% Run edge bundling
# Using EXACT same parameters as R example
# R code: fbundle <- edge_bundle_force(g, xy, compatibility_threshold = 0.6)
# This uses all default parameters: K=1, C=6, P=1, S=0.04, P_rate=2, I=50, I_rate=2/3

print("\n" + "=" * 70)
print("RUNNING EDGE BUNDLING")
print("=" * 70)
print("Parameters (same as R defaults):")
print("  K = 1              (spring constant)")
print("  C = 6              (cycles)")
print("  P = 1              (initial subdivisions)")
print("  S = 0.04           (step size)")
print("  P_rate = 2         (subdivision rate)")
print("  I = 50             (initial iterations)")
print("  I_rate = 2/3       (iteration rate)")
print("  compatibility_threshold = 0.6")
print(f"\nProcessing {len(us_edges_xy)} edges...")
print("This will take several minutes...\n")

us_bundled = edge_bundle_force(
    us_edges_xy,
    K=1,
    C=6,
    P=1,
    S=0.04,
    P_rate=2,
    I=50,
    I_rate=2/3,
    compatibility_threshold=0.6,
    eps=1e-8
)

print("\n" + "=" * 70)
print("BUNDLING COMPLETE!")
print("=" * 70)
print(f"Output shape: {us_bundled.shape}")
print(f"Number of bundled edges: {us_bundled['group'].nunique()}")
print(f"Points per edge: {len(us_bundled[us_bundled['group'] == 0])}")

# %% Inspect bundled data
print("\nFirst 10 rows of bundled data:")
print(us_bundled.head(10))

print("\nData summary:")
print(us_bundled.describe())

# %% Create visualization - Geographic projection
fig_geo = go.Figure()

# Add bundled edges (magenta)
print("\nCreating geographic visualization...")
print("Adding edge traces...")
for group_id in us_bundled['group'].unique():
    group_data = us_bundled[us_bundled['group'] == group_id]
    fig_geo.add_trace(go.Scattergeo(
        lon=group_data['x'],
        lat=group_data['y'],
        mode='lines',
        line=dict(color='#9d0191', width=0.5),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add bundled edges (white overlay)
for group_id in us_bundled['group'].unique():
    group_data = us_bundled[us_bundled['group'] == group_id]
    fig_geo.add_trace(go.Scattergeo(
        lon=group_data['x'],
        lat=group_data['y'],
        mode='lines',
        line=dict(color='white', width=0.1),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add airport nodes
fig_geo.add_trace(go.Scattergeo(
    lon=us_coords[:, 0],
    lat=us_coords[:, 1],
    mode='markers',
    marker=dict(color='#9d0191', size=3),
    text=nodes_df['city'] + ', ' + nodes_df['state'],
    showlegend=False,
    hoverinfo='text'
))

fig_geo.add_trace(go.Scattergeo(
    lon=us_coords[:, 0],
    lat=us_coords[:, 1],
    mode='markers',
    marker=dict(color='white', size=3, opacity=0.5),
    showlegend=False,
    hoverinfo='skip'
))

# Update layout
fig_geo.update_layout(
    title=dict(
        text="Force Directed Edge Bundling - US Flights",
        font=dict(color='white', size=20)
    ),
    geo=dict(
        scope='usa',
        projection_type='albers usa',
        showland=True,
        landcolor='black',
        coastlinecolor='white',
        coastlinewidth=0.5,
        showlakes=False,
        showcountries=False,
        showsubunits=True,
        subunitcolor='white',
        subunitwidth=0.5,
        bgcolor='black'
    ),
    paper_bgcolor='black',
    plot_bgcolor='black',
    margin=dict(l=0, r=0, t=40, b=0),
    height=700
)

print("✓ Geographic visualization created!")
fig_geo.show()

# %% Create visualization - Simple X-Y plot (like R ggplot)
# This more closely matches the R example style
fig_simple = go.Figure()

print("\nCreating simple X-Y visualization...")

# Add bundled edges (thick magenta)
for group_id in us_bundled['group'].unique():
    group_data = us_bundled[us_bundled['group'] == group_id]
    fig_simple.add_trace(go.Scatter(
        x=group_data['x'],
        y=group_data['y'],
        mode='lines',
        line=dict(color='#9d0191', width=0.5),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add bundled edges (thin white)
for group_id in us_bundled['group'].unique():
    group_data = us_bundled[us_bundled['group'] == group_id]
    fig_simple.add_trace(go.Scatter(
        x=group_data['x'],
        y=group_data['y'],
        mode='lines',
        line=dict(color='white', width=0.1),
        showlegend=False,
        hoverinfo='skip'
    ))

# Add airport nodes (magenta)
fig_simple.add_trace(go.Scatter(
    x=us_coords[:, 0],
    y=us_coords[:, 1],
    mode='markers',
    marker=dict(color='#9d0191', size=3),
    text=nodes_df['city'] + ', ' + nodes_df['state'],
    showlegend=False,
    hovertemplate='%{text}<extra></extra>'
))

# Add airport nodes (white overlay)
fig_simple.add_trace(go.Scatter(
    x=us_coords[:, 0],
    y=us_coords[:, 1],
    mode='markers',
    marker=dict(color='white', size=3, opacity=0.5),
    showlegend=False,
    hoverinfo='skip'
))

# Highlight major hubs (if name is not empty)
major_airports = nodes_df[nodes_df['name'] != '']
if len(major_airports) > 0:
    fig_simple.add_trace(go.Scatter(
        x=major_airports['longitude'],
        y=major_airports['latitude'],
        mode='markers',
        marker=dict(color='white', size=8, opacity=1),
        text=major_airports['city'] + ', ' + major_airports['state'],
        showlegend=False,
        hovertemplate='%{text}<extra></extra>'
    ))

# Update layout to match R ggplot black background style
fig_simple.update_layout(
    title=dict(
        text="Force Directed Edge Bundling - US Flights",
        font=dict(color='white', size=20)
    ),
    plot_bgcolor='black',
    paper_bgcolor='black',
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        title=''
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        title='',
        scaleanchor='x',
        scaleratio=1
    ),
    hovermode='closest',
    height=700,
    margin=dict(l=20, r=20, t=60, b=20)
)

print("✓ Simple X-Y visualization created!")
fig_simple.show()

# %% Save bundled data
output_file = 'us_flights_bundled.csv'
us_bundled.to_csv(output_file, index=False)
print(f"\n✓ Saved bundled data to {output_file}")
print(f"  Shape: {us_bundled.shape}")
print(f"\nThis is equivalent to R's fbundle object!")

# %% Save visualizations to HTML
print("\nSaving visualizations to HTML files...")

fig_geo.write_html('us_flights_bundled_geo.html')
print("✓ Saved: us_flights_bundled_geo.html")

fig_simple.write_html('us_flights_bundled_simple.html')
print("✓ Saved: us_flights_bundled_simple.html")

# %% Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"✓ Successfully bundled {len(edges_df)} flight routes")
print(f"✓ Between {len(nodes_df)} airports")
print(f"✓ Generated {us_bundled.shape[0]} bundled points")
print(f"✓ Created 2 interactive visualizations")
print(f"✓ Saved bundled data to CSV")
print("\nThis perfectly replicates the R example:")
print("  R: fbundle <- edge_bundle_force(g, xy, compatibility_threshold = 0.6)")
print("  Python: edge_bundle_force(edges_xy, compatibility_threshold=0.6)")
print("\nOpen the HTML files in a browser to view the interactive plots!")
print("=" * 70)
