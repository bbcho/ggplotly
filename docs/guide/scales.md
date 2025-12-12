# Scales

Scales control how data values are mapped to visual properties and how axes are displayed.

## Axis Scales

### Continuous Axes

```python
# Basic continuous scale
ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_continuous()

# With limits
scale_x_continuous(limits=(0, 100))

# With breaks
scale_y_continuous(breaks=[0, 25, 50, 75, 100])
```

### Log Scales

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10() + scale_y_log10()
```

### Date/Time Axes

```python
# Date axis
ggplot(df, aes(x='date', y='value')) + geom_line() + scale_x_date()

# DateTime axis
scale_x_datetime()
```

### Interactive Scales

```python
# Range slider for zooming
ggplot(df, aes(x='date', y='value')) + geom_line() + scale_x_rangeslider()

# Range selector buttons
scale_x_rangeselector(buttons=['1m', '6m', '1y', 'all'])
```

## Color Scales

### Manual Colors

```python
ggplot(df, aes(x='x', y='y', color='category')) + geom_point() + \
    scale_color_manual(values=['red', 'blue', 'green'])

# With names
scale_color_manual(values={'A': 'red', 'B': 'blue', 'C': 'green'})
```

### Color Gradients

```python
# Two-color gradient
ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + \
    scale_color_gradient(low='blue', high='red')

# Three-color diverging gradient
scale_color_gradient2(low='blue', mid='white', high='red', midpoint=0)
```

### ColorBrewer Palettes

```python
# Sequential palette
scale_color_brewer(palette='Blues')

# Diverging palette
scale_color_brewer(type='div', palette='RdBu')

# Qualitative palette
scale_color_brewer(type='qual', palette='Set1')
```

Available palettes:

- **Sequential**: Blues, Greens, Oranges, Reds, Purples, Greys, BuGn, BuPu, GnBu, OrRd, PuBu, PuRd, RdPu, YlGn, YlGnBu, YlOrBr, YlOrRd
- **Diverging**: BrBG, PiYG, PRGn, PuOr, RdBu, RdGy, RdYlBu, RdYlGn, Spectral
- **Qualitative**: Accent, Dark2, Paired, Pastel1, Pastel2, Set1, Set2, Set3

### Viridis Palette

```python
scale_fill_viridis_c()  # Continuous viridis
```

## Fill Scales

Fill scales work the same as color scales but for filled areas:

```python
scale_fill_manual(values=['red', 'blue'])
scale_fill_gradient(low='white', high='darkblue')
scale_fill_brewer(palette='Set2')
```

## Shape Scale

```python
ggplot(df, aes(x='x', y='y', shape='category')) + geom_point() + \
    scale_shape_manual(values=['circle', 'square', 'triangle-up'])
```

## Size Scale

```python
ggplot(df, aes(x='x', y='y', size='value')) + geom_point() + \
    scale_size(range=(1, 10))
```

## Axis Limits

Quick ways to set axis limits:

```python
# Using xlim/ylim
ggplot(df, aes(x='x', y='y')) + geom_point() + xlim(0, 100) + ylim(0, 50)

# Using lims
ggplot(df, aes(x='x', y='y')) + geom_point() + lims(x=(0, 100), y=(0, 50))

# Using coord_cartesian (doesn't clip data)
ggplot(df, aes(x='x', y='y')) + geom_point() + coord_cartesian(xlim=(0, 100))
```

## Scale Reference

| Scale | Description |
|-------|-------------|
| `scale_x_continuous` | Continuous x-axis |
| `scale_y_continuous` | Continuous y-axis |
| `scale_x_log10` | Log10 x-axis |
| `scale_y_log10` | Log10 y-axis |
| `scale_x_date` | Date x-axis |
| `scale_x_datetime` | DateTime x-axis |
| `scale_x_rangeslider` | Interactive range slider |
| `scale_x_rangeselector` | Range selector buttons |
| `scale_color_manual` | Manual color mapping |
| `scale_color_gradient` | 2-color gradient |
| `scale_color_gradient2` | 3-color diverging gradient |
| `scale_color_brewer` | ColorBrewer palettes |
| `scale_fill_manual` | Manual fill mapping |
| `scale_fill_gradient` | Fill gradient |
| `scale_fill_brewer` | ColorBrewer fill |
| `scale_fill_viridis_c` | Viridis fill |
| `scale_shape_manual` | Manual shape mapping |
| `scale_size` | Size scaling |
