# layer.py
"""
Layer class for ggplotly.

A Layer is the fundamental unit of the Grammar of Graphics. It combines:
- Data: The dataset to visualize
- Mapping: Aesthetic mappings (x, y, color, etc.)
- Geom: The geometric object that renders the data
- Stat: Statistical transformation applied before rendering
- Position: Position adjustment (dodge, stack, etc.)

In ggplot2, every geom creates a layer, and stats can also create layers.
This class formalizes that relationship and provides a clean abstraction
for managing the rendering pipeline.

Why Layer?
----------
In ggplot2, the layer concept is central but often implicit. When you write:

    ggplot(df, aes(x='x', y='y')) + geom_point()

You're actually creating a layer with:
- geom = geom_point
- stat = stat_identity (default)
- data = df (inherited from plot)
- mapping = {x: 'x', y: 'y'} (inherited from plot)

This explicit Layer class allows:
1. Direct layer creation without going through geom functions
2. Custom stat+geom combinations
3. Clearer separation between data transformation (stat) and rendering (geom)
4. Better support for advanced layer manipulation

Usage Examples:
--------------
    # Simple layer with geom class
    layer = Layer(geom=geom_point, mapping=aes(x='x', y='y'))

    # Layer with stat transformation
    layer = Layer(geom=geom_line, stat=stat_smooth)

    # Layer with custom data
    layer = Layer(geom=geom_point, data=subset_df, mapping=aes(x='a', y='b'))

    # Using the convenience function
    lyr = layer(geom=geom_point, color='red')
"""

import copy

import pandas as pd

from .aes import aes


class Layer:
    """
    A layer in a ggplot visualization.

    A layer combines data, aesthetic mappings, a geometric object (geom),
    and an optional statistical transformation (stat) into a single unit
    that can be rendered on a plot.

    The Layer class follows the Grammar of Graphics architecture where:
    1. Data flows through the stat for transformation
    2. Transformed data is rendered by the geom
    3. Aesthetic mappings connect data columns to visual properties

    Attributes:
        geom: The geometric object (class or instance) for rendering
        stat: The statistical transformation (class or instance)
        data: DataFrame for this layer (or None to inherit from plot)
        mapping: Dict of aesthetic mappings
        position: Position adjustment strategy name
        inherit_aes: Whether to inherit aesthetics from the plot
        params: Additional parameters for geom and stat
        theme: Theme object for styling
    """

    def __init__(
        self,
        geom=None,
        stat=None,
        data=None,
        mapping=None,
        position='identity',
        inherit_aes=True,
        **params
    ):
        """
        Initialize a Layer.

        Parameters:
            geom: Geom class or instance for rendering. Can be:
                - A geom class (e.g., geom_point) - will be instantiated at draw time
                - A geom instance - will be used directly
                - None - will raise error at draw time

            stat: Stat class or instance for transformation. Can be:
                - A stat class (e.g., stat_smooth) - will be instantiated at compute time
                - A stat instance - will be used directly
                - None - no transformation (equivalent to stat_identity)

            data: DataFrame for this layer. If None, inherits from the plot.
                Layer-specific data allows different data sources in the same plot.

            mapping: Aesthetic mappings. Can be:
                - aes object: aes(x='col_a', y='col_b')
                - dict: {'x': 'col_a', 'y': 'col_b'}
                - None: no layer-specific mappings (inherit from plot)

            position: Position adjustment strategy name:
                - 'identity': No adjustment (default)
                - 'dodge': Dodge overlapping elements side-by-side
                - 'stack': Stack overlapping elements
                - 'fill': Stack and normalize to fill

            inherit_aes: Whether to inherit aesthetics from the plot.
                - True (default): Layer mapping extends plot mapping
                - False: Layer mapping replaces plot mapping entirely

            **params: Additional parameters passed to geom and stat.
                Common parameters include: color, size, alpha, linetype, etc.
        """
        # Store the geom (class or instance)
        self.geom = geom

        # Store the stat (class or instance, or None for identity)
        self.stat = stat

        # Store layer-specific data (may be None to inherit)
        self._data = data

        # Position adjustment strategy
        self.position = position

        # Whether to inherit aesthetics from the plot
        self.inherit_aes = inherit_aes

        # Additional parameters for geom/stat (color, size, etc.)
        self.params = params

        # Theme will be set when layer is added to plot
        self.theme = None

        # Handle mapping - normalize to dict format
        # We accept both aes objects and plain dicts for flexibility
        if mapping is None:
            self._mapping = {}
        elif isinstance(mapping, aes):
            # Extract dict from aes object and copy to avoid mutation
            self._mapping = mapping.mapping.copy()
        elif isinstance(mapping, dict):
            # Copy dict to avoid external mutation
            self._mapping = mapping.copy()
        else:
            raise TypeError(f"mapping must be aes or dict, got {type(mapping)}")

        # Global color/shape maps for consistent colors across facets.
        # These are set by the plot when using faceting to ensure that
        # the same category gets the same color in all facet panels.
        self._global_color_map = None
        self._global_shape_map = None

    # =========================================================================
    # Properties for data and mapping access
    # =========================================================================

    @property
    def data(self):
        """
        Get the layer's data.

        Returns:
            DataFrame or None: The layer's data, or None if inheriting from plot.
        """
        return self._data

    @data.setter
    def data(self, value):
        """
        Set the layer's data.

        Parameters:
            value: DataFrame or None to clear layer-specific data.
        """
        self._data = value

    @property
    def mapping(self):
        """
        Get the layer's aesthetic mappings.

        Returns:
            dict: Mapping of aesthetic names to column names.
        """
        return self._mapping

    @mapping.setter
    def mapping(self, value):
        """
        Set the layer's aesthetic mappings.

        Accepts either an aes object or a dict. The value is copied
        to prevent external mutation.

        Parameters:
            value: aes object, dict, or other (stored directly).
        """
        if isinstance(value, aes):
            self._mapping = value.mapping.copy()
        elif isinstance(value, dict):
            self._mapping = value.copy()
        else:
            # Allow direct assignment for special cases
            self._mapping = value

    # =========================================================================
    # Layer operations
    # =========================================================================

    def copy(self):
        """
        Create a deep copy of this layer.

        Deep copy ensures that modifying the copy doesn't affect the original.
        This is important for the ggplot __add__ pattern where we return
        a new object rather than modifying in place.

        Returns:
            Layer: A new Layer instance with all attributes copied.
        """
        return copy.deepcopy(self)

    def setup_data(self, plot_data, plot_mapping):
        """
        Set up the layer's data by combining plot-level and layer-level data/mappings.

        This method implements the data inheritance rules:
        1. If layer has data, use it; otherwise use plot data
        2. If inherit_aes=True, combine plot and layer mappings (layer takes precedence)
        3. If inherit_aes=False, use only layer mappings

        This is called by the plot before drawing to prepare the layer.

        Parameters:
            plot_data: The plot's default DataFrame.
            plot_mapping: The plot's default aesthetic mappings dict.

        Returns:
            DataFrame: The prepared data for this layer (also stored in self._data).
        """
        # Determine which data to use
        # Layer data takes precedence if provided
        if self._data is not None:
            data = self._data.copy()  # Copy to avoid mutating original
        elif plot_data is not None:
            data = plot_data.copy()
        else:
            data = None

        # Combine mappings based on inherit_aes setting
        if self.inherit_aes:
            # Layer mappings extend plot mappings (layer takes precedence)
            # Example: plot has {x:'a', y:'b'}, layer has {color:'c'}
            # Result: {x:'a', y:'b', color:'c'}
            combined_mapping = {**plot_mapping, **self._mapping}
        else:
            # Layer mappings completely replace plot mappings
            combined_mapping = self._mapping.copy()

        # Store the combined values
        self._mapping = combined_mapping
        self._data = data

        return data

    def compute_stat(self, data):
        """
        Apply the statistical transformation to the data.

        Stats transform data before it's rendered by the geom. For example:
        - stat_bin: Bins continuous data into discrete bins
        - stat_smooth: Computes a smoothing line
        - stat_density: Computes kernel density estimate

        If no stat is set (None), the data is returned unchanged
        (equivalent to stat_identity).

        Parameters:
            data: DataFrame to transform.

        Returns:
            DataFrame: Transformed data ready for rendering.
        """
        # No stat = identity transformation
        if self.stat is None:
            return data

        # Handle both class and instance for stat
        if isinstance(self.stat, type):
            # Stat is a class - instantiate with mapping and params
            stat_instance = self.stat(mapping=self._mapping, **self.params)
        else:
            # Stat is already an instance
            stat_instance = self.stat

        # Apply the stat transformation
        # Stats return (result, new_mapping) tuple
        result, new_mapping = stat_instance.compute(data)

        # Handle different result types from stats
        if isinstance(result, dict):
            # Some stats return dict with arrays (e.g., stat_contour)
            # Convert to DataFrame for consistent handling
            result = pd.DataFrame(result)

        # Update mapping if stat returns new column names
        # This allows stats to rename columns (e.g., x -> density)
        if new_mapping:
            self._mapping.update(new_mapping)

        return result

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the layer on the figure.

        This is the main rendering method. It:
        1. Applies the stat transformation (if any)
        2. Instantiates the geom (if it's a class)
        3. Passes through styling configuration
        4. Calls the geom's draw method

        Parameters:
            fig: Plotly figure object to draw on.
            data: Optional data subset (used for faceting). If None, uses layer data.
            row: Row position in subplot grid (1-indexed, for faceting).
            col: Column position in subplot grid (1-indexed, for faceting).

        Raises:
            ValueError: If no geom is set on the layer.
        """
        # Use provided data (for faceting) or fall back to layer data
        draw_data = data if data is not None else self._data

        # Apply stat transformation to prepare data for rendering
        if self.stat is not None:
            draw_data = self.compute_stat(draw_data)

        # Validate that we have a geom
        if self.geom is None:
            raise ValueError("Layer must have a geom to draw")

        # Get or instantiate the geom
        if isinstance(self.geom, type):
            # Geom is a class - create new instance with our configuration
            geom_instance = self.geom(
                data=draw_data,
                mapping=aes(**self._mapping),
                **self.params
            )
        else:
            # Geom is already an instance - update its state
            geom_instance = self.geom
            geom_instance.data = draw_data
            geom_instance.mapping = self._mapping

        # Pass through global maps for consistent colors in faceted plots
        # These ensure the same category gets the same color across all panels
        geom_instance._global_color_map = self._global_color_map
        geom_instance._global_shape_map = self._global_shape_map
        geom_instance.theme = self.theme

        # Delegate to the geom's draw method
        geom_instance.draw(fig, draw_data, row, col)

    # =========================================================================
    # Factory methods
    # =========================================================================

    @classmethod
    def from_geom(cls, geom):
        """
        Create a Layer from an existing Geom instance.

        This factory method wraps a Geom in a Layer, preserving all its
        configuration. Useful for converting the current geom-based API
        to the layer-based model.

        The method extracts:
        - The geom instance itself
        - The first stat (if any)
        - Data and mapping
        - All params
        - Global color/shape maps
        - Theme

        Parameters:
            geom: A Geom instance to wrap.

        Returns:
            Layer: A new Layer wrapping the geom with its full configuration.

        Example:
            >>> geom = geom_point(data=df, mapping=aes(x='x', y='y'), color='red')
            >>> lyr = Layer.from_geom(geom)
            >>> # lyr now contains all of geom's configuration
        """
        # Extract the first stat from the geom's stats list (if any)
        stat = geom.stats[0] if geom.stats else None

        # Create layer with geom's configuration
        layer = cls(
            geom=geom,
            stat=stat,
            data=geom.data,
            mapping=geom.mapping,
            **geom.params
        )

        # Copy over global maps that may have been set for faceting
        layer._global_color_map = getattr(geom, '_global_color_map', None)
        layer._global_shape_map = getattr(geom, '_global_shape_map', None)
        layer.theme = getattr(geom, 'theme', None)

        return layer

    # =========================================================================
    # String representation
    # =========================================================================

    def __repr__(self):
        """
        String representation of the layer.

        Shows the geom type, stat type, and mapping for debugging.
        Handles both class and instance forms of geom/stat.

        Returns:
            str: Human-readable representation like
                 "Layer(geom=geom_point, stat=identity, mapping={'x': 'mpg'})"
        """
        # Get geom name - handle both class and instance
        if self.geom is None:
            geom_name = 'None'
        elif isinstance(self.geom, type):
            # It's a class, use __name__
            geom_name = self.geom.__name__
        else:
            # It's an instance, use class name
            geom_name = self.geom.__class__.__name__

        # Get stat name - handle both class and instance
        if self.stat is None:
            stat_name = 'identity'  # No stat = identity transformation
        elif isinstance(self.stat, type):
            stat_name = self.stat.__name__
        else:
            stat_name = self.stat.__class__.__name__

        return f"Layer(geom={geom_name}, stat={stat_name}, mapping={self._mapping})"


# =============================================================================
# Convenience function
# =============================================================================

def layer(
    geom=None,
    stat=None,
    data=None,
    mapping=None,
    position='identity',
    inherit_aes=True,
    **params
):
    """
    Create a new layer.

    This is a convenience function that creates a Layer instance.
    It matches the ggplot2 layer() function signature for familiarity.

    Use this when you need more control than the standard geom_* functions
    provide, such as:
    - Custom stat+geom combinations
    - Explicit position adjustment
    - Non-inheriting aesthetics

    Parameters:
        geom: Geom class or instance for rendering.
        stat: Stat class or instance for transformation.
        data: DataFrame for this layer.
        mapping: Aesthetic mappings (dict or aes object).
        position: Position adjustment strategy.
        inherit_aes: Whether to inherit aesthetics from the plot.
        **params: Additional parameters for geom and stat.

    Returns:
        Layer: A new Layer instance ready to add to a plot.

    Examples:
        >>> # Equivalent to geom_point()
        >>> layer(geom=geom_point)

        >>> # With stat transformation (smoothed line)
        >>> layer(geom=geom_line, stat=stat_smooth, mapping=aes(x='x', y='y'))

        >>> # Non-inheriting layer with custom data
        >>> layer(geom=geom_point, data=other_df, mapping=aes(x='a', y='b'),
        ...       inherit_aes=False, color='red')
    """
    return Layer(
        geom=geom,
        stat=stat,
        data=data,
        mapping=mapping,
        position=position,
        inherit_aes=inherit_aes,
        **params
    )
