# Theming & Styling

Customize the appearance of your plots with built-in themes and custom styling options.

## Built-in Themes

### theme_default

The default Plotly styling:

```python
import pandas as pd
import numpy as np
from ggplotly import *

df = pd.DataFrame({'x': range(1, 6), 'y': [2, 4, 3, 5, 4]})
base = ggplot(df, aes(x='x', y='y')) + geom_line() + geom_point(size=10)

base  # Default theme
```

### theme_minimal

Clean, minimal design:

```python
base + theme_minimal() + labs(title='theme_minimal')
```

### theme_classic

Classic look with axis lines, no gridlines:

```python
base + theme_classic() + labs(title='theme_classic')
```

### theme_dark

Dark background for high contrast:

```python
base + theme_dark() + labs(title='theme_dark')
```

### theme_ggplot2

Mimic R's ggplot2 default appearance:

```python
base + theme_ggplot2() + labs(title='theme_ggplot2')
```

### theme_bbc

BBC-style news graphics:

```python
base + theme_bbc() + labs(title='theme_bbc')
```

### theme_nytimes

New York Times style:

```python
base + theme_nytimes() + labs(title='theme_nytimes')
```

## Custom Theme Elements

### theme() Function

Customize individual elements:

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + theme(
     plot_background=element_rect(fill='#f0f0f0'),
     panel_background=element_rect(fill='white'),
     axis_text=element_text(size=12, color='darkblue'),
     axis_title=element_text(size=14, color='darkblue')
 )
 + labs(title='Custom Theme'))
```

### element_text

Customize text elements:

```python
element_text(
    size=12,          # Font size
    color='black',    # Text color
    family='Arial',   # Font family
    face='bold',      # 'plain', 'bold', 'italic', 'bold.italic'
    angle=45          # Rotation angle
)
```

### element_rect

Customize rectangular elements (backgrounds, borders):

```python
element_rect(
    fill='white',      # Background color
    color='black',     # Border color
    size=1,            # Border width
    linetype='solid'   # Border style
)
```

### element_line

Customize line elements:

```python
element_line(
    color='gray',      # Line color
    size=1,            # Line width
    linetype='dash'    # 'solid', 'dash', 'dot', 'dashdot'
)
```

### Grid Customization

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + theme(
     panel_grid_major=element_line(color='lightgray', width=1, dash='dash'),
     panel_grid_minor=element_line(color='#f0f0f0', width=0.5),
     axis_line=element_line(color='black', width=2)
 )
 + labs(title='Custom Grid'))
```

## Legend Customization

### Legend Position

```python
df = pd.DataFrame({
    'x': np.random.randn(100),
    'y': np.random.randn(100),
    'group': np.random.choice(['A', 'B'], 100)
})

# Position: 'top', 'bottom', 'left', 'right', 'none'
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point()
 + theme(legend_position='top'))
```

### Hide Legend

```python
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point()
 + theme(legend_position='none'))

# Or using guides
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point()
 + guides(color='none'))
```

### guide_legend

Customize categorical legends:

```python
(ggplot(df, aes(x='x', y='y', color='category'))
 + geom_point(size=8)
 + guides(color=guide_legend(title='Category Type', nrow=1))
 + theme(legend_position='top'))
```

### guide_colorbar

Customize continuous color legends:

```python
df = pd.DataFrame({
    'x': np.random.rand(100),
    'y': np.random.rand(100),
    'z': np.random.rand(100) * 100
})

(ggplot(df, aes(x='x', y='y', color='z'))
 + geom_point(size=8)
 + scale_color_gradient(low='blue', high='red')
 + guides(color=guide_colorbar(title='Value', barwidth=20)))
```

## Labels and Titles

### labs() Function

```python
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
```

### ggtitle()

Quick title addition:

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=10)
 + ggtitle('Quick Title'))
```

## Annotations

### Text Annotations

```python
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
```

### Arrow Annotations

```python
df = pd.DataFrame({
    'x': range(10),
    'y': [1, 3, 2, 5, 8, 6, 4, 3, 2, 1]
})

(ggplot(df, aes(x='x', y='y'))
 + geom_line(size=2, color='steelblue')
 + geom_point(size=8)
 + annotate('segment', x=6, y=9, xend=4, yend=8.2, arrow=True, color='red', size=2)
 + annotate('text', x=6, y=9.5, label='Peak value', size=12, color='red'))
```

## Figure Size

### ggsize()

Control output dimensions:

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_line()
 + geom_point(size=10)
 + ggsize(width=1000, height=400)
 + labs(title='Wide Plot'))
```

## Publication-Ready Examples

### BBC Style

```python
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
```

### Minimal Academic Style

```python
(ggplot(df, aes(x='x', y='y'))
 + geom_point(size=6)
 + geom_smooth(method='lm', color='red')
 + theme_minimal()
 + theme(
     axis_title=element_text(size=12),
     plot_title=element_text(size=14, face='bold')
 )
 + labs(title='Scatter with Linear Fit',
        x='Independent Variable',
        y='Dependent Variable'))
```

### Dark Dashboard

```python
(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point(size=8)
 + theme_dark()
 + scale_color_manual(values=['#00ff00', '#ff00ff'])
 + labs(title='Dashboard Metric'))
```

## Color Scales with Themes

### Sequential Palettes

```python
df = pd.DataFrame({
    'x': np.tile(np.arange(10), 10),
    'y': np.repeat(np.arange(10), 10),
    'z': np.random.randn(100)
})

(ggplot(df, aes(x='x', y='y', fill='z'))
 + geom_tile()
 + scale_fill_gradient(low='blue', high='red')
 + theme_minimal()
 + labs(title='Heatmap with Custom Gradient'))
```

### Viridis for Accessibility

```python
(ggplot(df, aes(x='x', y='y', fill='z'))
 + geom_tile()
 + scale_fill_viridis_c()
 + theme_minimal()
 + labs(title='Colorblind-Friendly Heatmap'))
```

### ColorBrewer Palettes

```python
df = pd.DataFrame({
    'x': np.random.randn(150),
    'y': np.random.randn(150),
    'group': np.repeat(['A', 'B', 'C'], 50)
})

(ggplot(df, aes(x='x', y='y', color='group'))
 + geom_point(size=8)
 + scale_color_brewer(palette='Set2')
 + theme_minimal())
```

## Theme Reference

| Theme Element | Description |
|---------------|-------------|
| `plot_background` | Overall plot background |
| `panel_background` | Panel (data area) background |
| `panel_grid_major` | Major gridlines |
| `panel_grid_minor` | Minor gridlines |
| `axis_line` | Axis lines |
| `axis_text` | Axis tick labels |
| `axis_title` | Axis titles |
| `axis_text_x` | X-axis tick labels only |
| `axis_text_y` | Y-axis tick labels only |
| `legend_position` | Legend placement |
| `legend_title` | Legend title text |
| `legend_text` | Legend item text |
| `plot_title` | Main title |
| `plot_subtitle` | Subtitle |
| `plot_caption` | Caption text |
