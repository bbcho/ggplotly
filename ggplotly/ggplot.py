# ggplot.py

import plotly.graph_objects as go
import plotly.subplots as sp
from .aes import aes
from .geoms.geom_base import Geom
from .scales.scale_base import Scale
from .themes import Theme
from .facets import Facet
from .coords.coord_base import Coord
from .guides import Labs


class ggplot:
    def __init__(self, data=None, mapping=None):
        """
        Initialize a ggplot object.

        Parameters:
            data (DataFrame): The dataset to plot.
            mapping (aes): Aesthetic mappings created by aes().
        """
        self.data = data
        self.mapping = mapping.mapping if mapping else {}
        self.layers = []
        self.scales = []
        self.theme = Theme()
        self.facets = None
        self.coords = Coord()
        self.labs = None  # Initialize labs
        self.fig = go.Figure()

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
        else:
            raise TypeError("Unsupported component")

    def __add__(self, other):
        self.add_component(other)
        return self

    def add_geom(self, geom):
        """
        Add a geom layer to the plot.

        Parameters:
            geom (Geom): The geom to add.
        """
        geom.setup_data(self.data, self.mapping)
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

    def set_facets(self, facets):
        """
        Set the facets for the plot.

        Parameters:
            facets (Facet): The facet to apply.
        """
        self.facets = facets

    def set_coords(self, coords):
        """
        Set the coordinate system for the plot.

        Parameters:
            coords (Coord): The coordinate system to apply.
        """
        self.coords = coords

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

            # Apply coordinate transformations before plotting
            self.coords.apply(self.fig)

            # Draw all geoms on the main figure
            for geom in self.layers:
                geom.draw(self.fig, row=1, col=1)

        # Apply scales after plotting the geoms
        for scale in self.scales:
            scale.apply(self.fig)

        # Apply theme
        self.theme.apply(self.fig)

        # Apply labels
        if self.labs:
            self.labs.apply(self.fig)

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
