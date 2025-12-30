# %%
%load_ext autoreload
%autoreload 2
import os
import sys

from ggplotly import *
import pandas as pd
import numpy as np

# %%
# Create sample data: US states with population (millions)
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI',
              'CO', 'MN', 'SC', 'AL', 'LA', 'KY', 'OR', 'OK', 'CT', 'UT',
              'IA', 'NV', 'AR', 'MS', 'KS', 'NM', 'NE', 'ID', 'WV', 'HI',
              'NH', 'ME', 'MT', 'RI', 'DE', 'SD', 'ND', 'AK', 'VT', 'WY', 'DC'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0,
                   9.3, 8.6, 7.6, 7.3, 7.0, 6.9, 6.8, 6.2, 6.2, 5.9,
                   5.8, 5.7, 5.1, 5.0, 4.7, 4.5, 4.2, 4.0, 3.6, 3.3,
                   3.2, 3.1, 3.0, 3.0, 2.9, 2.1, 2.0, 1.9, 1.8, 1.4,
                   1.4, 1.4, 1.1, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.6, 0.7]
})

# Get the map data
states = map_data('state')

# Create the choropleth map
(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues'))

# %%
# State data for choropleth
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI',
              'NJ', 'VA', 'WA', 'AZ', 'MA', 'TN', 'IN', 'MO', 'MD', 'WI',
              'CO', 'MN', 'SC', 'AL', 'LA', 'KY', 'OR', 'OK', 'CT', 'UT',
              'IA', 'NV', 'AR', 'MS', 'KS', 'NM', 'NE', 'ID', 'WV', 'HI',
              'NH', 'ME', 'MT', 'RI', 'DE', 'SD', 'ND', 'AK', 'VT', 'WY', 'DC'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0,
                   9.3, 8.6, 7.6, 7.3, 7.0, 6.9, 6.8, 6.2, 6.2, 5.9,
                   5.8, 5.7, 5.1, 5.0, 4.7, 4.5, 4.2, 4.0, 3.6, 3.3,
                   3.2, 3.1, 3.0, 3.0, 2.9, 2.1, 2.0, 1.9, 1.8, 1.4,
                   1.4, 1.4, 1.1, 1.1, 1.0, 0.9, 0.8, 0.7, 0.6, 0.6, 0.7]
})

# City data for points
cities = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
             'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'Austin',
             'San Francisco', 'Seattle', 'Denver', 'Boston', 'Miami'],
    'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484,
            39.9526, 29.4241, 32.7157, 32.7767, 30.2672,
            37.7749, 47.6062, 39.7392, 42.3601, 25.7617],
    'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740,
            -75.1652, -98.4936, -117.1611, -96.7970, -97.7431,
            -122.4194, -122.3321, -104.9903, -71.0589, -80.1918],
    'pop_millions': [8.3, 3.9, 2.7, 2.3, 1.6, 1.6, 1.5, 1.4, 1.3, 1.0, 0.9, 0.7, 0.7, 0.7, 0.5]
})

# Get map data
states = map_data('state')

# Layer geom_map + geom_point (ggplot2 style!)
# In ggplot2: geom_point(data=cities, aes(x=lon, y=lat))
p = (ggplot(state_data, aes(map_id='state', fill='population'))
     + geom_map(map=states, palette='Blues')
     + geom_point(cities, aes(x='lon', y='lat', size='pop_millions'), color='red'))

p.draw()

# %%
import pandas as pd
from ggplotly import ggplot, aes, geom_map, geom_point, map_data

# State data for choropleth - FULL DATA, no ellipsis!
state_data = pd.DataFrame({
    'state': ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'],
    'population': [39.5, 29.0, 21.5, 19.5, 13.0, 12.8, 11.8, 10.7, 10.4, 10.0]
})

# City data for points - FULL DATA, no ellipsis!
cities = pd.DataFrame({
    'city': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
    'lat': [40.7128, 34.0522, 41.8781, 29.7604, 33.4484],
    'lon': [-74.0060, -118.2437, -87.6298, -95.3698, -112.0740],
    'pop_millions': [8.3, 3.9, 2.7, 2.3, 1.6]
})

# Get map data
states = map_data('state')

# Layer geom_map + geom_point (ggplot2 style!)
(ggplot(state_data, aes(map_id='state', fill='population'))
 + geom_map(map=states, palette='Blues')
 + geom_point(cities, aes(x='lon', y='lat', size='pop_millions'), color='red'))

# %%
import pandas as pd
from ggplotly import *

# Country GDP data
country_data = pd.DataFrame({
    'country': ['USA', 'CHN', 'JPN', 'DEU', 'GBR', 'IND', 'FRA', 'ITA', 'CAN', 'KOR',
                'RUS', 'BRA', 'AUS', 'ESP', 'MEX'],
    'gdp_trillion': [25.5, 18.3, 4.2, 4.1, 3.1, 3.4, 2.8, 2.0, 2.1, 1.7,
                    2.2, 1.9, 1.7, 1.4, 1.3]
})

# Major world cities
cities = pd.DataFrame({
    'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Dubai',
             'Singapore', 'Hong Kong', 'Mumbai', 'São Paulo', 'Toronto', 'Berlin'],
    'lat': [40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 25.2048,
            1.3521, 22.3193, 19.0760, -23.5505, 43.6532, 52.5200],
    'lon': [-74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 55.2708,
            103.8198, 114.1694, 72.8777, -46.6333, -79.3832, 13.4050],
    'population_millions': [8.3, 9.0, 13.9, 2.2, 5.3, 3.3, 5.7, 7.5, 20.7, 12.3, 2.9, 3.6]
})

# Get world map data
countries = map_data('world')

# Layer geom_map + geom_point for world map
p = (ggplot(country_data, aes(map_id='country', fill='gdp_trillion'))
     + geom_map(map=countries, map_type='world', palette='Viridis')
     + geom_point(cities, aes(x='lon', y='lat', size='population_millions'), color='red', alpha=0.7))
p

# %%
# Create USArrests-like data (R's USArrests dataset)
# Data from https://stat.ethz.ch/R-manual/R-devel/library/datasets/html/USArrests.html
us_arrests = pd.DataFrame({
    'state': ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
              'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
              'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
              'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
              'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
    'Murder': [13.2, 10.0, 8.1, 8.8, 9.0, 7.9, 3.3, 5.9, 15.4, 17.4,
               5.3, 2.6, 10.4, 7.2, 2.2, 6.0, 9.7, 15.4, 2.1, 11.3,
               4.4, 12.1, 2.7, 16.1, 9.0, 6.0, 4.3, 12.2, 2.1, 7.4,
               11.4, 11.1, 13.0, 0.8, 7.3, 6.6, 4.9, 6.3, 3.4, 14.4,
               3.8, 13.2, 12.7, 3.2, 2.2, 8.5, 4.0, 5.7, 2.6, 6.8],
    'Assault': [236, 263, 294, 190, 276, 204, 110, 238, 335, 211,
                46, 120, 249, 113, 56, 115, 109, 249, 83, 300,
                149, 255, 72, 259, 178, 109, 102, 252, 57, 159,
                285, 254, 337, 45, 120, 151, 159, 106, 174, 279,
                86, 188, 201, 120, 48, 156, 145, 81, 53, 161],
    'UrbanPop': [58, 48, 80, 50, 91, 78, 77, 72, 80, 60,
                 83, 54, 83, 65, 57, 66, 52, 66, 51, 67,
                 85, 74, 66, 44, 70, 53, 62, 81, 56, 89,
                 70, 86, 45, 44, 75, 68, 67, 72, 87, 48,
                 45, 59, 80, 80, 32, 63, 73, 39, 66, 60],
    'Rape': [21.2, 44.5, 31.0, 19.5, 40.6, 38.7, 11.1, 15.8, 31.9, 25.8,
             20.2, 14.2, 24.0, 21.0, 11.3, 18.0, 16.3, 22.2, 7.8, 27.8,
             16.3, 35.1, 14.9, 17.1, 28.2, 16.4, 16.5, 46.0, 9.5, 18.8,
             32.1, 26.1, 16.1, 7.3, 21.4, 20.0, 29.3, 14.9, 8.3, 22.5,
             12.8, 26.9, 25.5, 22.9, 11.2, 20.7, 26.2, 9.3, 10.8, 15.6]
})

# %%
states_map = map_data('state')

(
    ggplot(us_arrests, aes(map_id='state', fill='Murder'))
    + geom_map(map=states_map, palette='Reds')
    + labs(title='Murder Arrests per 100,000 (1973)')
)

# %%
# Pivot data to long format
crimes_long = pd.melt(
    us_arrests,
    id_vars=['state'],
    value_vars=['Murder', 'Assault', 'UrbanPop', 'Rape'],
    var_name='variable',
    value_name='value'
)

# Create faceted map
(
    ggplot(crimes_long, aes(map_id='state', fill='value'))
    + geom_map(map=states_map, palette='Reds')
    + facet_wrap('variable', ncol=2)
    + labs(title='US Arrests Statistics (1973)')
)

# %%
import math

t_vals = [i * 4 * math.pi / 100 for i in range(100)]
spiral = pd.DataFrame({
    'x': [t * math.cos(t) for t in t_vals],
    'y': [t * math.sin(t) for t in t_vals],
})

(ggplot(spiral, aes(x='x', y='y'))
 + geom_path(color='steelblue', size=2)
 + labs(title='Spiral with geom_path (correct)'))

# %%
# Same spiral with geom_line - WRONG! (sorts by x, breaks the spiral)
(ggplot(spiral, aes(x='x', y='y'))
 + geom_line(color='red', size=2)
 + labs(title='Spiral with geom_line (wrong - sorted by x)'))

# %%
# Example 2: Connected scatterplot (Gapminder-style)
# GDP vs Life Expectancy over time - trace each country's trajectory

gapminder = pd.DataFrame({
    'country': ['USA']*5 + ['China']*5 + ['Brazil']*5,
    'year': [1960, 1980, 2000, 2010, 2020] * 3,
    'gdp': [3007, 12575, 36330, 48468, 63028,    # USA
            90, 195, 959, 4550, 10500,            # China
            210, 1947, 3749, 11286, 6797],        # Brazil
    'life_exp': [69.8, 73.7, 76.6, 78.5, 77.0,   # USA
                 43.7, 66.8, 71.4, 75.0, 77.1,   # China
                 54.7, 62.7, 70.3, 73.1, 75.9]   # Brazil
})

(ggplot(gapminder, aes(x='gdp', y='life_exp', color='country'))
 + geom_path(size=2)
 + geom_point(size=8)
 + labs(title='GDP vs Life Expectancy Over Time',
        x='GDP per Capita (USD)', y='Life Expectancy'))

# %%
# Example 3: Draw a star shape
points = 5
outer_r, inner_r = 1, 0.4
star_x, star_y = [], []
for i in range(points * 2 + 1):
    angle = i * math.pi / points - math.pi / 2
    r = outer_r if i % 2 == 0 else inner_r
    star_x.append(r * math.cos(angle))
    star_y.append(r * math.sin(angle))

star = pd.DataFrame({'x': star_x, 'y': star_y})

(ggplot(star, aes(x='x', y='y'))
 + geom_path(color='gold', size=3)
 + labs(title='Star drawn with geom_path'))

# %%
# scale_x_date - Date axis formatting

# Monthly time series data
dates = pd.date_range('2020-01-01', periods=24, freq='ME')
ts_data = pd.DataFrame({
    'date': dates,
    'value': [10 + i*0.5 + np.random.randn()*2 for i in range(24)]
})

(ggplot(ts_data, aes(x='date', y='value'))
 + geom_line(color='steelblue', size=2)
 + geom_point(size=5)
 + scale_x_date(date_breaks='3 months', date_labels='%b %Y')
 + labs(title='Time Series with scale_x_date', x='Date', y='Value'))

# %%
# annotate() - Add text, shapes, arrows to plots

# Scatter data
np.random.seed(42)
scatter_data = pd.DataFrame({
    'x': np.random.randn(50),
    'y': np.random.randn(50)
})
# Add an outlier
scatter_data.loc[50] = [3, 3]

(ggplot(scatter_data, aes(x='x', y='y'))
 + geom_point(size=6, alpha=0.6)
 + annotate('text', x=3, y=3.5, label='Outlier!', size=14, color='red')
 + annotate('rect', xmin=-1, xmax=1, ymin=-1, ymax=1, fill='lightblue', alpha=0.3)
 + annotate('text', x=0, y=0, label='Main cluster', size=12, color='blue')
 + labs(title='Scatter Plot with Annotations'))

# %%
# Arrow annotation pointing to peak
peak_data = pd.DataFrame({
    'x': range(10),
    'y': [1, 3, 2, 5, 8, 6, 4, 3, 2, 1]
})

(ggplot(peak_data, aes(x='x', y='y'))
 + geom_line(size=2, color='steelblue')
 + geom_point(size=8)
 + annotate('segment', x=6, y=9, xend=4, yend=8.2, arrow=True, color='red', size=2)
 + annotate('text', x=6, y=9.5, label='Peak value', size=12, color='red')
 + labs(title='With Arrow Annotation'))
