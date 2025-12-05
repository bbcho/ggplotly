# geoms/geom_point_map.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd
import numpy as np


class geom_point_map(Geom):
    """
    Geom for drawing points on geographic maps.

    Creates scatter points on a map using longitude (x) and latitude (y) coordinates.
    Useful for plotting cities, locations, or any point data on maps.
    Follows ggplot2 convention where x=longitude and y=latitude.

    Parameters:
        color (str, optional): Color of the points. Can be a column name for mapping.
        size (float or str, optional): Size of the points. Can be a column name for mapping. Default is 8.
        alpha (float, optional): Transparency level. Default is 1.
        shape (str, optional): Marker symbol. Default is 'circle'.
        map (str, optional): The map scope. Options:
            - 'state': US map (default)
            - 'world': World map
            - 'europe', 'asia', 'africa', 'north america', 'south america'
        projection (str, optional): Map projection type. Default depends on map type.
        landcolor (str, optional): Color of land areas. Default is 'rgb(243, 243, 243)'.
        oceancolor (str, optional): Color of ocean areas. Default is 'rgb(204, 229, 255)'.
        lakecolor (str, optional): Color of lakes. Default is 'rgb(204, 229, 255)'.
        countrycolor (str, optional): Color of country borders. Default is 'rgb(204, 204, 204)'.
        coastlinecolor (str, optional): Color of coastlines. Default is 'rgb(204, 204, 204)'.
        subunitcolor (str, optional): Color of subunit borders (e.g., US states). Default is 'rgb(204, 204, 204)'.
        bgcolor (str, optional): Background color of the geo plot. Default is None (transparent).

    Aesthetics:
        - x: Column containing longitude values
        - y: Column containing latitude values
        - color: Column for point colors (optional)
        - size: Column for point sizes (optional)
        - label: Column for point labels (optional)

    Examples:
        # Plot cities on US map (ggplot2 style: x=lon, y=lat)
        ggplot(cities, aes(x='lon', y='lat')) + geom_point_map()

        # With color mapping
        ggplot(cities, aes(x='lon', y='lat', color='population')) + geom_point_map()

        # World map with sized points
        ggplot(cities, aes(x='lon', y='lat', size='value')) + geom_point_map(map='world')
    """

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        self.map_type = params.get('map', 'state')

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if "alpha" not in self.params:
            self.params["alpha"] = 1
        if "size" not in self.params:
            self.params["size"] = 8

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        # ggplot2 style: x=longitude, y=latitude
        lon_col = self.mapping.get("x")
        lat_col = self.mapping.get("y")
        color_col = self.mapping.get("color")
        size_col = self.mapping.get("size")
        label_col = self.mapping.get("label")

        if lat_col is None or lon_col is None:
            raise ValueError("geom_point_map requires both 'x' (longitude) and 'y' (latitude) aesthetics")

        lat = data[lat_col] if lat_col in data.columns else None
        lon = data[lon_col] if lon_col in data.columns else None

        if lat is None or lon is None:
            raise ValueError(f"Columns '{lon_col}' (x/lon) and/or '{lat_col}' (y/lat) not found in data")

        alpha = style_props['alpha']

        # Determine scope based on map type
        if self.map_type in ('state', 'usa'):
            scope = 'usa'
            default_projection = 'albers usa'
        elif self.map_type == 'world':
            scope = 'world'
            default_projection = 'natural earth'
        else:
            scope = self.map_type
            default_projection = 'natural earth'

        projection = self.params.get('projection', default_projection)

        # Build hover text
        if label_col and label_col in data.columns:
            hover_text = data[label_col]
        else:
            hover_text = None

        # Handle color
        if color_col and color_col in data.columns:
            color_values = data[color_col]
            if pd.api.types.is_numeric_dtype(color_values):
                # Continuous color
                marker_color = color_values
                colorscale = self.params.get('palette', 'Viridis')
                showscale = self.params.get('show_colorbar', True)
            else:
                # Categorical color
                categories = color_values.unique()
                colors = px.colors.qualitative.Plotly[:len(categories)]
                if len(categories) > len(colors):
                    colors = px.colors.qualitative.Alphabet[:len(categories)]
                color_map = {cat: colors[i % len(colors)] for i, cat in enumerate(categories)}
                marker_color = color_values.map(color_map)
                colorscale = None
                showscale = False
        else:
            marker_color = style_props.get('color') or style_props['default_color']
            colorscale = None
            showscale = False

        # Handle size
        if size_col and size_col in data.columns:
            size_values = data[size_col]
            # Normalize size to reasonable range
            size_min = self.params.get('size_min', 5)
            size_max = self.params.get('size_max', 20)
            if size_values.max() != size_values.min():
                marker_size = size_min + (size_values - size_values.min()) / (size_values.max() - size_values.min()) * (size_max - size_min)
            else:
                marker_size = (size_min + size_max) / 2
        else:
            marker_size = style_props['size']

        # Handle labels/text
        text_values = None
        text_position = self.params.get('text_position', 'top center')
        if label_col and label_col in data.columns:
            text_values = data[label_col]

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
            if showscale:
                marker_dict['colorbar'] = dict(
                    title=self.params.get('colorbar_title', color_col or ''),
                )
        else:
            marker_dict['color'] = marker_color

        # Add scatter geo trace
        # Note: Scattergeo traces don't support row/col subplots, add directly to figure
        fig.add_trace(
            go.Scattergeo(
                lat=lat,
                lon=lon,
                mode='markers+text' if text_values is not None else 'markers',
                marker=marker_dict,
                text=text_values,
                textposition=text_position,
                hovertext=hover_text,
                hoverinfo='text' if hover_text is not None else 'lat+lon',
                name=self.params.get('name', 'Points'),
                showlegend=self.params.get('showlegend', False),
            ),
        )

        # Update geo layout
        geo_update = dict(
            scope=scope,
            projection_type=projection,
            showland=True,
            landcolor=self.params.get('landcolor', 'rgb(243, 243, 243)'),
            showocean=True,
            oceancolor=self.params.get('oceancolor', 'rgb(204, 229, 255)'),
            showlakes=self.params.get('showlakes', True),
            lakecolor=self.params.get('lakecolor', 'rgb(204, 229, 255)'),
            showcountries=self.params.get('showcountries', True),
            countrycolor=self.params.get('countrycolor', 'rgb(204, 204, 204)'),
            showcoastlines=self.params.get('showcoastlines', True),
            coastlinecolor=self.params.get('coastlinecolor', 'rgb(204, 204, 204)'),
            showsubunits=self.params.get('showsubunits', True),
            subunitcolor=self.params.get('subunitcolor', 'rgb(204, 204, 204)'),
        )

        # Add bgcolor if specified
        if 'bgcolor' in self.params:
            geo_update['bgcolor'] = self.params['bgcolor']

        fig.update_geos(**geo_update)
