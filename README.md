# GGPLOTLY

A data visualization library for Python that combines the power of ggplot and plotly.

## Installation

```bash
pip install ggplotly
```

## Usage

```python
from ggplotly import *
import pandas as pd

df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 2, 3, 4, 5]
})

ggplot(df, aes(x='x', y='y')) + geom_point()
```

## Working Geoms

- geom_point
- geom_line
- geom_bar
- geom_area
- geom_boxplot

## Working Utils

- ggtitle
- lab
- themes
- ggsave