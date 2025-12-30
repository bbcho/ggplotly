# %%
%load_ext autoreload
%autoreload 2

# Cell 1 - Setup
import pandas as pd
import numpy as np
from ggplotly import *

# Cell 2 - Basic scatter with xlim/ylim
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B', 'C'], 100)
})

# %%
(ggplot(df, aes(x='x', y='y', color='group')) +
 geom_point() +
 xlim(-2, 0) +
 ylim(-2, 4) +
 labs(title='Scatter with axis limits'))

# %%
# Cell 3 - Using lims() for both axes
(ggplot(df, aes(x='x', y='y', color='group')) +
 geom_point() +
 lims(x=(-8, 3), y=(-3, 5)) +
 labs(title='Using lims()'))

# %%
# Cell 4 - geom_range example (5-year historical)
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
temps = []
for d in dates:
    seasonal = 55 + 25 * np.sin(2 * np.pi * (d.dayofyear - 80) / 365)
    trend = (d.year - 2019) * 0.5
    noise = np.random.randn() * 15
    temps.append(seasonal + trend + noise)

df_temp = pd.DataFrame({'date': dates, 'temperature': temps})

(ggplot(df_temp, aes(x='date', y='temperature')) +
 geom_range(freq='ME') +
 labs(title='Temperature: 5-Year Historical Range',
      x='Month', y='Temperature (°F)') +
 theme_minimal())

# Cell 5 - geom_smooth with confidence band
(ggplot(df, aes(x='x', y='y')) +
 geom_point(alpha=0.5) +
 geom_smooth(method='loess', se=True) +
 labs(title='Scatter with LOESS smooth'))

# Cell 6 - Faceted plot
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_wrap('group') +
 labs(title='Faceted by group'))

# %%
%load_ext autoreload
%autoreload 2


# Cell 1 - Setup
import pandas as pd
import numpy as np
from ggplotly import *

# %%
# Cell 2 - Create test data
np.random.seed(42)

# Data with different ranges per group (for testing space parameter)
df = pd.DataFrame({
    'x': np.concatenate([
        np.random.uniform(0, 10, 50),    # Group A: x range 0-10
        np.random.uniform(0, 50, 50),    # Group B: x range 0-50
        np.random.uniform(0, 100, 50),   # Group C: x range 0-100
    ]),
    'y': np.concatenate([
        np.random.uniform(0, 5, 50),     # Group A: y range 0-5
        np.random.uniform(0, 20, 50),    # Group B: y range 0-20
        np.random.uniform(0, 50, 50),    # Group C: y range 0-50
    ]),
    'group': ['A']*50 + ['B']*50 + ['C']*50,
    'category': np.random.choice(['X', 'Y'], 150)
})

# %%
# Cell 3 - facet_wrap: default (dir='h')
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_wrap('group', ncol=2) +
 labs(title='facet_wrap: dir="h" (default)'))

# %%
df

# %%
# Cell 3 - facet_wrap: default (dir='h')
(ggplot(df, aes(x='x', y='y', color='group')) +
 geom_point() +
 facet_wrap('group', ncol=2) +
 labs(title='facet_wrap: dir="h" (default)'))

# %%
# Cell 4 - facet_wrap: vertical direction
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_wrap('group', nrow=3, dir='v') +
 labs(title='facet_wrap: dir="v" (vertical)'))

# %%
# Cell 5 - facet_wrap: labeller='both'
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_wrap('group', labeller='both') +
 labs(title='facet_wrap: labeller="both"'))

# %%
# Cell 6 - facet_wrap: custom labeller
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_wrap('group', labeller=lambda var, val: f'Panel {val}') +
 labs(title='facet_wrap: custom labeller'))

# %%
# Cell 7 - facet_grid: default (space='fixed')
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_grid('group', 'category') +
 labs(title='facet_grid: space="fixed" (default)'))

# %%
# Cell 8 - facet_grid: space='free' (proportional sizing)
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_grid('group', 'category', space='free') +
 labs(title='facet_grid: space="free" (proportional to data range)'))

# %%
# Cell 9 - facet_grid: space='free_x'
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_grid('group', 'category', space='free_x') +
 labs(title='facet_grid: space="free_x"'))

# %%
# Cell 10 - facet_grid: labeller='both'
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_grid('group', 'category', labeller='both') +
 labs(title='facet_grid: labeller="both"'))

# %%
# Cell 11 - Combining scales and space
(ggplot(df, aes(x='x', y='y')) +
 geom_point() +
 facet_grid('group', 'category', scales='free', space='free') +
 labs(title='facet_grid: scales="free" + space="free"'))

# %%
# Cell 12 - geom_range with facets (from earlier)
np.random.seed(789)
cities = ['New York', 'Los Angeles', 'Chicago']
city_data = []

for city in cities:
    dates = pd.date_range('2019-01-01', '2025-06-15', freq='D')
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

(ggplot(df_cities, aes(x='date', y='temperature')) +
 geom_range(freq='ME') +
 facet_wrap('city', nrow=1) +
 labs(title='geom_range with facets (shared y-axis)') +
 theme_minimal())

# %%
# Cell 13 - xlim/ylim test
(ggplot(df, aes(x='x', y='y', color='group')) +
 geom_point() +
 xlim(0, 50) +
 ylim(0, 25) +
 labs(title='xlim(0, 50) + ylim(0, 25)'))
