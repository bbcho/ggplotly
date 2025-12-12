# Facets

Faceting creates small multiples - the same plot repeated for subsets of your data.

## facet_wrap

Wraps a 1D sequence of panels into 2D.

```python
# Basic faceting by one variable
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('category')
```

### Controlling Layout

```python
# Specify number of columns
facet_wrap('category', ncol=3)

# Specify number of rows
facet_wrap('category', nrow=2)
```

### Free Scales

By default, all panels share the same axis scales. Allow them to vary:

```python
# Free both axes
facet_wrap('category', scales='free')

# Free only x-axis
facet_wrap('category', scales='free_x')

# Free only y-axis
facet_wrap('category', scales='free_y')
```

## facet_grid

Creates a 2D grid based on two variables.

```python
# Rows by one variable, columns by another
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_grid(rows='var1', cols='var2')
```

### Grid Layout

```python
# Only rows
facet_grid(rows='category')

# Only columns
facet_grid(cols='category')

# Both
facet_grid(rows='category1', cols='category2')
```

### Free Scales in Grid

```python
facet_grid(rows='a', cols='b', scales='free')
facet_grid(rows='a', cols='b', scales='free_x')
facet_grid(rows='a', cols='b', scales='free_y')
```

## Examples

### Comparing Distributions

```python
ggplot(df, aes(x='value')) + geom_histogram() + facet_wrap('group')
```

### Time Series by Category

```python
ggplot(df, aes(x='date', y='value')) + geom_line() + facet_wrap('category', ncol=1)
```

### Two-Way Comparison

```python
ggplot(df, aes(x='x', y='y')) + geom_point() + facet_grid(rows='region', cols='year')
```

## Facet Reference

| Function | Description |
|----------|-------------|
| `facet_wrap(facets)` | Wrap 1D into 2D grid |
| `facet_grid(rows, cols)` | 2D grid of panels |

### facet_wrap Parameters

| Parameter | Description |
|-----------|-------------|
| `facets` | Column name to facet by |
| `ncol` | Number of columns |
| `nrow` | Number of rows |
| `scales` | 'fixed', 'free', 'free_x', 'free_y' |

### facet_grid Parameters

| Parameter | Description |
|-----------|-------------|
| `rows` | Column name for rows |
| `cols` | Column name for columns |
| `scales` | 'fixed', 'free', 'free_x', 'free_y' |
