import copy

from ..aes import aes
from ..aesthetic_mapper import AestheticMapper
from ..trace_builders import get_trace_builder


class Geom:
    """
    Base class for all geoms (geometric objects).

    Geoms are the visual elements that represent data on a plot, such as
    points, lines, bars, etc. Each geom subclass implements a specific
    visual representation.

    Parameters:
        data (DataFrame, optional): Data to use for this geom. If None,
            uses the data from the ggplot object.
        mapping (aes, optional): Aesthetic mappings for this geom.
        **params: Additional parameters passed to the geom.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point()
        >>> ggplot(df, aes(x='x', y='y')) + geom_point(color='red', size=3)
    """

    # Default parameters for this geom. Subclasses should override this.
    default_params: dict = {}

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the geom.

        Parameters:
            data (DataFrame or aes, optional): Data for this geom, or an aes object.
            mapping (aes, optional): Aesthetic mappings for this geom.
            **params: Additional visual parameters (color, size, alpha, etc.).
        """
        # check to see if data was passed first or if aes was passed first
        if isinstance(data, aes):
            self.mapping = data.mapping
            self.data = None
        else:
            self.data = data
            self.mapping = mapping.mapping if mapping else {}

        # Merge default params with user-provided params (user params take precedence)
        self.params = {**self.default_params, **params}

        # Handle parameter aliases for ggplot2 compatibility
        # linewidth is an alias for size (line width in ggplot2 3.4+)
        if "linewidth" in self.params and "size" not in params:
            self.params["size"] = self.params["linewidth"]

        self.stats = []
        self.layers = []
        # Track whether this geom has explicit data or inherited from plot
        self._has_explicit_data = data is not None and not isinstance(data, aes)
        # Global color/shape maps for consistent colors across facets
        self._global_color_map = None
        self._global_shape_map = None

    # def __add__(self, other):
    #     if isinstance(other, Geom):
    #         self.layers.append(other)

    #     return self.copy()
    # else:
    # raise ValueError("Only Geom and Stat objects can be added to Geom objects.")

    def copy(self):
        """
        Create a deep copy of this geom.

        Returns:
            Geom: A new geom instance with copied data and stats.
        """
        new = copy.deepcopy(self)
        new.stats = [*self.stats.copy()]
        return new

    def setup_data(self, data, plot_mapping):
        """
        Combine plot mapping with geom-specific mapping and set data.

        Parameters:
            data (DataFrame): The dataset to use.
            plot_mapping (dict): The global aesthetic mappings from the plot.

        Returns:
            None: Modifies the geom in place.
        """
        # Merge plot mapping and geom mapping, with geom mapping taking precedence
        combined_mapping = {**plot_mapping, **self.mapping}
        self.mapping = combined_mapping
        self.data = data.copy()

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the geometry on the figure.

        This method applies any attached stats to transform the data,
        then delegates to _draw_impl for the actual rendering.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot (for faceting). Default is 1.
            col (int): Column position in subplot (for faceting). Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Apply any stats to transform the data
        data = self._apply_stats(data)

        # Delegate to subclass implementation
        self._draw_impl(fig, data, row, col)

    def _apply_stats(self, data):
        """
        Apply all attached stats to transform the data.

        Parameters:
            data (DataFrame): Input data.

        Returns:
            DataFrame: Transformed data after all stats applied.
        """
        for stat in self.stats:
            data, self.mapping = stat.compute(data)
        return data

    def _draw_impl(self, fig, data, row, col):
        """
        Implementation of the actual drawing logic.

        Subclasses should override this method instead of draw().

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Data (already transformed by stats).
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).

        Raises:
            NotImplementedError: Must be implemented by subclasses.
        """
        raise NotImplementedError("The _draw_impl method must be implemented by subclasses.")

    def _get_style_props(self, data):
        """
        Get style properties from aesthetic mapper.

        This is a convenience method to reduce boilerplate in geom subclasses.

        Parameters:
            data (DataFrame): The data to use for aesthetic mapping.

        Returns:
            dict: Style properties from AestheticMapper.
        """
        mapper = AestheticMapper(
            data, self.mapping, self.params, self.theme,
            global_color_map=self._global_color_map,
            global_shape_map=self._global_shape_map
        )
        return mapper.get_style_properties()

    def _apply_color_targets(self, target_props: dict, style_props: dict, value_key=None, data_mask=None, shape_key=None) -> dict:
        """
        Apply color/fill/size/shape to trace properties based on target mapping.

        Parameters:
            target_props: Dict mapping aesthetics to trace property names
                         e.g., {'color': 'marker_color', 'size': 'marker_size', 'shape': 'marker_symbol'}
            style_props: Style properties from AestheticMapper
            value_key: Optional key for looking up color from color_map
            data_mask: Optional boolean mask to filter size series data
            shape_key: Optional key for looking up shape from shape_map

        Returns:
            Dict of trace properties to apply
        """
        result = {}

        def is_valid_color(value):
            """Check if a value looks like a valid color (not a column name)."""
            if value is None:
                return False
            if not isinstance(value, str):
                return False
            # Check for common color formats
            if value.startswith('#'):
                return True
            if value.startswith('rgb') or value.startswith('hsl'):
                return True
            # Check against a list of known CSS color names
            # This is safer than heuristics since column names like 'group', 'species', etc.
            # could otherwise be mistaken for colors
            css_colors = {
                'aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
                'beige', 'bisque', 'black', 'blanchedalmond', 'blue', 'blueviolet',
                'brown', 'burlywood', 'cadetblue', 'chartreuse', 'chocolate',
                'coral', 'cornflowerblue', 'cornsilk', 'crimson', 'cyan',
                'darkblue', 'darkcyan', 'darkgoldenrod', 'darkgray', 'darkgreen',
                'darkgrey', 'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
                'darkorchid', 'darkred', 'darksalmon', 'darkseagreen', 'darkslateblue',
                'darkslategray', 'darkslategrey', 'darkturquoise', 'darkviolet',
                'deeppink', 'deepskyblue', 'dimgray', 'dimgrey', 'dodgerblue',
                'firebrick', 'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
                'ghostwhite', 'gold', 'goldenrod', 'gray', 'green', 'greenyellow',
                'grey', 'honeydew', 'hotpink', 'indianred', 'indigo', 'ivory',
                'khaki', 'lavender', 'lavenderblush', 'lawngreen', 'lemonchiffon',
                'lightblue', 'lightcoral', 'lightcyan', 'lightgoldenrodyellow',
                'lightgray', 'lightgreen', 'lightgrey', 'lightpink', 'lightsalmon',
                'lightseagreen', 'lightskyblue', 'lightslategray', 'lightslategrey',
                'lightsteelblue', 'lightyellow', 'lime', 'limegreen', 'linen',
                'magenta', 'maroon', 'mediumaquamarine', 'mediumblue', 'mediumorchid',
                'mediumpurple', 'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
                'mediumturquoise', 'mediumvioletred', 'midnightblue', 'mintcream',
                'mistyrose', 'moccasin', 'navajowhite', 'navy', 'oldlace', 'olive',
                'olivedrab', 'orange', 'orangered', 'orchid', 'palegoldenrod',
                'palegreen', 'paleturquoise', 'palevioletred', 'papayawhip',
                'peachpuff', 'peru', 'pink', 'plum', 'powderblue', 'purple',
                'rebeccapurple', 'red', 'rosybrown', 'royalblue', 'saddlebrown',
                'salmon', 'sandybrown', 'seagreen', 'seashell', 'sienna', 'silver',
                'skyblue', 'slateblue', 'slategray', 'slategrey', 'snow',
                'springgreen', 'steelblue', 'tan', 'teal', 'thistle', 'tomato',
                'turquoise', 'violet', 'wheat', 'white', 'whitesmoke', 'yellow',
                'yellowgreen'
            }
            return value.lower() in css_colors

        # Determine the color to use
        if value_key is not None:
            # Looking up color for a specific category
            if style_props['color_series'] is not None:
                color_value = style_props['color_map'].get(value_key)
            elif style_props['fill_series'] is not None:
                color_value = style_props['fill_map'].get(value_key)
            else:
                # Handle None explicitly for literal values
                color_value = style_props.get('color') if style_props.get('color') is not None else \
                             style_props.get('fill') if style_props.get('fill') is not None else \
                             style_props['default_color']
        else:
            # Use literal value or default (handle None explicitly)
            # Only use color/fill if they're actual colors, not column names that couldn't be resolved
            color_val = style_props.get('color')
            fill_val = style_props.get('fill')

            # If there's a color_series or fill_series, the color/fill value is a column name, not a color
            # In that case, use the default color instead
            if style_props.get('color_series') is not None or style_props.get('fill_series') is not None:
                # There's a mapping but we don't have a value_key - use default
                color_value = style_props['default_color']
            elif color_val is not None and is_valid_color(color_val):
                color_value = color_val
            elif fill_val is not None and is_valid_color(fill_val):
                color_value = fill_val
            else:
                color_value = style_props['default_color']

        # Apply to appropriate trace properties
        for aesthetic, trace_prop in target_props.items():
            if aesthetic == 'color' or aesthetic == 'fill':
                result[trace_prop] = color_value
            elif aesthetic == 'size':
                # Check if size is mapped to a column (series) or is a literal value
                if style_props['size_series'] is not None:
                    # Size is mapped to a column - use the series data
                    if data_mask is not None:
                        result[trace_prop] = style_props['size_series'][data_mask]
                    else:
                        result[trace_prop] = style_props['size_series']
                else:
                    # Size is a literal value
                    result[trace_prop] = style_props['size']
            elif aesthetic == 'shape':
                # Determine shape to use
                if shape_key is not None and style_props.get('shape_map'):
                    result[trace_prop] = style_props['shape_map'].get(shape_key, 'circle')
                elif style_props.get('shape') is not None and style_props.get('shape_series') is None:
                    # Literal shape value
                    result[trace_prop] = style_props['shape']
                else:
                    # Default shape
                    result[trace_prop] = 'circle'

        return result

    def _transform_fig(
        self, plot, fig, data, payload, color_targets, row, col, **layout
    ):
        """
        Transform data into Plotly traces using the appropriate builder strategy.

        This method delegates trace building to specialized TraceBuilder classes
        based on the grouping strategy (by group, color, shape, continuous, etc.).

        Parameters:
            plot: Plotly graph object class (e.g., go.Scatter)
            fig: Plotly figure object
            data: DataFrame with the data to plot
            payload: Additional trace parameters
            color_targets: Dict mapping aesthetics to trace property names
            row: Row position in subplot
            col: Column position in subplot
            **layout: Additional layout parameters
        """
        # Create aesthetic mapper for this geom, passing global maps for faceting
        mapper = AestheticMapper(
            data, self.mapping, self.params, self.theme,
            global_color_map=self._global_color_map,
            global_shape_map=self._global_shape_map
        )
        style_props = mapper.get_style_properties()
        alpha = style_props['alpha']

        # Get the appropriate trace builder and build traces
        builder = get_trace_builder(
            fig=fig,
            plot=plot,
            data=data,
            mapping=self.mapping,
            style_props=style_props,
            color_targets=color_targets,
            payload=payload,
            row=row,
            col=col,
            alpha=alpha,
            params=self.params
        )
        builder.build(self._apply_color_targets)

        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(**layout)
