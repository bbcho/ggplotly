# %%[markdown]
# coding: utf-8

# # ggplotly Master Examples Notebook
# 
# A comprehensive guide to ggplotly - Python's grammar of graphics using Plotly.
# 
# ## Table of Contents
# 
# 1. **Getting Started** - Setup and basic concepts
# 2. **Built-in Datasets** - Using ggplotly's included datasets
# 3. **Basic Geoms** - Point, line, bar, area, step, ribbon
# 4. **Statistical Geoms** - Histogram, density, boxplot, violin
# 5. **Annotations & Reference Lines** - Text, vline, hline, abline, segment
# 6. **Aesthetics Deep Dive** - Color, size, shape, alpha, fill mappings
# 7. **Scales** - Axis transformations and color scales
# 8. **Faceting** - Small multiples with facet_wrap and facet_grid
# 9. **Coordinates** - coord_flip, coord_cartesian, coord_polar
# 10. **Themes** - Customizing plot appearance
# 11. **Labels & Titles** - Adding text annotations
# 12. **Combining Layers** - Multiple geoms on one plot
# 13. **Statistical Transformations** - geom_smooth, stat_summary
# 14. **Positions** - dodge, stack, jitter
# 15. **Time Series** - geom_range, scale_x_date
# 16. **Financial Charts** - Candlestick and OHLC
# 17. **3D Plots** - geom_point_3d, geom_surface, geom_wireframe
# 18. **Maps** - Choropleth maps with geom_map
# 19. **Network Visualization** - Edge bundling
# 20. **Contours & Heatmaps** - geom_tile, geom_contour, geom_contour_filled
# 21. **Segments & Paths** - geom_segment, geom_path
# 22. **Error Visualization** - geom_errorbar, geom_ribbon
# 23. **Advanced Examples** - Complex multi-layer compositions

# ---
# # 1. Getting Started
# 
# First, let's import ggplotly and set up our environment.

# %%


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

import numpy as np
import pandas as pd
from ggplotly import *

np.random.seed(42)
print("ggplotly loaded successfully!")
print(f"Available datasets: {data()}")


# ## The Grammar of Graphics
# 
# ggplotly uses a layered approach:
# - **Data**: A pandas DataFrame
# - **Aesthetics** (`aes`): Map data columns to visual properties (x, y, color, size, etc.)
# - **Geoms**: Geometric objects that represent data (points, lines, bars, etc.)
# - **Scales**: Control how data values map to visual values
# - **Facets**: Create small multiples by splitting data
# - **Themes**: Customize non-data elements (fonts, colors, grid)
# 
# Plots are built by adding layers with the `+` operator.

# %%


# Your first ggplotly plot!
df = pd.DataFrame({'x': [1, 2, 3, 4, 5], 'y': [2, 4, 3, 5, 4]})

ggplot(df, aes(x='x', y='y')) + geom_point()


# %%


# Add more layers
ggplot(df, aes(x='x', y='y')) + geom_point(size=10) + geom_line(color='blue')


# ---
# # 2. Built-in Datasets
# 
# ggplotly includes several classic datasets for learning and testing.

# %%


# List all available datasets
print("Available datasets:", data())


# %%


# Load the iris dataset
iris = data('iris')
print(f"Iris dataset: {iris.shape[0]} rows, {iris.shape[1]} columns")
iris.head()


# %%


# Classic iris scatter plot
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    labs(title='Iris Dataset: Sepal Dimensions', x='Sepal Length (cm)', y='Sepal Width (cm)')
)


# %%


# Iris petal dimensions
(
    ggplot(iris, aes(x='petal_length', y='petal_width', color='species')) +
    geom_point(size=8, alpha=0.7) +
    labs(title='Iris: Petal Dimensions', x='Petal Length (cm)', y='Petal Width (cm)')
)


# %%


# Load the mpg dataset
mpg = data('mpg')
print(f"MPG dataset: {mpg.shape[0]} rows, {mpg.shape[1]} columns")
mpg.head()


# %%


# MPG: Engine displacement vs highway mpg
(
    ggplot(mpg, aes(x='displ', y='hwy', color='class')) +
    geom_point(size=8, alpha=0.7) +
    labs(title='Fuel Economy by Engine Size', x='Displacement (L)', y='Highway MPG')
)


# %%


# MPG: City vs Highway
(
    ggplot(mpg, aes(x='cty', y='hwy', color='drv')) +
    geom_point(size=6, alpha=0.6) +
    geom_abline(slope=1, intercept=0, linetype='dash', color='gray') +
    labs(title='City vs Highway MPG', x='City MPG', y='Highway MPG')
)


# %%


# Load the diamonds dataset
diamonds = data('diamonds')
print(f"Diamonds dataset: {diamonds.shape[0]} rows, {diamonds.shape[1]} columns")
diamonds.head()


# %%


# Sample diamonds for faster plotting
diamonds_sample = diamonds.sample(1000, random_state=42)

(
    ggplot(diamonds_sample, aes(x='carat', y='price', color='cut')) +
    geom_point(alpha=0.5, size=5) +
    labs(title='Diamond Price vs Carat')
)


# %%


# Diamonds: Price by clarity
(
    ggplot(diamonds_sample, aes(x='clarity', y='price', fill='clarity')) +
    geom_boxplot(alpha=0.7) +
    labs(title='Diamond Price by Clarity')
)


# %%


# Load mtcars dataset
mtcars = data('mtcars')
print(f"mtcars dataset: {mtcars.shape[0]} rows")
mtcars.head()


# %%


# mtcars: MPG vs Weight by cylinders
mtcars['cyl'] = mtcars['cyl'].astype(str)  # Convert to categorical
(
    ggplot(mtcars, aes(x='wt', y='mpg', color='cyl', size='hp')) +
    geom_point(alpha=0.7) +
    labs(title='MPG vs Weight', x='Weight (1000 lbs)', y='Miles per Gallon')
)


# %%


# mtcars: HP vs Quarter Mile Time
(
    ggplot(mtcars, aes(x='hp', y='qsec', color='cyl')) +
    geom_point(size=10, alpha=0.7) +
    geom_smooth(method='lm') +
    labs(title='Horsepower vs Quarter Mile Time', x='Horsepower', y='Quarter Mile (sec)')
)


# %%


# Load economics dataset
economics = data('economics')
economics['date'] = pd.to_datetime(economics['date'])
print(f"Economics dataset: {economics.shape[0]} rows")
economics.head()


# %%


# Economics: Unemployment over time
(
    ggplot(economics, aes(x='date', y='unemploy')) +
    geom_line(color='steelblue', size=1) +
    labs(title='US Unemployment Over Time', x='Date', y='Unemployed (thousands)')
)


# %%


# Economics: Personal savings rate
(
    ggplot(economics, aes(x='date', y='psavert')) +
    geom_area(fill='steelblue', alpha=0.5) +
    geom_line(color='darkblue', size=1) +
    labs(title='Personal Savings Rate Over Time', x='Date', y='Savings Rate (%)')
)


# ---
# # 3. Basic Geoms
# 
# The fundamental building blocks for visualization.

# ## geom_point - Scatter Plots

# %%


# Basic scatter plot
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50)})
ggplot(df, aes(x='x', y='y')) + geom_point() + ggtitle('Basic Scatter Plot')


# %%


# Styled scatter plot with fixed aesthetics
ggplot(df, aes(x='x', y='y')) + geom_point(color='steelblue', size=10, alpha=0.6)


# %%


# Scatter plot with mapped color
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'category': np.random.choice(['A', 'B', 'C'], 100)
})
ggplot(df, aes(x='x', y='y', color='category')) + geom_point(size=8)


# %%


# Scatter plot with continuous color
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'value': np.random.rand(100)
})
(
    ggplot(df, aes(x='x', y='y', color='value')) +
    geom_point(size=10) +
    scale_color_gradient(low='yellow', high='red')
)


# %%


# Scatter with size mapping (bubble chart)
df = pd.DataFrame({
    'x': np.random.rand(30),
    'y': np.random.rand(30),
    'size_val': np.random.rand(30) * 100,
    'category': np.random.choice(['X', 'Y'], 30)
})
(
    ggplot(df, aes(x='x', y='y', size='size_val', color='category')) +
    geom_point(alpha=0.6) +
    ggtitle('Bubble Chart')
)


# %%


# Scatter with shape mapping
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', shape='species')) +
    geom_point(size=10, color='steelblue') +
    ggtitle('Shape Mapping')
)


# %%


# Scatter with color AND shape
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species', shape='species')) +
    geom_point(size=10) +
    ggtitle('Color + Shape Mapping')
)


# ## geom_line - Line Plots

# %%


# Simple line plot
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50))})
ggplot(df, aes(x='x', y='y')) + geom_line() + ggtitle('Sine Wave')


# %%


# Styled line
ggplot(df, aes(x='x', y='y')) + geom_line(color='red', size=2, linetype='dash')


# %%


# Different line types
x = np.linspace(0, 10, 50)
df_lines = pd.DataFrame({
    'x': np.tile(x, 4),
    'y': np.concatenate([np.sin(x), np.sin(x)+0.5, np.sin(x)+1, np.sin(x)+1.5]),
    'type': ['solid']*50 + ['dash']*50 + ['dot']*50 + ['dashdot']*50
})
(
    ggplot(df_lines, aes(x='x', y='y', linetype='type', color='type')) +
    geom_line(size=2) +
    ggtitle('Line Types')
)


# %%


# Line + points
df = pd.DataFrame({'x': np.linspace(0, 10, 20), 'y': np.sin(np.linspace(0, 10, 20))})
ggplot(df, aes(x='x', y='y')) + geom_line(color='blue', size=2) + geom_point(color='red', size=5)


# %%


# Multiple lines with color grouping
x = np.linspace(0, 10, 50)
df = pd.DataFrame({
    'x': np.tile(x, 3),
    'y': np.concatenate([np.sin(x), np.cos(x), np.sin(x) + np.cos(x)]),
    'function': ['sin']*50 + ['cos']*50 + ['sin+cos']*50
})
(
    ggplot(df, aes(x='x', y='y', color='function')) +
    geom_line(size=2) +
    ggtitle('Multiple Trigonometric Functions')
)


# ## geom_bar & geom_col - Bar Charts

# %%


# geom_bar counts occurrences (stat='count')
df = pd.DataFrame({'category': ['A', 'B', 'C', 'A', 'B', 'A', 'C', 'C', 'C', 'B', 'B', 'A']})
ggplot(df, aes(x='category')) + geom_bar() + ggtitle('geom_bar: Counts Categories')


# %%


# geom_bar with fill
ggplot(df, aes(x='category', fill='category')) + geom_bar(alpha=0.8)


# %%


# geom_col uses pre-computed values (stat='identity')
df = pd.DataFrame({'category': ['A', 'B', 'C', 'D', 'E'], 'value': [10, 25, 15, 20, 30]})
ggplot(df, aes(x='category', y='value')) + geom_col(fill='coral') + ggtitle('geom_col: Uses Values')


# %%


# Stacked bars with fill aesthetic
df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'group': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'value': [10, 15, 12, 8, 20, 10]
})
ggplot(df, aes(x='category', y='value', fill='group')) + geom_col() + ggtitle('Stacked Bars')


# %%


# Dodged (side-by-side) bars
ggplot(df, aes(x='category', y='value', fill='group')) + geom_col(position='dodge') + ggtitle('Dodged Bars')


# %%


# Horizontal bar chart (with coord_flip)
df = pd.DataFrame({'item': ['Apple', 'Banana', 'Cherry', 'Date', 'Elderberry'], 'count': [45, 32, 28, 15, 8]})
(
    ggplot(df, aes(x='item', y='count')) +
    geom_col(fill='steelblue') +
    coord_flip() +
    ggtitle('Horizontal Bar Chart')
)


# %%


# Bar chart with custom colors
df = pd.DataFrame({
    'quarter': ['Q1', 'Q2', 'Q3', 'Q4'],
    'revenue': [100, 150, 200, 175]
})
(
    ggplot(df, aes(x='quarter', y='revenue', fill='quarter')) +
    geom_col() +
    scale_fill_manual(values={'Q1': '#3498db', 'Q2': '#2ecc71', 'Q3': '#f39c12', 'Q4': '#e74c3c'}) +
    ggtitle('Quarterly Revenue')
)


# ## geom_area - Area Plots

# %%


# Simple area plot
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50)) + 1.5})
ggplot(df, aes(x='x', y='y')) + geom_area(fill='lightblue', alpha=0.7)


# %%


# Area with line on top
(
    ggplot(df, aes(x='x', y='y')) +
    geom_area(fill='lightblue', alpha=0.5) +
    geom_line(color='darkblue', size=2)
)


# %%


# Stacked area plot
np.random.seed(42)
df = pd.DataFrame({
    'x': np.tile(np.arange(20), 3),
    'y': np.concatenate([
        np.random.rand(20) * 10 + 5,
        np.random.rand(20) * 8 + 3,
        np.random.rand(20) * 6 + 2
    ]),
    'group': ['Product A']*20 + ['Product B']*20 + ['Product C']*20
})
(
    ggplot(df, aes(x='x', y='y', fill='group')) +
    geom_area(alpha=0.7) +
    ggtitle('Stacked Area Chart')
)


# ## geom_step - Step Functions

# %%


# Basic step plot
df = pd.DataFrame({'x': np.arange(10), 'y': np.cumsum(np.random.randn(10))})
ggplot(df, aes(x='x', y='y')) + geom_step(color='purple', size=2)


# %%


# Step plot with points
(
    ggplot(df, aes(x='x', y='y')) +
    geom_step(color='steelblue', size=2) +
    geom_point(color='red', size=8)
)


# %%


# ECDF (Empirical Cumulative Distribution Function)
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_step(stat='ecdf', color='steelblue', size=2) + ggtitle('Empirical CDF')


# ## geom_ribbon - Ribbon/Band Plots

# %%


# Ribbon for confidence bands
x = np.linspace(0, 10, 50)
y = np.sin(x)
df = pd.DataFrame({
    'x': x,
    'y': y,
    'ymin': y - 0.3,
    'ymax': y + 0.3
})
(
    ggplot(df, aes(x='x')) +
    geom_ribbon(aes(ymin='ymin', ymax='ymax'), fill='lightblue', alpha=0.5) +
    geom_line(aes(y='y'), color='darkblue', size=2) +
    ggtitle('Ribbon: Confidence Band')
)


# %%


# Ribbon with varying width
x = np.linspace(0, 10, 50)
y = np.sin(x)
uncertainty = 0.1 + 0.3 * np.abs(np.sin(x * 0.5))  # Varying uncertainty
df = pd.DataFrame({
    'x': x, 'y': y, 
    'ymin': y - uncertainty, 'ymax': y + uncertainty
})
(
    ggplot(df, aes(x='x')) +
    geom_ribbon(aes(ymin='ymin', ymax='ymax'), fill='coral', alpha=0.4) +
    geom_line(aes(y='y'), color='darkred', size=2) +
    ggtitle('Varying Confidence Band')
)


# ---
# # 4. Statistical Geoms
# 
# Geoms that compute statistics from the data.

# ## geom_histogram - Histograms

# %%


# Basic histogram
df = pd.DataFrame({'x': np.random.randn(500)})
ggplot(df, aes(x='x')) + geom_histogram(bins=30, fill='steelblue', alpha=0.7)


# %%


# Histogram with custom binwidth
ggplot(df, aes(x='x')) + geom_histogram(binwidth=0.25, fill='coral', alpha=0.7)


# %%


# Histogram by group (overlapping)
df = pd.DataFrame({
    'value': np.concatenate([np.random.randn(300), np.random.randn(300) + 2]),
    'group': ['A']*300 + ['B']*300
})
ggplot(df, aes(x='value', fill='group')) + geom_histogram(bins=30, alpha=0.5)


# %%


# Histogram with density overlay
df = pd.DataFrame({'x': np.random.randn(500)})
(
    ggplot(df, aes(x='x')) +
    geom_histogram(bins=30, fill='lightblue', alpha=0.5) +
    ggtitle('Histogram')
)


# ## geom_density - Density Plots

# %%


# Basic density
df = pd.DataFrame({'x': np.random.randn(500)})
ggplot(df, aes(x='x')) + geom_density(fill='lightblue', alpha=0.5)


# %%


# Density with color only (no fill)
ggplot(df, aes(x='x')) + geom_density(color='steelblue', size=2)


# %%


# Multiple densities
df = pd.DataFrame({
    'value': np.concatenate([
        np.random.randn(300),
        np.random.randn(300) + 2,
        np.random.randn(300) * 0.5 + 1
    ]),
    'group': ['Normal']*300 + ['Shifted']*300 + ['Narrow']*300
})
ggplot(df, aes(x='value', color='group', fill='group')) + geom_density(alpha=0.3)


# %%


# Density with rug plot
df = pd.DataFrame({'x': np.random.randn(100)})
(
    ggplot(df, aes(x='x')) +
    geom_density(fill='lightblue', alpha=0.5) +
    geom_rug(alpha=0.3)
)


# ## geom_boxplot - Box Plots

# %%


# Basic boxplot
df = pd.DataFrame({
    'category': ['A']*50 + ['B']*50 + ['C']*50,
    'value': np.concatenate([np.random.randn(50), np.random.randn(50)+1, np.random.randn(50)+0.5])
})
ggplot(df, aes(x='category', y='value')) + geom_boxplot()


# %%


# Colored boxplot
ggplot(df, aes(x='category', y='value', fill='category')) + geom_boxplot(alpha=0.7)


# %%


# Boxplot with jittered points
(
    ggplot(df, aes(x='category', y='value')) +
    geom_boxplot(alpha=0.3, fill='lightgray') +
    geom_jitter(width=0.15, alpha=0.5, color='steelblue', size=5)
)


# %%


# Horizontal boxplot
(
    ggplot(df, aes(x='category', y='value', fill='category')) +
    geom_boxplot(alpha=0.7) +
    coord_flip() +
    ggtitle('Horizontal Boxplot')
)


# %%


# Grouped boxplot
df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'] * 30,
    'group': ['X', 'Y'] * 90,
    'value': np.random.randn(180) + np.tile([0, 1, 0.5, 1.5, 1, 2], 30)
})
(
    ggplot(df, aes(x='category', y='value', fill='group')) +
    geom_boxplot() +
    ggtitle('Grouped Boxplot')
)


# ## geom_violin - Violin Plots

# %%


# Basic violin plot
df = pd.DataFrame({
    'category': ['A']*100 + ['B']*100 + ['C']*100,
    'value': np.concatenate([
        np.random.randn(100),
        np.random.randn(100)*0.5 + 1,
        np.concatenate([np.random.randn(50) - 1, np.random.randn(50) + 1])  # Bimodal
    ])
})
ggplot(df, aes(x='category', y='value', fill='category')) + geom_violin(alpha=0.7)


# %%


# Violin + boxplot combination
(
    ggplot(df, aes(x='category', y='value')) +
    geom_violin(fill='lightblue', alpha=0.5) +
    geom_boxplot(width=0.1, fill='white') +
    ggtitle('Violin + Boxplot')
)


# %%


# Violin + Points
(
    ggplot(df, aes(x='category', y='value', fill='category')) +
    geom_violin(alpha=0.4) +
    geom_jitter(width=0.1, alpha=0.3, size=3) +
    ggtitle('Violin + Jittered Points')
)


# ---
# # 5. Annotations & Reference Lines

# ## geom_text - Text Labels

# %%


# Basic text labels
df = pd.DataFrame({'x': [1, 2, 3], 'y': [3, 1, 2], 'label': ['Point A', 'Point B', 'Point C']})
ggplot(df, aes(x='x', y='y', label='label')) + geom_point(size=10) + geom_text(vjust=-1)


# %%


# Bar chart with value labels
df = pd.DataFrame({'category': ['A', 'B', 'C', 'D'], 'value': [25, 40, 30, 55]})
(
    ggplot(df, aes(x='category', y='value', label='value')) +
    geom_col(fill='steelblue') +
    geom_text(vjust=-0.5, size=12)
)


# %%


# Colored text labels
df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [2, 4, 3, 5],
    'label': ['Low', 'High', 'Medium', 'Very High'],
    'category': ['A', 'B', 'A', 'B']
})
(
    ggplot(df, aes(x='x', y='y', label='label', color='category')) +
    geom_point(size=12) +
    geom_text(vjust=-1, size=10)
)


# ## geom_vline, geom_hline, geom_abline - Reference Lines

# %%


# Vertical and horizontal reference lines
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50)})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.6, size=8) +
    geom_vline(data=0.5, color='red', linetype='dash', size=2) +
    geom_hline(data=0.5, color='blue', linetype='dash', size=2) +
    ggtitle('Vertical and Horizontal Reference Lines')
)


# %%


# Multiple reference lines
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.5, size=6) +
    geom_vline(data=-1, color='red', linetype='dash') +
    geom_vline(data=0, color='black', size=2) +
    geom_vline(data=1, color='red', linetype='dash') +
    geom_hline(data=0, color='black', size=2) +
    ggtitle('Multiple Reference Lines')
)


# %%


# Diagonal reference line (y = mx + b)
x = np.linspace(0, 10, 50)
y = 2 * x + 1 + np.random.randn(50) * 2
df = pd.DataFrame({'x': x, 'y': y})

(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.6, size=6) +
    geom_abline(slope=2, intercept=1, color='red', size=2, linetype='dash') +
    ggtitle('geom_abline: y = 2x + 1')
)


# %%


# Identity line (y = x)
df = pd.DataFrame({
    'actual': np.random.rand(50) * 100,
    'predicted': np.random.rand(50) * 100
})
(
    ggplot(df, aes(x='actual', y='predicted')) +
    geom_point(size=6, alpha=0.6) +
    geom_abline(slope=1, intercept=0, color='red', linetype='dash') +
    ggtitle('Actual vs Predicted with Identity Line')
)


# ## geom_segment - Line Segments

# %%


# Basic segments
df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [1, 2, 1],
    'xend': [2, 3, 4],
    'yend': [2, 1, 2]
})
(
    ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) +
    geom_segment(color='steelblue', size=2) +
    geom_point(size=10, color='red') +
    ggtitle('Line Segments')
)


# %%


# Segments with arrows (lollipop chart)
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D', 'E'],
    'value': [35, 50, 25, 70, 45]
})
df['y_base'] = 0
(
    ggplot(df, aes(x='category', y='y_base', xend='category', yend='value')) +
    geom_segment(color='steelblue', size=2) +
    geom_point(aes(y='value'), size=12, color='steelblue') +
    ggtitle('Lollipop Chart')
)


# ## annotate() - Add Annotations

# %%


# Text and rectangle annotations
df = pd.DataFrame({'x': np.random.randn(50), 'y': np.random.randn(50)})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(size=6, alpha=0.6) +
    annotate('rect', xmin=-1, xmax=1, ymin=-1, ymax=1, fill='yellow', alpha=0.3) +
    annotate('text', x=0, y=1.2, label='Core Region', size=12) +
    ggtitle('Rectangle Annotation')
)


# ---
# # 6. Aesthetics Deep Dive
# 
# Map data to visual properties.

# %%


# Color + Size + Shape
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', 
                     color='species', size='petal_length', shape='species')) +
    geom_point(alpha=0.7) +
    ggtitle('Multiple Aesthetics: Color + Size + Shape')
)


# %%


# Manual colors
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    scale_color_manual(values={'setosa': '#e41a1c', 'versicolor': '#377eb8', 'virginica': '#4daf4a'})
)


# %%


# Manual shapes
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', shape='species', color='species')) +
    geom_point(size=12) +
    scale_shape_manual(values={'setosa': 'circle', 'versicolor': 'square', 'virginica': 'diamond'})
)


# %%


# Fixed alpha for overplotting
df = pd.DataFrame({'x': np.random.randn(1000), 'y': np.random.randn(1000)})
ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.1, size=8, color='blue')


# %%


# Size scale
df = pd.DataFrame({
    'x': np.random.rand(50),
    'y': np.random.rand(50),
    'size_val': np.random.rand(50) * 100
})
(
    ggplot(df, aes(x='x', y='y', size='size_val')) +
    geom_point(alpha=0.5, color='steelblue') +
    scale_size(range=[5, 30]) +
    ggtitle('Size Scale with Custom Range')
)


# %%


# Fill vs Color for bars
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [10, 25, 15, 20],
    'group': ['X', 'Y', 'X', 'Y']
})
(
    ggplot(df, aes(x='category', y='value', fill='group')) +
    geom_col(color='black', size=1) +  # color is outline, fill is interior
    ggtitle('Fill (interior) vs Color (outline)')
)


# ---
# # 7. Scales
# 
# Control how data maps to visual properties.

# %%


# Custom limits and breaks
df = pd.DataFrame({'x': range(10), 'y': [i**2 for i in range(10)]})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(size=8) +
    geom_line() +
    scale_x_continuous(limits=(2, 8), breaks=[2, 4, 6, 8]) +
    scale_y_continuous(limits=(0, 70))
)


# %%


# Log scales
df = pd.DataFrame({'x': np.logspace(0, 3, 50), 'y': np.logspace(0, 3, 50) * (1 + np.random.rand(50)*0.5)})
ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10() + scale_y_log10()


# %%


# Brewer palettes - qualitative
df = pd.DataFrame({
    'x': np.random.rand(90),
    'y': np.random.rand(90),
    'group': np.random.choice(['A', 'B', 'C'], 90)
})
(
    ggplot(df, aes(x='x', y='y', color='group')) +
    geom_point(size=8) +
    scale_color_brewer(type='qual', palette='Set1')
)


# %%


# Brewer palettes - sequential
(
    ggplot(df, aes(x='x', y='y', color='group')) +
    geom_point(size=8) +
    scale_color_brewer(type='qual', palette='Set2') +
    ggtitle('Set2 Palette')
)


# %%


# Continuous color gradient
df = pd.DataFrame({'x': np.random.rand(100), 'y': np.random.rand(100), 'value': np.random.rand(100)})
(
    ggplot(df, aes(x='x', y='y', color='value')) +
    geom_point(size=8) +
    scale_color_gradient(low='yellow', high='red')
)


# %%


# Two-color gradient
(
    ggplot(df, aes(x='x', y='y', color='value')) +
    geom_point(size=8) +
    scale_color_gradient(low='blue', high='orange') +
    ggtitle('Blue to Orange Gradient')
)


# %%


# Viridis colorscale for heatmaps
x = np.arange(0, 15, 1)
y = np.arange(0, 15, 1)
X, Y = np.meshgrid(x, y)
Z = np.sin(X/3) * np.cos(Y/3)

df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})
ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + scale_fill_viridis_c()


# %%


# Fill gradient
(
    ggplot(df, aes(x='x', y='y', fill='z')) +
    geom_tile() +
    scale_fill_gradient(low='white', high='darkblue') +
    ggtitle('Custom Fill Gradient')
)


# %%


# Quick axis limits
df = pd.DataFrame({'x': np.random.randn(100), 'y': np.random.randn(100)})
ggplot(df, aes(x='x', y='y')) + geom_point() + xlim(-2, 2) + ylim(-2, 2)


# ---
# # 8. Faceting
# 
# Create small multiples by splitting data into panels.

# %%


# Basic facet_wrap
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width')) +
    geom_point(size=6) +
    facet_wrap('species')
)


# %%


# Facet wrap with ncol
mpg = data('mpg')
(
    ggplot(mpg, aes(x='displ', y='hwy')) +
    geom_point(size=5, alpha=0.6) +
    facet_wrap('class', ncol=4)
)


# %%


# Facet wrap with free scales
(
    ggplot(mpg, aes(x='displ', y='hwy')) +
    geom_point(size=5, alpha=0.6) +
    facet_wrap('class', ncol=4, scales='free')
)


# %%


# Facet wrap with free_x scales only
(
    ggplot(mpg, aes(x='displ', y='hwy')) +
    geom_point(size=5, alpha=0.6) +
    facet_wrap('class', ncol=4, scales='free_x') +
    ggtitle('Free X Scales Only')
)


# %%


# Facet grid with rows and columns
mpg_subset = mpg[mpg['cyl'].isin([4, 6, 8]) & mpg['drv'].isin(['f', 'r'])].copy()
mpg_subset['cyl'] = mpg_subset['cyl'].astype(str)

(
    ggplot(mpg_subset, aes(x='displ', y='hwy')) +
    geom_point(size=5, alpha=0.6) +
    facet_grid(rows='drv', cols='cyl')
)


# %%


# Facet with color mapping
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=6) +
    facet_wrap('species') +
    ggtitle('Faceted with Color')
)


# %%


# Faceted histograms
(
    ggplot(iris, aes(x='sepal_length', fill='species')) +
    geom_histogram(bins=15, alpha=0.7) +
    facet_wrap('species', ncol=1) +
    ggtitle('Faceted Histograms')
)


# ---
# # 9. Coordinates

# %%


# coord_flip - Horizontal bar chart
df = pd.DataFrame({'category': ['Apple', 'Banana', 'Cherry', 'Date'], 'value': [45, 32, 28, 15]})
(
    ggplot(df, aes(x='category', y='value')) +
    geom_col(fill='steelblue') +
    coord_flip() +
    ggtitle('Horizontal Bar Chart')
)


# %%


# coord_flip with boxplot
iris = data('iris')
(
    ggplot(iris, aes(x='species', y='sepal_length', fill='species')) +
    geom_boxplot() +
    coord_flip() +
    ggtitle('Horizontal Boxplot')
)


# %%


# coord_cartesian - Zoom without clipping
df = pd.DataFrame({'x': range(20), 'y': [i**2 for i in range(20)]})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(size=8) +
    geom_line() +
    coord_cartesian(xlim=(5, 15), ylim=(0, 200)) +
    ggtitle('Zoomed with coord_cartesian')
)


# %%


# coord_polar - Pie chart
df = pd.DataFrame({'category': ['A', 'B', 'C', 'D'], 'value': [30, 25, 25, 20]})
(
    ggplot(df, aes(x='category', y='value', fill='category')) +
    geom_col() +
    coord_polar() +
    ggtitle('Polar Coordinates (Pie-like)')
)


# %%


# coord_polar - Spiral
df = pd.DataFrame({'x': np.linspace(0, 4*np.pi, 100), 'y': np.linspace(0, 4*np.pi, 100)})
ggplot(df, aes(x='x', y='y')) + geom_line(color='purple', size=2) + coord_polar()


# ---
# # 10. Themes
# 
# Customize the overall appearance of plots.

# %%


# Sample data for theme demos
iris = data('iris')
base_plot = ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) + geom_point(size=8)


# %%


base_plot


# %%


base_plot + theme_minimal() + ggtitle('theme_minimal')


# %%


base_plot + theme_dark() + ggtitle('theme_dark')


# %%


base_plot + theme_bbc() + ggtitle('theme_bbc')


# %%


base_plot + theme_ggplot2() + ggtitle('theme_ggplot2')


# %%


base_plot + theme_nytimes() + ggtitle('theme_nytimes')


# %%


base_plot + theme_classic() + ggtitle('theme_classic')


# %%


# Custom theme
(
    base_plot +
    theme_custom(background_color='#f5f5f5', grid_color='white', text_color='#333') +
    ggtitle('theme_custom')
)


# %%


# Dark custom theme
(
    base_plot +
    theme_custom(background_color='#1a1a2e', grid_color='#16213e', text_color='#eee') +
    ggtitle('Dark Custom Theme')
)


# ---
# # 11. Labels & Titles

# %%


# Full labs() with all options
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    labs(
        title='Iris Dataset Analysis',
        subtitle='Relationship between sepal dimensions',
        x='Sepal Length (cm)',
        y='Sepal Width (cm)',
        caption='Data source: Fisher, 1936'
    ) +
    theme_minimal()
)


# %%


# ggtitle shorthand
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    ggtitle('Quick Title with ggtitle()')
)


# %%


# Custom plot size with ggsize
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    ggsize(900, 400) +
    ggtitle('Wide Format Plot (900x400)')
)


# %%


# Tall plot
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8) +
    ggsize(500, 700) +
    ggtitle('Tall Format Plot (500x700)')
)


# ---
# # 12. Combining Layers
# 
# Build complex visualizations by layering multiple geoms.

# %%


# Line + Points
df = pd.DataFrame({'x': np.linspace(0, 10, 20), 'y': np.sin(np.linspace(0, 10, 20))})
ggplot(df, aes(x='x', y='y')) + geom_line(color='blue', size=2) + geom_point(color='red', size=8)


# %%


# Scatter + Smooth + Rug
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width')) +
    geom_point(alpha=0.5, size=6, color='steelblue') +
    geom_smooth(method='loess', color='red') +
    geom_rug(color='gray', alpha=0.3) +
    ggtitle('Scatter + Smooth + Rug')
)


# %%


# Points + Error bars
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D', 'E'],
    'y': [10, 15, 12, 18, 14],
    'ymin': [8, 13, 10, 15, 11],
    'ymax': [12, 17, 14, 21, 17]
})
(
    ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) +
    geom_errorbar(width=0.2, color='gray') +
    geom_point(size=12, color='steelblue') +
    ggtitle('Points with Error Bars')
)


# %%


# Violin + Boxplot + Points
iris = data('iris')
(
    ggplot(iris, aes(x='species', y='sepal_length')) +
    geom_violin(fill='lightblue', alpha=0.5) +
    geom_boxplot(width=0.1, fill='white') +
    geom_jitter(width=0.5, alpha=0.3, size=3) +
    ggtitle('Violin + Boxplot + Points')
)


# %%


# Area + Line + Points
df = pd.DataFrame({'x': np.linspace(0, 10, 30), 'y': np.sin(np.linspace(0, 10, 30)) + 1.5})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_area(fill='lightblue', alpha=0.4) +
    geom_line(color='steelblue', size=2) +
    geom_point(color='darkblue', size=6) +
    ggtitle('Area + Line + Points')
)


# %%


# Bar + Text labels
df = pd.DataFrame({'category': ['A', 'B', 'C', 'D'], 'value': [25, 40, 30, 55]})
(
    ggplot(df, aes(x='category', y='value', fill='category', label='value')) +
    geom_col() +
    geom_text(vjust=-0.5, size=12) +
    ggtitle('Bar Chart with Labels')
)


# %%


# Histogram + Density overlay
df = pd.DataFrame({'x': np.random.randn(500)})
(
    ggplot(df, aes(x='x')) +
    geom_histogram(bins=30, fill='lightgray', alpha=0.7) +
    ggtitle('Histogram')
)


# ---
# # 13. Statistical Transformations

# %%


# LOESS smoothing (default)
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.randn(100) * 0.3
})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.5, size=5) +
    geom_smooth(method='loess', color='red', size=2) +
    ggtitle('LOESS Smoothing')
)


# %%


# Linear regression
df = pd.DataFrame({
    'x': np.linspace(0, 10, 50),
    'y': 2 * np.linspace(0, 10, 50) + 5 + np.random.randn(50) * 3
})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.5, size=6) +
    geom_smooth(method='lm', color='red', size=2) +
    ggtitle('Linear Regression')
)


# %%


# Smoothing by group
iris = data('iris')
(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(alpha=0.5, size=5) +
    geom_smooth(method='lm') +
    ggtitle('Linear Regression by Species')
)


# %%


# Compare smoothing methods
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.randn(100) * 0.3
})
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point(alpha=0.3, size=4) +
    geom_smooth(method='loess', color='red', size=2) +
    geom_smooth(method='lm', color='blue', size=2, linetype='dash') +
    ggtitle('LOESS (red) vs Linear (blue)')
)


# ---
# # 14. Positions

# %%


# Stacked bars (default)
df = pd.DataFrame({
    'category': ['A', 'A', 'A', 'B', 'B', 'B', 'C', 'C', 'C'],
    'group': ['X', 'Y', 'Z', 'X', 'Y', 'Z', 'X', 'Y', 'Z'],
    'value': [10, 15, 5, 12, 8, 10, 20, 10, 8]
})
(
    ggplot(df, aes(x='category', y='value', fill='group')) +
    geom_col(position='stack') +
    ggtitle('Stacked Bars')
)


# %%


# Dodged bars
(
    ggplot(df, aes(x='category', y='value', fill='group')) +
    geom_col(position='dodge') +
    ggtitle('Dodged Bars')
)


# %%


# geom_jitter for overplotting
iris = data('iris')
(
    ggplot(iris, aes(x='species', y='sepal_length')) +
    geom_jitter(width=0.2, alpha=0.5, size=6, color='steelblue') +
    ggtitle('Jittered Points')
)


# %%


# Jitter with color
(
    ggplot(iris, aes(x='species', y='sepal_length', color='species')) +
    geom_jitter(width=0.2, alpha=0.6, size=6) +
    ggtitle('Colored Jittered Points')
)


# ---
# # 15. Time Series

# %%


# Time series with date scale
economics = data('economics')
economics['date'] = pd.to_datetime(economics['date'])

(
    ggplot(economics, aes(x='date', y='unemploy')) +
    geom_line(color='steelblue', size=1) +
    scale_x_date(date_breaks='5 years', date_labels='%Y') +
    labs(title='US Unemployment', x='Year', y='Unemployed (thousands)')
)


# %%


# Area chart time series
(
    ggplot(economics, aes(x='date', y='unemploy')) +
    geom_area(fill='steelblue', alpha=0.5) +
    geom_line(color='darkblue', size=1) +
    scale_x_date(date_breaks='10 years', date_labels='%Y') +
    labs(title='US Unemployment Over Time')
)


# %%


# Multiple time series
econ = economics.copy()
econ['unemploy_scaled'] = econ['unemploy'] / 1000
econ['pce_scaled'] = econ['pce'] / 1000

df_long = pd.melt(econ[['date', 'unemploy_scaled', 'psavert']], 
                  id_vars=['date'], 
                  var_name='metric', 
                  value_name='value')

(
    ggplot(df_long, aes(x='date', y='value', color='metric')) +
    geom_line(size=1) +
    scale_x_date(date_breaks='10 years', date_labels='%Y') +
    labs(title='Economic Indicators Over Time')
)


# %%


# geom_range - Historical Range Comparison
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')

temperatures = []
for date in dates:
    seasonal = 55 + 25 * np.sin(2 * np.pi * (date.dayofyear - 80) / 365)
    trend = (date.year - 2019) * 0.5
    noise = np.random.randn() * 15
    temperatures.append(seasonal + trend + noise)

df_temp = pd.DataFrame({'date': dates, 'temperature': temperatures})

(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='ME') +
    labs(title='Temperature: 5-Year Historical Range',
         x='Month', y='Temperature') +
    theme_minimal()
)


# ---
# # 16. Financial Charts

# %%


# Create sample OHLC data
np.random.seed(42)
n_days = 60
dates = pd.date_range('2024-01-01', periods=n_days, freq='B')
close = 100 + np.cumsum(np.random.randn(n_days) * 2)

ohlc = pd.DataFrame({
    'date': dates,
    'open': close + np.random.randn(n_days) * 1,
    'high': close + np.abs(np.random.randn(n_days) * 2),
    'low': close - np.abs(np.random.randn(n_days) * 2),
    'close': close
})
ohlc['high'] = ohlc[['open', 'high', 'close']].max(axis=1)
ohlc['low'] = ohlc[['open', 'low', 'close']].min(axis=1)


# %%


# Candlestick chart
(
    ggplot(ohlc, aes(x='date', open='open', high='high', low='low', close='close')) +
    geom_candlestick() +
    labs(title='Stock Price - Candlestick Chart', x='Date', y='Price') +
    theme_minimal()
)


# %%


# Candlestick with custom colors
(
    ggplot(ohlc, aes(x='date', open='open', high='high', low='low', close='close')) +
    geom_candlestick(increasing_color='#2196F3', decreasing_color='#FF9800') +
    labs(title='Candlestick with Custom Colors', x='Date', y='Price') +
    theme_minimal()
)


# %%


# OHLC bar chart
(
    ggplot(ohlc, aes(x='date', open='open', high='high', low='low', close='close')) +
    geom_ohlc() +
    labs(title='Stock Price - OHLC Chart', x='Date', y='Price') +
    theme_minimal()
)


# ---
# # 17. 3D Plots

# %%


# 3D scatter plot
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'z': np.random.randn(100)
})
(
    ggplot(df, aes(x='x', y='y', z='z')) +
    geom_point_3d(size=6, color='steelblue') +
    ggtitle('3D Scatter Plot')
)


# %%


# 3D scatter with color grouping
df = pd.DataFrame({
    'x': np.concatenate([np.random.randn(50), np.random.randn(50) + 3]),
    'y': np.concatenate([np.random.randn(50), np.random.randn(50) + 2]),
    'z': np.concatenate([np.random.randn(50), np.random.randn(50) + 1]),
    'group': ['A']*50 + ['B']*50
})
(
    ggplot(df, aes(x='x', y='y', z='z', color='group')) +
    geom_point_3d(size=8, alpha=0.7) +
    ggtitle('3D Scatter with Groups')
)


# %%


# 3D scatter with size
df = pd.DataFrame({
    'x': np.random.randn(50),
    'y': np.random.randn(50),
    'z': np.random.randn(50),
    'size_val': np.random.rand(50) * 20
})
(
    ggplot(df, aes(x='x', y='y', z='z', size='size_val')) +
    geom_point_3d(color='coral', alpha=0.7) +
    ggtitle('3D Scatter with Size Mapping')
)


# %%


# 3D surface
x = np.linspace(-5, 5, 50)
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})

(
    ggplot(df, aes(x='x', y='y', z='z')) +
    geom_surface(colorscale='Viridis') +
    ggtitle('3D Surface - Ripple')
)


# %%


# 3D surface with different colorscale
(
    ggplot(df, aes(x='x', y='y', z='z')) +
    geom_surface(colorscale='Plasma') +
    ggtitle('3D Surface - Plasma Colorscale')
)


# %%


# Saddle surface
x = np.linspace(-3, 3, 40)
y = np.linspace(-3, 3, 40)
X, Y = np.meshgrid(x, y)
Z = X**2 - Y**2  # Saddle

df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})

(
    ggplot(df, aes(x='x', y='y', z='z')) +
    geom_surface(colorscale='RdBu') +
    ggtitle('3D Surface - Saddle')
)


# %%


# Wireframe plot
x = np.linspace(-3, 3, 25)
y = np.linspace(-3, 3, 25)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})

(
    ggplot(df, aes(x='x', y='y', z='z')) +
    geom_wireframe(color='steelblue', linewidth=1) +
    ggtitle('3D Wireframe')
)


# ---
# # 18. Maps

# %%


# US state choropleth
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0]
})

states = map_data('state')

(
    ggplot(state_data, aes(map_id='state', fill='population')) +
    geom_map(map=states, palette='Blues') +
    labs(title='US State Population (millions)')
)


# %%


# Map with different palette
(
    ggplot(state_data, aes(map_id='state', fill='population')) +
    geom_map(map=states, palette='Reds') +
    labs(title='US State Population - Red Scale')
)


# %%


# Map + Points overlay (cities)
cities = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    'pop_millions': [8.3, 3.9, 2.7, 2.3, 1.6]
})

(
    ggplot(state_data, aes(map_id='state', fill='population')) +
    geom_map(map=states, palette='Greens') +
    geom_point(cities, aes(x='lon', y='lat', size='pop_millions'), color='red', alpha=0.7) +
    labs(title='US Population with Major Cities')
)


# ---
# # 19. Network Visualization

# %%


# Simple circular network with edge bundling
np.random.seed(42)
n_nodes = 20
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)

edges = []
for _ in range(50):
    i, j = np.random.randint(0, n_nodes, 2)
    if i != j:
        edges.append({
            'x': np.cos(angles[i]),
            'y': np.sin(angles[i]),
            'xend': np.cos(angles[j]),
            'yend': np.sin(angles[j])
        })

edges_df = pd.DataFrame(edges)

(
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend')) +
    geom_edgebundle(K=0.1, cycles=6, alpha=0.5, color='steelblue') +
    ggtitle('Edge Bundling - Circular Layout')
)


# %%


# Edge bundling with different K parameter
(
    ggplot(edges_df, aes(x='x', y='y', xend='xend', yend='yend')) +
    geom_edgebundle(K=0.3, cycles=6, alpha=0.5, color='coral') +
    ggtitle('Edge Bundling - K=0.3 (tighter bundles)')
)


# %%


data()


# %%


# US flights network
import os

us_flights_nodes = data('us_flights_nodes')
us_flights_edges = data('us_flights_edges')

# Get coordinates
us_coords = us_flights_nodes[['longitude', 'latitude']].values

# Convert edges to coordinate format
# Edge file has V1, V2 columns (0-indexed node IDs)
us_flights_df = pd.DataFrame({
    'x': [us_coords[int(row['V1']), 0] for _, row in us_flights_edges.iterrows()],
    'y': [us_coords[int(row['V1']), 1] for _, row in us_flights_edges.iterrows()],
    'xend': [us_coords[int(row['V2']), 0] for _, row in us_flights_edges.iterrows()],
    'yend': [us_coords[int(row['V2']), 1] for _, row in us_flights_edges.iterrows()]
})

us_airports_df = pd.DataFrame({
    'lon': us_flights_nodes['longitude'],
    'lat': us_flights_nodes['latitude'],
    'city': us_flights_nodes['city'],
    'state': us_flights_nodes['state']
})


K = 1.0
E = 2.0
example_16_geo = (
    ggplot(us_flights_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_map(map_type='usa', projection='albers usa')
    + geom_point(
        data=us_airports_df,
        mapping=aes(x='lon', y='lat'),
        color='#9d0191',
        size=3
    )
    + geom_edgebundle(
        K=K,
        E=E,
        C=6,
        P=1,
        S=0.04,
        P_rate=2,
        I=50,
        I_rate=2/3,
        compatibility_threshold=0.6,
        color="#01169d",
        highlight_color='red',
        alpha=0.8,
        highlight_alpha=0.3,
        linewidth=0.5,
        verbose=True  # Show progress for this long computation
    )
    + labs(title=f'US Flights Edge Bundling ({len(us_flights_df)} routes, K = {K})')
    + theme_dark()
    + ggsize(width=1000, height=700)
)

example_16_geo


# ---
# # 20. Contours & Heatmaps

# %%


# Basic heatmap with geom_tile
x = np.arange(10)
y = np.arange(10)
X, Y = np.meshgrid(x, y)
Z = np.sin(X/2) + np.cos(Y/2)

df = pd.DataFrame({'x': X.flatten(), 'y': Y.flatten(), 'z': Z.flatten()})

(
    ggplot(df, aes(x='x', y='y', fill='z')) +
    geom_tile() +
    ggtitle('Heatmap with geom_tile')
)


# %%


# Correlation heatmap
iris = data('iris')
corr = iris[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].corr()
corr_long = corr.reset_index().melt(id_vars='index', var_name='var2', value_name='correlation')
corr_long = corr_long.rename(columns={'index': 'var1'})

(
    ggplot(corr_long, aes(x='var1', y='var2', fill='correlation')) +
    geom_tile() +
    scale_fill_gradient(low='blue', high='red') +
    ggtitle('Iris Correlation Heatmap')
)


# %%


# Contour plot
df = pd.DataFrame({'x': np.random.randn(500), 'y': np.random.randn(500)})

(
    ggplot(df, aes(x='x', y='y')) +
    geom_contour(bins=10) +
    geom_point(alpha=0.3, size=3) +
    ggtitle('Contour Lines')
)


# %%


# Filled contours
(
    ggplot(df, aes(x='x', y='y')) +
    geom_contour_filled(bins=15, colorscale='Viridis', alpha=0.8) +
    geom_point(color='white', alpha=0.5, size=2) +
    ggtitle('Filled Contours')
)


# %%


# Filled contours with different colorscale
(
    ggplot(df, aes(x='x', y='y')) +
    geom_contour_filled(bins=12, colorscale='Hot', alpha=0.8) +
    ggtitle('Filled Contours - Hot Colorscale')
)


# ---
# # 21. Segments & Paths

# %%


# geom_path - Connect points in order
import math
t_vals = [i * 4 * math.pi / 100 for i in range(100)]
spiral = pd.DataFrame({
    'x': [t * math.cos(t) for t in t_vals],
    'y': [t * math.sin(t) for t in t_vals]
})

ggplot(spiral, aes(x='x', y='y')) + geom_path(color='steelblue', size=2) + ggtitle('Spiral with geom_path')


# %%


# geom_path with color
spiral['t'] = t_vals
(
    ggplot(spiral, aes(x='x', y='y', color='t')) +
    geom_path(size=2) +
    scale_color_gradient(low='blue', high='red') +
    ggtitle('Spiral with Color Gradient')
)


# %%


# Arrow diagram with segments
df = pd.DataFrame({
    'x': [0, 1, 2],
    'y': [0, 0, 0],
    'xend': [1, 2, 3],
    'yend': [1, 0, 1],
    'label': ['Step 1', 'Step 2', 'Step 3']
})
(
    ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) +
    geom_segment(color='steelblue', size=2) +
    geom_point(size=10, color='coral') +
    geom_point(aes(x='xend', y='yend'), size=10, color='darkred') +
    ggtitle('Process Flow with Segments')
)


# ---
# # 22. Error Visualization

# %%


# Error bars
df = pd.DataFrame({
    'treatment': ['Control', 'Treatment A', 'Treatment B', 'Treatment C'],
    'mean': [10, 15, 12, 18],
    'se': [1.2, 1.5, 1.1, 2.0]
})
df['ymin'] = df['mean'] - df['se']
df['ymax'] = df['mean'] + df['se']

(
    ggplot(df, aes(x='treatment', y='mean', ymin='ymin', ymax='ymax')) +
    geom_errorbar(width=0.2, color='gray', size=1) +
    geom_point(size=12, color='steelblue') +
    ggtitle('Error Bars (Standard Error)')
)


# %%


# Error bars with bars
(
    ggplot(df, aes(x='treatment', y='mean', ymin='ymin', ymax='ymax', fill='treatment')) +
    geom_col(alpha=0.7) +
    geom_errorbar(width=0.2, color='black', size=1) +
    ggtitle('Bar Chart with Error Bars')
)


# %%


# Confidence band with geom_ribbon
x = np.linspace(0, 10, 50)
y = 2 * x + 5
noise = np.random.randn(50) * 3

df = pd.DataFrame({
    'x': x,
    'y_obs': y + noise,
    'y_pred': y,
    'ymin': y - 2,  # 95% CI lower
    'ymax': y + 2   # 95% CI upper
})

(
    ggplot(df, aes(x='x')) +
    geom_ribbon(aes(ymin='ymin', ymax='ymax'), fill='lightblue', alpha=0.5) +
    geom_line(aes(y='y_pred'), color='blue', size=2) +
    geom_point(aes(y='y_obs'), alpha=0.5, size=5) +
    ggtitle('Regression with Confidence Band')
)


# ---
# # 23. Advanced Examples

# %%


iris


# %%


# Comprehensive iris analysis
iris = data('iris')

(
    ggplot(iris, aes(x='sepal_length', y='sepal_width', color='species')) +
    geom_point(size=8, alpha=0.6) +
    geom_smooth(method='lm', se=False) +
    geom_rug(alpha=0.3) +
    facet_wrap('species') +
    scale_color_brewer(type='qual', palette='Set1') +
    labs(
        title='Iris Dataset: Sepal Analysis by Species',
        subtitle='With linear regression and marginal distributions',
        x='Sepal Length (cm)',
        y='Sepal Width (cm)'
    ) +
    theme_minimal()
)


# %%


# Dashboard-style multi-panel
mpg = data('mpg')
mpg['cyl'] = mpg['cyl'].astype(str)

(
    ggplot(mpg, aes(x='displ', y='hwy')) +
    geom_point(aes(color='cyl'), size=6, alpha=0.6) +
    geom_smooth(method='loess', color='black', size=1) +
    facet_wrap('drv', ncol=3) +
    scale_color_brewer(type='qual', palette='Set2') +
    labs(
        title='Fuel Economy Analysis',
        subtitle='Highway MPG vs Engine Displacement by Drive Type',
        x='Engine Displacement (L)',
        y='Highway MPG'
    ) +
    theme_bbc()
)


# %%


# Multi-variable diamond analysis
diamonds_sample = data('diamonds').sample(500, random_state=42)

(
    ggplot(diamonds_sample, aes(x='carat', y='price', color='cut')) +
    geom_point(alpha=0.5, size=5) +
    geom_smooth(method='lm', se=False) +
    facet_wrap('clarity', ncol=4) +
    scale_y_continuous(limits=(0, 20000)) +
    labs(
        title='Diamond Price Analysis',
        subtitle='Price vs Carat by Cut and Clarity',
        x='Carat',
        y='Price ($)'
    ) +
    theme_minimal()
)


# %%


# Petal dimensions with all aesthetics
iris = data('iris')

(
    ggplot(iris, aes(x='petal_length', y='petal_width', 
                     color='species', shape='species', size='sepal_length')) +
    geom_point(alpha=0.7) +
    scale_size(range=[3, 15]) +
    labs(
        title='Iris: Petal Dimensions',
        subtitle='Color & Shape by Species, Size by Sepal Length',
        x='Petal Length (cm)',
        y='Petal Width (cm)'
    ) +
    theme_ggplot2()
)


# %%


# Complex time series
economics = data('economics')
economics['date'] = pd.to_datetime(economics['date'])
economics['year'] = economics['date'].dt.year

# Filter to recent decades
econ_recent = economics[economics['year'] >= 1990].copy()

(
    ggplot(econ_recent, aes(x='date', y='unemploy')) +
    geom_area(fill='steelblue', alpha=0.3) +
    geom_line(color='steelblue', size=1) +
    geom_hline(data=econ_recent['unemploy'].mean(), color='red', linetype='dash') +
    scale_x_date(date_breaks='5 years', date_labels='%Y') +
    labs(
        title='US Unemployment Since 1990',
        subtitle='Red line = average',
        x='Year',
        y='Unemployed (thousands)'
    ) +
    theme_nytimes()
)


# %%

# Publication-ready plot
mtcars = data('mtcars')
mtcars['cyl'] = mtcars['cyl'].astype(str)
mtcars['am'] = mtcars['am'].map({0: 'Automatic', 1: 'Manual'})

(
    ggplot(mtcars, aes(x='wt', y='mpg', color='cyl', shape='am')) +
    geom_point(size=10, alpha=0.8) +
    geom_smooth(aes(group='cyl'), method='lm', se=False, size=1) +
    scale_color_manual(values={'4': '#2ecc71', '6': '#3498db', '8': '#e74c3c'}) +
    labs(
        title='Fuel Economy vs Vehicle Weight',
        subtitle='By Number of Cylinders and Transmission Type',
        x='Weight (1000 lbs)',
        y='Miles per Gallon',
        caption='Data: Motor Trend Car Road Tests (1974)'
    ) +
    theme_classic()
)


# ---
# # Summary
# 
# ## Key Concepts
# 
# 1. **Data + Aesthetics + Geoms** = Basic plot
# 2. **Scales** control mapping between data and visual properties
# 3. **Facets** create small multiples
# 4. **Themes** customize appearance
# 5. **Layers** can be combined with `+`
# 
# ## Quick Reference
# 
# ### Basic Geoms
# | Geom | Use Case |
# |------|----------|
# | `geom_point` | Scatter plots |
# | `geom_line` | Line charts |
# | `geom_bar` | Count categories |
# | `geom_col` | Pre-computed values |
# | `geom_area` | Area charts |
# | `geom_step` | Step functions |
# | `geom_ribbon` | Confidence bands |
# 
# ### Statistical Geoms
# | Geom | Use Case |
# |------|----------|
# | `geom_histogram` | Distribution |
# | `geom_density` | Smooth distribution |
# | `geom_boxplot` | Summary stats |
# | `geom_violin` | Distribution shape |
# | `geom_smooth` | Trend lines |
# 
# ### Advanced Geoms
# | Geom | Use Case |
# |------|----------|
# | `geom_tile` | Heatmaps |
# | `geom_contour` | Contour lines |
# | `geom_contour_filled` | Filled contours |
# | `geom_map` | Choropleth maps |
# | `geom_range` | Time series comparison |
# | `geom_candlestick` | Financial charts |
# | `geom_ohlc` | Financial OHLC |
# | `geom_point_3d` | 3D scatter |
# | `geom_surface` | 3D surface |
# | `geom_wireframe` | 3D wireframe |
# | `geom_edgebundle` | Network visualization |
# 
# ### Annotation Geoms
# | Geom | Use Case |
# |------|----------|
# | `geom_text` | Text labels |
# | `geom_vline` | Vertical reference |
# | `geom_hline` | Horizontal reference |
# | `geom_abline` | Diagonal reference |
# | `geom_segment` | Line segments |
# | `geom_errorbar` | Error bars |
# | `geom_rug` | Marginal distributions |
# 
# ## Themes
# 
# - `theme_minimal()` - Clean, minimal
# - `theme_dark()` - Dark background
# - `theme_bbc()` - BBC style
# - `theme_ggplot2()` - Classic R ggplot2
# - `theme_nytimes()` - NYT style
# - `theme_classic()` - Traditional
# - `theme_custom()` - Fully customizable
# 
# ## Built-in Datasets
# 
# - `iris` - Fisher's iris measurements
# - `mpg` - Fuel economy data
# - `diamonds` - Diamond prices
# - `mtcars` - Motor car data
# - `economics` - US economic time series
# - `us_flights_nodes` - US airport nodes
# - `us_flights_edges` - US flight connections
# 
# ## Scales
# 
# - `scale_x_continuous()`, `scale_y_continuous()` - Continuous axes
# - `scale_x_log10()`, `scale_y_log10()` - Log scales
# - `scale_x_date()` - Date axes
# - `scale_color_manual()`, `scale_fill_manual()` - Custom colors
# - `scale_color_brewer()`, `scale_fill_brewer()` - ColorBrewer palettes
# - `scale_color_gradient()`, `scale_fill_gradient()` - Continuous gradients
# - `scale_fill_viridis_c()` - Viridis colorscale
# - `scale_shape_manual()` - Custom shapes
# - `scale_size()` - Size mapping

# 
