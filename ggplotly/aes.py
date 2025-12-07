# aes.py
"""
Aesthetic mapping functions for ggplotly.
"""


class after_stat:
    """
    Reference a computed statistic in aesthetic mapping.

    Use this to map an aesthetic to a variable computed by a stat,
    rather than a variable in the original data.

    Parameters:
        var (str): Name of the computed variable to use.

    Common computed variables by stat:
        - stat_count/stat_bin: count, density, ncount, ndensity
        - stat_density: density, count, scaled, ndensity
        - stat_smooth: y, ymin, ymax, se

    Examples:
        >>> aes(x='x', y=after_stat('density'))  # Map y to computed density
        >>> aes(x='x', y=after_stat('count'))    # Map y to computed count
    """

    def __init__(self, var):
        self.var = var

    def __repr__(self):
        return f"after_stat('{self.var}')"


class after_scale:
    """
    Reference a variable after scale transformation.

    Use this to create aesthetics that depend on the output
    of scale transformations.

    Parameters:
        expr (str): Expression referencing scaled variables.

    Examples:
        >>> aes(fill=after_scale('alpha(color, 0.5)'))
    """

    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return f"after_scale('{self.expr}')"


class stage:
    """
    Control aesthetic evaluation at different stages.

    Allows you to specify different values for an aesthetic
    at the start (original data), after stat transformation,
    and after scale transformation.

    Parameters:
        start: Value at start (before stat)
        after_stat: Value after stat transformation
        after_scale: Value after scale transformation

    Examples:
        >>> aes(color=stage(start='group', after_scale='alpha(color, 0.5)'))
    """

    def __init__(self, start=None, after_stat=None, after_scale=None):
        self.start = start
        self.after_stat = after_stat
        self.after_scale = after_scale


class aes:
    """
    Aesthetic mappings for ggplot.

    Aesthetic mappings describe how variables in the data are mapped
    to visual properties (aesthetics) of geoms. This is the fundamental
    concept in the grammar of graphics.

    Parameters:
        x (str): Variable for x-axis position
        y (str): Variable for y-axis position
        z (str): Variable for z-axis position (3D plots)
        color/colour (str): Variable for color aesthetic
        fill (str): Variable for fill color
        size (str): Variable for point/line size
        shape (str): Variable for point shape
        alpha (str): Variable for transparency
        linetype (str): Variable for line type
        label (str): Variable for text labels
        group (str): Variable for grouping
        **kwargs: Additional aesthetic mappings

    Examples:
        >>> aes(x='mpg', y='hp')
        >>> aes(x='mpg', y='hp', color='cyl')
        >>> aes(x='mpg', y='hp', color='cyl', size='wt')
        >>> aes(x='x', y=after_stat('density'))  # Use computed stat
    """

    def __init__(self, x=None, y=None, z=None, color=None, colour=None,
                 fill=None, size=None, shape=None, alpha=None, linetype=None,
                 label=None, group=None, **kwargs):
        self.mapping = {}

        # Handle standard aesthetics
        if x is not None:
            self.mapping['x'] = x
        if y is not None:
            self.mapping['y'] = y
        if z is not None:
            self.mapping['z'] = z
        if color is not None:
            self.mapping['color'] = color
        if colour is not None:  # British spelling alias
            self.mapping['color'] = colour
        if fill is not None:
            self.mapping['fill'] = fill
        if size is not None:
            self.mapping['size'] = size
        if shape is not None:
            self.mapping['shape'] = shape
        if alpha is not None:
            self.mapping['alpha'] = alpha
        if linetype is not None:
            self.mapping['linetype'] = linetype
        if label is not None:
            self.mapping['label'] = label
        if group is not None:
            self.mapping['group'] = group

        # Add any additional kwargs
        self.mapping.update(kwargs)

    def __repr__(self):
        items = ', '.join(f'{k}={repr(v)}' for k, v in self.mapping.items())
        return f"aes({items})"

    def get(self, key, default=None):
        """Get an aesthetic mapping value."""
        return self.mapping.get(key, default)

    def keys(self):
        """Get all aesthetic keys."""
        return self.mapping.keys()

    def values(self):
        """Get all aesthetic values."""
        return self.mapping.values()

    def items(self):
        """Get all aesthetic key-value pairs."""
        return self.mapping.items()

    def __getitem__(self, key):
        """Get aesthetic mapping by key."""
        return self.mapping[key]

    def __contains__(self, key):
        """Check if aesthetic is mapped."""
        return key in self.mapping

    def copy(self):
        """Create a copy of the aesthetic mapping."""
        new_aes = aes()
        new_aes.mapping = self.mapping.copy()
        return new_aes

    def update(self, other):
        """Update mappings from another aes or dict."""
        if isinstance(other, aes):
            self.mapping.update(other.mapping)
        else:
            self.mapping.update(other)
