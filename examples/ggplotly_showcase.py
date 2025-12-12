# ggplotly Comprehensive Showcase
# A complete demonstration of all ggplotly features organized from simple to complex.
# Run cells individually in VS Code or Jupyter using the `# %%` markers.

# %% [markdown]
# # ggplotly: A Grammar of Graphics for Plotly
#
# This notebook showcases all features of ggplotly, organized from basic to advanced:
# 1. **Basics** - Setup, simple plots, aesthetics
# 2. **Geoms** - All geometry types (point, line, bar, etc.)
# 3. **Scales** - Axis customization, color scales
# 4. **Themes** - Built-in and custom themes
# 5. **Facets** - Multi-panel plots
# 6. **Labels & Annotations** - Titles, labels, annotations
# 7. **Statistics** - Smoothing, density, histograms
# 8. **Coordinates** - Cartesian, flip, polar
# 9. **Maps & Geo** - Choropleth, geom_sf, projections
# 10. **3D Plots** - Scatter, surface, wireframe
# 11. **Financial** - Candlestick, OHLC
# 12. **Time Series** - geom_range, scale_x_date
# 13. **Network Graphs** - Edge bundling
# 14. **Advanced** - Complex multi-layer plots

# =============================================================================
# PART 1: BASICS
# =============================================================================

# %% [markdown]
# ## 1.1 Setup and Imports

# %%
import pandas as pd
import numpy as np
from ggplotly import *
from ggplotly.stats import stat_summary, stat_ecdf, stat_density, stat_smooth

# Set random seed for reproducibility
np.random.seed(42)

# %% [markdown]
# ## 1.2 Your First Plot - Basic Scatter

# %%
# Simple DataFrame
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 4]
})

# Minimal scatter plot
ggplot(df, aes(x='x', y='y')) + geom_point()

# %% [markdown]
# ## 1.3 Aesthetics (aes) - Mapping Data to Visual Properties

# %%
# Data with categories
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'size_var': np.random.rand(100) * 50
})

# Color mapped to category
ggplot(df, aes(x='x', y='y', color='category')) + geom_point()

# %%
# Size mapped to a variable
ggplot(df, aes(x='x', y='y', size='size_var')) + geom_point(color='steelblue', alpha=0.6)

# %%
# Multiple aesthetics combined
ggplot(df, aes(x='x', y='y', color='category', size='size_var')) + geom_point(alpha=0.7)

# %% [markdown]
# ## 1.4 Using Index as X-Axis (Pandas Integration)

# %%
# Series with DatetimeIndex - x is automatically the index
dates = pd.date_range('2024-01-01', periods=30)
values = np.cumsum(np.random.randn(30))
ts = pd.Series(values, index=dates, name='Price')

ggplot(ts) + geom_line()

# %%
# DataFrame with named index
df_indexed = pd.DataFrame(
    {'value': np.sin(np.linspace(0, 4*np.pi, 100))},
    index=pd.Index(np.linspace(0, 10, 100), name='Time')
)

ggplot(df_indexed, aes(y='value')) + geom_line()

# %% [markdown]
# ## 1.5 Built-in Datasets

# %%
# List available datasets
data()

# %%
# mpg - Fuel economy data for 234 cars (1999-2008)
mpg = data('mpg')
ggplot(mpg, aes(x='displ', y='hwy', color='class')) + geom_point()

# %%
# diamonds - Prices of 50,000+ diamonds
diamonds = data('diamonds')
(ggplot(diamonds.sample(1000), aes(x='carat', y='price', color='cut'))
 + geom_point(alpha=0.5)
 + labs(title='Diamond Prices by Carat and Cut'))

# %%
# iris - Classic flower measurements dataset
iris = data('iris')
(ggplot(iris, aes(x='Sepal.Length', y='Sepal.Width', color='Species'))
 + geom_point(size=8)
 + labs(title='Iris Dataset'))

# %%
# mtcars - Motor Trend car road tests
mtcars = data('mtcars')
(ggplot(mtcars, aes(x='wt', y='mpg', color='cyl'))
 + geom_point(size=10)
 + labs(title='Car Weight vs MPG', x='Weight (1000 lbs)', y='Miles per Gallon'))

# %%
# economics - US economic time series
economics = data('economics')
(ggplot(economics, aes(x='date', y='unemploy'))
 + geom_line()
 + labs(title='US Unemployment Over Time', y='Unemployed (thousands)'))

# %%
# midwest - Midwest demographics
midwest = data('midwest')
(ggplot(midwest, aes(x='popdensity', y='percollege', color='state'))
 + geom_point(alpha=0.6)
 + scale_x_log10()
 + labs(title='Population Density vs College Education'))

# %%
# txhousing - Texas housing market data
txhousing = data('txhousing')
houston = txhousing[txhousing['city'] == 'Houston']
(ggplot(houston, aes(x='date', y='median'))
 + geom_line()
 + labs(title='Houston Median Home Prices'))

# %%
# faithfuld - Old Faithful geyser eruption data (2D density)
faithfuld = data('faithfuld')
(ggplot(faithfuld, aes(x='waiting', y='eruptions', fill='density'))
 + geom_tile()
 + scale_fill_viridis_c()
 + labs(title='Old Faithful Eruption Patterns'))

# %%
# msleep - Mammal sleep data
msleep = data('msleep')
(ggplot(msleep.dropna(subset=['sleep_total', 'bodywt']),
        aes(x='bodywt', y='sleep_total', color='vore'))
 + geom_point(size=8)
 + scale_x_log10()
 + labs(title='Body Weight vs Sleep Time', x='Body Weight (kg, log scale)', y='Total Sleep (hours)'))

# %%
# presidential - US presidential terms
presidential = data('presidential')
(ggplot(presidential, aes(x='start', y='name', color='party'))
 + geom_point(size=10)
 + labs(title='US Presidents', x='Start Date'))

# =============================================================================
# PART 2: GEOMS - Geometry Types
# =============================================================================

# %% [markdown]
# ## 2.1 geom_point - Scatter Plots

# %%
# Random scatter with transparency
df = pd.DataFrame({
    'x': np.random.randn(500),
    'y': np.random.randn(500)
})

ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5, color='purple')

# %%
# Scatter with custom size and shape
ggplot(df, aes(x='x', y='y')) + geom_point(size=10, color='red', shape='diamond')

# %% [markdown]
# ## 2.2 geom_line - Line Plots

# %%
# Simple line plot
x = np.linspace(0, 10, 100)
df = pd.DataFrame({'x': x, 'y': np.sin(x)})

ggplot(df, aes(x='x', y='y')) + geom_line(color='steelblue', size=2)

# %%
# Multiple lines with color grouping
df = pd.DataFrame({
    'x': np.tile(np.linspace(0, 10, 50), 3),
    'y': np.concatenate([
        np.sin(np.linspace(0, 10, 50)),
        np.cos(np.linspace(0, 10, 50)),
        np.sin(np.linspace(0, 10, 50)) + np.cos(np.linspace(0, 10, 50))
    ]),
    'group': np.repeat(['sin', 'cos', 'sin+cos'], 50)
})

ggplot(df, aes(x='x', y='y', color='group')) + geom_line(size=2)

# %% [markdown]
# ## 2.3 geom_path - Connect Points in Order (Not Sorted by X)

# %%
import math

# Spiral - geom_path preserves point order
t_vals = [i * 4 * math.pi / 100 for i in range(100)]
spiral = pd.DataFrame({
    'x': [t * math.cos(t) for t in t_vals],
    'y': [t * math.sin(t) for t in t_vals],
})

(ggplot(spiral, aes(x='x', y='y'))
 + geom_path(color='steelblue', size=2)
 + labs(title='Spiral with geom_path (correct)'))

# %%
# Star shape using geom_path
points = 5
outer_r, inner_r = 1, 0.4
star_x, star_y = [], []
for i in range(points * 2 + 1):
    angle = i * math.pi / points - math.pi / 2
    r = outer_r if i % 2 == 0 else inner_r
    star_x.append(r * math.cos(angle))
    star_y.append(r * math.sin(angle))

star = pd.DataFrame({'x': star_x, 'y': star_y})
ggplot(star, aes(x='x', y='y')) + geom_path(color='gold', size=3)

# %% [markdown]
# ## 2.4 geom_bar - Bar Charts

# %%
# Count-based bar chart
df = pd.DataFrame({'category': np.random.choice(['A', 'B', 'C', 'D', 'E'], 200)})
ggplot(df, aes(x='category')) + geom_bar()

# %%
# Bar chart with fill color by category
mpg = data('mpg')
ggplot(mpg, aes(x='class', fill='class')) + geom_bar(alpha=0.8)

# %%
# Stacked bar chart
ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar()

# %%
# Dodged (side-by-side) bar chart
ggplot(mpg, aes(x='cyl', fill='drv')) + geom_bar(position='dodge')

# %%
# Using position_dodge explicitly with custom width
(ggplot(mpg, aes(x='cyl', fill='drv'))
 + geom_bar(position=position_dodge(width=0.8)))

# %%
# Using position_stack explicitly (default for bar)
(ggplot(mpg, aes(x='cyl', fill='drv'))
 + geom_bar(position=position_stack()))

# %% [markdown]
# ## 2.5 geom_col - Column Chart (Pre-Computed Heights)

# %%
# Pre-aggregated data
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [25, 40, 30, 55]
})

ggplot(df, aes(x='category', y='value')) + geom_col(fill='steelblue')

# %%
# Grouped column chart
df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'group': ['G1', 'G2'] * 3,
    'value': [10, 15, 20, 25, 15, 20]
})

ggplot(df, aes(x='category', y='value', fill='group')) + geom_col(position='dodge')

# %% [markdown]
# ## 2.6 geom_histogram - Distribution Plots

# %%
# Basic histogram
df = pd.DataFrame({'x': np.random.randn(1000)})
ggplot(df, aes(x='x')) + geom_histogram(fill='steelblue', alpha=0.7)

# %%
# Histogram with custom bins and color
ggplot(df, aes(x='x')) + geom_histogram(bins=30, color='white', fill='#FF6B6B')

# %%
# Overlapping histograms by group
df = pd.DataFrame({
    'x': np.concatenate([np.random.normal(0, 1, 500), np.random.normal(2, 1.5, 500)]),
    'group': ['A'] * 500 + ['B'] * 500
})

ggplot(df, aes(x='x', fill='group')) + geom_histogram(alpha=0.5, bins=30)

# %% [markdown]
# ## 2.7 geom_boxplot - Box and Whisker Plots

# %%
# Basic boxplot
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C', 'D'], 50),
    'value': np.random.randn(200) * np.tile([1, 2, 1.5, 0.8], 50) + np.tile([0, 1, -1, 2], 50)
})

ggplot(df, aes(x='category', y='value')) + geom_boxplot()

# %%
# Boxplot with color by category
ggplot(df, aes(x='category', y='value', fill='category')) + geom_boxplot(alpha=0.7)

# %% [markdown]
# ## 2.8 geom_violin - Violin Plots

# %%
ggplot(df, aes(x='category', y='value', fill='category')) + geom_violin(alpha=0.6)

# %% [markdown]
# ## 2.9 geom_area - Area Plots

# %%
# Simple area plot
x = np.linspace(0, 10, 100)
df = pd.DataFrame({'x': x, 'y': np.sin(x) + 1.5})

ggplot(df, aes(x='x', y='y')) + geom_area(fill='lightblue', alpha=0.7)

# %%
# Stacked area with groups
df = pd.DataFrame({
    'x': np.tile(np.linspace(0, 10, 50), 3),
    'y': np.abs(np.concatenate([
        np.sin(np.linspace(0, 10, 50)),
        0.5 * np.cos(np.linspace(0, 10, 50)) + 0.5,
        0.3 * np.sin(2 * np.linspace(0, 10, 50)) + 0.3
    ])),
    'group': np.repeat(['A', 'B', 'C'], 50)
})

ggplot(df, aes(x='x', y='y', fill='group')) + geom_area(alpha=0.6)

# %% [markdown]
# ## 2.10 geom_ribbon - Confidence Bands

# %%
x = np.linspace(0, 10, 50)
y = np.sin(x)
df = pd.DataFrame({
    'x': x,
    'ymin': y - 0.3,
    'ymax': y + 0.3
})

ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(fill='steelblue', alpha=0.3)

# %% [markdown]
# ## 2.11 geom_step - Step Plots

# %%
x = np.linspace(0, 10, 20)
df = pd.DataFrame({'x': x, 'y': np.sin(x)})

ggplot(df, aes(x='x', y='y')) + geom_step(color='blue', size=2)

# %% [markdown]
# ## 2.12 geom_segment - Line Segments

# %%
df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [1, 2, 1],
    'xend': [2, 3, 4],
    'yend': [3, 1, 2]
})

ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment(color='red', size=2)

# %% [markdown]
# ## 2.13 geom_errorbar - Error Bars

# %%
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [10, 15, 12, 18],
    'ymin': [8, 13, 10, 15],
    'ymax': [12, 17, 14, 21]
})

(ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax'))
 + geom_col(fill='steelblue', alpha=0.7)
 + geom_errorbar(width=0.2))

# %% [markdown]
# ## 2.14 geom_tile / geom_raster - Heatmaps

# %%
# Create grid data
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)
Z = np.sin(X / 2) * np.cos(Y / 2)

df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + scale_fill_viridis_c()

# %% [markdown]
# ## 2.15 geom_text - Text Labels

# %%
df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [2, 4, 3, 5],
    'label': ['Point A', 'Point B', 'Point C', 'Point D']
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10, color='steelblue')
 + geom_text(aes(label='label'), vjust=-1))

# %% [markdown]
# ## 2.16 geom_density - Density Plots

# %%
df = pd.DataFrame({'x': np.random.randn(500)})
ggplot(df, aes(x='x')) + geom_density(fill='lightblue', alpha=0.5)

# %% [markdown]
# ## 2.17 geom_hline / geom_vline - Reference Lines

# %%
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + geom_hline(data=0, color='red', linetype='dash')
 + geom_vline(data=0, color='blue', linetype='dash'))

# %% [markdown]
# ## 2.18 geom_abline - Slope/Intercept Lines

# %%
df = pd.DataFrame({'x': range(10), 'y': [i * 2 + 1 for i in range(10)]})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=8)
 + geom_abline(slope=2, intercept=1, color='red', linetype='dash')
 + geom_abline(slope=1.5, intercept=3, color='blue'))

# %% [markdown]
# ## 2.19 geom_jitter - Jittered Points (Avoid Overplotting)

# %%
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 50),
    'value': np.random.randn(150)
})

# Without jitter - points overlap
(ggplot(df, aes(x='category', y='value'))
 + geom_point(alpha=0.5)
 + labs(title='Without Jitter'))

# %%
# With jitter - points spread out
(ggplot(df, aes(x='category', y='value'))
 + geom_jitter(width=0.2, alpha=0.5)
 + labs(title='With Jitter'))

# %%
# Using position_jitter with geom_point
(ggplot(df, aes(x='category', y='value'))
 + geom_point(position=position_jitter(width=0.3, height=0), alpha=0.5)
 + labs(title='geom_point with position_jitter'))

# %% [markdown]
# ## 2.20 geom_rug - Marginal Rug Plots

# %%
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_rug(sides='bl', alpha=0.3)  # bottom and left
 + labs(title='Scatter with Marginal Rugs'))

# %% [markdown]
# ## 2.21 geom_contour - Contour Lines

# %%
# Create 2D density data
x = np.linspace(-3, 3, 50)
y = np.linspace(-3, 3, 50)
X, Y = np.meshgrid(x, y)
Z = np.exp(-(X**2 + Y**2))

df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

ggplot(df, aes(x='x', y='y', z='z')) + geom_contour()

# %% [markdown]
# ## 2.22 geom_contour_filled - Filled Contours

# %%
(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_contour_filled()
 + labs(title='Filled Contour Plot'))

# =============================================================================
# PART 3: SCALES
# =============================================================================

# %% [markdown]
# ## 3.1 Axis Limits with xlim / ylim

# %%
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + xlim(-2, 2)
 + ylim(-2, 2))

# %%
# Using lims() for both axes
(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + lims(x=(-3, 3), y=(-3, 3)))

# %% [markdown]
# ## 3.2 scale_x_continuous / scale_y_continuous

# %%
df = pd.DataFrame({'x': range(1, 11), 'y': [i**2 for i in range(1, 11)]})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=8)
 + geom_line()
 + scale_x_continuous(name='X Axis', breaks=[2, 4, 6, 8, 10])
 + scale_y_continuous(name='Y Axis (squared)', limits=(0, 120)))

# %% [markdown]
# ## 3.3 Log Scales

# %%
df = pd.DataFrame({
    'x': np.linspace(1, 100, 50),
    'y': np.exp(np.linspace(0, 5, 50))
})

(ggplot(df, aes(x='x', y='y'))
 + geom_line()
 + scale_y_log10()
 + labs(title='Log Scale Y-Axis'))

# %% [markdown]
# ## 3.4 scale_color_manual - Custom Colors

# %%
df = pd.DataFrame({
    'x': np.random.randn(150),
    'y': np.random.randn(150),
    'group': np.repeat(['A', 'B', 'C'], 50)
})

(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point(size=8)
 + scale_color_manual(values=['#E41A1C', '#377EB8', '#4DAF4A']))

# %% [markdown]
# ## 3.5 scale_color_brewer - ColorBrewer Palettes

# %%
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point(size=8)
 + scale_color_brewer(palette='Set2'))

# %% [markdown]
# ## 3.6 scale_fill_gradient - Continuous Color Gradients

# %%
df = pd.DataFrame({
    'x': np.tile(np.arange(10), 10),
    'y': np.repeat(np.arange(10), 10),
    'z': np.random.randn(100)
})

(ggplot(df, aes(x='x', y='y', fill='z'))
 + geom_tile()
 + scale_fill_gradient(low='blue', high='red'))

# %% [markdown]
# ## 3.7 scale_size - Size Scaling

# %%
df = pd.DataFrame({
    'x': np.random.rand(50),
    'y': np.random.rand(50),
    'size_var': np.random.rand(50) * 100
})

(ggplot(df, aes(x='x', y='y', size='size_var'))
 + geom_point(color='steelblue', alpha=0.6)
 + scale_size(range=(2, 20)))

# %% [markdown]
# ## 3.8 scale_fill_manual - Custom Fill Colors

# %%
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [25, 40, 30, 55]
})

(ggplot(df, aes(x='category', y='value', fill='category'))
 + geom_col()
 + scale_fill_manual(values=['#E41A1C', '#377EB8', '#4DAF4A', '#984EA3']))

# %% [markdown]
# ## 3.9 scale_shape_manual - Custom Shapes

# %%
df = pd.DataFrame({
    'x': np.random.randn(60),
    'y': np.random.randn(60),
    'group': np.repeat(['A', 'B', 'C'], 20)
})

(ggplot(df, aes(x='x', y='y', shape='group'))
 + geom_point(size=10)
 + scale_shape_manual(values=['circle', 'square', 'diamond']))

# %% [markdown]
# ## 3.10 scale_color_gradient - Continuous Color Gradient

# %%
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'z': np.random.rand(100)
})

(ggplot(df, aes(x='x', y='y', color='z'))
 + geom_point(size=8)
 + scale_color_gradient(low='yellow', high='red'))

# %% [markdown]
# ## 3.11 scale_x_rangeslider - Interactive Range Slider

# %%
dates = pd.date_range('2020-01-01', periods=365, freq='D')
df = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.randn(365))
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line()
 + scale_x_rangeslider()
 + labs(title='Drag the slider below to zoom'))

# %% [markdown]
# ## 3.12 scale_x_rangeselector - Date Range Buttons

# %%
(ggplot(df, aes(x='date', y='value'))
 + geom_line()
 + scale_x_rangeselector(buttons=['1m', '3m', '6m', 'ytd', '1y', 'all'])
 + labs(title='Click buttons to select date range'))

# =============================================================================
# PART 4: THEMES
# =============================================================================

# %% [markdown]
# ## 4.1 Built-in Themes

# %%
df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
base = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10)

# Default theme
base

# %%
# Minimal theme
base + theme_minimal() + labs(title='theme_minimal')

# %%
# Classic theme
base + theme_classic() + labs(title='theme_classic')

# %%
# Dark theme
base + theme_dark() + labs(title='theme_dark')

# %%
# ggplot2 theme
base + theme_ggplot2() + labs(title='theme_ggplot2')

# %%
# BBC style theme
base + theme_bbc() + labs(title='theme_bbc')

# %%
# NY Times style theme
base + theme_nytimes() + labs(title='theme_nytimes')

# %% [markdown]
# ## 4.2 theme() - Custom Theme Elements

# %%
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + theme(
     plot_background=element_rect(fill='#f0f0f0'),
     panel_background=element_rect(fill='white'),
     axis_text=element_text(size=12, color='darkblue'),
     axis_title=element_text(size=14, color='darkblue')
 )
 + labs(title='Custom Theme'))

# %%
# Using element_line to customize lines
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + theme(
     panel_grid_major=element_line(color='lightgray', width=1, dash='dash'),
     axis_line=element_line(color='black', width=2)
 )
 + labs(title='Custom Grid with element_line'))

# %% [markdown]
# ## 4.3 Hiding Legends

# %%
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B'], 100)
})

# Hide legend with theme
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point()
 + theme(legend_position='none'))

# %%
# Hide specific guide
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point()
 + guides(color='none'))

# %% [markdown]
# ## 4.4 guide_legend / guide_colorbar - Legend Customization

# %%
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})

# Customize legend title and position
(ggplot(df, aes(x='x', y='y', color='category'))
 + geom_point(size=8)
 + guides(color=guide_legend(title='Category Type', nrow=1))
 + theme(legend_position='top'))

# %%
# Continuous scale with colorbar
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'z': np.random.rand(100) * 100
})

(ggplot(df, aes(x='x', y='y', color='z'))
 + geom_point(size=8)
 + scale_color_gradient(low='blue', high='red')
 + guides(color=guide_colorbar(title='Value', barwidth=20)))

# =============================================================================
# PART 5: FACETS
# =============================================================================

# %% [markdown]
# ## 5.1 facet_wrap - Single Variable Faceting

# %%
df = pd.DataFrame({
    'x': np.random.randn(300),
    'y': np.random.randn(300),
    'category': np.random.choice(['A', 'B', 'C'], 300)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category'))

# %%
# Control number of columns
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', ncol=1))

# %% [markdown]
# ## 5.2 facet_grid - Two Variable Faceting

# %%
df = pd.DataFrame({
    'x': np.random.randn(400),
    'y': np.random.randn(400),
    'row_var': np.tile(np.repeat(['R1', 'R2'], 100), 2),
    'col_var': np.repeat(['C1', 'C2'], 200)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_grid(rows='row_var', cols='col_var'))

# %% [markdown]
# ## 5.3 Facet with Free Scales

# %%
# Different data ranges per facet
df = pd.DataFrame({
    'x': np.concatenate([
        np.random.uniform(0, 10, 50),
        np.random.uniform(0, 100, 50)
    ]),
    'y': np.concatenate([
        np.random.uniform(0, 5, 50),
        np.random.uniform(0, 50, 50)
    ]),
    'group': ['A'] * 50 + ['B'] * 50
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + facet_wrap('group', scales='free'))

# %% [markdown]
# ## 5.4 Facet Labellers

# %%
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'category': np.tile(['Group A', 'Group B'], 100)
})

# label_both shows variable name and value
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', labeller=label_both)
 + labs(title='Using label_both labeller'))

# %%
# label_value shows just the value (default)
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + facet_wrap('category', labeller=label_value)
 + labs(title='Using label_value labeller'))

# =============================================================================
# PART 6: LABELS & ANNOTATIONS
# =============================================================================

# %% [markdown]
# ## 6.1 labs() - Plot Labels

# %%
df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})

(ggplot(df, aes(x='x', y='y'))
 + geom_line()
 + geom_point(size=10)
 + labs(
     title='Main Title',
     subtitle='This is a subtitle',
     x='X-Axis Label',
     y='Y-Axis Label',
     caption='Data source: Example'
 ))

# %% [markdown]
# ## 6.2 ggtitle() - Quick Title

# %%
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + ggtitle('Quick Title'))

# %% [markdown]
# ## 6.3 annotate() - Add Annotations

# %%
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.randn(50),
    'y': np.random.randn(50)
})
df.loc[50] = [3, 3]  # Add outlier

(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=6, alpha=0.6)
 + annotate('text', x=3, y=3.5, label='Outlier!', size=14, color='red')
 + annotate('rect', xmin=-1, xmax=1, ymin=-1, ymax=1, fill='lightblue', alpha=0.3)
 + annotate('text', x=0, y=0, label='Main cluster', size=12, color='blue'))

# %%
# Arrow annotation
df = pd.DataFrame({
    'x': range(10),
    'y': [1, 3, 2, 5, 8, 6, 4, 3, 2, 1]
})

(ggplot(df, aes(x='x', y='y'))
 + geom_line(size=2, color='steelblue')
 + geom_point(size=8)
 + annotate('segment', x=6, y=9, xend=4, yend=8.2, arrow=True, color='red', size=2)
 + annotate('text', x=6, y=9.5, label='Peak value', size=12, color='red'))

# =============================================================================
# PART 7: STATISTICS
# =============================================================================

# %% [markdown]
# ## 7.1 geom_smooth - Smoothed Regression Lines

# %%
np.random.seed(42)
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(0, 0.3, 100)
})

# LOESS smoothing (default)
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', color='blue'))

# %%
# Linear regression
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='lm', color='red'))

# %%
# Smoothing with confidence interval (se=True)
(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', se=True, color='green')
 + labs(title='LOESS with Confidence Interval'))

# %% [markdown]
# ## 7.2 stat_ecdf - Empirical CDF

# %%
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_step(stat='ecdf') + labs(title='Empirical CDF')

# %% [markdown]
# ## 7.3 stat_summary - Summary Statistics

# %%
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 30),
    'value': np.random.randn(90) + np.tile([0, 2, 1], 30)
})

(ggplot(df, aes(x='category', y='value'))
 + geom_point(alpha=0.3)
 + stat_summary(fun='mean', geom='point', color='red', size=15))

# =============================================================================
# PART 8: COORDINATES
# =============================================================================

# %% [markdown]
# ## 8.1 coord_cartesian - Zoom Without Clipping

# %%
df = pd.DataFrame({'x': range(1, 11), 'y': [i**2 for i in range(1, 11)]})

(ggplot(df, aes(x='x', y='y'))
 + geom_point()
 + geom_line()
 + coord_cartesian(xlim=(3, 8), ylim=(10, 60)))

# %% [markdown]
# ## 8.2 coord_flip - Swap X and Y

# %%
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D', 'E'],
    'value': [25, 40, 30, 55, 20]
})

(ggplot(df, aes(x='category', y='value'))
 + geom_col(fill='steelblue')
 + coord_flip())

# %% [markdown]
# ## 8.3 coord_polar - Polar Coordinates (Pie/Radar Charts)

# %%
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [30, 25, 20, 25]
})

(ggplot(df, aes(x='category', y='value', fill='category'))
 + geom_col()
 + coord_polar())

# =============================================================================
# PART 9: MAPS & GEOGRAPHIC
# =============================================================================

# %% [markdown]
# ## 9.1 geom_map - Basic US Choropleth

# %%
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0]
})

states = map_data('state')

(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues')
 + labs(title='US States by Population'))

# %% [markdown]
# ## 9.2 Layering Map with Points

# %%
cities = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    'pop': [8.3, 3.9, 2.7, 2.3, 1.6]
})

(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues')
 + geom_point(cities, aes(x='lon', y='lat', size='pop'), color='red'))

# %% [markdown]
# ## 9.3 World Map

# %%
country_data = pd.DataFrame({
    'country': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'IND', 'FRA', 'BRA'],
    'gdp': [25.5, 18.3, 4.2, 4.1, 3.1, 3.4, 2.8, 1.9]
})

countries = map_data('world')

(ggplot(country_data, aes(map_id='country', fill='gdp'))
 + geom_map(map=countries, map_type='world', palette='Viridis')
 + labs(title='GDP by Country'))

# %% [markdown]
# ## 9.4 coord_sf - Map Projections

# %%
cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Sydney'],
    'lon': [-74.006, -0.128, 139.692, 151.209],
    'lat': [40.713, 51.507, 35.690, -33.868]
})

# Robinson projection
(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='red', size=10)
 + coord_sf(crs='robinson')
 + labs(title='Robinson Projection'))

# %%
# Orthographic (globe) projection
(ggplot(cities, aes(x='lon', y='lat'))
 + geom_map(map_type='world')
 + geom_point(color='yellow', size=8)
 + coord_sf(crs='orthographic')
 + theme_dark()
 + labs(title='Orthographic Projection'))

# =============================================================================
# PART 10: 3D PLOTS
# =============================================================================

# %% [markdown]
# ## 10.1 geom_point_3d - 3D Scatter

# %%
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'z': np.random.randn(200),
    'group': np.random.choice(['A', 'B', 'C'], 200)
})

ggplot(df, aes(x='x', y='y', z='z')) + geom_point_3d()

# %%
# 3D scatter with color grouping
ggplot(df, aes(x='x', y='y', z='z', color='group')) + geom_point_3d(size=6)

# %% [markdown]
# ## 10.2 geom_surface - 3D Surface Plots

# %%
# Create surface data
def make_surface(func, x_range=(-5, 5), y_range=(-5, 5), resolution=50):
    x = np.linspace(x_range[0], x_range[1], resolution)
    y = np.linspace(y_range[0], y_range[1], resolution)
    X, Y = np.meshgrid(x, y)
    Z = func(X, Y)
    return pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})

# Paraboloid
df = make_surface(lambda x, y: x**2 + y**2)
ggplot(df, aes(x='x', y='y', z='z')) + geom_surface(colorscale='Viridis')

# %%
# Saddle surface
df = make_surface(lambda x, y: x**2 - y**2)
(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_surface(colorscale='RdBu')
 + labs(title='Saddle Surface'))

# %%
# Sinc function
def sinc_2d(x, y):
    r = np.sqrt(x**2 + y**2)
    return np.where(r == 0, 1, np.sin(r) / r)

df = make_surface(sinc_2d, x_range=(-10, 10), y_range=(-10, 10), resolution=80)
(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_surface(colorscale='Plasma')
 + labs(title='2D Sinc Function'))

# %% [markdown]
# ## 10.3 geom_wireframe - Wireframe Plots

# %%
df = make_surface(lambda x, y: np.sin(x) * np.cos(y), resolution=30)
(ggplot(df, aes(x='x', y='y', z='z'))
 + geom_wireframe(color='steelblue', linewidth=1)
 + labs(title='Wireframe Plot'))

# =============================================================================
# PART 11: FINANCIAL CHARTS
# =============================================================================

# %% [markdown]
# ## 11.1 geom_candlestick - Candlestick Charts

# %%
from datetime import datetime, timedelta

# Generate OHLC data
np.random.seed(42)
n = 60
dates = pd.date_range('2024-01-01', periods=n, freq='B')
returns = np.random.normal(0.0005, 0.02, n)
close = 100 * np.cumprod(1 + returns)
open_prices = np.roll(close, 1)
open_prices[0] = 100
high = np.maximum(open_prices, close) + np.abs(np.random.randn(n)) * close * 0.01
low = np.minimum(open_prices, close) - np.abs(np.random.randn(n)) * close * 0.01

df = pd.DataFrame({
    'date': dates,
    'open': open_prices,
    'high': high,
    'low': low,
    'close': close
})

(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_candlestick()
 + labs(title='Stock Price', y='Price ($)'))

# %%
# Custom colors
(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_candlestick(increasing_color='#089981', decreasing_color='#F23645')
 + theme_dark()
 + labs(title='TradingView Style'))

# %% [markdown]
# ## 11.2 geom_ohlc - OHLC Bar Charts

# %%
(ggplot(df, aes(x='date', open='open', high='high', low='low', close='close'))
 + geom_ohlc()
 + labs(title='OHLC Bar Chart'))

# =============================================================================
# PART 12: TIME SERIES
# =============================================================================

# %% [markdown]
# ## 12.1 scale_x_date - Date Axis Formatting

# %%
dates = pd.date_range('2020-01-01', periods=24, freq='ME')
df = pd.DataFrame({
    'date': dates,
    'value': np.cumsum(np.random.randn(24)) + 50
})

(ggplot(df, aes(x='date', y='value'))
 + geom_line(color='steelblue', size=2)
 + geom_point(size=5)
 + scale_x_date(date_breaks='3 months', date_labels='%b %Y')
 + labs(title='Monthly Time Series'))

# %%
# scale_x_datetime for timestamp data with time component
timestamps = pd.date_range('2024-01-01 08:00', periods=48, freq='h')
df_hourly = pd.DataFrame({
    'timestamp': timestamps,
    'value': np.sin(np.linspace(0, 4*np.pi, 48)) + np.random.randn(48) * 0.2
})

(ggplot(df_hourly, aes(x='timestamp', y='value'))
 + geom_line()
 + scale_x_datetime(date_labels='%b %d %H:%M')
 + labs(title='Hourly Data with scale_x_datetime'))

# %% [markdown]
# ## 12.2 geom_range - 5-Year Historical Range Plots

# %%
# Generate multi-year daily data
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
temps = []
for d in dates:
    seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
    trend = (d.year - 2019) * 0.5
    noise = np.random.randn() * 15
    temps.append(seasonal + trend + noise)

df_temp = pd.DataFrame({'date': dates, 'temperature': temps})

# 5-year range plot with monthly aggregation
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='ME')
 + labs(title='Temperature: 5-Year Historical Range',
        subtitle='Gray: 5yr min/max, Black: 5yr avg, Blue: prior year, Red: current year'))

# %%
# Weekly aggregation
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='W-Fri')
 + labs(title='Weekly Temperature Range'))

# %%
# Show specific historical years
(ggplot(df_temp, aes(x='date', y='temperature'))
 + geom_range(freq='ME', show_years=[2020, 2021])
 + labs(title='Temperature with 2020 and 2021 highlighted'))

# %%
# geom_range with facets
np.random.seed(789)
cities = ['New York', 'Los Angeles', 'Chicago']
city_data = []
for city in cities:
    base_temp = {'New York': 50, 'Los Angeles': 65, 'Chicago': 45}[city]
    amplitude = {'New York': 30, 'Los Angeles': 15, 'Chicago': 35}[city]
    for d in dates:
        seasonal = base_temp + amplitude * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
        noise = np.random.randn() * 15
        city_data.append({'date': d, 'temperature': seasonal + noise, 'city': city})

df_cities = pd.DataFrame(city_data)

(ggplot(df_cities, aes(x='date', y='temperature'))
 + geom_range(freq='ME')
 + facet_wrap('city', nrow=1)
 + labs(title='Temperature by City')
 + theme_minimal())

# =============================================================================
# PART 13: NETWORK GRAPHS
# =============================================================================

# %% [markdown]
# ## 13.1 geom_edgebundle - Force-Directed Edge Bundling

# %%
# Circular layout network
n_nodes = 20
angles = np.linspace(0, 2 * np.pi, n_nodes, endpoint=False)
radius = 10
node_x = radius * np.cos(angles)
node_y = radius * np.sin(angles)

# Create edges across the circle
edges = []
for i in range(n_nodes):
    for offset in [5, 7, 10]:
        j = (i + offset) % n_nodes
        edges.append({'x': node_x[i], 'y': node_y[i], 'xend': node_x[j], 'yend': node_y[j]})

edges_df = pd.DataFrame(edges)
nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})

(ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_edgebundle(compatibility_threshold=0.6)
 + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='white', size=4)
 + theme_dark()
 + labs(title='Circular Network with Edge Bundling'))

# %% [markdown]
# ## 13.2 Random Network Edge Bundling

# %%
np.random.seed(42)
n_nodes = 30
n_edges = 80
node_x = np.random.uniform(0, 100, n_nodes)
node_y = np.random.uniform(0, 100, n_nodes)

edges = []
for _ in range(n_edges):
    i, j = np.random.choice(n_nodes, 2, replace=False)
    edges.append({'x': node_x[i], 'y': node_y[i], 'xend': node_x[j], 'yend': node_y[j]})

edges_df = pd.DataFrame(edges)
nodes_df = pd.DataFrame({'x': node_x, 'y': node_y})

(ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_edgebundle(C=5, compatibility_threshold=0.5)
 + geom_point(data=nodes_df, mapping=aes(x='x', y='y'), color='#00ff00', size=5)
 + theme_dark()
 + labs(title='Random Network with Edge Bundling'))

# %% [markdown]
# ## 13.3 geom_searoute - Realistic Maritime Shipping Routes
#
# Uses the `searoute` package to calculate actual shipping lanes that avoid land.
# Requires: `pip install searoute`

# %%
# Define shipping routes between major ports
shipping_routes = pd.DataFrame({
    'origin': ['Rotterdam', 'Shanghai', 'Los Angeles'],
    'x': [4.48, 121.47, -118.24],       # origin longitude
    'y': [51.92, 31.23, 33.73],         # origin latitude
    'xend': [121.47, -74.01, 4.48],     # destination longitude
    'yend': [31.23, 40.71, 51.92]       # destination latitude
})

# Basic sea route (requires searoute package)
# Uncomment to run (requires: pip install searoute)
(ggplot(shipping_routes, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_map(map_type='world')
 + geom_searoute(color='steelblue', linewidth=1.0)
 + theme_dark()
 + labs(title='Maritime Shipping Routes'))

# %%
# Sea routes with restrictions (avoid Suez Canal - routes go around Africa)
(ggplot(shipping_routes, aes(x='x', y='y', xend='xend', yend='yend'))
 + geom_map(map_type='world')
 + geom_searoute(
     restrictions=['suez'],  # Force routes around Cape of Good Hope
     color='#ff6b35',
     show_highlight=True,
     show_ports=True,
     port_color='#00ff88',
     verbose=True  # Shows route distances
 )
 + theme_dark()
 + labs(title='Shipping Routes Avoiding Suez Canal'))

# %% [markdown]
# ## 13.4 Edge Bundling on Maps

# %%
airports = pd.DataFrame({
    'lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4],
    'lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6],
    'name': ['SFO', 'JFK', 'ORD', 'LAX', 'IAH', 'ATL']
})

flights = pd.DataFrame({
    'src_lon': [-122.4, -73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -73.8],
    'src_lat': [37.8, 40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 40.6],
    'dst_lon': [-73.8, -87.6, -118.4, -95.3, -84.4, -122.4, -84.4, -118.4],
    'dst_lat': [40.6, 41.9, 34.0, 29.8, 33.6, 37.8, 33.6, 34.0]
})

(ggplot(flights, aes(x='src_lon', y='src_lat', xend='dst_lon', yend='dst_lat'))
 + geom_map(map_type='usa')
 + geom_point(data=airports, mapping=aes(x='lon', y='lat'), color='white', size=8)
 + geom_edgebundle(C=4, compatibility_threshold=0.5, verbose=False)
 + theme_dark()
 + labs(title='US Flights with Edge Bundling'))

# =============================================================================
# PART 14: ADVANCED EXAMPLES
# =============================================================================

# %% [markdown]
# ## 14.1 Multi-Layer Complex Plot

# %%
np.random.seed(0)
df = pd.DataFrame({
    'x': np.arange(1, 21),
    'y': np.random.normal(size=20).cumsum(),
    'error': np.random.rand(20),
    'category': np.random.choice(['A', 'B'], 20),
    'label': [f'P{i}' for i in range(1, 21)]
})

(ggplot(df, aes(x='x', y='y', color='category'))
 + geom_line()
 + geom_point(size=5)
 + geom_errorbar(aes(yerr='error'), width=0.2)
 + geom_text(aes(label='label'), vjust=-1)
 + scale_color_brewer(type='qual', palette='Set1')
 + labs(title='Multi-Layer Plot', x='X-axis', y='Y-axis', caption='With error bars and labels')
 + coord_cartesian(xlim=(0, 25), ylim=(-5, 10))
 + theme_minimal())

# %% [markdown]
# ## 14.2 Faceted with Multiple Geoms

# %%
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'category': np.random.choice(['A', 'B'], 200)
})

(ggplot(df, aes(x='x', y='y'))
 + geom_point(alpha=0.5)
 + geom_smooth(method='loess', color='red')
 + geom_density(aes(x='x'), color='blue')
 + facet_wrap('category')
 + theme_minimal())

# %% [markdown]
# ## 14.3 BBC Style Publication Chart

# %%
gapminder = pd.DataFrame({
    'year': [1952, 1962, 1972, 1982, 1992, 2002, 2007] * 2,
    'lifeExp': [36.3, 40.0, 43.5, 48.1, 52.0, 52.7, 54.1,
                68.4, 70.0, 71.0, 74.0, 77.0, 78.8, 78.2],
    'country': ['Malawi'] * 7 + ['United States'] * 7
})

(ggplot(gapminder, aes(x='year', y='lifeExp', color='country'))
 + geom_line(size=3)
 + scale_x_continuous(format='d')
 + theme_bbc()
 + labs(title='Life Expectancy Over Time',
        subtitle='Malawi vs United States'))

# %% [markdown]
# ## 14.4 Complex Heatmap with Gradient

# %%
x = np.arange(0, 10, 1)
y = np.arange(0, 10, 1)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

(ggplot(df, aes(x='x', y='y', fill='z'))
 + geom_tile()
 + scale_fill_gradient(low='blue', high='red', name='Intensity')
 + theme_minimal()
 + labs(title='Heatmap with Custom Gradient'))

# %% [markdown]
# ## 14.5 Saving Plots

# %%
# Save to HTML (interactive)
p = (ggplot(df, aes(x='x', y='y', fill='z'))
     + geom_tile()
     + scale_fill_viridis_c())

# p.save('my_plot.html')  # Uncomment to save

# %%
# Save with custom size
# p + ggsize(1200, 800) + ggsave('my_plot_large.html')  # Uncomment to save

# %% [markdown]
# ## 14.6 Figure Size Control

# %%
df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})

(ggplot(df, aes(x='x', y='y'))
 + geom_line()
 + geom_point(size=10)
 + ggsize(width=1000, height=400)
 + labs(title='Wide Plot'))

# %% [markdown]
# # Summary
#
# This notebook covered all major ggplotly features:
#
# **Geoms (22+):**
# - Basic: point, line, path, bar, col, histogram, boxplot, violin
# - Areas: area, ribbon, tile, density, contour, contour_filled
# - Annotations: text, segment, errorbar, step, hline, vline, abline
# - Special: jitter, rug, smooth, range
# - Financial: candlestick, ohlc
# - 3D: point_3d, surface, wireframe
# - Maps: map, sf
# - Networks: edgebundle, searoute (realistic shipping lanes)
#
# **Scales (15+):**
# - Axis: x/y_continuous, x/y_log10, x_date, x_datetime
# - Interactive: x_rangeslider, x_rangeselector
# - Color: color_manual, color_gradient, color_brewer
# - Fill: fill_manual, fill_gradient, fill_brewer, fill_viridis_c
# - Other: size, shape_manual
#
# **Themes (7+):**
# - Built-in: minimal, classic, dark, ggplot2, bbc, nytimes
# - Customization: theme(), element_text, element_rect, element_line
#
# **Facets:**
# - facet_wrap, facet_grid
# - scales='free', labeller (label_both, label_value)
#
# **Coordinates:**
# - coord_cartesian, coord_flip, coord_polar, coord_sf (map projections)
#
# **Guides:**
# - guides(), guide_legend, guide_colorbar
# - legend_position='none' to hide
#
# **Statistics:**
# - geom_smooth (lm, loess, se=True)
# - stat_ecdf, stat_summary, stat_count, stat_bin, stat_density
#
# **Positions:**
# - position_dodge, position_stack, position_jitter
#
# **Built-in Datasets:**
# - mpg, diamonds, iris, mtcars, economics, midwest
# - txhousing, faithfuld, msleep, presidential, seals
# - commodity_prices, economics_long, luv_colours
# - us_flights (igraph network)
#
# **Extras:**
# - labs, ggtitle, annotate (text, rect, segment with arrow)
# - ggsize, ggsave, xlim, ylim, lims
# - Pandas index auto-handling (x='index' or automatic)
# - data() to list/load datasets, map_data() for geographic data
#
# For more details, see the documentation at https://ggplotly.readthedocs.io

# %%
