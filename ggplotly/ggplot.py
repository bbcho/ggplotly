# ggplot.py

import copy

import plotly.graph_objects as go
import plotly.subplots as sp

from .aes import aes
from .coords.coord_base import Coord
from .data_utils import INDEX_COLUMN, normalize_data
from .facets import Facet
from .geoms.geom_base import Geom
from .guides import Annotate, Guides, Labs
from .scales.scale_base import Scale, ScaleRegistry
from .stats.stat_base import Stat
from .themes import Theme
from .utils import Utils, ggsize


class ggplot:
    def __init__(self, data=None, mapping=None):
        """
        Initialize a ggplot object.

        Parameters:
            data (DataFrame or Series): The dataset to plot. Can be None if geoms provide
                their own data. Supports automatic index handling:

                - Series: Converted to DataFrame with values as y and index as x
                - DataFrame: Index can be referenced using x='index' in aes()

            mapping (aes): Aesthetic mappings created by aes(). Supports index references:

                - x='index': Explicitly use the DataFrame/Series index as x-axis
                - If x is omitted but y is specified, x defaults to the index
                - Named indices (df.index.name) are used as axis labels

        Examples:
            # Explicit index reference
            >>> df = pd.DataFrame({'y': [1, 2, 3]}, index=[10, 20, 30])
            >>> ggplot(df, aes(x='index', y='y')) + geom_point()

            # Auto-populate x from index (same result as above)
            >>> ggplot(df, aes(y='y')) + geom_point()

            # Series input (x=index, y=values automatically)
            >>> s = pd.Series([1, 2, 3], index=['a', 'b', 'c'], name='values')
            >>> ggplot(s) + geom_point()

            # Named index becomes axis label
            >>> df.index.name = 'time'
            >>> ggplot(df, aes(y='y')) + geom_point()  # x-axis labeled 'time'

            # Explicit x column takes precedence over index
            >>> df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
            >>> ggplot(df, aes(x='x', y='y')) + geom_point()  # uses column 'x'
        """
        # Extract mapping dict from aes object
        mapping_dict = mapping.mapping if mapping else {}

        # Normalize data (handles Series, index references, auto-x)
        normalized_data, normalized_mapping, index_name = normalize_data(data, mapping_dict)

        self.data = normalized_data
        self.mapping = normalized_mapping
        self._index_name = index_name  # Store for axis labeling
        self.layers = []
        self._scale_registry = ScaleRegistry()  # Use registry for scale management
        self.stats = []
        self.theme = Theme()
        self.facets = None
        self.coords = []  # List of coordinate transformations
        self.labs = None  # Initialize labs
        self.size = None  # Initialize size
        self.annotations = []  # Initialize annotations list
        self.guides_obj = None  # Initialize guides
        self.fig = go.Figure()
        self.auto_draw = True  # Automatically draw after adding components by default

    def copy(self):
        """
        Create a deep copy of the ggplot object.

        Returns:
            ggplot: A copy of the ggplot object.
        """
        return copy.deepcopy(self)

    def add_component(self, component):
        """
        Add a component (geom, scale, theme, etc.) to the plot.

        Parameters:
            component: The component to add.
        """
        if isinstance(component, Geom):
            self.add_geom(component)
        elif isinstance(component, Scale):
            self.add_scale(component)
        elif isinstance(component, Theme):
            self.set_theme(component)
        elif isinstance(component, Facet):
            self.set_facets(component)
        elif isinstance(component, Coord):
            self.set_coords(component)
        elif isinstance(component, Labs):
            self.labs = component
        elif isinstance(component, Annotate):
            self.annotations.append(component)
        elif isinstance(component, Guides):
            self.guides_obj = component
        elif isinstance(component, Utils):
            component.apply(self)
        elif isinstance(component, ggsize):
            self.size = component
        elif isinstance(component, Stat):
            self.add_stat(component)
        else:
            raise TypeError("Unsupported component")

    def __add__(self, other):
        self.add_component(other)
        return self.copy()

    def _needs_mathjax(self):
        """Check if any geom uses parse=True for LaTeX rendering."""
        for geom in self.layers:
            if geom.params.get('parse', False):
                return True
        return False

    def _repr_html_(self):
        """Return HTML representation for Jupyter/IPython display."""
        if self.auto_draw:
            fig = self.draw()
            # Only include MathJax CDN if parse=True is used (for LaTeX rendering)
            if self._needs_mathjax():
                return fig.to_html(full_html=False, include_plotlyjs='cdn', include_mathjax='cdn')
            return fig._repr_html_()
        return ""

    def _repr_mimebundle_(self, **kwargs):
        """Return MIME bundle for Jupyter display (preferred by VS Code, JupyterLab)."""
        if self.auto_draw:
            fig = self.draw()
            # Only include MathJax CDN if parse=True is used (for LaTeX rendering)
            if self._needs_mathjax():
                html = fig.to_html(full_html=False, include_plotlyjs='cdn', include_mathjax='cdn')
                return {'text/html': html}
            bundle = fig._repr_mimebundle_(**kwargs)
            if 'text/html' not in bundle:
                bundle['text/html'] = fig._repr_html_()
            return bundle
        return {}

    def add_stat(self, stat):
        """
        Add stat as a new layer with its own geom.

        In ggplot2, stats create their own layer rather than modifying the previous one.
        The stat's 'geom' parameter determines which geom to use for rendering.
        """
        import inspect

        from . import geoms as geoms_module

        # Get the geom class from stat's geom parameter
        geom_name = getattr(stat, 'geom', 'point')
        geom_class_name = f'geom_{geom_name}'

        # Dynamically get the geom class from the geoms module
        if hasattr(geoms_module, geom_class_name):
            geom_class = getattr(geoms_module, geom_class_name)
        else:
            # Fallback to geom_point if the specified geom doesn't exist
            geom_class = geoms_module.geom_point

        # Get stat-specific params by inspecting the stat's __init__ signature
        # These are params defined on the stat class, not general geom params
        stat_init_params = set(inspect.signature(stat.__class__.__init__).parameters.keys())
        stat_init_params.discard('self')
        stat_init_params.discard('data')
        stat_init_params.discard('mapping')
        stat_init_params.discard('params')
        stat_init_params.discard('kwargs')

        # Also exclude 'geom' as it's used to select the geom class, not passed to it
        stat_init_params.add('geom')

        # Extract params that should be passed to the geom (exclude stat-specific params)
        geom_params = {k: v for k, v in stat.params.items() if k not in stat_init_params}

        # Create a new geom with the stat's params
        geom_data = self.data.copy() if self.data is not None else None
        new_geom = geom_class(data=geom_data, mapping=aes(**self.mapping), **geom_params)

        # Copy stat's mapping and data before attaching
        stat_copy = stat.copy()
        stat_copy.mapping = {**self.mapping, **stat.mapping}
        stat_copy.data = geom_data

        new_geom.stats = [stat_copy]

        self.add_geom(new_geom)

    def add_geom(self, geom):
        """
        Add a geom (trace) to the ggplot object.
        Geoms will inherit the theme and other properties set on the plot.
        """

        if geom.data is None:
            geom.data = self.data.copy() if self.data is not None else None
        else:
            # Geom has its own data - normalize it with combined mapping
            geom_mapping = geom.mapping or {}
            combined_mapping = {**self.mapping, **geom_mapping}
            geom.data, normalized_mapping, _ = normalize_data(geom.data, combined_mapping)
            # Only update geom.mapping with the geom-specific parts that were normalized
            geom.mapping = {k: normalized_mapping[k] for k in geom_mapping if k in normalized_mapping}

        if geom.mapping is None:
            geom.mapping = self.mapping
        else:
            # Merge plot mapping and geom mapping, with geom mapping taking precedence
            geom.mapping = {**self.mapping, **geom.mapping}

        geom.theme = self.theme  # Pass the theme to the geom

        if hasattr(geom, "before_add"):
            geom = geom.before_add()

        if len(geom.layers) > 0:
            for tgeom in geom.layers:
                if tgeom.data is None:
                    tgeom.data = self.data.copy() if self.data is not None else None
                else:
                    # Normalize geom-specific data
                    tgeom_mapping = tgeom.mapping or {}
                    combined_mapping = {**self.mapping, **tgeom_mapping}
                    tgeom.data, normalized_mapping, _ = normalize_data(tgeom.data, combined_mapping)
                    tgeom.mapping = {k: normalized_mapping[k] for k in tgeom_mapping if k in normalized_mapping}

                if tgeom.mapping is None:
                    tgeom.mapping = self.mapping
                else:
                    # Merge plot mapping and geom mapping, with geom mapping taking precedence
                    tgeom.mapping = {**self.mapping, **tgeom.mapping}

                tgeom.theme = self.theme

                self.layers.append(tgeom)
        else:
            self.layers.append(geom)

    @property
    def scales(self):
        """Return scales as a list for backward compatibility."""
        return self._scale_registry.to_list()

    def add_scale(self, scale):
        """
        Add a scale to the plot.

        If a scale already exists for the same aesthetic, it will be replaced
        with a warning (matching ggplot2 behavior).

        Parameters:
            scale (Scale): The scale to add.
        """
        self._scale_registry.add(scale)

    def set_theme(self, theme):
        """
        Set the theme for the plot.

        Parameters:
            theme (Theme): The theme to apply.
        """
        self.theme = theme
        self.theme.apply(self.fig)

    def set_facets(self, facets):
        """
        Set the facets for the plot.

        Parameters:
            facets (Facet): The facet to apply.
        """
        self.facets = facets

    def set_coords(self, coords):
        """
        Add a coordinate transformation to the plot.

        Parameters:
            coords (Coord): The coordinate system to apply.
        """
        self.coords.append(coords)

    def draw(self):
        """
        Render the plot.

        Returns:
            go.Figure: The Plotly figure object.
        """
        # Initialize the figure with subplots
        if self.facets:
            # Faceting is applied; the facet's apply method will handle subplot creation
            self.fig = self.facets.apply(self)
        else:
            # No faceting; create a single-subplot figure
            self.fig = sp.make_subplots(rows=1, cols=1)

            # Draw all geoms on the main figure
            for geom in self.layers:
                geom.draw(self.fig, row=1, col=1)

        # Apply scales after plotting the geoms
        for scale in self.scales:
            scale.apply(self.fig)

        # Apply coordinate transformations (xlim, ylim, etc.) after scales
        for coord in self.coords:
            coord.apply(self.fig)

        # Apply theme
        self.theme.apply(self.fig)

        # Apply labels
        if self.labs:
            self.labs.apply(self.fig)

        # Set default x-axis label if using index and no explicit label set
        if (self.mapping.get('x') == INDEX_COLUMN and
            self._index_name and
            (not self.labs or not hasattr(self.labs, 'x') or self.labs.x is None)):
            self.fig.update_xaxes(title_text=self._index_name)

        # Apply guides
        if self.guides_obj:
            self.guides_obj.apply(self.fig)

        # Apply annotations
        for annotation in self.annotations:
            annotation.apply(self.fig)

        # Apply resizing
        if self.size:
            self.size.apply(self)

        # Show the plot
        return self.fig

    def show(self):
        """
        Show the current plot in the default viewer.

        Returns:
            None
        """
        self.draw().show()

    def save(self, filepath):
        """
        Save the current plot to a file (e.g., HTML, PNG).

        Parameters:
            filepath (str): The file path where the plot should be saved.

        Note:
            HTML files use CDN references for Plotly.js and MathJax, resulting
            in small file sizes (~8KB) but requiring internet for viewing.
            MathJax CDN enables LaTeX rendering (e.g., geom_text with parse=True).
        """
        if not hasattr(self, "fig"):
            raise AttributeError("No figure to save. Call draw() before saving.")

        if filepath.endswith(".html"):
            self.fig.write_html(filepath, include_plotlyjs='cdn', include_mathjax='cdn')
        elif filepath.endswith(".png"):
            self.fig.write_image(filepath)
        else:
            raise ValueError("Unsupported file format. Use .html or .png.")
