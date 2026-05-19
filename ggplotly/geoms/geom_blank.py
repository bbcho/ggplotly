# geoms/geom_blank.py

import pandas as pd
import plotly.graph_objects as go

from .geom_base import Geom


class geom_blank(Geom):
    """Train plot scales without drawing a visible mark."""

    required_aes = []
    default_params = {"show_legend": False, "showlegend": False}

    def _draw_impl(self, fig, data, row, col):
        if data is None or data.empty:
            return

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        x = data[x_col] if x_col in data else pd.Series([0] * len(data), index=data.index)
        y = data[y_col] if y_col in data else pd.Series([0] * len(data), index=data.index)

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                marker=dict(color="rgba(0,0,0,0)", opacity=0, size=1),
                line=dict(color="rgba(0,0,0,0)"),
                opacity=0,
                showlegend=False,
                hoverinfo="skip",
                name=self.params.get("name", "Blank"),
            ),
            row=row,
            col=col,
        )
