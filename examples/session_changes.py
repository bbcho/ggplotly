# %% [markdown]
# # Session Changes - Visual Verification
#
# This notebook demonstrates all changes made in the current development session.
#
# ## Contents
# 1. **New Geoms**
#    - `geom_rect` - Rectangles for highlighting regions
#    - `geom_label` - Text labels with background boxes
#
# 2. **New Scales**
#    - `scale_x_reverse` / `scale_y_reverse` - Reversed axes
#
# 3. **New Coordinates**
#    - `coord_fixed` - Fixed aspect ratio
#
# 4. **New Parameters**
#    - `stroke` for `geom_point` (marker border width)
#    - `arrow` and `arrow_size` for `geom_segment`
#    - `width` for `geom_errorbar` (cap width)
#    - `linewidth` alias for `size` (ggplot2 3.4+ compatibility)
#    - `parse` for `geom_text` (LaTeX/MathJax support)
#
# 5. **New Position Exports**
#    - `position_fill`, `position_nudge`, `position_identity`, `position_dodge2`

# %%
import pandas as pd
import numpy as np

from ggplotly import (
    ggplot, aes, labs,
    # New geoms
    geom_rect, geom_label,
    # New scales
    scale_x_reverse, scale_y_reverse,
    # New coords
    coord_fixed,
    # Existing geoms with new parameters
    geom_point, geom_segment, geom_errorbar, geom_line, geom_text,
    geom_bar, geom_boxplot, geom_path,
    # Positions
    position_fill, position_nudge, position_identity, position_dodge2,
    # Other
    theme_minimal, facet_wrap
)

# %% [markdown]
# ---
# ## 1. geom_rect - Rectangles
#
# Draw rectangles defined by corner coordinates (xmin, xmax, ymin, ymax).

# %% [markdown]
# ### Basic Rectangle

# %%
rect_df = pd.DataFrame({
    'xmin': [1, 4],
    'xmax': [3, 6],
    'ymin': [1, 3],
    'ymax': [4, 6]
})

(
    ggplot(rect_df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'))
    + geom_rect()
    + labs(title='Basic geom_rect')
    + theme_minimal()
)

# %% [markdown]
# ### Rectangle with Custom Styling

# %%
(
    ggplot(rect_df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'))
    + geom_rect(fill='lightblue', color='navy', size=2, alpha=0.7)
    + labs(title='geom_rect with fill, border color, and alpha')
    + theme_minimal()
)

# %% [markdown]
# ### Rectangle with Fill Mapped to Category

# %%
rect_cat_df = pd.DataFrame({
    'xmin': [1, 4, 7],
    'xmax': [3, 6, 9],
    'ymin': [1, 2, 1],
    'ymax': [4, 5, 3],
    'category': ['A', 'B', 'C']
})

(
    ggplot(rect_cat_df, aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax', fill='category'))
    + geom_rect(alpha=0.6)
    + labs(title='geom_rect with fill aesthetic')
    + theme_minimal()
)

# %% [markdown]
# ### Rectangle as Highlight Overlay

# %%
# Scatter data
np.random.seed(42)
scatter_df = pd.DataFrame({
    'x': np.random.uniform(0, 10, 50),
    'y': np.random.uniform(0, 10, 50)
})

# Highlight region
highlight_df = pd.DataFrame({
    'xmin': [3], 'xmax': [7],
    'ymin': [4], 'ymax': [8]
})

(
    ggplot(scatter_df, aes(x='x', y='y'))
    + geom_rect(
        data=highlight_df,
        mapping=aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
        fill='yellow', alpha=0.3
    )
    + geom_point(color='steelblue', size=8)
    + labs(title='geom_rect as highlight overlay on scatter plot')
    + theme_minimal()
)

# %% [markdown]
# ---
# ## 2. geom_label - Text Labels with Background
#
# Like `geom_text` but with a visible background box for better readability.

# %% [markdown]
# ### Basic Labels

# %%
label_df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [2, 4, 3, 5],
    'name': ['Alpha', 'Beta', 'Gamma', 'Delta']
})

(
    ggplot(label_df, aes(x='x', y='y', label='name'))
    + geom_label()
    + labs(title='Basic geom_label')
    + theme_minimal()
)

# %% [markdown]
# ### Styled Labels

# %%
(
    ggplot(label_df, aes(x='x', y='y', label='name'))
    + geom_label(fill='lightgreen', color='darkgreen', size=14, alpha=0.9)
    + labs(title='geom_label with custom fill, color, and size')
    + theme_minimal()
)

# %% [markdown]
# ### Labels with Points and Nudge

# %%
(
    ggplot(label_df, aes(x='x', y='y'))
    + geom_point(size=12, color='coral')
    + geom_label(aes(label='name'), nudge_y=0.4, fill='white', size=10)
    + labs(title='geom_label with nudge_y to offset from points')
    + theme_minimal()
)

# %% [markdown]
# ### Labels with Fill Mapped to Category

# %%
label_cat_df = pd.DataFrame({
    'x': [1, 2, 3, 4],
    'y': [2, 4, 3, 5],
    'name': ['A', 'B', 'C', 'D'],
    'group': ['Group 1', 'Group 1', 'Group 2', 'Group 2']
})

(
    ggplot(label_cat_df, aes(x='x', y='y', label='name', fill='group'))
    + geom_label(size=14)
    + labs(title='geom_label with fill aesthetic mapped to category')
    + theme_minimal()
)

# %% [markdown]
# ### geom_label vs geom_text Comparison

# %%
compare_df = pd.DataFrame({
    'x': [1, 2],
    'y': [1, 1],
    'label': ['geom_text', 'geom_label'],
    'type': ['text', 'label']
})

# Create a busy background
bg_df = pd.DataFrame({
    'x': np.random.uniform(0.5, 2.5, 100),
    'y': np.random.uniform(0.5, 1.5, 100)
})

(
    ggplot(bg_df, aes(x='x', y='y'))
    + geom_point(alpha=0.3, size=6)
    + geom_text(data=compare_df[compare_df['type']=='text'],
                mapping=aes(x='x', y='y', label='label'), size=14, color='red')
    + geom_label(data=compare_df[compare_df['type']=='label'],
                 mapping=aes(x='x', y='y', label='label'), size=14, color='red', fill='white')
    + labs(title='geom_text (left) vs geom_label (right) - label has background')
    + theme_minimal()
)

# %% [markdown]
# ---
# ## 2.5 scale_x_reverse / scale_y_reverse - Reversed Axes
#
# Reverse the direction of axes. Useful for depth charts, rankings, or inverted coordinate systems.

# %% [markdown]
# ### scale_x_reverse - Reversed X-axis

# %%
# Normal vs Reversed X-axis comparison
reverse_df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [2, 4, 3, 5, 4]
})

(
    ggplot(reverse_df, aes(x='x', y='y'))
    + geom_line(color='steelblue', size=2)
    + geom_point(color='steelblue', size=10)
    + scale_x_reverse()
    + labs(title='scale_x_reverse - X-axis runs from 5 to 1')
    + theme_minimal()
)

# %% [markdown]
# ### scale_y_reverse - Reversed Y-axis
#
# Useful for depth charts, rankings, or inverted visualizations.

# %%
# Depth chart example - useful for ocean/ground depth, rankings, etc.
depth_df = pd.DataFrame({
    'depth': [0, 10, 20, 30, 40, 50],
    'temperature': [25, 22, 18, 15, 12, 10]
})

(
    ggplot(depth_df, aes(x='temperature', y='depth'))
    + geom_line(color='darkblue', size=2)
    + geom_point(color='darkblue', size=10)
    + scale_y_reverse()
    + labs(title='scale_y_reverse - Ocean Temperature Profile',
           x='Temperature (°C)', y='Depth (m)')
    + theme_minimal()
)

# %% [markdown]
# ### coord_fixed - Fixed Aspect Ratio
#
# Essential for maps and geometric visualizations where the x/y ratio matters.

# %%
# coord_fixed ensures 1 unit on x = 1 unit on y
circle_t = np.linspace(0, 2 * np.pi, 100)
circle_df = pd.DataFrame({
    'x': np.cos(circle_t),
    'y': np.sin(circle_t)
})

(
    ggplot(circle_df, aes(x='x', y='y'))
    + geom_path(color='coral', size=2)
    + coord_fixed(ratio=1)
    + labs(title='coord_fixed(ratio=1) - Circle appears as circle, not ellipse')
    + theme_minimal()
)

# %% [markdown]
# ### coord_fixed with Different Ratios

# %%
# Different ratio - 2:1 means y is stretched (1 y unit = 2 x units)
square_df = pd.DataFrame({
    'x': [0, 1, 1, 0, 0],
    'y': [0, 0, 1, 1, 0]
})

(
    ggplot(square_df, aes(x='x', y='y'))
    + geom_path(color='forestgreen', size=2)
    + coord_fixed(ratio=2)
    + labs(title='coord_fixed(ratio=2) - Square becomes tall rectangle (y stretched)')
    + theme_minimal()
)

# %% [markdown]
# ---
# ## 3. New Parameters for Existing Geoms

# %% [markdown]
# ### geom_point: `stroke` parameter
#
# Controls the border width around markers.

# %%
stroke_df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y': [1, 1, 1, 1, 1],
    'stroke_val': [0, 1, 2, 3, 4]
})

(
    ggplot(stroke_df, aes(x='x', y='y'))
    + geom_point(data=stroke_df[stroke_df['x']==1], stroke=0, size=20, color='steelblue')
    + geom_point(data=stroke_df[stroke_df['x']==2], stroke=1, size=20, color='steelblue')
    + geom_point(data=stroke_df[stroke_df['x']==3], stroke=2, size=20, color='steelblue')
    + geom_point(data=stroke_df[stroke_df['x']==4], stroke=3, size=20, color='steelblue')
    + geom_point(data=stroke_df[stroke_df['x']==5], stroke=4, size=20, color='steelblue')
    + geom_text(aes(label='stroke_val'), nudge_y=0.15, size=12)
    + labs(title='geom_point stroke parameter (0, 1, 2, 3, 4)', y='')
    + theme_minimal()
)

# %% [markdown]
# ### geom_segment: `arrow` parameter
#
# Adds arrowheads to line segments.

# %%
arrow_df = pd.DataFrame({
    'x': [1, 1, 1],
    'y': [1, 2, 3],
    'xend': [3, 3, 3],
    'yend': [1.5, 2.5, 3.5]
})

(
    ggplot(arrow_df, aes(x='x', y='y', xend='xend', yend='yend'))
    + geom_segment(arrow=True, arrow_size=15, color='darkblue', size=2)
    + labs(title='geom_segment with arrow=True')
    + theme_minimal()
)

# %% [markdown]
# ### Arrow Size Comparison

# %%
arrow_size_df = pd.DataFrame({
    'x': [1, 1, 1],
    'y': [1, 2, 3],
    'xend': [3, 3, 3],
    'yend': [1, 2, 3],
    'size_label': ['arrow_size=10', 'arrow_size=20', 'arrow_size=30']
})

(
    ggplot()
    + geom_segment(data=arrow_size_df[arrow_size_df['y']==1],
                   mapping=aes(x='x', y='y', xend='xend', yend='yend'),
                   arrow=True, arrow_size=10, color='coral')
    + geom_segment(data=arrow_size_df[arrow_size_df['y']==2],
                   mapping=aes(x='x', y='y', xend='xend', yend='yend'),
                   arrow=True, arrow_size=20, color='coral')
    + geom_segment(data=arrow_size_df[arrow_size_df['y']==3],
                   mapping=aes(x='x', y='y', xend='xend', yend='yend'),
                   arrow=True, arrow_size=30, color='coral')
    + geom_label(data=arrow_size_df, mapping=aes(x='xend', y='yend', label='size_label'),
                 nudge_x=0.5, hjust=0, size=10)
    + labs(title='geom_segment arrow_size comparison')
    + theme_minimal()
)

# %% [markdown]
# ### geom_errorbar: `width` parameter
#
# Controls the width of error bar caps.

# %%
error_df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [5, 7, 6],
    'ymin': [4, 5.5, 4.5],
    'ymax': [6, 8.5, 7.5],
    'width_label': ['width=2', 'width=8', 'width=15']
})

(
    ggplot()
    + geom_errorbar(data=error_df[error_df['x']==1],
                    mapping=aes(x='x', y='y', ymin='ymin', ymax='ymax'),
                    width=2, color='purple')
    + geom_errorbar(data=error_df[error_df['x']==2],
                    mapping=aes(x='x', y='y', ymin='ymin', ymax='ymax'),
                    width=8, color='purple')
    + geom_errorbar(data=error_df[error_df['x']==3],
                    mapping=aes(x='x', y='y', ymin='ymin', ymax='ymax'),
                    width=15, color='purple')
    + geom_point(data=error_df, mapping=aes(x='x', y='y'), size=10, color='purple')
    + geom_text(data=error_df, mapping=aes(x='x', y='ymax', label='width_label'),
                nudge_y=0.5, size=10)
    + labs(title='geom_errorbar width parameter comparison')
    + theme_minimal()
)

# %% [markdown]
# ### geom_line: `linewidth` alias
#
# The `linewidth` parameter is now an alias for `size` (ggplot2 3.4+ compatibility).

# %%
line_df = pd.DataFrame({
    'x': [1, 2, 3, 4, 5],
    'y1': [1, 2, 1.5, 3, 2.5],
    'y2': [2, 3, 2.5, 4, 3.5],
    'y3': [3, 4, 3.5, 5, 4.5]
})

(
    ggplot(line_df, aes(x='x'))
    + geom_line(aes(y='y1'), linewidth=1, color='blue')   # Using new linewidth
    + geom_line(aes(y='y2'), linewidth=3, color='green')  # Using new linewidth
    + geom_line(aes(y='y3'), size=5, color='red')         # Using old size (still works)
    + labs(title='linewidth=1 (blue), linewidth=3 (green), size=5 (red)')
    + theme_minimal()
)

# %% [markdown]
# ### geom_text: `parse` parameter
#
# Enables LaTeX/MathJax rendering for mathematical expressions.

# %%
math_df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [1, 2, 3],
    'formula': ['\\alpha', '\\beta^2', '\\gamma + \\delta']
})

(
    ggplot(math_df, aes(x='x', y='y', label='formula'))
    + geom_point(size=12, color='gray')
    + geom_text(parse=True, size=16, nudge_y=0.2)
    + labs(title='geom_text with parse=True (LaTeX rendering)')
    + theme_minimal()
)

# %% [markdown]
# ---
# ## 4. New Position Exports

# %% [markdown]
# ### position_fill - Stacked bars normalized to 100%

# %%
pos_df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B', 'C', 'C'],
    'group': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'value': [10, 20, 15, 25, 8, 12]
})

(
    ggplot(pos_df, aes(x='category', y='value', fill='group'))
    + geom_bar(stat='identity', position=position_fill())
    + labs(title='position_fill - stacked bars normalized to 100%')
    + theme_minimal()
)

# %% [markdown]
# ### position_nudge - Offset labels from points

# %%
nudge_df = pd.DataFrame({
    'x': [1, 2, 3],
    'y': [1, 2, 3],
    'label': ['Point A', 'Point B', 'Point C']
})

(
    ggplot(nudge_df, aes(x='x', y='y'))
    + geom_point(size=12, color='tomato')
    + geom_text(aes(label='label'), position=position_nudge(x=0.2, y=0.2))
    + labs(title='position_nudge - offset text from points')
    + theme_minimal()
)

# %% [markdown]
# ### position_dodge2 - Dodge without grouping variable

# %%
dodge_df = pd.DataFrame({
    'category': ['A', 'A', 'B', 'B'],
    'type': ['X', 'Y', 'X', 'Y'],
    'value': [10, 15, 12, 18]
})

(
    ggplot(dodge_df, aes(x='category', y='value', fill='type'))
    + geom_bar(stat='identity', position=position_dodge2())
    + labs(title='position_dodge2 - side-by-side bars')
    + theme_minimal()
)

# %% [markdown]
# ---
# ## 5. Combined Example
#
# A comprehensive plot using multiple new features together.

# %%
# Create sample data
np.random.seed(123)
combined_df = pd.DataFrame({
    'x': range(1, 11),
    'y': np.cumsum(np.random.randn(10)) + 10,
})
combined_df['label'] = combined_df['y'].round(1).astype(str)

# Highlight region
highlight = pd.DataFrame({
    'xmin': [3], 'xmax': [7],
    'ymin': [combined_df['y'].min() - 1],
    'ymax': [combined_df['y'].max() + 1]
})

# Arrow annotation
arrow_annot = pd.DataFrame({
    'x': [8], 'y': [combined_df['y'].iloc[7] + 2],
    'xend': [8], 'yend': [combined_df['y'].iloc[7] + 0.3]
})

(
    ggplot(combined_df, aes(x='x', y='y'))
    # Highlight region using geom_rect
    + geom_rect(
        data=highlight,
        mapping=aes(xmin='xmin', xmax='xmax', ymin='ymin', ymax='ymax'),
        fill='lightyellow', alpha=0.5
    )
    # Line with linewidth
    + geom_line(linewidth=2, color='steelblue')
    # Points with stroke
    + geom_point(size=12, color='steelblue', stroke=2)
    # Arrow annotation using geom_segment with arrow
    + geom_segment(
        data=arrow_annot,
        mapping=aes(x='x', y='y', xend='xend', yend='yend'),
        arrow=True, arrow_size=12, color='red'
    )
    # Label for arrow
    + geom_label(
        data=pd.DataFrame({'x': [8], 'y': [combined_df['y'].iloc[7] + 2.5], 'label': ['Peak!']}),
        mapping=aes(x='x', y='y', label='label'),
        fill='white', color='red', size=12
    )
    + labs(
        title='Combined Example: rect, label, stroke, arrow, linewidth',
        x='Time', y='Value'
    )
    + theme_minimal()
)

# %% [markdown]
# ---
# ## Summary of Changes
#
# | Feature | Type | Description |
# |---------|------|-------------|
# | `geom_rect` | New Geom | Rectangles defined by xmin/xmax/ymin/ymax |
# | `geom_label` | New Geom | Text labels with background boxes |
# | `scale_x_reverse` | New Scale | Reversed x-axis direction |
# | `scale_y_reverse` | New Scale | Reversed y-axis direction |
# | `coord_fixed` | New Coord | Fixed aspect ratio (e.g., for maps) |
# | `stroke` | New Param | Border width for `geom_point` markers |
# | `arrow`, `arrow_size` | New Params | Arrowheads for `geom_segment` |
# | `width` | New Param | Cap width for `geom_errorbar` |
# | `linewidth` | New Alias | Alias for `size` in line geoms (ggplot2 3.4+) |
# | `parse` | New Param | LaTeX rendering for `geom_text` |
# | `position_fill` | Export | Stacked bars normalized to 100% |
# | `position_nudge` | Export | Offset elements by fixed amount |
# | `position_identity` | Export | No position adjustment |
# | `position_dodge2` | Export | Dodge without explicit grouping |
