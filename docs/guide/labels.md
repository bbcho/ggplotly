# Labels & Annotations

Add titles, axis labels, and annotations to your plots.

## labs()

The primary function for setting plot labels.

```python
ggplot(df, aes(x='x', y='y', color='category')) + geom_point() + \
    labs(
        title='Main Title',
        subtitle='A subtitle with more detail',
        x='X Axis Label',
        y='Y Axis Label',
        color='Legend Title',
        caption='Data source: XYZ'
    )
```

### All labs() Parameters

| Parameter | Description |
|-----------|-------------|
| `title` | Main plot title |
| `subtitle` | Subtitle below title |
| `x` | X-axis label |
| `y` | Y-axis label |
| `z` | Z-axis label (3D plots) |
| `color` | Color legend title |
| `fill` | Fill legend title |
| `size` | Size legend title |
| `shape` | Shape legend title |
| `caption` | Caption at bottom-right |

## ggtitle()

Quick way to set just the title.

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + ggtitle('My Plot')
```

## Annotations

Add text, shapes, and lines at specific positions.

### Text Annotation

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + \
    annotate('text', x=5, y=10, label='Important point!')
```

### Label (text with background)

```python
annotate('label', x=5, y=10, label='Note', fill='yellow')
```

### Shapes

```python
# Rectangle highlight
annotate('rect', xmin=2, xmax=4, ymin=5, ymax=10, fill='yellow', alpha=0.3)

# Point
annotate('point', x=5, y=10, size=10, color='red')
```

### Lines

```python
# Segment
annotate('segment', x=1, y=1, xend=5, yend=10, color='red')

# Arrow
annotate('segment', x=1, y=1, xend=5, yend=10, arrow=True)

# Curved arrow
annotate('curve', x=1, y=1, xend=5, yend=10, arrow=True)
```

### Reference Lines

```python
# Horizontal line
annotate('hline', y=5, color='red', linetype='dash')

# Vertical line
annotate('vline', x=3, color='blue', linetype='dot')
```

## Annotation Parameters

| Parameter | Description |
|-----------|-------------|
| `x`, `y` | Position coordinates |
| `xend`, `yend` | End coordinates (segments) |
| `xmin`, `xmax`, `ymin`, `ymax` | Rectangle bounds |
| `label` | Text content |
| `color` | Color |
| `fill` | Fill color |
| `size` | Size (text or point) |
| `alpha` | Transparency |
| `hjust`, `vjust` | Horizontal/vertical alignment |
| `arrow` | Add arrowhead (bool) |

## Controlling Legends

### guides()

Control legend display for each aesthetic.

```python
# Hide color legend
ggplot(df, aes(x='x', y='y', color='cat')) + geom_point() + guides(color='none')

# Hide all legends
guides(color='none', fill='none', shape='none')
```

### guide_legend()

Customize legend appearance.

```python
from ggplotly import guide_legend

ggplot(df, aes(x='x', y='y', color='cat')) + geom_point() + \
    guides(color=guide_legend(
        title='Categories',
        ncol=2,
        reverse=True
    ))
```

### guide_colorbar()

Customize continuous color bar.

```python
from ggplotly import guide_colorbar

ggplot(df, aes(x='x', y='y', color='value')) + geom_point() + \
    guides(color=guide_colorbar(
        title='Values',
        direction='horizontal'
    ))
```

## Examples

### Annotated Scatter Plot

```python
(
    ggplot(df, aes(x='x', y='y', color='category'))
    + geom_point()
    + annotate('text', x=max_x, y=max_y, label='Maximum')
    + annotate('rect', xmin=2, xmax=4, ymin=5, ymax=10, fill='gray', alpha=0.2)
    + labs(
        title='Scatter Plot with Annotations',
        subtitle='Highlighting a region of interest',
        x='X Variable',
        y='Y Variable',
        caption='Source: My Data'
    )
)
```

### Clean Plot with Hidden Legend

```python
(
    ggplot(df, aes(x='x', y='y', color='category'))
    + geom_point()
    + theme_minimal()
    + theme(legend_position='none')
    + labs(title='Clean Plot')
)
```
