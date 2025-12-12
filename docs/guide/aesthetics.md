# Aesthetics

Aesthetics map columns in your data to visual properties of the plot. They are specified using the `aes()` function.

## Basic Aesthetics

| Aesthetic | Description | Example |
|-----------|-------------|---------|
| `x` | X-axis position | `aes(x='column')` |
| `y` | Y-axis position | `aes(y='column')` |
| `color` | Point/line color | `aes(color='category')` |
| `fill` | Fill color (bars, areas) | `aes(fill='category')` |
| `size` | Point/line size | `aes(size='value')` |
| `shape` | Point shape | `aes(shape='category')` |
| `alpha` | Transparency | `aes(alpha='value')` |
| `group` | Grouping variable | `aes(group='category')` |

## Mapping vs Setting

There's an important distinction between **mapping** an aesthetic (data-driven) and **setting** it (fixed value).

### Mapping (inside `aes()`)

Values come from your data:

```python
# Color varies by 'species' column
ggplot(df, aes(x='x', y='y', color='species')) + geom_point()
```

### Setting (inside geom)

Fixed value for all points:

```python
# All points are blue
ggplot(df, aes(x='x', y='y')) + geom_point(color='blue')
```

## Index as Aesthetic

You can use the DataFrame index as an aesthetic value:

```python
# Explicit index reference
ggplot(df, aes(x='index', y='value')) + geom_line()

# Auto-populate: if x is omitted, index is used
ggplot(df, aes(y='value')) + geom_line()
```

This works with named indices too:

```python
df.index.name = 'date'
ggplot(df, aes(y='price')) + geom_line()  # x-axis labeled 'date'
```

## Color and Fill

`color` affects lines and point outlines. `fill` affects filled areas.

```python
# Points: color = outline, fill doesn't apply
ggplot(df, aes(x='x', y='y', color='cat')) + geom_point()

# Bars: fill = bar color, color = outline
ggplot(df, aes(x='cat', y='count', fill='cat')) + geom_bar(stat='identity')
```

## Grouping

The `group` aesthetic controls how data is grouped for geoms like `geom_line`:

```python
# Without group: one line through all points
ggplot(df, aes(x='x', y='y')) + geom_line()

# With group: separate line per group
ggplot(df, aes(x='x', y='y', group='id')) + geom_line()

# color/fill automatically sets group
ggplot(df, aes(x='x', y='y', color='id')) + geom_line()
```

## Inheriting Aesthetics

Aesthetics set in `ggplot()` are inherited by all geoms:

```python
# Both geoms use x='x', y='y', color='cat'
(
    ggplot(df, aes(x='x', y='y', color='cat'))
    + geom_point()
    + geom_line()
)
```

Override in individual geoms:

```python
(
    ggplot(df, aes(x='x', y='y'))
    + geom_point(aes(color='cat'))  # Points colored by category
    + geom_line(color='gray')        # Line is gray
)
```

## Common Aesthetic Values

### Colors

```python
# Named colors
geom_point(color='red')
geom_point(color='steelblue')

# Hex colors
geom_point(color='#FF5733')

# RGB/RGBA
geom_point(color='rgba(255, 87, 51, 0.5)')
```

### Shapes

```python
# Plotly marker symbols
geom_point(shape='circle')
geom_point(shape='square')
geom_point(shape='diamond')
geom_point(shape='cross')
geom_point(shape='triangle-up')
```

### Line Types

```python
geom_line(linetype='solid')
geom_line(linetype='dash')
geom_line(linetype='dot')
geom_line(linetype='dashdot')
```
