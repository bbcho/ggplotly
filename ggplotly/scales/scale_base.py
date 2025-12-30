# scales/scale_base.py
"""
Base class for all scale transformations.

Scales control how data values are mapped to visual properties like
position, color, size, and shape. They can also modify axis appearance.
"""

import warnings


class Scale:
    """
    Base class for all scales in ggplotly.

    Scales transform data values into visual properties. Subclasses implement
    specific transformations for axes, colors, sizes, shapes, etc.

    All scales must implement the apply() method which takes a Plotly figure
    and modifies it in place.

    Attributes:
        aesthetic (str): The aesthetic this scale affects (e.g., 'x', 'y', 'color',
            'fill', 'size', 'shape'). Used by the scale registry to ensure only
            one scale per aesthetic (matching ggplot2 behavior).

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + scale_x_log10()
        >>> ggplot(df, aes(x='x', y='y', color='group')) + geom_point() + scale_color_manual(['red', 'blue'])
    """

    # The aesthetic this scale affects. Subclasses should override.
    aesthetic = None

    def apply(self, fig):
        """
        Apply the scale transformation to the figure.

        Parameters:
            fig (Figure): Plotly figure object to modify.

        Note:
            Subclasses must implement this method.
        """
        pass  # To be implemented by subclasses

    def _apply_manual_color_mapping(self, fig, values, name=None, breaks=None,
                                     labels=None, update_fill=False, guide='legend'):
        """
        Apply manual color mapping to figure traces.

        Shared implementation for scale_color_manual and scale_fill_manual.

        Parameters:
            fig (Figure): Plotly figure object.
            values (dict or list): Color mapping or list of colors.
            name (str, optional): Legend title.
            breaks (list, optional): Categories to show in legend.
            labels (list, optional): Labels for breaks.
            update_fill (bool): If True, also update fillcolor attribute.
            guide (str): 'legend' or 'none' to control legend visibility.
        """
        # Create a mapping of categories to colors
        if isinstance(values, dict):
            color_map = values
        else:
            # Extract categories from trace names
            categories = []
            for trace in fig.data:
                if hasattr(trace, 'name') and trace.name not in categories:
                    categories.append(trace.name)
            color_map = dict(zip(categories, values))

        # Update trace colors based on the mapping
        for trace in fig.data:
            if hasattr(trace, 'name') and trace.name in color_map:
                color = color_map[trace.name]
                if hasattr(trace, 'marker') and trace.marker is not None:
                    trace.marker.color = color
                if hasattr(trace, 'line') and trace.line is not None:
                    trace.line.color = color
                if update_fill and hasattr(trace, 'fillcolor'):
                    trace.fillcolor = color

        # Update the legend title if provided
        if name is not None:
            fig.update_layout(legend_title_text=name)

        # Update legend items if breaks and labels are provided
        if breaks is not None and labels is not None:
            for trace in fig.data:
                if hasattr(trace, 'name') and trace.name in breaks:
                    idx = breaks.index(trace.name)
                    trace.name = labels[idx]

        # Hide legend if guide is 'none'
        if guide == 'none':
            fig.update_layout(showlegend=False)


class ScaleRegistry:
    """
    Registry for managing scales by aesthetic.

    Ensures only one scale per aesthetic is active, matching ggplot2's behavior.
    When a new scale is added for an aesthetic that already has a scale,
    the old scale is replaced with a warning (like ggplot2's message:
    "Scale for 'colour' is already present. Adding another scale for 'colour',
    which will replace the existing scale.")
    """

    def __init__(self):
        self._scales = {}  # aesthetic -> scale mapping
        self._order = []   # maintains insertion order for all scales

    def add(self, scale):
        """
        Add a scale to the registry.

        If the scale has an aesthetic and a scale already exists for that
        aesthetic, the old scale is replaced with a warning.

        Parameters:
            scale (Scale): The scale to add.
        """
        aesthetic = getattr(scale, 'aesthetic', None)

        if aesthetic is not None:
            # Check for existing scale for this aesthetic
            if aesthetic in self._scales:
                old_scale = self._scales[aesthetic]
                # Remove old scale from order list
                if old_scale in self._order:
                    self._order.remove(old_scale)
                # Warn about replacement (matching ggplot2 behavior)
                warnings.warn(
                    f"Scale for '{aesthetic}' is already present. "
                    f"Adding another scale for '{aesthetic}', which will replace the existing scale.",
                    UserWarning,
                    stacklevel=3
                )

            self._scales[aesthetic] = scale
            self._order.append(scale)
        else:
            # Scale without aesthetic - just add to order
            self._order.append(scale)

    def get(self, aesthetic):
        """
        Get the scale for a given aesthetic.

        Parameters:
            aesthetic (str): The aesthetic to look up.

        Returns:
            Scale or None: The scale for that aesthetic, or None if not set.
        """
        return self._scales.get(aesthetic)

    def __iter__(self):
        """Iterate over scales in order added."""
        return iter(self._order)

    def __len__(self):
        return len(self._order)

    def __bool__(self):
        return len(self._order) > 0

    def to_list(self):
        """Return scales as a list (for backward compatibility)."""
        return list(self._order)
