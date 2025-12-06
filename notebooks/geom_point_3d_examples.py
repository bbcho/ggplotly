# geom_point_3d Examples
# Comprehensive examples for 3D scatter plots in ggplotly
# Each cell is self-contained and can be run independently in Jupyter

# %% [markdown]
# # geom_point_3d Examples
#
# This notebook demonstrates the various features of `geom_point_3d` for creating
# interactive 3D scatter plots with ggplotly.

# %% [markdown]
# ## Setup

# %%
import pandas as pd
import numpy as np
from ggplotly import (
    ggplot, aes, geom_point_3d,
    facet_wrap, facet_grid,
    scale_color_manual, scale_color_brewer,
    theme_minimal, theme_dark, theme_classic, theme_ggplot2,
    labs, annotate,
    ggsize,
)

# Set random seed for reproducibility
np.random.seed(42)

# %% [markdown]
# ## 1. Basic 3D Scatter Plot

# %%
# Generate simple 3D data
df_basic = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'z': np.random.randn(200),
})

# Basic 3D scatter plot
(
    ggplot(df_basic, aes(x='x', y='y', z='z'))
    + geom_point_3d()
)

# %% [markdown]
# ## 2. Customizing Point Appearance

# %%
# Custom size, color, and transparency
(
    ggplot(df_basic, aes(x='x', y='y', z='z'))
    + geom_point_3d(size=10, color='steelblue', alpha=0.6)
)

# %%
# Custom marker shape
(
    ggplot(df_basic, aes(x='x', y='y', z='z'))
    + geom_point_3d(size=8, color='crimson', shape='diamond')
)

# %% [markdown]
# ## 3. Color Mapping by Category

# %%
# Generate data with categories
df_categorical = pd.DataFrame({
    'x': np.random.randn(300),
    'y': np.random.randn(300),
    'z': np.random.randn(300),
    'species': np.random.choice(['Setosa', 'Versicolor', 'Virginica'], 300),
    'region': np.random.choice(['North', 'South', 'East', 'West'], 300),
})

# Color by category
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
)

# %% [markdown]
# ## 4. Shape Mapping by Category

# %%
# Shape by category (uses 3D-compatible symbols: circle, square, diamond, cross, x)
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', shape='species'))
    + geom_point_3d(size=8, color='darkblue')
)

# %% [markdown]
# ## 5. Combined Color and Shape Mapping

# %%
# Both color and shape mapped to different variables
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species', shape='region'))
    + geom_point_3d(size=7)
)

# %%
# Color and shape mapped to the same variable
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species', shape='species'))
    + geom_point_3d(size=8)
)

# %% [markdown]
# ## 6. Using Scales for Custom Colors

# %%
# Manual color scale
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=7)
    + scale_color_manual(values=['#e41a1c', '#377eb8', '#4daf4a'])
)

# %%
# Brewer color palette
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=7)
    + scale_color_brewer(palette='Set2')
)

# %% [markdown]
# ## 7. Faceting with facet_wrap

# %%
# facet_wrap - single variable faceting
(
    ggplot(df_categorical, aes(x='x', y='y', z='z'))
    + geom_point_3d(size=5, color='steelblue')
    + facet_wrap('species')
)

# %%
# facet_wrap with color grouping inside each facet
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='region'))
    + geom_point_3d(size=5)
    + facet_wrap('species')
)

# %%
# facet_wrap with custom number of columns
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=5)
    + facet_wrap('region', ncol=2)
)

# %% [markdown]
# ## 8. Faceting with facet_grid

# %%
# Create data with two categorical variables for grid faceting
df_grid = pd.DataFrame({
    'x': np.random.randn(400),
    'y': np.random.randn(400),
    'z': np.random.randn(400),
    'treatment': np.tile(np.repeat(['Control', 'Treatment'], 100), 2),
    'timepoint': np.repeat(['Day 1', 'Day 7'], 200),
})

# facet_grid - two variable faceting (rows x columns)
(
    ggplot(df_grid, aes(x='x', y='y', z='z'))
    + geom_point_3d(size=5, color='purple', alpha=0.7)
    + facet_grid('treatment', 'timepoint')
)

# %%
# facet_grid with color encoding
(
    ggplot(df_grid, aes(x='x', y='y', z='z', color='treatment'))
    + geom_point_3d(size=5)
    + facet_grid('treatment', 'timepoint')
)

# %% [markdown]
# ## 9. Applying Themes

# %%
# Minimal theme
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + theme_minimal()
)

# %%
# Dark theme
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + theme_dark()
)

# %%
# Classic theme
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + theme_classic()
)

# %%
# ggplot2 theme
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + theme_ggplot2()
)

# %% [markdown]
# ## 10. Adding Labels with labs()

# %%
# Custom title and axis labels
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + labs(
        title='3D Scatter Plot of Species Data',
        x='X Coordinate',
        y='Y Coordinate',
    )
)

# %% [markdown]
# ## 11. Adjusting Figure Size

# %%
# Custom figure size
(
    ggplot(df_categorical, aes(x='x', y='y', z='z', color='species'))
    + geom_point_3d(size=6)
    + labs(title='Large 3D Plot')
    + ggsize(width=900, height=700)
)

# %% [markdown]
# ## 12. Real-World Example: Iris-like Dataset

# %%
# Simulate iris-like data with actual measurements
np.random.seed(123)

# Setosa: smaller, clustered
setosa = pd.DataFrame({
    'sepal_length': np.random.normal(5.0, 0.35, 50),
    'sepal_width': np.random.normal(3.4, 0.38, 50),
    'petal_length': np.random.normal(1.5, 0.17, 50),
    'species': 'Setosa'
})

# Versicolor: medium, spread
versicolor = pd.DataFrame({
    'sepal_length': np.random.normal(5.9, 0.52, 50),
    'sepal_width': np.random.normal(2.8, 0.31, 50),
    'petal_length': np.random.normal(4.3, 0.47, 50),
    'species': 'Versicolor'
})

# Virginica: larger, spread
virginica = pd.DataFrame({
    'sepal_length': np.random.normal(6.6, 0.64, 50),
    'sepal_width': np.random.normal(3.0, 0.32, 50),
    'petal_length': np.random.normal(5.5, 0.55, 50),
    'species': 'Virginica'
})

iris_df = pd.concat([setosa, versicolor, virginica], ignore_index=True)

# Visualize the 3D structure of iris data
(
    ggplot(iris_df, aes(x='sepal_length', y='sepal_width', z='petal_length', color='species'))
    + geom_point_3d(size=6, alpha=0.8)
    + scale_color_manual(values=['#1b9e77', '#d95f02', '#7570b3'])
    + labs(title='Iris Dataset in 3D')
    + theme_minimal()
)

# %% [markdown]
# ## 13. Time Series in 3D

# %%
# Create time-based 3D data (e.g., stock prices over time)
dates = pd.date_range('2023-01-01', periods=100, freq='D')
df_time = pd.DataFrame({
    'day': np.arange(100),
    'price': 100 + np.cumsum(np.random.randn(100) * 2),
    'volume': np.abs(np.random.randn(100) * 1000 + 5000),
    'volatility': np.abs(np.random.randn(100) * 0.5 + 1),
    'trend': np.where(np.arange(100) < 50, 'Bearish', 'Bullish'),
})

# 3D visualization of price, volume, and volatility over time
(
    ggplot(df_time, aes(x='day', y='price', z='volume', color='trend'))
    + geom_point_3d(size=5)
    + labs(
        title='Stock Analysis in 3D',
        x='Trading Day',
        y='Price ($)',
    )
    + scale_color_manual(values=['#d62728', '#2ca02c'])
    + theme_minimal()
)

# %% [markdown]
# ## 14. Clustering Visualization

# %%
# Generate clustered 3D data
def generate_cluster(center, n_points, spread):
    return pd.DataFrame({
        'x': np.random.normal(center[0], spread, n_points),
        'y': np.random.normal(center[1], spread, n_points),
        'z': np.random.normal(center[2], spread, n_points),
    })

cluster1 = generate_cluster([0, 0, 0], 100, 0.5)
cluster1['cluster'] = 'A'

cluster2 = generate_cluster([3, 3, 3], 100, 0.5)
cluster2['cluster'] = 'B'

cluster3 = generate_cluster([0, 3, 6], 100, 0.5)
cluster3['cluster'] = 'C'

cluster4 = generate_cluster([6, 0, 3], 100, 0.5)
cluster4['cluster'] = 'D'

df_clusters = pd.concat([cluster1, cluster2, cluster3, cluster4], ignore_index=True)

# Visualize clusters
(
    ggplot(df_clusters, aes(x='x', y='y', z='z', color='cluster'))
    + geom_point_3d(size=5, alpha=0.7)
    + scale_color_brewer(palette='Set1')
    + labs(title='3D Cluster Visualization')
    + theme_minimal()
)

# %% [markdown]
# ## 15. PCA-like Dimensionality Reduction Visualization

# %%
# Simulate PCA output with 3 principal components
np.random.seed(456)

df_pca = pd.DataFrame({
    'PC1': np.concatenate([
        np.random.normal(-2, 0.8, 80),
        np.random.normal(0, 0.8, 80),
        np.random.normal(2, 0.8, 80),
    ]),
    'PC2': np.concatenate([
        np.random.normal(0, 0.6, 80),
        np.random.normal(2, 0.6, 80),
        np.random.normal(-1, 0.6, 80),
    ]),
    'PC3': np.concatenate([
        np.random.normal(1, 0.5, 80),
        np.random.normal(-1, 0.5, 80),
        np.random.normal(0, 0.5, 80),
    ]),
    'class': np.repeat(['Class A', 'Class B', 'Class C'], 80),
    'batch': np.tile(np.repeat(['Batch 1', 'Batch 2'], 40), 3),
})

# PCA visualization with class coloring
(
    ggplot(df_pca, aes(x='PC1', y='PC2', z='PC3', color='class'))
    + geom_point_3d(size=5, alpha=0.8)
    + labs(title='PCA Results - 3 Principal Components')
    + theme_minimal()
)

# %%
# PCA with faceting by batch
(
    ggplot(df_pca, aes(x='PC1', y='PC2', z='PC3', color='class'))
    + geom_point_3d(size=5, alpha=0.8)
    + facet_wrap('batch')
    + labs(title='PCA Results by Batch')
    + theme_minimal()
)

# %% [markdown]
# ## 16. Geospatial-like 3D Data

# %%
# Simulate elevation data with x=longitude, y=latitude, z=elevation
np.random.seed(789)

n_points = 300
df_geo = pd.DataFrame({
    'longitude': np.random.uniform(-120, -70, n_points),
    'latitude': np.random.uniform(25, 50, n_points),
    'elevation': np.random.exponential(1000, n_points) + 500,
    'terrain': np.random.choice(['Mountain', 'Valley', 'Plain', 'Coast'], n_points),
})

# 3D geographic visualization
(
    ggplot(df_geo, aes(x='longitude', y='latitude', z='elevation', color='terrain'))
    + geom_point_3d(size=5, alpha=0.7)
    + scale_color_brewer(palette='Dark2')
    + labs(
        title='3D Terrain Visualization',
        x='Longitude',
        y='Latitude',
    )
    + theme_minimal()
)

# %% [markdown]
# ## 17. Scientific Data: Molecular Positions

# %%
# Simulate molecular/atomic positions
np.random.seed(101)

# Create a simple molecule-like structure
atoms = []
atom_types = ['Carbon', 'Hydrogen', 'Oxygen', 'Nitrogen']
atom_colors = {'Carbon': 'gray', 'Hydrogen': 'white', 'Oxygen': 'red', 'Nitrogen': 'blue'}

for i in range(50):
    atom_type = np.random.choice(atom_types, p=[0.4, 0.3, 0.2, 0.1])
    atoms.append({
        'x': np.random.uniform(-5, 5),
        'y': np.random.uniform(-5, 5),
        'z': np.random.uniform(-5, 5),
        'atom': atom_type,
    })

df_molecule = pd.DataFrame(atoms)

# Molecular visualization
(
    ggplot(df_molecule, aes(x='x', y='y', z='z', color='atom', shape='atom'))
    + geom_point_3d(size=10, alpha=0.9)
    + scale_color_manual(values=['#404040', '#FFFFFF', '#FF0000', '#0000FF'])
    + labs(title='Molecular Structure Visualization')
    + theme_dark()
)

# %% [markdown]
# ## 18. Comparing Groups with Facets and Color

# %%
# A/B testing scenario with multiple metrics
np.random.seed(202)

df_ab = pd.DataFrame({
    'conversion_rate': np.concatenate([
        np.random.normal(0.05, 0.01, 100),
        np.random.normal(0.07, 0.01, 100),
    ]),
    'time_on_page': np.concatenate([
        np.random.normal(120, 30, 100),
        np.random.normal(150, 35, 100),
    ]),
    'bounce_rate': np.concatenate([
        np.random.normal(0.4, 0.08, 100),
        np.random.normal(0.35, 0.07, 100),
    ]),
    'variant': np.repeat(['Control', 'Treatment'], 100),
    'device': np.tile(np.repeat(['Mobile', 'Desktop'], 50), 2),
})

# Compare A/B test results in 3D
(
    ggplot(df_ab, aes(x='conversion_rate', y='time_on_page', z='bounce_rate', color='variant'))
    + geom_point_3d(size=5, alpha=0.7)
    + facet_wrap('device')
    + labs(title='A/B Test Results by Device')
    + scale_color_manual(values=['#1f77b4', '#ff7f0e'])
    + theme_minimal()
)

# %% [markdown]
# ## 19. Dense Data with Transparency

# %%
# Large dataset with many overlapping points
np.random.seed(303)

df_dense = pd.DataFrame({
    'x': np.random.randn(2000),
    'y': np.random.randn(2000),
    'z': np.random.randn(2000),
})

# Use transparency to see density
(
    ggplot(df_dense, aes(x='x', y='y', z='z'))
    + geom_point_3d(size=3, alpha=0.2, color='darkblue')
    + labs(title='Dense 3D Point Cloud')
    + theme_minimal()
)

# %% [markdown]
# ## 20. Combining Multiple Features

# %%
# Full-featured example combining many options
np.random.seed(404)

df_full = pd.DataFrame({
    'metric_a': np.concatenate([
        np.random.normal(10, 2, 75),
        np.random.normal(15, 2, 75),
        np.random.normal(12, 2, 75),
    ]),
    'metric_b': np.concatenate([
        np.random.normal(50, 10, 75),
        np.random.normal(70, 10, 75),
        np.random.normal(60, 10, 75),
    ]),
    'metric_c': np.concatenate([
        np.random.normal(100, 20, 75),
        np.random.normal(150, 20, 75),
        np.random.normal(120, 20, 75),
    ]),
    'category': np.repeat(['Alpha', 'Beta', 'Gamma'], 75),
    'quarter': np.tile(np.repeat(['Q1', 'Q2', 'Q3'], 25), 3),
})

# Comprehensive visualization
(
    ggplot(df_full, aes(x='metric_a', y='metric_b', z='metric_c', color='category'))
    + geom_point_3d(size=6, alpha=0.8)
    + facet_wrap('quarter', ncol=3)
    + scale_color_brewer(palette='Set1')
    + labs(
        title='Quarterly Performance by Category',
        x='Metric A',
        y='Metric B',
    )
    + theme_minimal()
    + ggsize(width=1000, height=400)
)

# %% [markdown]
# ## 21. Spiral/Helix Data

# %%
# Create a 3D spiral/helix
t = np.linspace(0, 4 * np.pi, 200)
df_spiral = pd.DataFrame({
    'x': np.cos(t) * (1 + t / 10),
    'y': np.sin(t) * (1 + t / 10),
    'z': t,
    'phase': np.where(t < 2 * np.pi, 'Phase 1', np.where(t < 3 * np.pi, 'Phase 2', 'Phase 3')),
})

# Visualize the spiral
(
    ggplot(df_spiral, aes(x='x', y='y', z='z', color='phase'))
    + geom_point_3d(size=5)
    + labs(title='3D Spiral Structure')
    + theme_dark()
)

# %% [markdown]
# ## 22. Sphere Distribution

# %%
# Generate points on a sphere surface
np.random.seed(505)

n = 500
phi = np.random.uniform(0, 2 * np.pi, n)
costheta = np.random.uniform(-1, 1, n)
theta = np.arccos(costheta)

df_sphere = pd.DataFrame({
    'x': np.sin(theta) * np.cos(phi),
    'y': np.sin(theta) * np.sin(phi),
    'z': np.cos(theta),
    'hemisphere': np.where(np.cos(theta) > 0, 'Northern', 'Southern'),
})

# Visualize spherical distribution
(
    ggplot(df_sphere, aes(x='x', y='y', z='z', color='hemisphere'))
    + geom_point_3d(size=4, alpha=0.7)
    + labs(title='Points on a Sphere')
    + scale_color_manual(values=['#3498db', '#e74c3c'])
    + theme_minimal()
)

# %%
