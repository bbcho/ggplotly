# Datasets API Reference

Built-in datasets for ggplotly, mirroring those available in ggplot2.

## Loading Datasets

::: ggplotly.datasets.data
    options:
      show_root_heading: true

## Map Data

::: ggplotly.map_data.map_data
    options:
      show_root_heading: true

## Available Datasets

The following datasets are included with ggplotly:

| Dataset | Description |
|---------|-------------|
| `mpg` | Fuel economy data for 234 cars (1999-2008) |
| `diamonds` | Prices and attributes of ~54,000 diamonds |
| `iris` | Classic Fisher's iris flower measurements |
| `mtcars` | Motor Trend car road tests (1974) |
| `economics` | US economic time series data |
| `economics_long` | Long format US economic time series |
| `midwest` | Midwest demographics data |
| `txhousing` | Texas housing market data |
| `faithfuld` | Old Faithful geyser eruption data (2D density) |
| `msleep` | Mammalian sleep data |
| `presidential` | US presidential terms |
| `seals` | Location data for seal movements |
| `commodity_prices` | Historical commodity price data |
| `luv_colours` | Color data in LUV color space |
| `us_flights` | US flight network (returns igraph Graph) |

### Example Usage

```python
from ggplotly import data

# List all available datasets
data()

# Load a specific dataset
mpg = data('mpg')
diamonds = data('diamonds')

# Load network data (requires igraph)
flights = data('us_flights')
```
