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
        color = self.params.get("color", "grey")
        self.layers = [
            geom_line(
                aes(x=self.mapping["x"], y=self.mapping["ymin"], color=color),
                **self.params
            ),
            geom_line(
                aes(x=self.mapping["x"], y=self.mapping["ymax"], color=color),
                fill="tonexty",
                **self.params
            ),
        ]

        return self

    def draw(self, fig, data=None, row=1, col=1):
        pass
