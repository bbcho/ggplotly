# geoms/geom_map.py

import plotly.graph_objects as go
import plotly.express as px
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd
import json


def _has_geopandas():
    """Check if geopandas is available."""
    try:
        import geopandas
        return True
    except ImportError:
        return False


def _is_geodataframe(data):
    """Check if data is a GeoDataFrame."""
    if not _has_geopandas():
        return False
    import geopandas as gpd
    return isinstance(data, gpd.GeoDataFrame)


def _extract_geojson(data):
    """Extract GeoJSON from various input formats.

    Supports:
    - GeoDataFrame (geopandas)
    - dict with 'type' key (GeoJSON dict)
    - object with __geo_interface__ attribute
    """
    # GeoDataFrame
    if _is_geodataframe(data):
        return json.loads(data.to_json())

    # GeoJSON dict
    if isinstance(data, dict) and 'type' in data:
        return data

    # __geo_interface__ (shapely, etc.)
    if hasattr(data, '__geo_interface__'):
        return data.__geo_interface__

    return None


class geom_map(Geom):
    """Geom for drawing geographic maps (base maps, choropleths, and GeoJSON/sf)."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Create a geographic map layer.

        Supports base maps, choropleths, and GeoJSON/sf-style rendering.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Key aesthetics:
            - map_id: Region identifiers (for choropleth)
            - fill: Values to map to fill color (triggers choropleth)
        map : DataFrame, optional
            Map region data with 'id' column. Use map_data('state') or map_data('world').
        geojson : dict or GeoDataFrame, optional
            GeoJSON dict or GeoDataFrame for sf-like rendering.
        featureidkey : str, default='properties.id'
            Path to feature ID in GeoJSON properties.
        map_type : str, default='state'
            Map scope: 'state', 'usa', 'world', 'europe', 'asia', 'africa', etc.
        region : str, optional
            Region format: 'USA-states', 'ISO-3', 'country names', 'geojson-id'.
        color : str, default='white'
            Border color.
        linewidth : float, default=0.5
            Border line width.
        alpha : float, default=1
            Transparency (0-1).
        palette : str, default='Viridis'
            Color palette for fill.
        projection : str, optional
            Map projection: 'albers usa', 'mercator', 'natural earth', etc.
        landcolor : str, optional
            Land area color.
        oceancolor : str, optional
            Ocean color.
        lakecolor : str, optional
            Lake color.
        bgcolor : str, optional
            Background color.
        fitbounds : str, optional
            How to fit bounds: 'locations', 'geojson', False.

        Examples
        --------
        >>> # Base map with points
        >>> ggplot(cities, aes(x='lon', y='lat')) + geom_map(map_type='usa') + geom_point()

        >>> # Choropleth
        >>> ggplot(data, aes(map_id='state', fill='pop')) + geom_map(map=map_data('state'))
        """
        super().__init__(data, mapping, **params)
        self.map_df = params.pop('map', None)  # The map dataframe (like ggplot2)
        self.geojson = params.pop('geojson', None)  # GeoJSON for sf-like mode
        self.featureidkey = params.get('featureidkey', 'properties.id')
        self.map_type = params.get('map_type', 'state')
        self.palette = params.get('palette', 'Viridis')

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if "alpha" not in self.params:
            self.params["alpha"] = 1

        # Check if data is a GeoDataFrame - auto-detect sf mode
        geojson = self.geojson
        if geojson is None and _is_geodataframe(data):
            # Data itself is a GeoDataFrame - extract GeoJSON
            geojson = _extract_geojson(data)

        # ggplot2 uses map_id aesthetic for choropleths
        map_id_col = self.mapping.get("map_id") if self.mapping else None
        fill_col = self.mapping.get("fill") if self.mapping else None
        geometry_col = self.mapping.get("geometry") if self.mapping else None

        # Determine the mode:
        # 1. GeoJSON mode (sf-like) - when geojson is provided or data is GeoDataFrame
        # 2. Choropleth mode - when map_id is provided
        # 3. Base map mode - no data aesthetics
        is_geojson_mode = geojson is not None
        is_base_map = map_id_col is None and fill_col is None and not is_geojson_mode

        if is_base_map:
            # Just set up the geo layout - no data traces needed
            self._setup_geo_layout(fig)
            return

        if is_geojson_mode:
            # GeoJSON/sf mode - render arbitrary geometries
            self._draw_geojson(fig, data, geojson, fill_col)
            return

        # Choropleth mode - require map_id
        if map_id_col is None:
            raise ValueError("geom_map choropleth requires a 'map_id' aesthetic")

        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

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
            # Don't add marker trace for choropleth - the choropleth trace itself signals geo context
            self._setup_geo_layout(fig, scope=scope, projection=projection, add_marker_trace=False)

    def _draw_geojson(self, fig, data, geojson, fill_col):
        """Draw GeoJSON geometries like ggplot2's geom_sf.

        This method renders arbitrary geometries (polygons, lines, points)
        from GeoJSON data. It auto-detects geometry types and renders
        them appropriately using Plotly's Choroplethmapbox or Scattermapbox.

        Args:
            fig: The plotly figure to add traces to
            data: DataFrame with data values (can be GeoDataFrame)
            geojson: GeoJSON dict
            fill_col: Column name for fill values (optional)
        """
        border_color = self.params.get('color', 'white')
        border_width = self.params.get('linewidth', 0.5)
        alpha = self.params.get('alpha', 1)
        show_colorbar = self.params.get('show_colorbar', True)
        fitbounds = self.params.get('fitbounds', 'locations')

        # Determine if we have data to join with geojson
        map_id_col = self.mapping.get("map_id") if self.mapping else None

        # For GeoDataFrame, use index as default locations
        if _is_geodataframe(data):
            if map_id_col is None:
                # Use index as locations
                locations = data.index.tolist()
                featureidkey = 'id'
            else:
                locations = data[map_id_col].tolist()
                featureidkey = self.featureidkey
        elif data is not None and map_id_col and map_id_col in data.columns:
            locations = data[map_id_col].tolist()
            featureidkey = self.featureidkey
        else:
            # No data - extract locations from geojson features
            locations = [f.get('id', i) for i, f in enumerate(geojson.get('features', []))]
            featureidkey = 'id'

        # Get fill values
        if fill_col and data is not None and fill_col in data.columns:
            fill_values = data[fill_col]
        else:
            fill_values = None

        # Determine geometry types in GeoJSON
        geom_types = set()
        for feature in geojson.get('features', []):
            geom_type = feature.get('geometry', {}).get('type', '')
            geom_types.add(geom_type)

        # Check if primarily polygons, lines, or points
        has_polygons = 'Polygon' in geom_types or 'MultiPolygon' in geom_types
        has_lines = 'LineString' in geom_types or 'MultiLineString' in geom_types
        has_points = 'Point' in geom_types or 'MultiPoint' in geom_types

        # Determine which trace type to use (prefer newer map types if available)
        # Plotly deprecated *mapbox traces in favor of *map traces
        try:
            ChoroplethMapTrace = go.Choroplethmap
            ScatterMapTrace = go.Scattermap
            map_layout_key = 'map'
        except AttributeError:
            # Fall back to mapbox for older plotly versions
            ChoroplethMapTrace = go.Choroplethmapbox
            ScatterMapTrace = go.Scattermapbox
            map_layout_key = 'mapbox'

        # Use Choroplethmap for polygons (most common case)
        if has_polygons:
            if fill_values is not None:
                if pd.api.types.is_numeric_dtype(fill_values):
                    # Continuous fill
                    trace = ChoroplethMapTrace(
                        geojson=geojson,
                        locations=locations,
                        z=fill_values,
                        featureidkey=featureidkey,
                        colorscale=self.palette,
                        marker=dict(
                            line=dict(color=border_color, width=border_width),
                            opacity=alpha,
                        ),
                        colorbar=dict(
                            title=self.params.get('colorbar_title', fill_col or ''),
                        ),
                        showscale=show_colorbar,
                        name=self.params.get('name', 'Map'),
                    )
                else:
                    # Categorical fill
                    categories = fill_values.unique()
                    cat_to_num = {cat: i for i, cat in enumerate(categories)}
                    z_values = fill_values.map(cat_to_num)

                    n_cats = len(categories)
                    colors = px.colors.qualitative.Plotly[:n_cats]
                    if n_cats > len(colors):
                        colors = px.colors.qualitative.Alphabet[:n_cats]

                    colorscale = []
                    for i, color in enumerate(colors[:n_cats]):
                        colorscale.append([i / n_cats, color])
                        colorscale.append([(i + 1) / n_cats, color])

                    trace = ChoroplethMapTrace(
                        geojson=geojson,
                        locations=locations,
                        z=z_values,
                        featureidkey=featureidkey,
                        colorscale=colorscale,
                        marker=dict(
                            line=dict(color=border_color, width=border_width),
                            opacity=alpha,
                        ),
                        colorbar=dict(
                            title=self.params.get('colorbar_title', fill_col or ''),
                            tickvals=list(range(n_cats)),
                            ticktext=list(categories),
                        ),
                        showscale=show_colorbar,
                        name=self.params.get('name', 'Map'),
                    )
            else:
                # No fill - uniform color
                default_color = self.params.get('fill_color', 'steelblue')
                trace = ChoroplethMapTrace(
                    geojson=geojson,
                    locations=locations,
                    z=[1] * len(locations),
                    featureidkey=featureidkey,
                    colorscale=[[0, default_color], [1, default_color]],
                    marker=dict(
                        line=dict(color=border_color, width=border_width),
                        opacity=alpha,
                    ),
                    showscale=False,
                    name=self.params.get('name', 'Map'),
                )

            fig.add_trace(trace)

        # Handle lines with Scattermap
        if has_lines and not has_polygons:
            # Extract line coordinates from GeoJSON
            lats, lons = [], []
            for feature in geojson.get('features', []):
                geom = feature.get('geometry', {})
                if geom.get('type') == 'LineString':
                    coords = geom.get('coordinates', [])
                    for lon, lat in coords:
                        lons.append(lon)
                        lats.append(lat)
                    lons.append(None)  # Break between lines
                    lats.append(None)
                elif geom.get('type') == 'MultiLineString':
                    for line in geom.get('coordinates', []):
                        for lon, lat in line:
                            lons.append(lon)
                            lats.append(lat)
                        lons.append(None)
                        lats.append(None)

            line_color = self.params.get('color', 'steelblue')
            trace = ScatterMapTrace(
                lat=lats,
                lon=lons,
                mode='lines',
                line=dict(color=line_color, width=border_width),
                opacity=alpha,
                name=self.params.get('name', 'Lines'),
            )
            fig.add_trace(trace)

        # Handle points with Scattermap
        if has_points and not has_polygons and not has_lines:
            lats, lons = [], []
            for feature in geojson.get('features', []):
                geom = feature.get('geometry', {})
                if geom.get('type') == 'Point':
                    lon, lat = geom.get('coordinates', [0, 0])
                    lons.append(lon)
                    lats.append(lat)
                elif geom.get('type') == 'MultiPoint':
                    for lon, lat in geom.get('coordinates', []):
                        lons.append(lon)
                        lats.append(lat)

            point_color = self.params.get('color', 'steelblue')
            point_size = self.params.get('size', 8)
            trace = ScatterMapTrace(
                lat=lats,
                lon=lons,
                mode='markers',
                marker=dict(color=point_color, size=point_size, opacity=alpha),
                name=self.params.get('name', 'Points'),
            )
            fig.add_trace(trace)

        # Store map layout key for later use
        self._map_layout_key = map_layout_key

        # Set up mapbox layout for GeoJSON mode
        self._setup_mapbox_layout(fig, geojson, fitbounds)

    def _setup_mapbox_layout(self, fig, geojson, fitbounds='locations'):
        """Set up map layout for GeoJSON rendering.

        Args:
            fig: The plotly figure
            geojson: GeoJSON dict for bounds calculation
            fitbounds: How to fit bounds ('locations', 'geojson', or False)
        """
        mapbox_style = self.params.get('mapbox_style', 'carto-positron')
        map_layout_key = getattr(self, '_map_layout_key', 'map')

        # Calculate center from GeoJSON bounds
        if geojson and 'features' in geojson:
            all_lons, all_lats = [], []
            for feature in geojson['features']:
                coords = self._extract_coords(feature.get('geometry', {}))
                for lon, lat in coords:
                    all_lons.append(lon)
                    all_lats.append(lat)

            if all_lons and all_lats:
                center_lat = (min(all_lats) + max(all_lats)) / 2
                center_lon = (min(all_lons) + max(all_lons)) / 2

                # Estimate zoom based on bounds
                lat_range = max(all_lats) - min(all_lats)
                lon_range = max(all_lons) - min(all_lons)
                max_range = max(lat_range, lon_range)
                if max_range > 100:
                    zoom = 2
                elif max_range > 50:
                    zoom = 3
                elif max_range > 20:
                    zoom = 4
                elif max_range > 10:
                    zoom = 5
                elif max_range > 5:
                    zoom = 6
                else:
                    zoom = 7
            else:
                center_lat, center_lon, zoom = 0, 0, 1
        else:
            center_lat, center_lon, zoom = 0, 0, 1

        # Override with params if provided
        center_lat = self.params.get('center_lat', center_lat)
        center_lon = self.params.get('center_lon', center_lon)
        zoom = self.params.get('zoom', zoom)

        map_config = dict(
            style=mapbox_style,
            center=dict(lat=center_lat, lon=center_lon),
            zoom=zoom,
        )

        # Use the appropriate layout key (map or mapbox)
        fig.update_layout(**{map_layout_key: map_config})

    def _extract_coords(self, geometry):
        """Extract all coordinates from a GeoJSON geometry."""
        coords = []
        geom_type = geometry.get('type', '')
        coordinates = geometry.get('coordinates', [])

        if geom_type == 'Point':
            coords.append(tuple(coordinates[:2]))
        elif geom_type == 'MultiPoint':
            for c in coordinates:
                coords.append(tuple(c[:2]))
        elif geom_type == 'LineString':
            for c in coordinates:
                coords.append(tuple(c[:2]))
        elif geom_type == 'MultiLineString':
            for line in coordinates:
                for c in line:
                    coords.append(tuple(c[:2]))
        elif geom_type == 'Polygon':
            for ring in coordinates:
                for c in ring:
                    coords.append(tuple(c[:2]))
        elif geom_type == 'MultiPolygon':
            for polygon in coordinates:
                for ring in polygon:
                    for c in ring:
                        coords.append(tuple(c[:2]))

        return coords

    def _setup_geo_layout(self, fig, scope=None, projection=None, add_marker_trace=True):
        """Set up the geographic layout for the map.

        This method configures the geo subplot with appropriate styling.
        It's used both for base maps and choropleth maps.

        Args:
            fig: The plotly figure to configure
            scope: Geographic scope (usa, world, europe, etc.)
            projection: Map projection type
            add_marker_trace: If True, adds an invisible scattergeo trace so other
                geoms can detect the geo context
        """
        # Determine scope based on map type if not provided
        if scope is None:
            if self.map_type in ('state', 'usa'):
                scope = 'usa'
            elif self.map_type == 'world':
                scope = 'world'
            else:
                scope = self.map_type

        # Determine projection if not provided
        if projection is None:
            if self.map_type in ('state', 'usa'):
                projection = self.params.get('projection', 'albers usa')
            else:
                projection = self.params.get('projection', 'natural earth')

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

        # Add an invisible scattergeo trace so other geoms can detect the geo context
        # This is needed for geom_point to know it should use Scattergeo instead of Scatter
        if add_marker_trace:
            fig.add_trace(
                go.Scattergeo(
                    lat=[],
                    lon=[],
                    mode='markers',
                    marker=dict(size=0, opacity=0),
                    showlegend=False,
                    hoverinfo='skip',
                    name='_geo_context',  # Internal marker name
                )
            )


# geom_sf is an alias for geom_map, following ggplot2 conventions
# where geom_sf is used for rendering simple features (sf) objects
geom_sf = geom_map
