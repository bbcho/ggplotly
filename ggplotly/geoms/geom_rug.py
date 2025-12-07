# geoms/geom_rug.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import numpy as np


class geom_rug(Geom):
    """Geom for drawing rug plots (marginal tick marks on axes)."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Draw rug plots (marginal tick marks) along axes.

        Rug plots display individual data points as tick marks along the axes,
        useful for showing the marginal distribution of data in scatter plots.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x and/or y.
        sides : str, default='bl'
            Which sides to draw rugs on:
            - 'b' = bottom (x-axis)
            - 't' = top (x-axis at top)
            - 'l' = left (y-axis)
            - 'r' = right (y-axis at right)
            Can combine, e.g., 'bl' for bottom and left.
        length : float, default=0.03
            Length of rug ticks as fraction of plot area.
        color : str, default='black'
            Color of the rug lines.
        alpha : float, default=0.5
            Transparency (0-1).
        size : float, default=1
            Line width of the rug ticks.

        Examples
        --------
        >>> geom_rug()  # default: bottom and left rugs
        >>> geom_rug(sides='b', color='red')  # bottom only
        """
        super().__init__(data, mapping, **params)
        self.sides = params.get('sides', 'bl')
        self.length = params.get('length', 0.03)

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        # Set defaults
        if "size" not in self.params:
            self.params["size"] = 1
        if "alpha" not in self.params:
            self.params["alpha"] = 0.5

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")

        x = data[x_col].values if x_col and x_col in data.columns else None
        y = data[y_col].values if y_col and y_col in data.columns else None

        alpha = style_props['alpha']
        # For rug plots, we use a single color (not mapped per data point)
        # If color is a column reference, use default color instead
        color = style_props.get('color')
        if color is None or style_props.get('color_series') is not None:
            # Color is either not set or is a column reference - use default
            color = style_props['default_color']
        line_width = style_props['size']

        # Get data ranges to calculate rug length
        if x is not None:
            x_min, x_max = np.nanmin(x), np.nanmax(x)
            x_range = x_max - x_min if x_max != x_min else 1
        else:
            x_range = 1

        if y is not None:
            y_min, y_max = np.nanmin(y), np.nanmax(y)
            y_range = y_max - y_min if y_max != y_min else 1
        else:
            y_range = 1

        # Calculate tick lengths
        x_tick_length = y_range * self.length
        y_tick_length = x_range * self.length

        # Draw rugs based on sides parameter
        traces_added = 0

        # Bottom rug (along x-axis at y minimum)
        if 'b' in self.sides and x is not None:
            x_coords = []
            y_coords = []
            y_base = y_min if y is not None else 0
            for xi in x:
                if not np.isnan(xi):
                    x_coords.extend([xi, xi, None])
                    y_coords.extend([y_base, y_base + x_tick_length, None])

            fig.add_trace(
                go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode="lines",
                    line=dict(color=color, width=line_width),
                    opacity=alpha,
                    name="Rug (bottom)",
                    showlegend=self.params.get("showlegend", False),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
            traces_added += 1

        # Top rug (along x-axis at y maximum)
        if 't' in self.sides and x is not None:
            x_coords = []
            y_coords = []
            y_base = y_max if y is not None else 1
            for xi in x:
                if not np.isnan(xi):
                    x_coords.extend([xi, xi, None])
                    y_coords.extend([y_base, y_base - x_tick_length, None])

            fig.add_trace(
                go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode="lines",
                    line=dict(color=color, width=line_width),
                    opacity=alpha,
                    name="Rug (top)",
                    showlegend=self.params.get("showlegend", False),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
            traces_added += 1

        # Left rug (along y-axis at x minimum)
        if 'l' in self.sides and y is not None:
            x_coords = []
            y_coords = []
            x_base = x_min if x is not None else 0
            for yi in y:
                if not np.isnan(yi):
                    x_coords.extend([x_base, x_base + y_tick_length, None])
                    y_coords.extend([yi, yi, None])

            fig.add_trace(
                go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode="lines",
                    line=dict(color=color, width=line_width),
                    opacity=alpha,
                    name="Rug (left)",
                    showlegend=self.params.get("showlegend", False),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
            traces_added += 1

        # Right rug (along y-axis at x maximum)
        if 'r' in self.sides and y is not None:
            x_coords = []
            y_coords = []
            x_base = x_max if x is not None else 1
            for yi in y:
                if not np.isnan(yi):
                    x_coords.extend([x_base, x_base - y_tick_length, None])
                    y_coords.extend([yi, yi, None])

            fig.add_trace(
                go.Scatter(
                    x=x_coords,
                    y=y_coords,
                    mode="lines",
                    line=dict(color=color, width=line_width),
                    opacity=alpha,
                    name="Rug (right)",
                    showlegend=self.params.get("showlegend", False),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
            traces_added += 1
