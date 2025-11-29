"""
Example usage of geom_range for 5-year range plots.

This demonstrates how to create plots showing:
- 5-year historical min/max as a ribbon
- 5-year historical average as a dotted line
- Prior year as a blue line
- Current year as a red line
"""

import pandas as pd
import numpy as np
from datetime import datetime

import sys
sys.path.insert(0, '/Users/ben/Projects/ggplotly')

from ggplotly import ggplot, aes, geom_range, labs


# Create sample data - 6 years of daily temperature data
np.random.seed(42)
dates = pd.date_range('2019-01-01', '2024-12-15', freq='D')

# Create realistic seasonal temperature pattern
temperatures = []
for date in dates:
    # Base seasonal pattern (warmer in summer)
    seasonal = 55 + 25 * np.sin(2 * np.pi * (date.dayofyear - 80) / 365)
    # Year-over-year warming trend
    trend = (date.year - 2019) * 0.5
    # Random daily variation
    noise = np.random.randn() * 8
    temperatures.append(seasonal + trend + noise)

df = pd.DataFrame({
    'date': dates,
    'temperature': temperatures
})

print("Sample data shape:", df.shape)
print(df.head())

# Basic 5-year range plot
print("\n--- Basic 5-Year Range Plot ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range()
     + labs(title='Temperature: 5-Year Historical Range',
            x='Date', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_basic.html')
print("Saved to range_basic.html")


# Monthly aggregation
print("\n--- Monthly Frequency ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range(freq='M')
     + labs(title='Temperature: Monthly 5-Year Range',
            x='Month', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_monthly.html')
print("Saved to range_monthly.html")


# Show additional specific years
print("\n--- With Additional Years ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range(show_years=[2020, 2021], freq='M')
     + labs(title='Temperature Comparison: Multiple Years',
            subtitle='2020 and 2021 highlighted alongside current/prior year',
            x='Month', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_multi_year.html')
print("Saved to range_multi_year.html")


# Custom colors
print("\n--- Custom Colors ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range(
         freq='M',
         current_color='darkgreen',
         prior_color='orange',
         avg_color='navy',
         ribbon_alpha=0.2
     )
     + labs(title='Temperature Range - Custom Styling',
            x='Month', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_custom.html')
print("Saved to range_custom.html")


# 3-year range instead of 5-year
print("\n--- 3-Year Range ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range(years=3, freq='M')
     + labs(title='Temperature: 3-Year Historical Range',
            x='Month', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_3year.html')
print("Saved to range_3year.html")


# Specify a different "current" year
print("\n--- Historical View (2022 as current) ---")
p = (ggplot(df, aes(x='date', y='temperature'))
     + geom_range(current_year=2022, freq='M')
     + labs(title='Temperature in 2022 vs 5-Year History',
            subtitle='Viewing 2022 as the "current" year',
            x='Month', y='Temperature (°F)'))
fig = p.draw()
fig.write_html('/Users/ben/Projects/ggplotly/examples/range_historical.html')
print("Saved to range_historical.html")


print("\n✓ All examples generated successfully!")
