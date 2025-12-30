# trace_builders.py
"""
Trace building strategies for _transform_fig().

This module implements the Strategy Pattern for building Plotly traces based on
different data grouping scenarios. The Grammar of Graphics allows data to be
grouped by various aesthetics (color, shape, group), and each grouping strategy
requires different trace-building logic.

Strategy Pattern Overview:
-------------------------
- TraceBuilder (ABC): Base class defining the interface
- GroupedTraceBuilder: For explicit 'group' aesthetic
- ColorOnlyTraceBuilder: For color/fill mapped to categorical column
- ShapeOnlyTraceBuilder: For shape mapped to categorical column
- ColorAndShapeTraceBuilder: For both color and shape mapped
- ContinuousColorTraceBuilder: For numeric color mapping (colorscale)
- SingleTraceBuilder: For ungrouped data (single trace)

The get_trace_builder() factory function selects the appropriate strategy
based on the style properties computed by AestheticMapper.

Usage:
------
    # In geom_base.py _transform_fig():
    builder = get_trace_builder(fig, plot, data, mapping, style_props, ...)
    builder.build(self._apply_color_targets)

Why This Pattern?
-----------------
The original _transform_fig() method had ~275 lines with 6 different code paths
based on grouping scenarios. This refactoring:
1. Separates each scenario into its own class (Single Responsibility)
2. Makes adding new grouping strategies easy (Open/Closed)
3. Allows testing each strategy independently
4. Reduces the complexity of _transform_fig() to ~45 lines
"""

from abc import ABC, abstractmethod


class TraceBuilder(ABC):
    """
    Abstract base class for trace building strategies.

    Each subclass implements a specific grouping strategy for building
    Plotly traces. The base class provides common initialization and
    helper methods shared across all strategies.

    Attributes:
        fig: The Plotly figure to add traces to
        plot: The Plotly graph object class (e.g., go.Scatter, go.Bar)
        data: DataFrame containing the data to plot
        mapping: Dict of aesthetic mappings (e.g., {'x': 'col_a', 'y': 'col_b'})
        style_props: Style properties computed by AestheticMapper
        color_targets: Dict mapping aesthetics to Plotly trace properties
        payload: Additional parameters to pass to the trace
        row, col: Subplot position for faceted plots
        alpha: Opacity value for the traces
        params: Additional geom parameters
        x, y: Extracted x and y data series from the DataFrame
    """

    def __init__(self, fig, plot, data, mapping, style_props, color_targets,
                 payload, row, col, alpha, params):
        """
        Initialize the trace builder with all required context.

        Parameters:
            fig: Plotly figure object to add traces to
            plot: Plotly graph object class (e.g., go.Scatter)
            data: DataFrame with the data to plot
            mapping: Aesthetic mappings dict (e.g., {'x': 'mpg', 'y': 'hp'})
            style_props: Style properties from AestheticMapper containing:
                - color_series, fill_series: Categorical color data
                - color_map, fill_map: Category -> color mappings
                - shape_series, shape_map: Shape data and mappings
                - group_series: Explicit group data
                - size, alpha: Literal values or series
                - color_is_continuous, fill_is_continuous: Flags for numeric color
            color_targets: Dict mapping aesthetics to trace property names
                e.g., {'color': 'marker_color', 'size': 'marker_size'}
            payload: Additional trace parameters (e.g., mode='markers')
            row: Row position in subplot grid (1-indexed)
            col: Column position in subplot grid (1-indexed)
            alpha: Opacity value (0-1)
            params: Additional geom parameters (e.g., showlegend)
        """
        self.fig = fig
        self.plot = plot
        self.data = data
        self.mapping = mapping
        self.style_props = style_props
        self.color_targets = color_targets
        # Remove 'name' from payload - we set it explicitly per trace
        self.payload = {k: v for k, v in payload.items() if k != 'name'}
        self.row = row
        self.col = col
        self.alpha = alpha
        self.params = params

        # Extract x and y data from the DataFrame using the mapping
        self.x = data[mapping["x"]] if "x" in mapping else None
        self.y = data[mapping["y"]] if "y" in mapping else None

        # Initialize legend tracking on the figure if not present.
        # This set tracks which legend groups have been shown to prevent
        # duplicate legend entries in faceted plots.
        # Note: We use a namespaced attribute to avoid conflicts with Plotly internals.
        # This is stored on the figure because legend state must persist across
        # multiple geom draws in the same plot.
        self._legendgroups_attr = '_ggplotly_shown_legendgroups'
        if not hasattr(fig, self._legendgroups_attr):
            setattr(fig, self._legendgroups_attr, set())

        # Respect the showlegend parameter from geom params
        self.base_showlegend = params.get("showlegend", True)

    def should_show_legend(self, legendgroup):
        """
        Determine if a trace should show its legend entry.

        In faceted plots, the same category may appear in multiple panels.
        We only want to show each legend entry once (in the first panel
        where it appears). This method tracks which groups have been shown.

        Parameters:
            legendgroup: String identifier for this trace's legend group

        Returns:
            bool: True if this is the first time showing this group
        """
        # If showlegend=False was set on the geom, never show legend
        if not self.base_showlegend:
            return False
        # Get the shown groups set from the figure
        shown_groups = getattr(self.fig, self._legendgroups_attr)
        # If we've already shown this group, don't show again
        if legendgroup in shown_groups:
            return False
        # Mark this group as shown and return True
        shown_groups.add(legendgroup)
        return True

    @abstractmethod
    def build(self, apply_color_targets_fn):
        """
        Build and add traces to the figure.

        Each subclass implements this method to create traces appropriate
        for its grouping strategy.

        Parameters:
            apply_color_targets_fn: Function to apply color/fill/size/shape
                to trace properties. This is passed from the Geom class
                (_apply_color_targets method) to maintain the mapping between
                aesthetics and Plotly trace properties.
        """
        pass


class GroupedTraceBuilder(TraceBuilder):
    """
    Builds traces grouped by an explicit 'group' aesthetic.

    Used when the user specifies aes(group='column_name'). Creates one
    trace per unique value in the group column. This is useful for:
    - Drawing separate lines through data subsets
    - Ensuring geom_path connects points within groups

    Example:
        ggplot(df, aes(x='x', y='y', group='id')) + geom_line()
        # Creates separate lines for each unique 'id' value
    """

    def build(self, apply_color_targets_fn):
        """Build one trace per unique group value."""
        group_values = self.style_props['group_series']

        # Check if color or shape are also mapped (affects how we style traces)
        has_color_grouping = (
            self.style_props['color_series'] is not None or
            self.style_props['fill_series'] is not None
        ) and not self.style_props.get('color_is_continuous', False)
        has_shape_grouping = self.style_props.get('shape_series') is not None

        # Iterate over each unique group value
        for group in group_values.unique():
            # Create boolean mask for rows belonging to this group
            group_mask = group_values == group

            # Determine color/shape keys for this group
            # If color is mapped to the same column as group, use group value
            color_key = group if has_color_grouping else None
            shape_key = group if has_shape_grouping else None

            # Get trace properties (color, size, shape) for this group
            trace_props = apply_color_targets_fn(
                self.color_targets, self.style_props,
                value_key=color_key, data_mask=group_mask, shape_key=shape_key
            )

            legend_name = str(group)
            self.fig.add_trace(
                self.plot(
                    x=self.x[group_mask],
                    y=self.y[group_mask],
                    showlegend=self.should_show_legend(legend_name),
                    legendgroup=legend_name,  # Links traces across facets
                    opacity=self.alpha,
                    name=legend_name,
                    **self.payload,
                    **trace_props,
                ),
                row=self.row,
                col=self.col,
            )


class ColorAndShapeTraceBuilder(TraceBuilder):
    """
    Builds traces when both color/fill AND shape are mapped to columns.

    Creates traces for each combination of (color_value, shape_value).
    For example, if color maps to species (A, B) and shape maps to sex (M, F),
    this creates up to 4 traces: (A,M), (A,F), (B,M), (B,F).

    Special case: If color and shape map to the same column, we avoid
    creating redundant combinations and use single-value legend names.

    Example:
        ggplot(df, aes(x='x', y='y', color='species', shape='sex')) + geom_point()
    """

    def build(self, apply_color_targets_fn):
        """Build traces for each color x shape combination."""
        style_props = self.style_props

        # Determine which column and map to use for color/fill
        if style_props['color_series'] is not None:
            cat_col = style_props['color']      # Column name
            cat_map = style_props['color_map']  # {value: color} mapping
        else:
            cat_col = style_props['fill']
            cat_map = style_props['fill_map']

        shape_col = style_props.get('shape')
        shape_map = style_props.get('shape_map')

        # Check if color and shape map to the same column
        # This affects legend naming (avoid "A, A" style names)
        same_column = cat_col == shape_col
        color_values = list(cat_map.keys())
        shape_values = list(shape_map.keys())

        # Create traces for each combination
        for color_val in color_values:
            for shape_val in shape_values:
                # Filter data for this specific combination
                combo_mask = (self.data[cat_col] == color_val) & (self.data[shape_col] == shape_val)

                # Skip if no data points match this combination
                # (common when categories don't fully cross)
                if not combo_mask.any():
                    continue

                x_subset = self.x[combo_mask] if self.x is not None else None
                y_subset = self.y[combo_mask] if self.y is not None else None

                # Get trace properties for this combination
                trace_props = apply_color_targets_fn(
                    self.color_targets, style_props,
                    value_key=color_val, data_mask=combo_mask, shape_key=shape_val
                )

                # Create legend name - avoid redundancy if same column
                if same_column:
                    legend_name = str(color_val)
                else:
                    legend_name = f"{color_val}, {shape_val}"

                self.fig.add_trace(
                    self.plot(
                        x=x_subset,
                        y=y_subset,
                        opacity=self.alpha,
                        name=legend_name,
                        showlegend=self.should_show_legend(legend_name),
                        legendgroup=legend_name,
                        **self.payload,
                        **trace_props,
                    ),
                    row=self.row,
                    col=self.col,
                )


class ColorOnlyTraceBuilder(TraceBuilder):
    """
    Builds traces when only color/fill is mapped to a categorical column.

    Creates one trace per unique category value, each with its own color.
    This is the most common grouping scenario in ggplot.

    Example:
        ggplot(df, aes(x='x', y='y', color='species')) + geom_point()
        # Creates separate colored traces for each species
    """

    def build(self, apply_color_targets_fn):
        """Build one trace per unique color/fill category."""
        style_props = self.style_props

        # Determine which column and map to use
        if style_props['color_series'] is not None:
            cat_col = style_props['color']
            cat_map = style_props['color_map']
        else:
            cat_col = style_props['fill']
            cat_map = style_props['fill_map']

        # Create a trace for each category value
        for cat_value in cat_map.keys():
            # Boolean mask for rows matching this category
            cat_mask = self.data[cat_col] == cat_value

            # Skip if no data for this category
            # (can happen in faceted plots where not all categories appear)
            if not cat_mask.any():
                continue

            x_subset = self.x[cat_mask] if self.x is not None else None
            y_subset = self.y[cat_mask] if self.y is not None else None

            # Get trace properties (color from cat_map, etc.)
            trace_props = apply_color_targets_fn(
                self.color_targets, style_props,
                value_key=cat_value, data_mask=cat_mask, shape_key=None
            )

            legend_name = str(cat_value)
            self.fig.add_trace(
                self.plot(
                    x=x_subset,
                    y=y_subset,
                    opacity=self.alpha,
                    name=legend_name,
                    showlegend=self.should_show_legend(legend_name),
                    legendgroup=legend_name,
                    **self.payload,
                    **trace_props,
                ),
                row=self.row,
                col=self.col,
            )


class ShapeOnlyTraceBuilder(TraceBuilder):
    """
    Builds traces when only shape is mapped to a categorical column.

    Creates one trace per unique shape value. Each trace uses the same
    color (default or literal) but different marker symbols.

    Example:
        ggplot(df, aes(x='x', y='y', shape='species')) + geom_point()
        # All points same color, but different shapes per species
    """

    def build(self, apply_color_targets_fn):
        """Build one trace per unique shape category."""
        style_props = self.style_props
        shape_col = style_props.get('shape')
        shape_map = style_props.get('shape_map')

        # Create a trace for each shape value
        for shape_val in shape_map.keys():
            shape_mask = self.data[shape_col] == shape_val

            # Skip if no data for this shape value
            if not shape_mask.any():
                continue

            x_subset = self.x[shape_mask] if self.x is not None else None
            y_subset = self.y[shape_mask] if self.y is not None else None

            # Get trace properties - no color_key since not color-grouped
            trace_props = apply_color_targets_fn(
                self.color_targets, style_props,
                value_key=None, data_mask=shape_mask, shape_key=shape_val
            )

            legend_name = str(shape_val)
            self.fig.add_trace(
                self.plot(
                    x=x_subset,
                    y=y_subset,
                    opacity=self.alpha,
                    name=legend_name,
                    showlegend=self.should_show_legend(legend_name),
                    legendgroup=legend_name,
                    **self.payload,
                    **trace_props,
                ),
                row=self.row,
                col=self.col,
            )


class ContinuousColorTraceBuilder(TraceBuilder):
    """
    Builds a single trace with continuous (numeric) color mapping.

    When color/fill is mapped to a numeric column, we create one trace
    with a colorscale instead of separate traces per category. Plotly
    handles the color interpolation via marker.color and marker.colorscale.

    For line-based traces (mode='lines'), we use a segment-based approach
    since Plotly's line.color only accepts single values, not arrays.

    Example:
        ggplot(df, aes(x='x', y='y', color='temperature')) + geom_point()
        # Single trace with colorscale from low to high temperature
    """

    # Default Viridis colorscale endpoints
    DEFAULT_COLORSCALE = [[0, '#440154'], [1, '#fde725']]

    def build(self, apply_color_targets_fn):
        """Build trace(s) with colorscale for continuous color."""
        # Check if this is a line-based trace
        # For lines, we need segment-based rendering since line.color
        # only accepts a single value, not an array
        if self.payload.get('mode') == 'lines':
            return self._build_line_gradient()

        # Original marker-based approach for scatter, bar, etc.
        return self._build_marker_gradient()

    def _build_marker_gradient(self):
        """Build a single trace with marker colorscale (original approach)."""
        style_props = self.style_props

        # Get the numeric color values
        if style_props.get('color_is_continuous'):
            color_values = style_props['color_series']
        else:
            color_values = style_props['fill_series']

        # Build marker dict with colorscale configuration
        marker_dict = dict(
            color=color_values,           # Numeric values drive the color
            colorscale='Viridis',         # Default, may be overridden by scale_color_gradient
            showscale=True,               # Show the colorbar
        )

        # Add size if the trace type supports it
        if 'size' in self.color_targets:
            if style_props['size_series'] is not None:
                marker_dict['size'] = style_props['size_series']
            else:
                marker_dict['size'] = style_props['size']

        # Add shape/symbol if the trace type supports it
        if 'shape' in self.color_targets:
            shape_val = style_props.get('shape')
            marker_dict['symbol'] = shape_val if shape_val else 'circle'

        # Create single trace - colorbar serves as legend
        self.fig.add_trace(
            self.plot(
                x=self.x,
                y=self.y,
                opacity=self.alpha,
                showlegend=False,  # Colorbar replaces discrete legend
                marker=marker_dict,
                **self.payload,
            ),
            row=self.row,
            col=self.col,
        )

    def _build_line_gradient(self):
        """
        Build gradient line using individual colored segments.

        Since Plotly's line.color only accepts a single value (not an array),
        we draw each segment as a separate Scattergl trace with its own color.
        Uses WebGL for efficient rendering of many traces.
        """
        import plotly.graph_objects as go

        style_props = self.style_props

        # Get the numeric color values
        if style_props.get('color_is_continuous'):
            color_values = style_props['color_series']
        else:
            color_values = style_props['fill_series']

        # Get line width from style_props or params
        line_width = style_props.get('size', 2)
        if line_width is None:
            line_width = self.params.get('size', 2)

        # Extract arrays
        x_vals = self.x.values if hasattr(self.x, 'values') else list(self.x)
        y_vals = self.y.values if hasattr(self.y, 'values') else list(self.y)
        c_vals = color_values.values if hasattr(color_values, 'values') else list(color_values)

        vmin, vmax = min(c_vals), max(c_vals)
        colorscale = self.DEFAULT_COLORSCALE

        # Draw each segment with interpolated color
        for i in range(len(x_vals) - 1):
            # Normalize color value at midpoint of segment
            t_norm = ((c_vals[i] + c_vals[i + 1]) / 2 - vmin) / (vmax - vmin) if vmax != vmin else 0
            color = self._interpolate_color(colorscale, t_norm)

            self.fig.add_trace(
                go.Scattergl(  # WebGL for performance with many traces
                    x=[x_vals[i], x_vals[i + 1]],
                    y=[y_vals[i], y_vals[i + 1]],
                    mode='lines',
                    line=dict(color=color, width=line_width),
                    opacity=self.alpha,
                    showlegend=False,
                    hoverinfo='skip',
                    # Tag for scale_color_gradient to update colors
                    meta={'_ggplotly_line_gradient': True, '_color_norm': t_norm}
                ),
                row=self.row,
                col=self.col,
            )

        # Add invisible trace for colorbar
        self.fig.add_trace(
            go.Scatter(
                x=[None],
                y=[None],
                mode='markers',
                marker=dict(
                    color=[vmin, vmax],
                    colorscale=colorscale,
                    showscale=True,
                    colorbar=dict(title=self.mapping.get('color', ''))
                ),
                showlegend=False,
                hoverinfo='skip'
            ),
            row=self.row,
            col=self.col,
        )

    @staticmethod
    def _interpolate_color(colorscale, t):
        """
        Interpolate between colorscale endpoints.

        Parameters:
            colorscale: List of [position, color] pairs (e.g., [[0, '#440154'], [1, '#fde725']])
            t: Normalized value between 0 and 1

        Returns:
            str: Interpolated RGB color string
        """
        t = max(0, min(1, t))  # Clamp to [0, 1]

        low_color = colorscale[0][1]
        high_color = colorscale[1][1]

        # Parse hex colors to RGB
        def hex_to_rgb(hex_color):
            hex_color = hex_color.lstrip('#')
            return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

        low_rgb = hex_to_rgb(low_color)
        high_rgb = hex_to_rgb(high_color)

        # Linear interpolation
        r = int(low_rgb[0] + t * (high_rgb[0] - low_rgb[0]))
        g = int(low_rgb[1] + t * (high_rgb[1] - low_rgb[1]))
        b = int(low_rgb[2] + t * (high_rgb[2] - low_rgb[2]))

        return f'rgb({r}, {g}, {b})'


class SingleTraceBuilder(TraceBuilder):
    """
    Builds a single trace when there's no grouping.

    This is the simplest case: all data points go into one trace with
    uniform styling. Used when no categorical aesthetics (color, fill,
    shape, group) are mapped.

    Example:
        ggplot(df, aes(x='x', y='y')) + geom_point()
        # All points in one trace with default/literal color
    """

    def __init__(self, fig, plot, data, mapping, style_props, color_targets,
                 payload, row, col, alpha, params):
        """Initialize, keeping original payload with 'name' intact."""
        # Keep original payload for single trace (includes 'name')
        # Other builders remove 'name' because they set it per-group
        self.original_payload = payload
        super().__init__(fig, plot, data, mapping, style_props, color_targets,
                        payload, row, col, alpha, params)

    def build(self, apply_color_targets_fn):
        """Build a single trace containing all data points."""
        # Get trace properties (literal color, size, etc.)
        trace_props = apply_color_targets_fn(
            self.color_targets, self.style_props,
            data_mask=None, shape_key=None
        )

        # Use name from payload or default to 'trace'
        trace_name = self.original_payload.get('name', 'trace')

        self.fig.add_trace(
            self.plot(
                x=self.x,
                y=self.y,
                opacity=self.alpha,
                showlegend=self.should_show_legend(trace_name),
                legendgroup=trace_name,
                **self.original_payload,  # Includes 'name'
                **trace_props,
            ),
            row=self.row,
            col=self.col,
        )


def get_trace_builder(fig, plot, data, mapping, style_props, color_targets,
                      payload, row, col, alpha, params):
    """
    Factory function to select the appropriate trace builder strategy.

    Analyzes the style properties to determine which grouping scenario
    applies, then returns an instance of the appropriate TraceBuilder
    subclass.

    Decision tree:
    1. If group_series exists -> GroupedTraceBuilder
    2. If color AND shape grouped -> ColorAndShapeTraceBuilder
    3. If only color grouped -> ColorOnlyTraceBuilder
    4. If only shape grouped -> ShapeOnlyTraceBuilder
    5. If continuous color -> ContinuousColorTraceBuilder
    6. Otherwise -> SingleTraceBuilder

    Parameters:
        fig: Plotly figure object
        plot: Plotly graph object class (e.g., go.Scatter)
        data: DataFrame with the data
        mapping: Aesthetic mappings dict
        style_props: Style properties from AestheticMapper
        color_targets: Dict mapping aesthetics to trace properties
        payload: Additional trace parameters
        row, col: Subplot position
        alpha: Opacity value
        params: Additional geom parameters

    Returns:
        TraceBuilder: Appropriate subclass instance for the grouping scenario
    """
    # Extract grouping information from style properties
    group_values = style_props['group_series']
    shape_series = style_props.get('shape_series')

    # Check for continuous (numeric) color mapping
    has_continuous_color = (
        style_props.get('color_is_continuous', False) or
        style_props.get('fill_is_continuous', False)
    )

    # Check for categorical color/fill mapping
    # (must not be continuous to count as categorical grouping)
    has_color_grouping = (
        style_props['color_series'] is not None or
        style_props['fill_series'] is not None
    ) and not has_continuous_color

    has_shape_grouping = shape_series is not None

    # Common arguments for all builders
    args = (fig, plot, data, mapping, style_props, color_targets,
            payload, row, col, alpha, params)

    # Select strategy based on grouping scenario
    # Priority order matters: explicit group > color+shape > color > shape > continuous > none

    # Case 1: Explicit 'group' aesthetic takes highest priority
    if group_values is not None:
        return GroupedTraceBuilder(*args)

    # Case 2: Both color/fill AND shape are mapped to columns
    if has_color_grouping and has_shape_grouping:
        return ColorAndShapeTraceBuilder(*args)

    # Case 3: Only color/fill is mapped (categorical)
    if has_color_grouping:
        return ColorOnlyTraceBuilder(*args)

    # Case 4: Only shape is mapped
    if has_shape_grouping:
        return ShapeOnlyTraceBuilder(*args)

    # Case 5: Continuous color mapping (numeric values with colorscale)
    if has_continuous_color:
        return ContinuousColorTraceBuilder(*args)

    # Case 6: No grouping - single trace with all data
    return SingleTraceBuilder(*args)
