# geoms/geom_point.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd


class geom_point(Geom):
    """
    Geom for drawing point plots.

    Automatically handles categorical variables for color, shape, and group.
    When used with geom_map (geographic plots), automatically uses geographic
    coordinates where x=longitude and y=latitude.

    Parameters:
        color (str, optional): Color of the points. If a column name, maps categories to colors.
        size (int, optional): Size of the points. Default is 8.
        alpha (float, optional): Transparency level for the points. Default is 1.
        shape (str, optional): Shape of the points. If a column name, maps categories to shapes.
            Literal values can be any Plotly marker symbol (e.g., 'circle', 'square', 'diamond',
            'cross', 'x', 'triangle-up', 'triangle-down', 'star', 'hexagon', etc.)
        group (str, optional): Grouping variable for the points.
    """

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        # Set default point size to 8 if not specified
        if "size" not in self.params:
            self.params["size"] = 8

        # Check if this figure has geographic traces (from geom_map)
        # If so, use Scattergeo instead of Scatter
        has_geo = any(
            hasattr(trace, 'type') and trace.type in ('choropleth', 'scattergeo')
            for trace in fig.data
        )

        if has_geo:
            self._draw_geo(fig, data)
        else:
            plot = go.Scatter
            payload = dict(
                mode="markers",
                name=self.params.get("name", "Point"),
            )

            color_targets = dict(
                color="marker_color",
                size="marker_size",
                shape="marker_symbol",
            )

            self._transform_fig(plot, fig, data, payload, color_targets, row, col)

    def _draw_geo(self, fig, data):
        """Draw points on a geographic map using Scattergeo."""
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        # x = longitude, y = latitude (ggplot2 convention)
        lon_col = self.mapping.get("x")
        lat_col = self.mapping.get("y")
        color_col = self.mapping.get("color")
        size_col = self.mapping.get("size")
        label_col = self.mapping.get("label")

        if lat_col is None or lon_col is None:
            raise ValueError("geom_point on maps requires both 'x' (longitude) and 'y' (latitude) aesthetics")

        lon = data[lon_col]
        lat = data[lat_col]

        alpha = style_props['alpha']

        # Build hover text
        if label_col and label_col in data.columns:
            hover_text = data[label_col]
        else:
            hover_text = None

        # Handle color
        if style_props.get('color_series') is not None:
            # Color is mapped to a column
            color_values = style_props['color_series']
            if pd.api.types.is_numeric_dtype(color_values):
                marker_color = color_values
                colorscale = self.params.get('palette', 'Viridis')
                showscale = self.params.get('show_colorbar', True)
            else:
                # Use the color map from style_props
                marker_color = color_values.map(style_props['color_map'])
                colorscale = None
                showscale = False
        else:
            marker_color = style_props.get('color') or style_props['default_color']
            colorscale = None
            showscale = False

        # Handle size
        size_series = style_props.get('size_series')
        if size_series is not None and isinstance(size_series, pd.Series) and pd.api.types.is_numeric_dtype(size_series):
            # Size is mapped to a numeric column
            size_values = size_series
            size_min = self.params.get('size_min', 5)
            size_max = self.params.get('size_max', 20)
            if size_values.max() != size_values.min():
                marker_size = size_min + (size_values - size_values.min()) / (size_values.max() - size_values.min()) * (size_max - size_min)
            else:
                marker_size = (size_min + size_max) / 2
        else:
            # Size is a literal value
            size_val = style_props.get('size', 8)
            marker_size = size_val if isinstance(size_val, (int, float)) else 8

        # Create marker dict
        marker_dict = dict(
            size=marker_size,
            opacity=alpha,
            symbol=self.params.get('shape', 'circle'),
        )

        if colorscale:
            marker_dict['color'] = marker_color
            marker_dict['colorscale'] = colorscale
            marker_dict['showscale'] = showscale
        else:
            marker_dict['color'] = marker_color

        # Add scatter geo trace
        fig.add_trace(
            go.Scattergeo(
                lat=lat,
                lon=lon,
                mode='markers+text' if hover_text is not None and self.params.get('show_labels', False) else 'markers',
                marker=marker_dict,
                text=hover_text,
                textposition=self.params.get('text_position', 'top center'),
                hovertext=hover_text,
                hoverinfo='text' if hover_text is not None else 'lat+lon',
                name=self.params.get('name', 'Points'),
                showlegend=self.params.get('showlegend', False),
            ),
        )
