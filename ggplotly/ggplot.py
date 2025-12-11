# ggplot.py

import plotly.graph_objects as go
import plotly.express as px
import plotly.subplots as sp
from .aes import aes
from .geoms.geom_base import Geom
from .scales.scale_base import Scale
from .themes import Theme
from .facets import Facet
from .coords.coord_base import Coord
from .guides import Labs, Annotate, Guides
from .utils import Utils, ggsize
from .stats.stat_base import Stat
import copy


class ggplot:
    def __init__(self, data=None, mapping=None):
        """
        Initialize a ggplot object.

        Parameters:
            data (DataFrame): The dataset to plot. Can be None if geoms provide their own data.
            mapping (aes): Aesthetic mappings created by aes().
        """
        self.data = data.copy() if data is not None else None
        self.mapping = mapping.mapping if mapping else {}
        self.layers = []
        self.scales = []
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
        self.color_map = None
        self.is_geo = False  # Track if plot uses geographic coordinates

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

    def _repr_html_(self):
        """Return HTML representation for Jupyter/IPython display."""
        if self.auto_draw:
            fig = self.draw()
            # return fig._repr_html_()
            fig.show()
        return ""

    def add_stat(self, stat):
        """
        Add stat to last geom in layer list
        """
        geom = self.layers[-1].copy()
        geom = geom + stat
        self.layers[-1] = geom

    #     stat.data = self.data.copy()
    #     stat.mapping = self.mapping.copy()
    #     self.stats.append(stat)

    def add_geom(self, geom):
        """
        Add a geom (trace) to the ggplot object.
        Geoms will inherit the theme and other properties set on the plot.
        """

        if geom.data is None:
            geom.data = self.data.copy()

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
                    tgeom.data = self.data.copy()

                if tgeom.mapping is None:
                    tgeom.mapping = self.mapping
                else:
                    # Merge plot mapping and geom mapping, with geom mapping taking precedence
                    tgeom.mapping = {**self.mapping, **tgeom.mapping}

                tgeom.theme = self.theme

                self.layers.append(tgeom)
        else:
            self.layers.append(geom)

    def add_scale(self, scale):
        """
        Add a scale to the plot.

        Parameters:
            scale (Scale): The scale to add.
        """
        self.scales.append(scale)

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
        """
        if not hasattr(self, "fig"):
            raise AttributeError("No figure to save. Call draw() before saving.")

        if filepath.endswith(".html"):
            self.fig.write_html(filepath)
        elif filepath.endswith(".png"):
            self.fig.write_image(filepath)
        else:
            raise ValueError("Unsupported file format. Use .html or .png.")
