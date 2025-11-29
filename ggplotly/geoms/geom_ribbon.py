# geoms/geom_ribbon.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd
from .geom_line import geom_line
from ..aes import aes

# geoms/geom_ribbon.py

import plotly.graph_objects as go
import plotly.express as px


class geom_ribbon(Geom):
    """
    Geom for drawing ribbon plots.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        ymin (float): Minimum y value for the ribbon.
        ymax (float): Maximum y value for the ribbon.
        fill (str, optional): Fill color for the ribbon.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        group (str, optional): Grouping variable for the ribbon.
    """

    __name__ = "geom_ribbon"

    def before_add(self):
        # Use color from params if specified, otherwise let geom_line use defaults
        color = self.params.get("color", None)
        fill = self.params.get("fill", None)

        # Filter out color and fill from other params
        other_params = {k: v for k, v in self.params.items() if k not in ['color', 'fill']}

        # Create aes mappings for the ribbon layers
        # aes() expects column names as values, so use self.mapping which contains the column names
        min_aes = aes(**{k: v for k, v in self.mapping.items() if k in ['x']})
        min_aes.mapping['y'] = self.mapping['ymin']

        max_aes = aes(**{k: v for k, v in self.mapping.items() if k in ['x']})
        max_aes.mapping['y'] = self.mapping['ymax']

        # Build layers with explicit data if this ribbon has explicit data
        layer_data = self.data if hasattr(self, '_has_explicit_data') and self._has_explicit_data else None

        if color is not None:
            # User specified a color
            self.layers = [
                geom_line(layer_data, min_aes, color=color, **other_params),
                geom_line(layer_data, max_aes, color=color, fill="tonexty", **other_params),
            ]
        elif fill is not None:
            # User specified a fill color
            self.layers = [
                geom_line(layer_data, min_aes, color=fill, **other_params),
                geom_line(layer_data, max_aes, color=fill, fill="tonexty", **other_params),
            ]
        else:
            # No color specified - let geom_line use its defaults
            self.layers = [
                geom_line(layer_data, min_aes, **other_params),
                geom_line(layer_data, max_aes, fill="tonexty", **other_params),
            ]

        return self

    def setup_data(self, data, plot_mapping):
        """
        Override setup_data to propagate data to child layers.

        Parameters:
            data (DataFrame): The dataset to use.
            plot_mapping (dict): The global aesthetic mappings from the plot.
        """
        # Call parent setup_data to handle this geom
        super().setup_data(data, plot_mapping)

        # Propagate to child layers
        for layer in self.layers:
            layer.setup_data(data, plot_mapping)

    def draw(self, fig, data=None, row=1, col=1):
        pass
