# %%
import os
import sys

from ggplotly import *
import pandas as pd
import numpy as np

# %%


a = np.random.random(1000)
b = np.random.random(1000)
df = pd.DataFrame({'a': a, 'b': b})

ggplot(df, aes(x='a', y='b')) + geom_point() + theme_dark()


# %%
x = np.random.random(1000)
y = np.random.random(1000)
df = pd.DataFrame({'x': x, 'y': y})

ggplot(df) + geom_point(aes(x='x', y='y')) + theme_dark()


# %%


x = np.random.random(1000)
y = np.random.random(1000)
df = pd.DataFrame({'x': x, 'y': y})

ggplot(df) + geom_point(aes(x='y', y='x')) + geom_point(aes(x='x', y='y')) + theme_dark()


# %%


x = np.random.random(1000)
y = np.random.random(1000)
df = pd.DataFrame({'x': x, 'y': y})

x = np.random.random(1000)
y = np.random.random(1000)
df2 = pd.DataFrame({'x': x, 'y': y})

ggplot(df, aes(x='x', y='y')) + geom_point() + geom_point(df2, aes(x='x', y='y', color='grey'), name="Ben") + theme_dark()


# %%


x = np.random.random(1000)
y = np.random.random(1000)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.random.random(1000)
y = np.random.random(1000)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y', color='category')) + geom_point()


# %%


x = np.random.random(1000)
y = np.random.random(1000)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.random.random(1000)
y = np.random.random(1000)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('category')


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})

ggplot(df, aes(x='x', y='y')) + geom_line(showlegend=True)


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})

ggplot(df, aes(x='x', y='y')) + geom_line() + geom_line(df2, aes(x='x', y='y', color='red'), name="Ben", showlegend=False)


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y', color='category')) + geom_line()


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y')) + geom_line() + facet_wrap('category')


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})

ggplot(df, aes(x='x', y='y')) + geom_area(showlegend=False)


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})

ggplot(df, aes(x='x', y='y')) + geom_area() + geom_area(df2, aes(x='x', y='y', color='red', fill='grey'), name="Ben", showlegend=False) + geom_point(df, aes(x='x', y='y', color="red", fill="red"), showlegend=False)


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y', color='category')) + geom_area()


# %%


x = np.linspace(0, 10, 100)
y = np.random.random(100)
df = pd.DataFrame({'x': x, 'y': y})
df['category'] = 'A'

x = np.linspace(0, 10, 100)
y = np.random.random(100)
df2 = pd.DataFrame({'x': x, 'y': y})
df2['category'] = 'B'

df = pd.concat([df, df2], axis=0)

ggplot(df, aes(x='x', y='y', color='category', fill='grey')) + geom_area()


# %%


# Step 2: Create a dictionary with more sample data
data = {
    'Category': ['A'] * 10 + ['B'] * 10 + ['C'] * 10 + ['D'] * 10 + ['E'] * 10,
    'Values': np.random.randn(50) * 10 + 50  # Random data for boxplot
}

# Step 3: Convert the dictionary to a Pandas DataFrame
df = pd.DataFrame(data)

# Step 4: Create a ggplot object
ggplot(df, aes(x='Category', y='Values')) + geom_boxplot()


# %%


# Step 2: Create a dictionary with more sample data
data = {
    'Category': ['A'] * 10 + ['B'] * 10 + ['C'] * 10 + ['D'] * 10 + ['E'] * 10,
    'Values': np.random.randn(50) * 10 + 50  # Random data for boxplot
}

# Step 3: Convert the dictionary to a Pandas DataFrame
df = pd.DataFrame(data)

# Step 4: Create a ggplot object
ggplot(df, aes(x='Category', y='Values', color="Category")) + geom_boxplot() + theme_dark()


# %%


ggplot(df, aes(x='Category', y='Values', color='red', fill='blue')) + geom_boxplot()


# %%


ggplot(df, aes(x='Category', y='Values', color='Category', fill='blue')) + geom_boxplot()


# %%


ggplot(df.groupby('Category').sum().reset_index(), aes(x='Category', y='Values')) + geom_bar(stat='identity')


# %%


np.random.seed(42)
data = pd.DataFrame({'x': np.random.randint(10, size=100)})
ggplot(data, aes(x='x')) + geom_bar() + stat_count()


# %%


np.random.seed(42)
data = {'x': np.random.randint(10, size=100)}
ggplot(data, aes(x='x')) + geom_bar() + geom_bar(data, aes(x='x', color='red'), name='Ben')


# %%


np.random.seed(42)
data = {'test': np.random.randint(10, size=100)}
ggplot(data, aes(y='test')) + geom_bar()


# %%


mpg_df=pd.read_csv('https://raw.githubusercontent.com/JetBrains/lets-plot-docs/master/data/mpg.csv')


# %%


ggplot(mpg_df, aes(x='class')) + \
    geom_bar(aes(color='class'), alpha=.8)


# %%


ggplot(mpg_df) + \
    geom_bar(aes(x='cyl', fill='drv'))
    # geom_bar(aes(x='cyl', fill='drv'), color='white', size=0.5)


# %%


ggplot(mpg_df) + \
    geom_bar(aes(x='cyl', fill='drv'), position='dodge')
    # geom_bar(aes(x='cyl', fill='drv'), color='white', size=0.5)


# %%


np.random.seed(42)
n = 10
x = np.arange(n)
y = 1 + np.random.randint(5, size=n)
df = pd.DataFrame({'x': x, 'y': y})
ggplot(df, aes(x='x', y='y')) + geom_bar(stat="mean")


# %%


import numpy as np

rng = np.random.RandomState(10)  # deterministic random data
a = np.hstack((rng.normal(size=1000),
               rng.normal(loc=5, scale=2, size=1000)))
a = pd.DataFrame({'x': a})

ggplot(a, aes(x='x', color="#FF00FF")) + geom_histogram()


# %%


np.random.seed(42)
n = 5000
x = np.random.normal(size=n)
c = np.random.choice(list('abcde'), size=n)

df = pd.DataFrame({'data': x, 'class': c})
ggplot(df, aes(x='data', color='class')) + geom_histogram(bin=36, alpha=0.5) + theme_bbc()


# %%


np.random.seed(42)
n = 5000
x = np.random.normal(size=n)
c = np.random.choice(list('abcde'), size=n)

df = pd.DataFrame({'data': x, 'class': c})
ggplot(df, aes(x='data', color='class')) + geom_histogram(bin=36, alpha=0.5) + theme_bbc() + geom_vline(data=2, color="blue") + geom_hline(data=100, color="red")


# %%


n = 10
np.random.seed(42)
x = np.arange(n)
ymin = np.random.randint(-5, 0, size=n)
ymax = np.random.randint(1, 6, size=n)

df = pd.DataFrame({'time': x, 'low': ymin, 'high': ymax})

ggplot(df, aes(x='time', ymin='low', ymax='high')) + geom_ribbon(alpha=0.1)


# %%


df = pd.read_csv("https://raw.githubusercontent.com/JetBrains/lets-plot-docs/master/data/gapminder.csv")
df.head()


# https://nextjournal.com/asmirnov-horis/bbc-visual-and-data-journalism-cookbook-for-lets-plot

# %%


line_df = df[df.country == "Malawi"]

ggplot(line_df, aes(x='year', y='lifeExp')) + \
    geom_line(color='green', size=1) + \
    scale_x_continuous(format='d') + \
    theme_bbc() + \
    ggsize(600, 450) + \
    labs(title="Living longer", subtitle="Life expectancy in Malawi 1952-2007")


# %%


line_df = df[df.country == "Malawi"]

ggplot(line_df, aes(x='year', y='lifeExp')) + \
    geom_line(color='#1380A1', size=25) + \
    scale_x_continuous(format='d') + \
    theme_bbc() + \
    theme(legend_position='bottom', legend_show=True) + \
    ggsize(600, 450) + \
    labs(title="Living longer", subtitle="Life expectancy in Malawi 1952-2007")


# %%


df


# %%


multiple_line_df = df[df.country.isin(["China", "United States"])]

multiple_line_plot = ggplot(multiple_line_df, aes(x='year', y='lifeExp', color='country')) + \
    geom_line(size=5) + \
    scale_x_continuous(format='d') + \
    theme_bbc() + \
    ggsize(600, 450) + \
    labs(title="Living longer", subtitle="Life expectancy in China and the US")
multiple_line_plot
    # scale_color_manual(values=['#FAAB18', '#1380A1']) + \


# %%


# Sample Data

df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})

# Create a plot with coord_flip
ggplot(df, aes(x='x', y='y')) + geom_point() + coord_flip()


# %%


(
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    labs(
        title='Main Title',
        subtitle='This is a subtitle',
        x='X-Axis',
        y='Y-Axis',
        caption='Data source: XYZ'
    ) +
    theme_minimal()
)


# %%


# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})

# Create Plot with Title
(
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    ggtitle('My Plot Title') +
    theme_minimal()
)


# %%


import pandas as pd

# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})

# Create Plot with Title
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    labs(title='My Plot Title', x='X-Axis Label', y='Y-Axis Label') +
    theme_minimal()
)

# Draw Plot
p.draw()


# %%


import pandas as pd
import numpy as np

# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)),
    'category': np.random.choice(['A', 'B'], 100)
})

# Area Plot with Faceting
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_area(fill='lightblue', alpha=0.5) +
    facet_wrap('category') +
    theme_minimal()
)
p.draw()


# %%


df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 15, 13, 17, 20]
})

# Create a plot with the NYTimes theme
(
    ggplot(df, aes(x='x', y='y')) +
    geom_line() +
    geom_point(size=10) +
    labs(title='GGPLOT2') +
    theme_ggplot2()  # Applying the NYT theme
)


# %%


df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [10, 15, 13, 17, 20]
})

# Create a plot with the NYTimes theme
(
    ggplot(df, aes(x='x', y='y')) +
    geom_line() +
    geom_point(size=10) +
    labs(title='New York Times Style Chart') +
    theme_nytimes()  # Applying the NYT theme
)


# %%


# Sample Data
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.randn(200),
    'y': np.random.randn(200),
    'category': np.random.choice(['A', 'B'], size=200)
})

# Create Plot with Faceting
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point(color='blue', alpha=0.5) +
    geom_smooth(method='loess', color='red') +
    facet_wrap('category', ncol=1) +
    theme_minimal()
)

# Draw Plot
p.draw()


# %%


# Sample Data
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})

# Create a plot with coord_flip
ggplot(df, aes(x='x', y='y')) + geom_point() + coord_flip() + ggsize(1000,1000) + ggsave("coord_flip.html")


# %%


# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 3, 5, 7, 11]
})

# Create Plot
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point(color='red', size=10) +
    geom_line() +
    scale_x_continuous(name='X-Axis') +
    theme_minimal()
)

# Draw Plot
p.draw()


# %%


df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [4, 5, 6]
})

# Create a plot with coord_flip
p = ggplot(df, aes(x='x', y='y')) + geom_point() + coord_flip()
p.draw()


# %%


# Testing geom_violin with faceting
df_violin = pd.DataFrame({
    'category': np.random.choice(['A', 'B'], 200),
    'value': np.random.randn(200)
})

p = (
    ggplot(df_violin, aes(x='category', y='value')) +
    geom_violin(fill='lightblue', color='black') +
    facet_wrap('category') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 1000),
    'y': np.sin(np.linspace(0, 10, 1000)),
    'category': np.random.choice(['A', 'B'], 1000),
    'sub_category': np.random.choice(['X', 'Y'], 1000)
})

# Area Plot with Grid Faceting
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_area(fill='lightblue', alpha=0.5) +
    facet_grid(rows='category', cols='sub_category') +  # Updated argument names
    theme_minimal()
)

# Draw Plot
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(scale=0.1, size=100)
})

# LOESS Example
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_smooth(method='loess', color='blue', alpha=0.6, linetype='solid') +
    theme_minimal()
)
p.draw()

# Linear Regression Example
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_smooth(method='lm', color='red', alpha=0.6, linetype='dash') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)),
    'category': np.random.choice(['A', 'B'], 100)
})

# Example Plot
p = (
    ggplot(df, aes(x='x', y='y', color='category')) +
    geom_line() +
    geom_point() +
    geom_smooth(method='loess') +
    facet_wrap('category') +
    theme_minimal()
)
p.draw()


# %%


mpg = pd.read_csv('https://raw.githubusercontent.com/tidyverse/ggplot2/main/data-raw/mpg.csv')

(
    ggplot(mpg, aes(x='displ', y='hwy')) + 
    geom_point() +
    geom_smooth(span=0.75, level=0.66)
)


# %%


# Sample Data
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.normal(size=100),
    'y': np.random.normal(size=100),
    'category': np.random.choice(['A', 'B'], size=100)
})

# Faceted Plot with geom_area and geom_density
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    geom_smooth(method='loess', span=0.75) +
    # geom_area(aes(y='y'), fill='lightblue', alpha=0.5) +
    geom_density(aes(x='x'), color='red') +
    facet_wrap('category') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data with Faceting
df_faceted = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'] * 2,
    'value': [10, 15, 12, 17, 8, 13, 11, 14],
    'group': ['G1']*4 + ['G2']*4
})

p = (
    ggplot(df_faceted, aes(x='category', y='value')) +
    geom_col(fill='orange', color='black') +
    facet_wrap('group') +
    theme_minimal()
)
p.draw()


# %%


df.category.describe()


# %%


import pandas as pd
import numpy as np

# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)),
    'category': np.random.choice(['A', 'B'], 100)
})

# Area Plot with Automatic Categorical Color Mapping
p = (
    ggplot(df, aes(x='x', y='y', fill='category', group='category')) +
    geom_area(alpha=0.5) +
    theme_minimal()
)

p.draw()



# %%


import pandas as pd
import numpy as np

# Sample Data
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [5, 10, 3, 7],
    'category': np.random.choice(['G1', 'G2'], 4)
})

# Bar Plot with Automatic Conversion and Color Mapping
p = (
    ggplot(df, aes(x='x', y='y', fill='category', group='category')) +
    geom_bar(alpha=0.7) +
    theme_minimal()
)

p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.random.choice(['A', 'B'], 100),
    'y': np.random.normal(size=100)
})

# Boxplot
p = (
    ggplot(df, aes(x='x', y='y', color='x')) +
    geom_boxplot(fill='lightblue') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [3, 7, 2, 5],
    'group': ['G1', 'G1', 'G2', 'G2']
})

# Column Plot
p = (
    ggplot(df, aes(x='x', y='y', fill='group', group='group')) +
    geom_col(alpha=0.7) +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': ['A', 'B', 'C', 'D'],
    'y': [5, 8, 3, 6],
    'ymin': [4, 7, 2, 5],
    'ymax': [6, 9, 4, 7]
})

# Error Bar Plot
p = (
    ggplot(df, aes(x='x', y='y', ymin='ymin', ymax='ymax')) +
    geom_errorbar() +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.random.normal(size=100)
})

# Histogram
p = (
    ggplot(df, aes(x='x')) +
    geom_histogram(fill='lightblue', alpha=0.7) +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'ymin': np.sin(np.linspace(0, 10, 100)) - 0.5,
    'ymax': np.sin(np.linspace(0, 10, 100)) + 0.5
})

# Ribbon Plot
p = (
    ggplot(df, aes(x='x', ymin='ymin', ymax='ymax')) +
    geom_ribbon(fill='grey', alpha=0.5) +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [4, 5, 6, 7],
    'xend': [2, 3, 4, 5],
    'yend': [6, 7, 8, 9]
})

# Segment Plot
p = (
    ggplot(df, aes(x='x', y='y', xend='xend', yend='yend')) +
    geom_segment(color='red', linetype='dash') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100))
})

# Step Plot
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_step(color='blue') +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.tile(np.arange(1, 11), 10),
    'y': np.repeat(np.arange(1, 11), 10),
    'z': np.random.randn(100)
})

# Tile Plot
(
    ggplot(df, aes(x='x', y='y', fill='z')) +
    geom_tile() +
    scale_fill_viridis_c() + 
    theme_minimal()
)


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.random.choice(['A', 'B'], 100),
    'y': np.random.normal(size=100)
})

# Violin Plot
p = (
    ggplot(df, aes(x='x', y='y', fill='x')) +
    geom_violin(alpha=0.5) +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'category': ['A', 'B', 'C', 'D'],
    'value': [10, 15, 12, 17]
})

# Basic Column Plot
p = ggplot(df, aes(x='category', y='value')) + geom_col()
p.draw()

# Column Plot with Custom Fill and Outline Colors
p = (
    ggplot(df, aes(x='category', y='value')) +
    geom_col(fill='skyblue', color='black') +
    theme_minimal()
)
p.draw()

# Column Plot with Grouping
df_grouped = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C', 'D', 'D'],
    'subgroup': ['X', 'Y'] * 4,
    'value': [5, 5, 8, 7, 6, 6, 9, 8]
})

p = (
    ggplot(df_grouped, aes(x='category', y='value', fill='subgroup')) +
    geom_col(position='dodge') +
    scale_fill_manual(values=['red', 'blue'], name='Subgroup') +
    theme_minimal()
)
p.draw()



# Stacked Bars (default)
p = (
    ggplot(df_grouped, aes(x='category', y='value', fill='subgroup')) +
    geom_col(position='stack')
)
p.draw()

# Side-by-Side Bars
p = (
    ggplot(df_grouped, aes(x='category', y='value', fill='subgroup')) +
    geom_col(position='dodge')
)
p.draw()


# %%


# Sample Data
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'size_var': np.random.rand(100) * 100
})

# Scatter Plot with Variable Point Sizes
p = (
    ggplot(df, aes(x='x', y='y', size='size_var')) +
    geom_point(color='blue', alpha=0.7) +
    scale_size(range=(2, 20), name='Variable Size')
)
p.draw()


# %%


# Sample Data
x = np.arange(0, 10, 1)
y = np.arange(0, 10, 1)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)
df = pd.DataFrame({
    'x': X.flatten(),
    'y': Y.flatten(),
    'z': Z.flatten()
})

# Heatmap with Gradient Fill
p = (
    ggplot(df, aes(x='x', y='y', fill='z')) +
    geom_tile() +
    scale_fill_gradient(low='blue', high='red', name='Intensity')
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)],
    'category': ['A']*5 + ['B']*5
})

# Plot with Manual Colors
p = (
    ggplot(df, aes(x='x', y='y', color='category')) +
    geom_point(size=10) +
    scale_color_manual(values=['red', 'blue'], name='Category', breaks=['A', 'B'], labels=['Group A', 'Group B'])
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': range(1, 11),
    'y': [i**2 for i in range(1, 11)]
})

# Customized Plot
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point(color='red', size=8) +
    scale_x_continuous(
        name='Custom X Axis',
        limits=(0, 12),
        breaks=[0, 3, 6, 9, 12],
        labels=['Zero', 'Three', 'Six', 'Nine', 'Twelve']
    ) +
    scale_y_continuous(
        name='Custom Y Axis',
        limits=(0, 120),
        breaks=[0, 20, 40, 60, 80, 100, 120],
        labels=['0', '20', '40', '60', '80', '100', '120']
    ) +
    theme_minimal()
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})

# Plot with Axis Limits
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    scale_x_continuous(limits=(2, 8)) +
    scale_y_continuous(limits=(0, 70))
)
p.draw()


# %%


# Custom Ticks and Labels
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    scale_x_continuous(
        breaks=[0, 2, 4, 6, 8, 10],
        labels=['zero', 'two', 'four', 'six', 'eight', 'ten']
    ) +
    scale_y_continuous(
        breaks=[0, 20, 40, 60, 80],
        labels=['0', 'Twenty', 'Forty', 'Sixty', 'Eighty']
    )
)
p.draw()


# %%


# Sample Data with Exponential Growth
df_log = pd.DataFrame({
    'x': np.linspace(1, 100, 100),
    'y': np.exp(np.linspace(0, 5, 100))
})

# Plot with Log Transformation
p = (
    ggplot(df_log, aes(x='x', y='y')) +
    geom_line() +
    scale_y_continuous(trans='log')
)
p.draw()


# %%


# Plot with Square Root Transformation
p = (
    ggplot(df, aes(x='x', y='y')) +
    geom_point() +
    scale_y_continuous(trans='sqrt')
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.random.normal(size=100)
})

# Histogram using stat_bin
p_hist = ggplot(df, aes(x='x')) + geom_histogram(bins=20)
p_hist.draw()

# Density Plot using stat_density
p_density = ggplot(df, aes(x='x')) + geom_density()
p_density.draw()

# Smoothed Line using stat_smooth
df_scatter = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)) + np.random.normal(scale=0.5, size=100)
})
p_smooth = ggplot(df_scatter, aes(x='x', y='y')) + geom_point() + geom_smooth(method='loess')
p_smooth.draw()

# ECDF using stat_ecdf
p_ecdf = ggplot(df, aes(x='x')) + geom_step(stat='ecdf')
p_ecdf.draw()


# %%


# Sample Data
np.random.seed(0)
df = pd.DataFrame({
    'x': np.random.randn(500),
    'y': np.random.randn(500) + np.arange(500) * 0.01,
    'category': np.random.choice(['A', 'B'], size=500)
})

# Histogram
p_hist = ggplot(df, aes(x='x')) + geom_histogram(bins=30, fill='blue', alpha=0.7)
p_hist.draw()

# Boxplot
p_box = ggplot(df, aes(x='category', y='y', fill='category')) + geom_boxplot()
p_box.draw()

# Scatter Plot with Smoothing Line
p_smooth = ggplot(df, aes(x='x', y='y')) + geom_point(alpha=0.5) + geom_smooth()
p_smooth.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(0, 10, 100),
    'y': np.sin(np.linspace(0, 10, 100)),
    'group': np.random.choice(['A', 'B'], 100)
})

# Basic Line Plot
p = ggplot(df, aes(x='x', y='y')) + geom_line()
p.draw()

# Line Plot with Points
p = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point()
p.draw()

# Line Plot with Grouping and Customization
p = (
    ggplot(df, aes(x='x', y='y', color='group', group='group')) +
    geom_line(size=2) +
    geom_point(size=4) +
    scale_color_manual(values=['blue', 'green'])
)
p.draw()


# %%


# Custom Line Color and Width
p = ggplot(df, aes(x='x', y='y')) + geom_line(color='red', size=3)
p.draw()

# Hiding Legend
p = ggplot(df, aes(x='x', y='y')) + geom_line(showlegend=False)
p.draw()

# Setting Custom Trace Name
p = ggplot(df, aes(x='x', y='y')) + geom_line(name='My Line')
p.draw()


# %%


# Introducing NaN values
df_with_nan = df.copy()
df_with_nan.loc[20:30, 'y'] = np.nan

# Line Plot with Missing Data
p = ggplot(df_with_nan, aes(x='x', y='y')) + geom_line()
p.draw()


# %%


# Adding Hover Information
p = ggplot(df, aes(x='x', y='y', text='group')) + geom_line()
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})

# Plot using theme_default
p_default = ggplot(df, aes(x='x', y='y')) + geom_point() + theme_default()
p_default.draw()

# Plot using theme_minimal
p_minimal = ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal()
p_minimal.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.arange(1, 21),
    'y': np.random.normal(size=20).cumsum(),
    'error': np.random.rand(20),  # yerr values
    'category': np.random.choice(['A', 'B'], 20),
    'label': [f'P{i}' for i in range(1, 21)]
})

# Advanced Plot
p = (
    ggplot(df, aes(x='x', y='y', color='category')) +
    geom_line() +
    geom_point(size=5) +
    geom_errorbar(aes(yerr='error'), width=0.2) +  # Error bars using the 'error' column (yerr)
    geom_text(aes(label='label'), textposition='top center') +
    scale_color_brewer(type='qual', palette='Set1') +
    theme_custom(
        background_color='lightgrey',
        grid_color='white',
        text_color='black'
    ) +
    labs(
        title='Advanced Plot',
        x='X-axis',
        y='Y-axis',
        color='Category Legend Title',  # Sets the legend title for the color aesthetic
        caption='This is a caption'
    ) +
    coord_cartesian(xlim=(0, 25), ylim=(-5, 10))
)
p.draw()


# %%





# %%


# Sample Data
df = pd.DataFrame({
    'x': np.arange(1, 21),
    'y': np.random.normal(size=20).cumsum(),
    'error': np.random.rand(20),
    'category': np.random.choice(['A', 'B'], 20),
    'label': [f'P{i}' for i in range(1, 21)]
})

# Advanced Plot
p = (
    ggplot(df, aes(x='x', y='y', color='category')) +
    geom_line() +
    geom_point(size=5) +
    geom_errorbar(aes(yerr='error'), width=0.2) +
    geom_text(aes(label='label'), textposition='top center') +
    scale_color_brewer(type='qual', palette='Set1') +
    theme_custom(
        background_color='lightgrey',
        grid_color='white',
        text_color='black'
    ) +
    labs(
        title='Advanced Plot',
        x='X-axis',
        y='Y-axis',
        color='Category'
    ) +
    facet_wrap('category', ncol=1) +
    coord_cartesian(xlim=(0, 25), ylim=(-5, 10))
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.arange(1, 21),
    'y': np.random.normal(size=20).cumsum(),
    'error': np.random.rand(20),
    'category': np.random.choice(['A', 'B'], 20),
    'label': [f'P{i}' for i in range(1, 21)]
})

# Advanced Plot
p = (
    ggplot(df, aes(x='x', y='y', color='category')) +
    geom_line() +
    geom_point(size=5) +
    geom_errorbar(aes(yerr='error'), width=0.2) +
    geom_text(aes(label='label'), vjust=-1) +
    scale_color_brewer(type='qual', palette='Set1') +
    theme_custom(
        background_color='lightgrey',
        grid_color='white',
        text_color='black'
    ) +
    labs(
        title='Advanced Plot',
        x='X-axis',
        y='Y-axis',
        color='Category'
    ) +
    facet_wrap('category', ncol=1) +
    coord_cartesian(xlim=(0, 25), ylim=(-5, 10))
)
p.draw()


# %%


# Sample Data
df = pd.DataFrame({
    'x': np.linspace(1, 100, 100),
    'y': np.random.randn(100).cumsum(),
    'category': np.random.choice(['A', 'B', 'C'], 100),
    'group': np.random.choice(['G1', 'G2'], 100),
    'size': np.random.rand(100) * 20,
    'alpha': np.random.rand(100),
    'fill_value': np.random.rand(100)
})

# Complex Plot
p = (
    ggplot(df, aes(x='x', y='y', color='category', size='size', alpha='alpha')) +
    geom_point() +
    geom_line(aes(group='group')) +
    geom_area(aes(fill='fill_value'), alpha=0.3) +
    scale_x_log10() +
    scale_y_continuous(limits=(-20, 20)) +
    scale_color_gradient(low='blue', high='red') +
    scale_fill_gradient(low='yellow', high='green') +
    theme_dark() +
    facet_grid(rows='group', cols='category') +
    coord_flip()
)
p.draw()

# Save to HTML
p.save('complex_plot.html')


# %%


p


# %%


# Save to HTML
p.save('plot_extended.html')


# %%


# Sample Data
df = pd.DataFrame({
    'x': range(10),
    'y': [i**2 for i in range(10)]
})

# Plot
p = ggplot(df, aes(x='x', y='y')) + geom_point() + geom_line()
p.draw()

# Save to HTML
p.save('plot.html')


# %%


p


# # geom_range - 5-Year Range Plots

# %%


# Create data from 2019 through June 2025
# Current year: 2025, Prior year: 2024, Historical range: 2019-2024
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')

temperatures = []
for date in dates:
    # Base seasonal pattern (warmer in summer)
    seasonal = 55 + 25 * np.sin(2 * np.pi * (date.dayofyear - 80) / 365)
    # Year-over-year warming trend
    trend = (date.year - 2019) * 0.5
    # Random daily variation
    noise = np.random.randn() * 20
    temperatures.append(seasonal + trend + noise)

df_temp = pd.DataFrame({
    'date': dates,
    'temperature': temperatures
})

print(f"Data: {len(df_temp)} rows from {df_temp['date'].min().date()} to {df_temp['date'].max().date()}")
print(f"Years: {sorted(df_temp['date'].dt.year.unique())}")
df_temp.head()


# %%


# Basic 5-year range plot with monthly aggregation
# Shows: gray ribbon (5-year min/max), black dotted line (5-year avg), 
#        blue line (prior year), red line (current year)
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='ME') +
    labs(title='Temperature: 5-Year Historical Range',
         subtitle='Current year (red) vs historical context',
         x='Month', y='Temperature (°F)')
)


# %%


# Weekly aggregation ending on Friday (pandas freq string)
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='W-Fri') +
    labs(title='Temperature: Weekly (Friday) Aggregation',
         x='Week', y='Temperature (°F)')
)


# %%


# Show additional specific years (2020, 2021) alongside current/prior
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='ME', show_years=[2020, 2021]) +
    labs(title='Temperature Comparison: Multiple Years',
         subtitle='2020 (green) and 2021 (purple) highlighted',
         x='Month', y='Temperature (°F)')
)


# %%


# Custom colors and styling
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(
        freq='ME',
        current_color='darkgreen',
        prior_color='orange', 
        avg_color='navy',
        ribbon_alpha=0.2
    ) +
    labs(title='Temperature Range - Custom Styling',
         x='Month', y='Temperature (°F)')
)


# ## Real-World Use Case: Energy Demand
# 
# A common use case for range plots is comparing current energy/resource consumption against historical patterns.

# %%


# Simulate energy demand data with realistic patterns
np.random.seed(457)
energy_dates = pd.date_range('2018-01-01', '2024-11-30', freq='D')

energy_demand = []
for date in energy_dates:
    # Base load
    base = 5000
    # Seasonal pattern (higher in summer/winter for HVAC)
    seasonal = 1500 * np.cos(2 * np.pi * (date.dayofyear - 200) / 365) ** 2
    # Weekly pattern (lower on weekends)
    weekend_factor = 0.7 if date.dayofweek >= 5 else 1.0
    # Year-over-year growth
    growth = (date.year - 2018) * 100
    # Random variation
    noise = np.random.randn() * 200
    energy_demand.append((base + seasonal + growth + noise) * weekend_factor)

df_energy = pd.DataFrame({
    'date': energy_dates,
    'demand_mwh': energy_demand
})

# Weekly ending Friday for energy reporting
(
    ggplot(df_energy, aes(x='date', y='demand_mwh')) +
    geom_range(freq='W-Fri', ribbon_alpha=0.25) +
    labs(title='Weekly Energy Demand: Current vs Historical',
         subtitle='5-year historical range with current year highlighted',
         x='Week', y='Demand (MWh)') +
    theme_minimal()
)


# ## Various Pandas Frequency Strings
# 
# `geom_range` supports all pandas frequency strings: `D`, `W`, `W-Fri`, `ME`, `MS`, `QE`, `2W`, etc.

# %%


# Bi-weekly aggregation
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='2W') +
    labs(title='Temperature: Bi-Weekly Aggregation',
         x='Bi-Week', y='Temperature (°F)')
)


# %%


# Quarterly aggregation
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='QE') +
    labs(title='Temperature: Quarterly Aggregation',
         x='Quarter', y='Temperature (°F)')
)


# %%


# Create data with DatetimeIndex (auto-detects freq from index)
np.random.seed(123)
weekly_dates = pd.date_range('2019-01-04', '2024-12-13', freq='W-Fri')
weekly_sales = 1000 + 200 * np.sin(2 * np.pi * np.arange(len(weekly_dates)) / 52) + np.random.randn(len(weekly_dates)) * 50

df_sales = pd.DataFrame({'sales': weekly_sales}, index=weekly_dates)
print(f"Index type: {type(df_sales.index).__name__}")
print(f"Index freq: {df_sales.index.freq}")
df_sales.head()


# %%


# Auto-detect datetime in index - no x aesthetic needed!
# Frequency is automatically detected from the DatetimeIndex.freq attribute
(
    ggplot(df_sales, aes(y='sales')) +
    geom_range() +
    labs(title='Weekly Sales: 5-Year Range (Auto-Detected Freq)',
         subtitle='DatetimeIndex with freq=W-Fri',
         x='Week', y='Sales ($)')
)


# ## DatetimeIndex Support
# 
# `geom_range` can auto-detect datetime in the DataFrame index and infer frequency from index attributes.

# %%


# 3-year range instead of default 5-year
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='ME', years=3) +
    labs(title='Temperature: 3-Year Historical Range',
         subtitle='Shorter historical window',
         x='Month', y='Temperature (°F)')
)


# %%


# View historical year as "current" (e.g., analyze 2022)
(
    ggplot(df_temp, aes(x='date', y='temperature')) +
    geom_range(freq='ME', current_year=2022) +
    labs(title='Temperature in 2022 vs 5-Year History',
         subtitle='Viewing 2022 as the "current" year',
         x='Month', y='Temperature (°F)')
)


# %%


# geom_range with facets - compare multiple regions/categories
np.random.seed(789)

# Create temperature data for multiple cities
cities = ['New York', 'Los Angeles', 'Chicago']
city_data = []

for city in cities:
    dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
    # Different base temperatures and patterns per city
    base_temp = {'New York': 50, 'Los Angeles': 65, 'Chicago': 45}[city]
    amplitude = {'New York': 30, 'Los Angeles': 15, 'Chicago': 35}[city]

    for date in dates:
        seasonal = base_temp + amplitude * np.sin(2 * np.pi * (date.dayofyear - 80) / 365)
        trend = (date.year - 2019) * 0.3
        noise = np.random.randn() * 15
        city_data.append({
            'date': date,
            'temperature': seasonal + trend + noise,
            'city': city
        })

df_cities = pd.DataFrame(city_data)

# Faceted range plot by city
(
    ggplot(df_cities, aes(x='date', y='temperature')) +
    geom_range(freq='ME') +
    facet_wrap('city', nrow=1) +
    labs(title='Temperature: 5-Year Range by City',
         subtitle='Comparing seasonal patterns across locations',
         x='Month', y='Temperature (°F)') +
    theme_minimal()
)


# %%


np.random.seed(789)

# Create temperature data for multiple cities
cities = ['New York', 'Los Angeles', 'Chicago']
city_data = []

for city in cities:
    dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
    # Different base temperatures and patterns per city
    base_temp = {'New York': 50, 'Los Angeles': 65, 'Chicago': 45}[city]
    amplitude = {'New York': 30, 'Los Angeles': 15, 'Chicago': 35}[city]

    for date in dates:
        seasonal = base_temp + amplitude * np.sin(2 * np.pi * (date.dayofyear - 80) / 365)
        trend = (date.year - 2019) * 0.3
        noise = np.random.randn() * 15
        city_data.append({
            'date': date,
            'temperature': seasonal + trend + noise,
            'city': city
        })

df_cities = pd.DataFrame(city_data)

# Faceted range plot by city
(
    ggplot(df_cities, aes(x='date', y='temperature')) +
    geom_range(freq='ME') +
    facet_wrap('city', nrow=1) +
    labs(title='Temperature: 5-Year Range by City',
         subtitle='Comparing seasonal patterns across locations',
         x='Month', y='Temperature (°F)') +
    theme_minimal()
)

# %%