# Themes

Themes control the overall appearance of your plots - backgrounds, fonts, gridlines, and more.

## Built-in Themes

### theme_minimal

Clean, minimal theme with no background.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_minimal()
```

### theme_classic

Classic look with axis lines, no gridlines.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_classic()
```

### theme_dark

Dark background theme.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_dark()
```

### theme_ggplot2

Replicates R's ggplot2 default theme.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_ggplot2()
```

### theme_bbc

BBC News style visualizations.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_bbc()
```

### theme_nytimes

New York Times style visualizations.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + theme_nytimes()
```

## Theme Customization

Use `theme()` to customize specific elements:

### Legend

```python
# Move legend position
theme(legend_position='bottom')  # 'right', 'left', 'top', 'bottom', 'none'

# Hide legend
theme(legend_position='none')
# or
theme(legend_show=False)
```

### Text Elements

```python
from ggplotly import element_text

theme(
    # Title styling
    plot_title=element_text(size=20, color='darkblue'),

    # Axis labels
    axis_title=element_text(size=14),
    axis_title_x=element_text(color='red'),
    axis_title_y=element_text(color='blue'),

    # Axis tick labels
    axis_text=element_text(size=10),
    axis_text_x=element_text(angle=45),

    # Legend
    legend_title=element_text(size=12, color='gray'),
    legend_text=element_text(size=10)
)
```

### Background Elements

```python
from ggplotly import element_rect

theme(
    # Plot background
    plot_background=element_rect(fill='white', color='black'),

    # Panel (plotting area) background
    panel_background=element_rect(fill='lightgray'),

    # Legend background
    legend_background=element_rect(fill='white', color='gray')
)
```

### Gridlines

```python
from ggplotly import element_line

theme(
    # Major gridlines
    panel_grid_major=element_line(color='gray', width=0.5),

    # Minor gridlines
    panel_grid_minor=element_line(color='lightgray', width=0.25)
)
```

## Combining Themes

Start with a base theme and customize:

```python
(
    ggplot(df, aes(x='x', y='y', color='category'))
    + geom_point()
    + theme_minimal()
    + theme(
        legend_position='bottom',
        plot_title=element_text(size=18)
    )
    + labs(title='My Customized Plot')
)
```

## Theme Reference

| Theme | Description |
|-------|-------------|
| `theme_default` | Default ggplotly theme |
| `theme_minimal` | Minimal, clean theme |
| `theme_classic` | Classic with axis lines |
| `theme_dark` | Dark background |
| `theme_ggplot2` | R's ggplot2 default |
| `theme_bbc` | BBC News style |
| `theme_nytimes` | NYT style |
| `theme_custom` | Build from scratch |

### theme() Parameters

| Parameter | Description |
|-----------|-------------|
| `legend_position` | Legend position ('right', 'left', 'top', 'bottom', 'none') |
| `legend_show` | Show/hide legend (bool) |
| `plot_title` | Title text styling |
| `plot_subtitle` | Subtitle styling |
| `axis_title` | Both axis titles |
| `axis_title_x` | X-axis title |
| `axis_title_y` | Y-axis title |
| `axis_text` | Both axis tick labels |
| `axis_text_x` | X-axis tick labels |
| `axis_text_y` | Y-axis tick labels |
| `legend_title` | Legend title styling |
| `legend_text` | Legend text styling |
| `panel_background` | Plot area background |
| `plot_background` | Full plot background |
| `panel_grid_major` | Major gridlines |
| `panel_grid_minor` | Minor gridlines |
