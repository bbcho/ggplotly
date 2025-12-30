#!/usr/bin/env python
# coding: utf-8

# # ggplotly Comprehensive Demo
# Complete demonstration of all geoms, coords, stats, scales, aesthetics, facets, themes, and utilities

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')

# Setup
import numpy as np
import pandas as pd
from ggplotly import *

np.random.seed(42)


# ## 1. GEOMS - All Geometry Types

# In[ ]:


# geom_point - Scatter plot
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50)})
ggplot(df, aes(x='x', y='y')) + geom_point() + ggtitle('geom_point')


# In[ ]:


# geom_line - Line plot
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50))})
ggplot(df, aes(x='x', y='y')) + geom_line() + ggtitle('geom_line')


# In[ ]:


# geom_area - Area plot
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50))})
ggplot(df, aes(x='x', y='y')) + geom_area() + ggtitle('geom_area')


# In[ ]:


# geom_bar - Bar chart with counts
df = pd.DataFrame({'category': ['A', 'B', 'C', 'A', 'B', 'A']})
ggplot(df, aes(x='category')) + geom_bar() + ggtitle('geom_bar')


# In[ ]:


# geom_col - Column chart with values
df = pd.DataFrame({'category': ['A', 'B', 'C'], 'value': [10, 15, 12]})
ggplot(df, aes(x='category', y='value')) + geom_col() + ggtitle('geom_col')


# In[ ]:


# geom_histogram - Histogram
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_histogram(bin=20) + ggtitle('geom_histogram')


# In[ ]:


# geom_boxplot - Box plot
df = pd.DataFrame({'category': ['A']*20 + ['B']*20, 'value': np.random.randn(40)})
ggplot(df, aes(x='category', y='value')) + geom_boxplot() + ggtitle('geom_boxplot')


# In[ ]:


# geom_violin - Violin plot
df = pd.DataFrame({'category': ['A']*50 + ['B']*50, 'value': np.random.randn(100)})
ggplot(df, aes(x='category', y='value')) + geom_violin() + ggtitle('geom_violin')


# In[ ]:


# geom_density - Density plot
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_density() + ggtitle('geom_density')


# In[ ]:


# geom_smooth - Smoothed line
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50)) + np.random.randn(50)*0.2})
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_smooth() + ggtitle('geom_smooth')


# In[ ]:


# geom_step - Step function
df = pd.DataFrame({'x': np.linspace(0, 10, 30), 'y': np.cumsum(np.random.randn(30))})
ggplot(df, aes(x='x', y='y')) + geom_step() + ggtitle('geom_step')


# In[ ]:


# geom_segment - Line segments
df = pd.DataFrame({'x': [1,2,3], 'y': [1,2,1], 'xend': [2,3,4], 'yend': [2,1,2]})
ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) + geom_segment() + ggtitle('geom_segment')


# In[ ]:


# geom_errorbar - Error bars
df = pd.DataFrame({'x': ['A','B','C'], 'y': [5,8,6], 'ymin': [4,7,5], 'ymax': [6,9,7]})
ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) + geom_errorbar() + ggtitle('geom_errorbar')


# In[ ]:


# geom_ribbon - Ribbon/confidence band
df = pd.DataFrame({'x': np.linspace(0,10,50), 'ymin': np.sin(np.linspace(0,10,50))-0.5, 'ymax': np.sin(np.linspace(0,10,50))+0.5})
ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) + geom_ribbon(alpha=0.3) + ggtitle('geom_ribbon')


# In[ ]:


# geom_tile - Heatmap tiles
df = pd.DataFrame({'x': np.repeat(range(5), 5), 'y': np.tile(range(5), 5), 'z': np.random.randn(25)})
ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + ggtitle('geom_tile')


# In[ ]:


# geom_text - Text labels
df = pd.DataFrame({'x': [1,2,3], 'y': [1,2,3], 'label': ['A','B','C']})
ggplot(df, aes(x='x', y='y', label='label')) + geom_text() + ggtitle('geom_text')


# In[ ]:


# geom_vline & geom_hline - Reference lines
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_vline(data=0.5, color='red') + geom_hline(data=0.5, color='blue') + ggtitle('geom_vline & geom_hline')


# ## 2. AESTHETICS - Mapping Data to Visual Properties

# In[ ]:


# Color aesthetic
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50), 'category': np.random.choice(['A','B','C'], 50)})
ggplot(df, aes(x='x', y='y', color='category')) + geom_point(size=10) + ggtitle('aes(color=...)')


# In[ ]:


# Size aesthetic
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30), 'size_var': np.random.rand(30)*20})
ggplot(df, aes(x='x', y='y', size='size_var')) + geom_point() + ggtitle('aes(size=...)')


# In[ ]:


# Fill aesthetic
df = pd.DataFrame({'category': ['A']*20+['B']*20, 'value': np.random.randn(40)})
ggplot(df, aes(x='category', y='value', fill='category')) + geom_boxplot() + ggtitle('aes(fill=...)')


# In[ ]:


# Alpha aesthetic
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50)})
ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.3, size=15) + ggtitle('alpha=0.3')


# In[ ]:


# Group aesthetic
df = pd.DataFrame({'x': np.tile(np.linspace(0,10,20), 3), 'y': np.random.randn(60).cumsum(), 'group': np.repeat(['A','B','C'], 20)})
ggplot(df, aes(x='x', y='y', group='group', color='group')) + geom_line() + ggtitle('aes(group=...)')


# ## 3. SCALES - Control Axis and Color Mappings

# In[ ]:


# scale_x_continuous & scale_y_continuous
df = pd.DataFrame({'x': range(10), 'y': [i**2 for i in range(10)]})
ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_continuous(limits=(2,8)) + scale_y_continuous(limits=(0,50)) + ggtitle('scale_x/y_continuous')


# In[ ]:


# scale_x_log10 & scale_y_log10
df = pd.DataFrame({'x': np.logspace(0, 3, 50), 'y': np.logspace(0, 3, 50)})
ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10() + scale_y_log10() + ggtitle('scale_x/y_log10')


# In[ ]:


# scale_color_manual
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30), 'cat': np.random.choice(['A','B'], 30)})
ggplot(df, aes(x='x', y='y', color='cat')) + geom_point(size=10) + scale_color_manual(values=['red','blue']) + ggtitle('scale_color_manual')


# In[ ]:


# scale_color_gradient
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50), 'val': np.random.rand(50)})
ggplot(df, aes(x='x', y='y', color='val')) + geom_point(size=10) + scale_color_gradient(low='yellow', high='red') + ggtitle('scale_color_gradient')


# In[ ]:


# scale_color_brewer
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50), 'cat': np.random.choice(['A','B','C'], 50)})
ggplot(df, aes(x='x', y='y', color='cat')) + geom_point(size=10) + scale_color_brewer(type='qual', palette='Set1') + ggtitle('scale_color_brewer')


# In[ ]:


# scale_fill_gradient & scale_fill_manual
df = pd.DataFrame({'x': np.repeat(range(5), 5), 'y': np.tile(range(5), 5), 'z': np.random.rand(25)})
ggplot(df, aes(x='x', y='y', fill='z')) + geom_tile() + scale_fill_gradient(low='white', high='darkblue') + ggtitle('scale_fill_gradient')


# In[ ]:


# scale_size
df = pd.DataFrame({'x': np.random.rand(50), 'y': np.random.rand(50), 'size_var': np.random.rand(50)*100})
ggplot(df, aes(x='x', y='y', size='size_var')) + geom_point() + scale_size(range=(2,20)) + ggtitle('scale_size')


# ## 4. FACETS - Create Small Multiples

# In[ ]:


# facet_wrap
df = pd.DataFrame({'x': np.random.rand(100), 'y': np.random.rand(100), 'category': np.random.choice(['A','B','C','D'], 100)})
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('category', ncol=2) + ggtitle('facet_wrap')


# In[ ]:


# facet_grid
df = pd.DataFrame({'x': np.random.rand(100), 'y': np.random.rand(100), 'row_var': np.random.choice(['R1','R2'], 100), 'col_var': np.random.choice(['C1','C2'], 100)})
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_grid(rows='row_var', cols='col_var') + ggtitle('facet_grid')


# ## 5. COORDINATES - Modify Coordinate Systems

# In[ ]:


# coord_cartesian - Zoom with limits
df = pd.DataFrame({'x': range(20), 'y': [i**2 for i in range(20)]})
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_line() + coord_cartesian(xlim=(5,15), ylim=(0,200)) + ggtitle('coord_cartesian')


# In[ ]:


# coord_flip - Flip x and y axes
df = pd.DataFrame({'category': ['A','B','C','D'], 'value': [10,15,12,18]})
ggplot(df, aes(x='category', y='value')) + geom_col() + coord_flip() + ggtitle('coord_flip')


# In[ ]:


# coord_polar - Polar coordinates
df = pd.DataFrame({'x': np.linspace(0, 2*np.pi, 100), 'y': np.sin(np.linspace(0, 2*np.pi, 100))})
ggplot(df, aes(x='x', y='y')) + geom_line() + coord_polar() + ggtitle('coord_polar')


# ## 6. THEMES - Customize Plot Appearance

# In[ ]:


# theme_default
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_default() + ggtitle('theme_default')


# In[ ]:


# theme_minimal
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal() + ggtitle('theme_minimal')


# In[ ]:


# theme_dark
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_dark() + ggtitle('theme_dark')


# In[ ]:


# theme_bbc
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_bbc() + ggtitle('theme_bbc')


# In[ ]:


# theme_ggplot2
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_ggplot2() + ggtitle('theme_ggplot2')


# In[ ]:


# theme_nytimes
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_nytimes() + ggtitle('theme_nytimes')


# ## 7. LABELS & TITLES - Add Text Annotations

# In[ ]:


# ggtitle
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + ggtitle('This is a Main Title')


# In[ ]:


# labs - Full labeling
df = pd.DataFrame({'x': np.random.rand(30), 'y': np.random.rand(30)})
ggplot(df, aes(x='x', y='y')) + geom_point() + labs(title='Main Title', x='X Axis Label', y='Y Axis Label', caption='Data source: Demo')


# ## 8. STATS - Statistical Transformations

# In[ ]:


# stat_identity (default for most geoms)
df = pd.DataFrame({'x': [1,2,3], 'y': [4,5,6]})
ggplot(df, aes(x='x', y='y')) + geom_line() + ggtitle('stat="identity"')


# In[ ]:


# stat_count (for bar charts)
df = pd.DataFrame({'category': ['A','B','C','A','B','A']})
ggplot(df, aes(x='category')) + geom_bar() + ggtitle('stat="count"')


# In[ ]:


# stat_bin (for histograms)
df = pd.DataFrame({'x': np.random.randn(200)})
ggplot(df, aes(x='x')) + geom_histogram(bin=20) + ggtitle('stat="bin"')


# In[ ]:


# stat_smooth (for smoothing)
df = pd.DataFrame({'x': np.linspace(0, 10, 50), 'y': np.sin(np.linspace(0, 10, 50)) + np.random.randn(50)*0.2})
ggplot(df, aes(x='x', y='y')) + geom_point() + geom_smooth(method='loess') + ggtitle('stat="smooth"')


# In[ ]:


# stat_ecdf (empirical cumulative distribution)
df = pd.DataFrame({'x': np.random.randn(100)})
ggplot(df, aes(x='x')) + geom_step(stat='ecdf') + ggtitle('stat="ecdf"')


# ## 9. COMPLEX EXAMPLES - Combining Multiple Components

# In[ ]:


# Complex plot with multiple aesthetics, facets, and themes
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'category': np.random.choice(['A','B','C'], 100),
    'size_var': np.random.rand(100) * 20
})

(ggplot(df, aes(x='x', y='y', color='category', size='size_var')) +
 geom_point(alpha=0.6) +
 geom_smooth(method='loess') +
 facet_wrap('category') +
 scale_color_brewer(type='qual', palette='Set1') +
 labs(title='Complex Multi-Component Plot', x='X Variable', y='Y Variable') +
 theme_minimal())


# In[ ]:


# Ultra-Complex Example: 5 DataFrames with Multiple Geoms, Facets, Themes, and Color Scales
# This demonstrates the power of ggplotly by combining:
# - 5 different datasets (points, trends, confidence intervals, errors, labels)
# - 5 different geoms (point, line, ribbon, errorbar, text)
# - Faceting by region
# - Custom color and fill scales
# - Theme customization
# - Comprehensive labeling

np.random.seed(123)

# DataFrame 1: Scatter data with measurements
df_measurements = pd.DataFrame({
    'time': np.tile(np.arange(1, 21), 3),
    'value': np.concatenate([
        np.random.normal(50, 10, 20) + np.arange(20) * 2,  # North
        np.random.normal(40, 8, 20) + np.arange(20) * 1.5,   # South
        np.random.normal(45, 12, 20) + np.arange(20) * 1.8   # East
    ]),
    'region': np.repeat(['North', 'South', 'East'], 20),
    'size': np.random.uniform(5, 15, 60)
})

# DataFrame 2: Trend lines (smoothed averages)
df_trends = pd.DataFrame({
    'time': np.tile(np.linspace(1, 20, 40), 3),
    'trend': np.concatenate([
        50 + np.linspace(1, 20, 40) * 2,     # North trend
        40 + np.linspace(1, 20, 40) * 1.5,   # South trend
        45 + np.linspace(1, 20, 40) * 1.8    # East trend
    ]),
    'region': np.repeat(['North', 'South', 'East'], 40)
})

# DataFrame 3: Confidence intervals
df_confidence = pd.DataFrame({
    'time': np.tile(np.linspace(1, 20, 40), 3),
    'upper': np.concatenate([
        50 + np.linspace(1, 20, 40) * 2 + 10,
        40 + np.linspace(1, 20, 40) * 1.5 + 8,
        45 + np.linspace(1, 20, 40) * 1.8 + 12
    ]),
    'lower': np.concatenate([
        50 + np.linspace(1, 20, 40) * 2 - 10,
        40 + np.linspace(1, 20, 40) * 1.5 - 8,
        45 + np.linspace(1, 20, 40) * 1.8 - 12
    ]),
    'region': np.repeat(['North', 'South', 'East'], 40)
})

# DataFrame 4: Error bars at key timepoints
df_errors = pd.DataFrame({
    'time': np.tile([5, 10, 15], 3),
    'value': [60, 70, 80, 48, 55, 62, 54, 63, 72],
    'error': [8, 9, 7, 6, 7, 5, 10, 8, 9],
    'region': np.repeat(['North', 'South', 'East'], 3)
})
df_errors['ymin'] = df_errors['value'] - df_errors['error']
df_errors['ymax'] = df_errors['value'] + df_errors['error']

# DataFrame 5: Text annotations
df_labels = pd.DataFrame({
    'time': [18, 18, 18],
    'value': [90, 70, 80],
    'label': ['High Growth', 'Steady', 'Moderate'],
    'region': ['North', 'South', 'East']
})

# Build the complex plot layer by layer
(ggplot(df_measurements, aes(x='time', y='value', color='region')) +
 # Layer 1: Confidence ribbons (3 ribbons, one per region)
 geom_ribbon(data=df_confidence, mapping=aes(x='time', ymin='lower', ymax='upper', fill='region'), alpha=0.2) +
 # Layer 2: Trend lines (3 lines, one per region)
 geom_line(data=df_trends, mapping=aes(x='time', y='trend', color='region'), size=3) +
 # Layer 3: Actual measurements (60 points colored by region with variable sizes)
 geom_point(alpha=0.7, size=8) +
 # Layer 4: Error bars at specific timepoints (9 error bars)
 geom_errorbar(data=df_errors, mapping=aes(x='time', y='value', ymin='ymin', ymax='ymax', color='region'), alpha=0.6) +
 # Layer 5: Text annotations (3 labels)
 geom_text(data=df_labels, mapping=aes(x='time', y='value', label='label', color='region'), size=12) +
 # Faceting: Create separate panels for each region
 facet_wrap('region', ncol=3) +
 # Color scale: Use a professional palette for lines and points
 scale_color_brewer(type='qual', palette='Dark2') +
 # Fill scale: Use matching palette for ribbons
 scale_fill_brewer(type='qual', palette='Dark2') +
 # Labels: Comprehensive titles and axis labels
 labs(
     title='Multi-Dataset Analysis: Regional Growth Trends with Confidence Intervals',
     subtitle='Combining 5 different data sources and 5 different geom types',
     x='Time Period',
     y='Measured Value',
     caption='Data: Simulated regional measurements with trends, CI, and error bars'
 ) +
 # Theme: Professional dark theme
 theme_dark()
)


# In[ ]:


# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    'sepal_length': np.concatenate([
        np.random.normal(5.0, 0.4, 50),
        np.random.normal(6.0, 0.5, 50),
        np.random.normal(6.5, 0.6, 50)
    ]),
    'sepal_width': np.concatenate([
        np.random.normal(3.4, 0.4, 50),
        np.random.normal(2.8, 0.3, 50),
        np.random.normal(3.0, 0.3, 50)
    ]),
    'species': ['setosa'] * 50 + ['versicolor'] * 50 + ['virginica'] * 50
})

# Example 1: Shape mapped to species
p1 = (ggplot(df, aes(x='sepal_length', y='sepal_width', shape='species'))
      + geom_point(size=10)
      + theme_minimal()
      + labs(title='Shape by Species'))
p1.show()

# Example 2: Both color AND shape mapped to species
p2 = (ggplot(df, aes(x='sepal_length', y='sepal_width', color='species', shape='species'))
      + geom_point(size=10)
      + theme_minimal()
      + labs(title='Color and Shape by Species'))
p2.show()

# Example 3: Custom shapes with scale_shape_manual
p3 = (ggplot(df, aes(x='sepal_length', y='sepal_width', color='species', shape='species'))
      + geom_point(size=12)
      + scale_shape_manual(values={'setosa': 'star', 'versicolor': 'diamond', 'virginica': 'hexagon'})
      + scale_color_manual(values={'setosa': '#e41a1c', 'versicolor': '#377eb8', 'virginica': '#4daf4a'})
      + theme_minimal()
      + labs(title='Custom Shapes and Colors'))
p3.show()

# Example 4: Literal shape for all points
p4 = (ggplot(df, aes(x='sepal_length', y='sepal_width', color='species'))
      + geom_point(shape='diamond', size=10)
      + theme_minimal()
      + labs(title='All Points as Diamonds'))
p4.show()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_jitter, geom_boxplot, theme_minimal, labs, scale_color_manual

# Create sample data with overlapping points
np.random.seed(42)
df = pd.DataFrame({
    'treatment': ['Control', 'Control', 'Control', 'Drug A', 'Drug A', 'Drug A', 'Drug B', 'Drug B', 'Drug B'] * 20,
    'response': np.concatenate([
        np.random.normal(5, 1, 60),   # Control
        np.random.normal(7, 1.2, 60), # Drug A
        np.random.normal(8, 0.8, 60)  # Drug B
    ]),
    'gender': ['M', 'F'] * 90
})

# Example 1: Basic jitter plot - see how points that would overlap are spread out
p1 = (ggplot(df, aes(x='treatment', y='response'))
      + geom_jitter(width=0.2, height=0, alpha=0.6, size=8)
      + theme_minimal()
      + labs(title='Jittered Points by Treatment'))
p1.show()

# Example 2: Jitter with color by gender
p2 = (ggplot(df, aes(x='treatment', y='response', color='gender'))
      + geom_jitter(width=0.2, height=0, alpha=0.7, size=8)
      + scale_color_manual(values={'M': '#3498db', 'F': '#e74c3c'})
      + theme_minimal()
      + labs(title='Response by Treatment and Gender'))
p2.show()

# Example 3: Combine boxplot with jitter (common pattern)
p3 = (ggplot(df, aes(x='treatment', y='response'))
      + geom_boxplot(alpha=0.3)
      + geom_jitter(width=0.15, height=0, alpha=0.5, size=6, color='steelblue')
      + theme_minimal()
      + labs(title='Boxplot with Jittered Points'))
p3.show()

# Example 4: Reproducible jitter with seed
p4 = (ggplot(df, aes(x='treatment', y='response', color='gender'))
      + geom_jitter(width=0.25, height=0, seed=123, size=8)
      + theme_minimal()
      + labs(title='Reproducible Jitter (seed=123)'))
p4.show()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_jitter, theme_minimal

# Create sample data with overlapping points
np.random.seed(42)
df = pd.DataFrame({
    'category': np.repeat(['A', 'B', 'C'], 60),
    'value': np.concatenate([
        np.random.normal(10, 2, 60),
        np.random.normal(15, 2, 60),
        np.random.normal(12, 2, 60)
    ])
})

# Jittered point plot - points should now spread horizontally within each category
p = (ggplot(df, aes(x='category', y='value'))
     + geom_jitter(width=0.2, color='steelblue', alpha=0.6)
     + theme_minimal())

p.draw()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_point, geom_rug, theme_minimal

# Create sample data
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100)
})

# Scatter plot with rug marks on bottom and left (default)
p = (ggplot(df, aes(x='x', y='y'))
     + geom_point(alpha=0.6, color='steelblue')
     + geom_rug(color='darkgray', alpha=0.5, sides='bl')
     + theme_minimal())

p.draw()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_point, geom_abline, theme_minimal

# Create sample data
np.random.seed(42)
x = np.linspace(0, 10, 50)
y = 2 * x + 1 + np.random.normal(0, 2, 50)  # y = 2x + 1 with noise
df = pd.DataFrame({'x': x, 'y': y})

# Scatter plot with reference line (y = 2x + 1)
p = (ggplot(df, aes(x='x', y='y'))
     + geom_point(alpha=0.6, color='steelblue')
     + geom_abline(slope=2, intercept=1, color='red', linetype='dash', size=2)
     + theme_minimal())

p.draw()


# In[ ]:


# Multiple reference lines
p = (ggplot(df, aes(x='x', y='y'))
     + geom_point(alpha=0.6)
     + geom_abline(slope=[1, 2, 3], intercept=[0, 0, 0], color='gray', linetype='dot')
     + theme_minimal())
p.draw()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_contour, geom_point, theme_minimal

# Create bivariate normal data
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.normal(0, 1, 500),
    'y': np.random.normal(0, 1, 500)
})

# Contour lines showing 2D density
p = (ggplot(df, aes(x='x', y='y'))
     + geom_contour(bins=10, color='steelblue')
     + geom_point(alpha=0.3, size=3)
     + theme_minimal())

p.draw()


# In[ ]:


import pandas as pd
import numpy as np
from ggplotly import ggplot, aes, geom_contour_filled, geom_point, theme_minimal

# Create bivariate normal data
np.random.seed(42)
df = pd.DataFrame({
    'x': np.random.normal(0, 1, 500),
    'y': np.random.normal(0, 1, 500)
})

# Filled contours with points overlay
p = (ggplot(df, aes(x='x', y='y'))
     + geom_contour_filled(bins=15, colorscale='Viridis', alpha=0.8)
     + geom_point(color='white', alpha=0.5, size=3)
     + theme_minimal())

p.draw()

