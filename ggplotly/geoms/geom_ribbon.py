# geoms/geom_ribbon.py

from .geom_base import Geom
import plotly.graph_objects as go
import numpy as np
import plotly.express as px
import pandas as pd

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

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data
        x = data[self.mapping["x"]]
        ymin = data[self.mapping["ymin"]]
        ymax = data[self.mapping["ymax"]]
        group_values = data[self.mapping["group"]] if "group" in self.mapping else None
        alpha = self.params.get("alpha", 0.5)

        # Get shared color logic from the parent Geom class
        color_info = self.handle_colors(data, self.mapping, self.params)
        fill_color = color_info["fill_colors"]

        # Draw ribbon plot traces
        if group_values is not None:
            for group in group_values.unique():
                group_mask = group_values == group
                fig.add_trace(
                    go.Scatter(
                        x=np.concatenate([x[group_mask], x[group_mask][::-1]]),
                        y=np.concatenate([ymax[group_mask], ymin[group_mask][::-1]]),
                        fill="toself",
                        fillcolor=(
                            group_values[group_mask].iloc[0]
                            if group_values is not None
                            else fill_color
                        ),
                        line=dict(color="rgba(0,0,0,0)"),
                        opacity=alpha,
                        name=str(group),
                    ),
                    row=row,
                    col=col,
                )
        else:
            fig.add_trace(
                go.Scatter(
                    x=np.concatenate([x, x[::-1]]),
                    y=np.concatenate([ymax, ymin[::-1]]),
                    fill="toself",
                    fillcolor=fill_color,
                    line=dict(color="rgba(0,0,0,0)"),
                    opacity=alpha,
                    name=self.params.get("name", "Ribbon"),
                ),
                row=row,
                col=col,
            )
