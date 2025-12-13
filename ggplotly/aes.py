# aes.py
"""Aesthetic mapping functions for ggplotly."""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    import pandas as pd


class after_stat:
    """
    Reference a computed statistic in aesthetic mapping.

    Supports both simple variable references and expressions using
    computed variables, similar to plotnine.

    Parameters:
        expr: Variable name or expression using computed variables.

    Common computed variables by stat:
        - stat_count/stat_bin: count, density, ncount, ndensity
        - stat_density: density, count, scaled, ndensity
        - stat_smooth: y, ymin, ymax, se

    Examples:
        >>> aes(y=after_stat('density'))              # Simple reference
        >>> aes(y=after_stat('count / count.sum()'))  # Proportion
        >>> aes(y=after_stat('density * 100'))        # Scaled density
    """

    __slots__ = ('expr',)

    def __init__(self, expr: str) -> None:
        self.expr = expr

    def __repr__(self) -> str:
        return f"after_stat({self.expr!r})"

    def is_expression(self) -> bool:
        """Check if this contains an expression vs simple variable name."""
        # Simple identifier: letters, digits, underscores, starting with letter/underscore
        return not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', self.expr)

    def evaluate(self, data: pd.DataFrame) -> pd.Series:
        """
        Evaluate the expression against computed data.

        Parameters:
            data: DataFrame containing computed stat variables.

        Returns:
            Series with evaluated results.

        Raises:
            KeyError: If a simple variable reference is not found.
            ValueError: If expression evaluation fails.
        """
        import numpy as np
        import pandas as pd

        if not self.is_expression():
            # Simple variable reference
            if self.expr not in data.columns:
                available = ', '.join(data.columns)
                raise KeyError(
                    f"Computed variable '{self.expr}' not found. "
                    f"Available: {available}"
                )
            return data[self.expr]

        # Expression evaluation with numpy/pandas in namespace
        namespace = {
            'np': np,
            'numpy': np,
            'sum': np.sum,
            'mean': np.mean,
            'max': np.max,
            'min': np.min,
            **{col: data[col] for col in data.columns}
        }

        try:
            return pd.eval(self.expr, local_dict=namespace)
        except Exception as e:
            available = ', '.join(data.columns)
            raise ValueError(
                f"Failed to evaluate expression '{self.expr}': {e}. "
                f"Available variables: {available}"
            ) from e

    # Backwards compatibility: allow access via .var
    @property
    def var(self) -> str:
        """Backwards compatible alias for expr."""
        return self.expr


class after_scale:
    """
    Reference a variable after scale transformation.

    Use this to create aesthetics that depend on the output
    of scale transformations.

    Parameters:
        expr: Expression referencing scaled variables.

    Examples:
        >>> aes(fill=after_scale('alpha(color, 0.5)'))
    """

    __slots__ = ('expr',)

    def __init__(self, expr: str) -> None:
        self.expr = expr

    def __repr__(self) -> str:
        return f"after_scale({self.expr!r})"


class stage:
    """
    Control aesthetic evaluation at different stages.

    Allows you to specify different values for an aesthetic
    at the start (original data), after stat transformation,
    and after scale transformation.

    Parameters:
        start: Value at start (before stat).
        after_stat: Value after stat transformation.
        after_scale: Value after scale transformation.

    Examples:
        >>> aes(color=stage(start='group', after_scale='alpha(color, 0.5)'))
    """

    __slots__ = ('start', 'after_stat', 'after_scale')

    def __init__(
        self,
        start: str | None = None,
        after_stat: str | None = None,
        after_scale: str | None = None
    ) -> None:
        self.start = start
        self.after_stat = after_stat
        self.after_scale = after_scale

    def __repr__(self) -> str:
        parts = []
        if self.start is not None:
            parts.append(f"start={self.start!r}")
        if self.after_stat is not None:
            parts.append(f"after_stat={self.after_stat!r}")
        if self.after_scale is not None:
            parts.append(f"after_scale={self.after_scale!r}")
        return f"stage({', '.join(parts)})"


# Type alias for aesthetic values
# Using Union for runtime compatibility with Python 3.9
AesValue = Union[str, after_stat, after_scale, stage, float, int, None]


class aes:
    """
    Aesthetic mappings for ggplot.

    Aesthetic mappings describe how variables in the data are mapped
    to visual properties (aesthetics) of geoms. This is the fundamental
    concept in the grammar of graphics.

    Parameters:
        x: Variable for x-axis position.
        y: Variable for y-axis position.
        z: Variable for z-axis position (3D plots).
        color/colour: Variable for color aesthetic.
        fill: Variable for fill color.
        size: Variable for point/line size.
        shape: Variable for point shape.
        alpha: Variable for transparency.
        linetype: Variable for line type.
        label: Variable for text labels.
        group: Variable for grouping.
        **kwargs: Additional aesthetic mappings.

    Examples:
        >>> aes(x='mpg', y='hp')
        >>> aes(x='mpg', y='hp', color='cyl')
        >>> aes(x='x', y=after_stat('density'))
        >>> aes(x='x', y=after_stat('count / count.sum()'))
    """

    __slots__ = ('mapping',)

    def __init__(
        self,
        x: AesValue = None,
        y: AesValue = None,
        z: AesValue = None,
        color: AesValue = None,
        colour: AesValue = None,
        fill: AesValue = None,
        size: AesValue = None,
        shape: AesValue = None,
        alpha: AesValue = None,
        linetype: AesValue = None,
        label: AesValue = None,
        group: str | None = None,
        **kwargs: Any
    ) -> None:
        self.mapping: dict[str, Any] = {}

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

    def __repr__(self) -> str:
        items = ', '.join(f'{k}={v!r}' for k, v in self.mapping.items())
        return f"aes({items})"

    def get(self, key: str, default: Any = None) -> Any:
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

    def __getitem__(self, key: str) -> Any:
        """Get aesthetic mapping by key."""
        return self.mapping[key]

    def __contains__(self, key: str) -> bool:
        """Check if aesthetic is mapped."""
        return key in self.mapping

    def copy(self) -> aes:
        """Create a copy of the aesthetic mapping."""
        new_aes = aes()
        new_aes.mapping = self.mapping.copy()
        return new_aes

    def update(self, other: aes | dict[str, Any]) -> None:
        """Update mappings from another aes or dict."""
        if isinstance(other, aes):
            self.mapping.update(other.mapping)
        else:
            self.mapping.update(other)
