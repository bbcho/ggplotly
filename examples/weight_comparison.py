# %% [markdown]
# ## Edge Weight Comparison Demo
# Shows side-by-side the effect of weighted vs unweighted edge bundling

# %%
import numpy as np
import pandas as pd
from ggplotly.stats.stat_edgebundle import stat_edgebundle
import plotly.graph_objects as go
from plotly.subplots import make_subplots

np.random.seed(42)

# %%
# Create a scenario with 3 edge groups: top, middle, bottom
# The middle edge will be pulled toward whichever group is heavier

edges_df = pd.DataFrame({
    # Top group (y=8)
    'x':    [0, 0, 0,   0,   0, 0, 0],
    'y':    [8, 8, 8,   5,   2, 2, 2],  # 3 top, 1 middle, 3 bottom
    'xend': [10, 10, 10, 10,  10, 10, 10],
    'yend': [8, 8, 8,   5,   2, 2, 2],
})

# Scenario 1: Top edges are heavy - middle should be pulled UP
weights_heavy_top = np.array([100, 100, 100,  1,  1, 1, 1])

# Scenario 2: Bottom edges are heavy - middle should be pulled DOWN
weights_heavy_bottom = np.array([1, 1, 1,  1,  100, 100, 100])

# %%
# Compute bundling with different weight scenarios
stat = stat_edgebundle(C=4, I=30, compatibility_threshold=0.5, verbose=True)

print("=" * 50)
print("Computing UNWEIGHTED bundling...")
print("=" * 50)
bundled_none = stat.compute(edges_df, weights=None)

stat._cached_result = None
stat._cached_data_hash = None

print("\n" + "=" * 50)
print("Computing with HEAVY TOP weights...")
print("=" * 50)
bundled_top = stat.compute(edges_df, weights=weights_heavy_top)

stat._cached_result = None
stat._cached_data_hash = None

print("\n" + "=" * 50)
print("Computing with HEAVY BOTTOM weights...")
print("=" * 50)
bundled_bottom = stat.compute(edges_df, weights=weights_heavy_bottom)

# %%
# Create comparison figure
fig = make_subplots(
    rows=1, cols=3,
    subplot_titles=[
        'No Weights (uniform)',
        'Heavy TOP (y=8) - middle pulled UP',
        'Heavy BOTTOM (y=2) - middle pulled DOWN'
    ],
    horizontal_spacing=0.05
)

# Color by group: top=orange, middle=white, bottom=cyan
def get_color(group_id):
    if group_id < 3:  # Top edges
        return '#ff6b35'
    elif group_id == 3:  # Middle edge
        return '#ffffff'
    else:  # Bottom edges
        return '#35a5ff'

def add_bundled_edges(fig, bundled, col):
    for group_id in bundled['group'].unique():
        group_data = bundled[bundled['group'] == group_id]
        fig.add_trace(
            go.Scatter(
                x=group_data['x'].values,
                y=group_data['y'].values,
                mode='lines',
                line=dict(color=get_color(group_id), width=3 if group_id == 3 else 2),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=1, col=col
        )

add_bundled_edges(fig, bundled_none, 1)
add_bundled_edges(fig, bundled_top, 2)
add_bundled_edges(fig, bundled_bottom, 3)

fig.update_layout(
    title=dict(
        text='<b>Edge Weight Effect on Bundling</b><br><sup>Heavy edges attract lighter edges more strongly</sup>',
        x=0.5,
        font=dict(size=16)
    ),
    height=400,
    width=1200,
    paper_bgcolor='#1a1a2e',
    plot_bgcolor='#1a1a2e',
    font=dict(color='white')
)

for i in range(1, 4):
    fig.update_xaxes(
        range=[-1, 11],
        showgrid=True,
        gridcolor='#333',
        row=1, col=i
    )
    fig.update_yaxes(
        range=[-1, 10],
        showgrid=True,
        gridcolor='#333',
        row=1, col=i
    )

fig.show()

# %%
# Print numerical comparison - focus on the MIDDLE edge (group 3)
print("\n" + "=" * 60)
print("MIDDLE EDGE (white line) DISPLACEMENT")
print("=" * 60)
print("Original position: y=5")
print()

for name, bundled in [("No weights", bundled_none),
                       ("Heavy TOP", bundled_top),
                       ("Heavy BOTTOM", bundled_bottom)]:
    group = bundled[bundled['group'] == 3]  # Middle edge
    mid_idx = len(group) // 2
    mid_y = group.iloc[mid_idx]['y']
    displacement = mid_y - 5.0
    direction = "UP ↑" if displacement > 0 else "DOWN ↓" if displacement < 0 else "NONE"
    print(f"{name:15}: midpoint y = {mid_y:.2f}  ({direction} {abs(displacement):.2f})")
