# geom_surface Examples
# Comprehensive examples for 3D surface plots in ggplotly
# Each cell is self-contained and can be run independently in Jupyter

# %% [markdown]
# # geom_surface Examples
#
# This notebook demonstrates the various features of `geom_surface` and `geom_wireframe`
# for creating interactive 3D surface plots with ggplotly.

# %% [markdown]
# ## Setup

# %%
import pandas as pd
import numpy as np
from ggplotly import (
    ggplot, aes, geom_surface, geom_wireframe, geom_point_3d,
    facet_wrap, facet_grid,
    theme_minimal, theme_dark, theme_classic, theme_ggplot2,
    labs,
    ggsize,
)

# Set random seed for reproducibility
np.random.seed(42)


# Helper function to create surface data from a function
def make_surface_data(func, x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    """Create a DataFrame from a z = f(x, y) function."""
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)
    return pd.DataFrame({
        'x': X.flatten(),
        'y': Y.flatten(),
        'z': Z.flatten(),
    })


# %% [markdown]
# ## 1. Basic Surface Plot

# %%
# Simple paraboloid: z = x^2 + y^2
df_paraboloid = make_surface_data(lambda x, y: x**2 + y**2)

(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface()
)

# %% [markdown]
# ## 2. Classic Mathematical Surfaces

# %%
# Sinc function: z = sin(sqrt(x^2 + y^2)) / sqrt(x^2 + y^2)
def sinc_2d(x, y):
    r = np.sqrt(x**2 + y**2)
    # Avoid division by zero
    return np.where(r == 0, 1, np.sin(r) / r)

df_sinc = make_surface_data(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=80)

(
    ggplot(df_sinc, aes(x='x', y='y', z='z'))
    + geom_surface()
    + labs(title='2D Sinc Function')
)

# %%
# Ripple pattern: z = sin(x) * cos(y)
df_ripple = make_surface_data(lambda x, y: np.sin(x) * np.cos(y))

(
    ggplot(df_ripple, aes(x='x', y='y', z='z'))
    + geom_surface()
    + labs(title='Ripple Pattern: sin(x) * cos(y)')
)

# %%
# Saddle surface: z = x^2 - y^2
df_saddle = make_surface_data(lambda x, y: x**2 - y**2)

(
    ggplot(df_saddle, aes(x='x', y='y', z='z'))
    + geom_surface()
    + labs(title='Saddle Surface: x² - y²')
)

# %% [markdown]
# ## 3. Colorscale Options

# %%
# Default Viridis colorscale
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis')
    + labs(title='Viridis (Default)')
)

# %%
# Plasma colorscale
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Plasma')
    + labs(title='Plasma Colorscale')
)

# %%
# Blues colorscale
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Blues')
    + labs(title='Blues Colorscale')
)

# %%
# RdBu (Red-Blue diverging) colorscale - great for saddle surfaces
(
    ggplot(df_saddle, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='RdBu')
    + labs(title='RdBu Colorscale (Diverging)')
)

# %%
# Hot colorscale
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Hot')
    + labs(title='Hot Colorscale')
)

# %%
# Earth colorscale - good for terrain
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Earth')
    + labs(title='Earth Colorscale')
)

# %%
# Reversed colorscale
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis', reversescale=True)
    + labs(title='Reversed Viridis')
)

# %% [markdown]
# ## 4. Opacity/Transparency

# %%
# Semi-transparent surface
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(alpha=0.7, colorscale='Plasma')
    + labs(title='Semi-Transparent Surface (alpha=0.7)')
)

# %%
# Very transparent for layering
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(alpha=0.4, colorscale='Blues')
    + labs(title='Highly Transparent Surface (alpha=0.4)')
)

# %% [markdown]
# ## 5. Contour Projections

# %%
# Z-axis contour projection
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(
        colorscale='Viridis',
        contours=dict(
            z=dict(show=True, usecolormap=True, project=dict(z=True))
        )
    )
    + labs(title='Surface with Z Contour Projection')
)

# %%
# Multiple contour projections
(
    ggplot(df_sinc, aes(x='x', y='y', z='z'))
    + geom_surface(
        colorscale='Plasma',
        contours=dict(
            x=dict(show=True, usecolormap=True, project=dict(x=True)),
            y=dict(show=True, usecolormap=True, project=dict(y=True)),
            z=dict(show=True, usecolormap=True, project=dict(z=True)),
        )
    )
    + labs(title='Surface with All Contour Projections')
)

# %%
# Show only contours (hide surface)
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(
        hidesurface=True,
        contours=dict(
            z=dict(show=True, usecolormap=True, highlightcolor='white', project=dict(z=True))
        )
    )
    + labs(title='Contours Only (Surface Hidden)')
)

# %% [markdown]
# ## 6. Colorbar Customization

# %%
# Hide colorbar
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(showscale=False)
    + labs(title='Surface Without Colorbar')
)

# %%
# Custom colorbar title
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorbar_title='Height (z)')
    + labs(title='Surface with Custom Colorbar Title')
)

# %% [markdown]
# ## 7. Basic Wireframe Plot

# %%
# Basic wireframe
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_wireframe()
    + labs(title='Basic Wireframe')
)

# %%
# Custom wireframe color
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_wireframe(color='darkblue', linewidth=1.5)
    + labs(title='Wireframe with Custom Color')
)

# %%
# Wireframe with transparency
(
    ggplot(df_sinc, aes(x='x', y='y', z='z'))
    + geom_wireframe(color='purple', alpha=0.6)
    + labs(title='Semi-Transparent Wireframe')
)

# %% [markdown]
# ## 8. Combining Surface with Points

# %%
# Create sample points on the surface
np.random.seed(123)
sample_x = np.random.uniform(-4, 4, 30)
sample_y = np.random.uniform(-4, 4, 30)
sample_z = sample_x**2 + sample_y**2 + np.random.randn(30) * 2  # With noise

df_points = pd.DataFrame({'x': sample_x, 'y': sample_y, 'z': sample_z})

# Surface with overlaid sample points
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(alpha=0.6, colorscale='Blues')
    + geom_point_3d(data=df_points, size=8, color='red')
    + labs(title='Surface with Sample Points')
)

# %% [markdown]
# ## 9. Fill Aesthetic (surfacecolor)

# %%
# Create data with separate fill variable
df_with_fill = make_surface_data(lambda x, y: np.sin(np.sqrt(x**2 + y**2)))
# Add a fill variable (e.g., gradient based on angle)
df_with_fill['angle'] = np.arctan2(df_with_fill['y'], df_with_fill['x'])

# Surface colored by angle instead of height
(
    ggplot(df_with_fill, aes(x='x', y='y', z='z', fill='angle'))
    + geom_surface(colorscale='Rainbow')
    + labs(title='Surface Colored by Angle')
)

# %%
# Create data with intensity variable
df_intensity = make_surface_data(lambda x, y: np.exp(-(x**2 + y**2) / 10))
df_intensity['intensity'] = np.sqrt(df_intensity['x']**2 + df_intensity['y']**2)

# Gaussian surface colored by radius
(
    ggplot(df_intensity, aes(x='x', y='y', z='z', fill='intensity'))
    + geom_surface(colorscale='Viridis')
    + labs(title='Gaussian Surface Colored by Radius')
)

# %% [markdown]
# ## 10. Themes

# %%
# Minimal theme
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Plasma')
    + theme_minimal()
    + labs(title='Minimal Theme')
)

# %%
# Dark theme
(
    ggplot(df_sinc, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Inferno')
    + theme_dark()
    + labs(title='Dark Theme')
)

# %%
# Classic theme
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Blues')
    + theme_classic()
    + labs(title='Classic Theme')
)

# %%
# ggplot2 theme
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis')
    + theme_ggplot2()
    + labs(title='ggplot2 Theme')
)

# %% [markdown]
# ## 11. Labels with labs()

# %%
# Custom axis labels
(
    ggplot(df_paraboloid, aes(x='x', y='y', z='z'))
    + geom_surface()
    + labs(
        title='Paraboloid Surface',
        x='X Coordinate',
        y='Y Coordinate',
        z='Height (z = x² + y²)',
    )
)

# %% [markdown]
# ## 12. Figure Size with ggsize()

# %%
# Custom figure size
(
    ggplot(df_sinc, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Plasma')
    + labs(title='Large 3D Surface')
    + ggsize(width=900, height=700)
)

# %% [markdown]
# ## 13. Faceting Surfaces

# %%
# Create data for multiple surfaces (different parameters)
def make_gaussian(center_x, center_y, sigma, label):
    df = make_surface_data(
        lambda x, y: np.exp(-((x - center_x)**2 + (y - center_y)**2) / (2 * sigma**2)),
        x_range=(-5, 5),
        y_range=(-5, 5),
        resolution=30,
    )
    df['type'] = label
    return df

df_facet = pd.concat([
    make_gaussian(0, 0, 1.0, 'Narrow'),
    make_gaussian(0, 0, 2.0, 'Medium'),
    make_gaussian(0, 0, 3.0, 'Wide'),
], ignore_index=True)

# Faceted surface plots
(
    ggplot(df_facet, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis')
    + facet_wrap('type')
    + labs(title='Gaussian Surfaces with Different Widths')
)

# %% [markdown]
# ## 14. Real-World Example: Terrain/Elevation

# %%
# Simulate terrain data
np.random.seed(42)

def generate_terrain(size=50):
    """Generate realistic-looking terrain using superposition of waves."""
    x = np.linspace(0, 10, size)
    y = np.linspace(0, 10, size)
    X, Y = np.meshgrid(x, y)

    # Combine multiple frequencies for realistic terrain
    Z = (
        2 * np.sin(0.5 * X) * np.cos(0.5 * Y) +
        1 * np.sin(1.0 * X + 0.5) * np.cos(0.8 * Y) +
        0.5 * np.sin(2.0 * X) * np.cos(2.0 * Y) +
        0.25 * np.random.randn(size, size)  # Add noise
    )
    Z = Z - Z.min()  # Make elevation positive

    return pd.DataFrame({
        'longitude': X.flatten(),
        'latitude': Y.flatten(),
        'elevation': Z.flatten(),
    })

df_terrain = generate_terrain()

# Terrain visualization
(
    ggplot(df_terrain, aes(x='longitude', y='latitude', z='elevation'))
    + geom_surface(colorscale='Earth')
    + labs(
        title='Simulated Terrain',
        x='Longitude',
        y='Latitude',
        z='Elevation (m)',
    )
    + theme_minimal()
)

# %% [markdown]
# ## 15. Real-World Example: 2D Probability Distribution

# %%
# Bivariate normal distribution
def bivariate_normal(x, y, mu_x=0, mu_y=0, sigma_x=1, sigma_y=1, rho=0):
    """2D Gaussian probability density."""
    z = (
        ((x - mu_x) / sigma_x)**2
        - 2 * rho * ((x - mu_x) / sigma_x) * ((y - mu_y) / sigma_y)
        + ((y - mu_y) / sigma_y)**2
    )
    return np.exp(-z / (2 * (1 - rho**2))) / (2 * np.pi * sigma_x * sigma_y * np.sqrt(1 - rho**2))

df_gaussian = make_surface_data(
    lambda x, y: bivariate_normal(x, y, sigma_x=1.5, sigma_y=1.0, rho=0.5),
    x_range=(-4, 4),
    y_range=(-4, 4),
    resolution=60,
)

# Probability density surface
(
    ggplot(df_gaussian, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis')
    + labs(
        title='Bivariate Normal Distribution',
        x='X',
        y='Y',
        z='Probability Density',
    )
    + theme_minimal()
)

# %% [markdown]
# ## 16. Real-World Example: Response Surface (Optimization)

# %%
# Simulate a response surface for optimization
def response_surface(x, y):
    """Response surface with a maximum (for optimization visualization)."""
    return 10 - (x - 2)**2 - (y + 1)**2 + 0.5 * np.sin(3 * x) * np.cos(3 * y)

df_response = make_surface_data(response_surface, x_range=(-2, 6), y_range=(-5, 3))

# Find the optimum
optimal_idx = df_response['z'].idxmax()
optimal_point = df_response.loc[[optimal_idx]]

# Response surface with optimum marked
(
    ggplot(df_response, aes(x='x', y='y', z='z'))
    + geom_surface(alpha=0.8, colorscale='RdYlGn')
    + geom_point_3d(data=optimal_point, size=12, color='black')
    + labs(title='Response Surface Optimization')
    + theme_minimal()
)

# %% [markdown]
# ## 17. Parametric Surfaces: Torus
#
# Note: Parametric surfaces like torus, sphere, and helicoid are defined in parameter
# space (u, v), not on a regular (x, y) grid. For these, we use Plotly directly
# since geom_surface is optimized for z = f(x, y) functions on Cartesian grids.

# %%
import plotly.graph_objects as go

# Create a torus using Plotly directly
def plot_torus(R=3, r=1, resolution=50):
    """Create a torus with major radius R and minor radius r."""
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, 2 * np.pi, resolution)
    U, V = np.meshgrid(u, v)

    X = (R + r * np.cos(V)) * np.cos(U)
    Y = (R + r * np.cos(V)) * np.sin(U)
    Z = r * np.sin(V)

    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Rainbow')])
    fig.update_layout(title='Torus', scene=dict(aspectmode='data'))
    return fig

plot_torus().show()

# %% [markdown]
# ## 18. Parametric Surfaces: Sphere

# %%
# Create a sphere using Plotly directly
def plot_sphere(radius=1, resolution=50):
    """Create a sphere."""
    u = np.linspace(0, 2 * np.pi, resolution)
    v = np.linspace(0, np.pi, resolution)
    U, V = np.meshgrid(u, v)

    X = radius * np.cos(U) * np.sin(V)
    Y = radius * np.sin(U) * np.sin(V)
    Z = radius * np.cos(V)

    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Blues')])
    fig.update_layout(title='Sphere', scene=dict(aspectmode='data'))
    return fig

plot_sphere().show()

# %% [markdown]
# ## 19. Parametric Surfaces: Helicoid

# %%
# Create a helicoid (twisted surface) using Plotly directly
def plot_helicoid(resolution=50):
    """Create a helicoid surface."""
    u = np.linspace(-2, 2, resolution)
    v = np.linspace(0, 4 * np.pi, resolution)
    U, V = np.meshgrid(u, v)

    X = U * np.cos(V)
    Y = U * np.sin(V)
    Z = V / 2

    fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, colorscale='Viridis')])
    fig.update_layout(title='Helicoid (Twisted Surface)')
    return fig

plot_helicoid().show()

# %% [markdown]
# ## 20. Comparing Wireframe and Surface

# %%
# Side-by-side comparison using facets
df_compare = make_surface_data(lambda x, y: np.sin(x) * np.cos(y), resolution=30)

# Show wireframe
(
    ggplot(df_compare, aes(x='x', y='y', z='z'))
    + geom_wireframe(color='steelblue', linewidth=1)
    + labs(title='Wireframe Representation')
)

# %%
# Show surface
(
    ggplot(df_compare, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis')
    + labs(title='Surface Representation')
)

# %% [markdown]
# ## 21. Real-World Example: Heat Map / Temperature Distribution

# %%
# Simulate temperature distribution (heat equation steady state)
def temperature_field(x, y):
    """Simulate steady-state temperature with heat source at origin."""
    r = np.sqrt(x**2 + y**2)
    return 100 * np.exp(-r / 3) + 20  # Room temp is 20, max is 120

df_temp = make_surface_data(temperature_field, x_range=(-10, 10), y_range=(-10, 10))

# Temperature surface
(
    ggplot(df_temp, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Hot')
    + labs(
        title='Temperature Distribution',
        x='X Position (m)',
        y='Y Position (m)',
        z='Temperature (°C)',
    )
    + theme_minimal()
)

# %% [markdown]
# ## 22. Real-World Example: Wave Interference

# %%
# Two-source wave interference pattern
def wave_interference(x, y, source1=(-3, 0), source2=(3, 0), wavelength=1):
    """Simulate wave interference from two point sources."""
    k = 2 * np.pi / wavelength
    r1 = np.sqrt((x - source1[0])**2 + (y - source1[1])**2)
    r2 = np.sqrt((x - source2[0])**2 + (y - source2[1])**2)
    return np.cos(k * r1) + np.cos(k * r2)

df_interference = make_surface_data(
    lambda x, y: wave_interference(x, y, wavelength=2),
    x_range=(-10, 10),
    y_range=(-10, 10),
    resolution=80,
)

# Wave interference pattern
(
    ggplot(df_interference, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='RdBu')
    + labs(title='Two-Source Wave Interference')
    + theme_dark()
)

# %% [markdown]
# ## 23. Real-World Example: Cost Function (Machine Learning)

# %%
# Simulate a cost function landscape for gradient descent
def cost_function(x, y):
    """Cost function with local minima (like neural network loss landscape)."""
    return (
        (1 - x)**2 + 100 * (y - x**2)**2  # Rosenbrock function (banana function)
    )

# Use log scale for better visualization of Rosenbrock
df_cost = make_surface_data(cost_function, x_range=(-2, 2), y_range=(-1, 3), resolution=60)
df_cost['log_cost'] = np.log10(df_cost['z'] + 1)

# Cost function visualization
(
    ggplot(df_cost, aes(x='x', y='y', z='log_cost'))
    + geom_surface(colorscale='Inferno')
    + labs(
        title='Rosenbrock Function (Log Scale)',
        z='log₁₀(Cost)',
    )
    + theme_minimal()
)

# %%
# Simpler convex cost function
df_convex = make_surface_data(lambda x, y: x**2 + y**2)

(
    ggplot(df_convex, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Viridis', alpha=0.8)
    + labs(title='Convex Cost Function: x² + y²')
)

# %% [markdown]
# ## 24. Non-Square Grids

# %%
# Create a rectangular (non-square) surface
x = np.linspace(-10, 10, 100)  # Wide
y = np.linspace(-2, 2, 20)     # Narrow
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.exp(-Y**2)

df_rect = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten(),
})

# Non-square surface
(
    ggplot(df_rect, aes(x='x', y='y', z='z'))
    + geom_surface(colorscale='Plasma')
    + labs(title='Non-Square Grid Surface')
)

# %% [markdown]
# ## 25. Combining Multiple Features

# %%
# Full-featured example
df_full = make_surface_data(
    lambda x, y: np.sin(np.sqrt(x**2 + y**2)) * np.exp(-(x**2 + y**2) / 20),
    x_range=(-8, 8),
    y_range=(-8, 8),
    resolution=70,
)

# Comprehensive visualization
(
    ggplot(df_full, aes(x='x', y='y', z='z'))
    + geom_surface(
        colorscale='Viridis',
        alpha=0.9,
        contours=dict(
            z=dict(show=True, usecolormap=True, project=dict(z=True))
        ),
    )
    + labs(
        title='Damped Ripple with Contour Projection',
        x='X Coordinate',
        y='Y Coordinate',
        z='Amplitude',
    )
    + theme_minimal()
    + ggsize(width=900, height=700)
)

# %%
