# geoms/geom_map.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd


class geom_map(Geom):
    """
    Geom for drawing choropleth maps.

    Creates geographic maps where regions are colored based on data values.
    Supports both US states and world countries. Like ggplot2, you can provide
    map data via the `map` parameter.

    Parameters:
        map (DataFrame, optional): A dataframe containing map region data with an 'id' column.
            Use map_data() to get pre-defined map data:
            - map_data('state'): US state abbreviations
            - map_data('world'): ISO-3 country codes
        map_type (str, optional): The type of map scope. Options:
            - 'state': US states map (default)
            - 'world': World countries map
        region (str, optional): How regions are specified. Options:
            - 'USA-states': US state abbreviations (e.g., 'CA', 'NY') - default for state map
            - 'ISO-3': ISO 3-letter country codes (e.g., 'USA', 'CAN') - default for world map
            - 'country names': Full country names
        color (str, optional): Border color of the regions. Default is 'white'.
        linewidth (float, optional): Border line width. Default is 0.5.
        alpha (float, optional): Transparency level. Default is 1.
        palette (str, optional): Color palette for continuous fill. Default is 'Viridis'.
        projection (str, optional): Map projection type. Default depends on map type.
            Options: 'albers usa', 'mercator', 'natural earth', 'orthographic', etc.

    Aesthetics:
        - map_id: Column containing region identifiers (state codes, country codes, etc.)
        - fill: Column containing values to map to fill color

    Examples:
        # US states choropleth (ggplot2 style with map_data)
        from ggplotly import map_data
        states = map_data('state')
        ggplot(data, aes(map_id='state', fill='population')) + geom_map(map=states)

        # World map
        countries = map_data('world')
        ggplot(data, aes(map_id='country', fill='gdp')) + geom_map(map=countries, map_type='world')

        # Custom projection
        ggplot(data, aes(map_id='state', fill='value')) + geom_map(map=states, projection='albers usa')
    """

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        self.map_df = params.pop('map', None)  # The map dataframe (like ggplot2)
        self.map_type = params.get('map_type', 'state')
        self.palette = params.get('palette', 'Viridis')

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if "alpha" not in self.params:
            self.params["alpha"] = 1

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        # ggplot2 uses map_id aesthetic
        map_id_col = self.mapping.get("map_id")
        fill_col = self.mapping.get("fill")

        if map_id_col is None:
            raise ValueError("geom_map requires a 'map_id' aesthetic")

        if map_id_col not in data.columns:
            available_cols = ', '.join(data.columns.tolist())
            raise ValueError(f"Column '{map_id_col}' not found in data. Available columns: {available_cols}")

        # Get locations from the data
        # If map dataframe provided, merge to get all regions; otherwise use data directly
        if self.map_df is not None:
            # Merge data with map dataframe on map_id to include all map regions
            map_id_in_map = 'id' if 'id' in self.map_df.columns else map_id_col
            merged = self.map_df.merge(
                data,
                left_on=map_id_in_map,
                right_on=map_id_col,
                how='left'
            )
            locations = merged[map_id_in_map]
            fill_values = merged[fill_col] if fill_col and fill_col in merged.columns else None
        else:
            locations = data[map_id_col]
            fill_values = data[fill_col] if fill_col and fill_col in data.columns else None

        alpha = style_props['alpha']
        border_color = self.params.get('color', 'white')
        border_width = self.params.get('linewidth', 0.5)

        # Determine location mode and scope based on map type
        if self.map_type in ('state', 'usa'):
            location_mode = self.params.get('region', 'USA-states')
            scope = 'usa'
            default_projection = 'albers usa'
        elif self.map_type == 'world':
            location_mode = self.params.get('region', 'ISO-3')
            scope = 'world'
            default_projection = 'natural earth'
        else:
            location_mode = self.params.get('region', 'ISO-3')
            scope = self.map_type
            default_projection = 'natural earth'

        projection = self.params.get('projection', default_projection)

        # Build hover text
        hover_text = locations

        # Get geo key if faceting (set by facet_wrap)
        geo_key = self.params.pop('_geo_key', None)
        facet_idx = self.params.pop('_facet_idx', None)
        facet_count = self.params.pop('_facet_count', None)
        facet_scales = self.params.pop('_facet_scales', 'free')
        global_zmin = self.params.pop('_global_zmin', None)
        global_zmax = self.params.pop('_global_zmax', None)

        # Determine colorbar visibility
        # For fixed scales: show colorbar only on last facet
        # For free scales: hide all colorbars (different ranges)
        if geo_key:
            if facet_scales == 'fixed' and global_zmin is not None:
                # Show colorbar only on last facet
                show_colorbar = (facet_idx == facet_count - 1)
            else:
                show_colorbar = False
        else:
            show_colorbar = self.params.get('show_colorbar', True)

        # Handle fill values
        # Note: Choropleth traces don't support row/col subplots, add directly to figure
        if fill_values is not None:
            if pd.api.types.is_numeric_dtype(fill_values):
                # Use global z range if provided (for shared colorbar)
                zmin = global_zmin if global_zmin is not None else None
                zmax = global_zmax if global_zmax is not None else None

                # Continuous fill
                trace = go.Choropleth(
                    locations=locations,
                    z=fill_values,
                    locationmode=location_mode,
                    colorscale=self.palette,
                    zmin=zmin,
                    zmax=zmax,
                    marker=dict(
                        line=dict(color=border_color, width=border_width)
                    ),
                    colorbar=dict(
                        title=self.params.get('colorbar_title', fill_col or ''),
                    ),
                    hovertext=hover_text,
                    hoverinfo='text+z',
                    showscale=show_colorbar,
                    name=self.params.get('name', 'Map'),
                )
                if geo_key:
                    trace.geo = geo_key
                fig.add_trace(trace)
            else:
                # Categorical fill - convert to numeric for choropleth
                categories = fill_values.unique()
                cat_to_num = {cat: i for i, cat in enumerate(categories)}
                z_values = fill_values.map(cat_to_num)

                # Create discrete colorscale
                n_cats = len(categories)
                colors = px.colors.qualitative.Plotly[:n_cats]
                if n_cats > len(colors):
                    colors = px.colors.qualitative.Alphabet[:n_cats]

                # Build discrete colorscale
                colorscale = []
                for i, color in enumerate(colors[:n_cats]):
                    colorscale.append([i / n_cats, color])
                    colorscale.append([(i + 1) / n_cats, color])

                trace = go.Choropleth(
                    locations=locations,
                    z=z_values,
                    locationmode=location_mode,
                    colorscale=colorscale,
                    marker=dict(
                        line=dict(color=border_color, width=border_width)
                    ),
                    colorbar=dict(
                        title=self.params.get('colorbar_title', fill_col or ''),
                        tickvals=list(range(n_cats)),
                        ticktext=list(categories),
                    ),
                    hovertext=hover_text,
                    hoverinfo='text+z',
                    showscale=show_colorbar,
                    name=self.params.get('name', 'Map'),
                )
                if geo_key:
                    trace.geo = geo_key
                fig.add_trace(trace)
        else:
            # No fill - just show regions with uniform color
            default_color = style_props.get('fill') or style_props['default_color']
            trace = go.Choropleth(
                locations=locations,
                z=[1] * len(locations),  # Uniform values
                locationmode=location_mode,
                colorscale=[[0, default_color], [1, default_color]],
                marker=dict(
                    line=dict(color=border_color, width=border_width)
                ),
                hovertext=hover_text,
                hoverinfo='text',
                showscale=False,
                name=self.params.get('name', 'Map'),
            )
            if geo_key:
                trace.geo = geo_key
            fig.add_trace(trace)

        # Update geo layout (only if not faceting - facet_wrap handles it)
        if not geo_key:
            fig.update_geos(
                scope=scope,
                projection_type=projection,
                showland=True,
                landcolor='rgb(243, 243, 243)',
                showocean=True,
                oceancolor='rgb(204, 229, 255)',
                showlakes=self.params.get('showlakes', True),
                lakecolor='rgb(204, 229, 255)',
                showcountries=self.params.get('showcountries', True),
                countrycolor='rgb(204, 204, 204)',
                showcoastlines=self.params.get('showcoastlines', True),
                coastlinecolor='rgb(204, 204, 204)',
            )
