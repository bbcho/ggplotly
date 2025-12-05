# coords/coord_sf.py

from .coord_base import Coord


class coord_sf(Coord):
    """Coordinate system for sf (simple features) geographic data."""

    # Map common CRS strings to Plotly projection types
    PROJECTION_MAP = {
        # EPSG codes
        'epsg:4326': 'equirectangular',  # WGS84
        'epsg:3857': 'mercator',  # Web Mercator
        'epsg:2163': 'albers usa',  # US National Atlas Equal Area

        # Named projections (lowercase for matching)
        'mercator': 'mercator',
        'natural earth': 'natural earth',
        'naturalearth': 'natural earth',
        'albers usa': 'albers usa',
        'albersusa': 'albers usa',
        'albers': 'albers usa',
        'orthographic': 'orthographic',
        'globe': 'orthographic',
        'equirectangular': 'equirectangular',
        'platecarree': 'equirectangular',
        'plate carree': 'equirectangular',
        'robinson': 'robinson',
        'miller': 'miller',
        'kavrayskiy7': 'kavrayskiy7',
        'kavrayskiy': 'kavrayskiy7',
        'winkel tripel': 'winkel tripel',
        'winkeltripel': 'winkel tripel',
        'aitoff': 'aitoff',
        'sinusoidal': 'sinusoidal',
        'mollweide': 'mollweide',
        'conic equal area': 'conic equal area',
        'conicequalarea': 'conic equal area',
        'conic conformal': 'conic conformal',
        'conicconformal': 'conic conformal',
        'stereographic': 'stereographic',
        'transverse mercator': 'transverse mercator',
        'transversemercator': 'transverse mercator',
        'azimuthal equal area': 'azimuthal equal area',
        'azimuthalequalarea': 'azimuthal equal area',
    }

    def __init__(
        self,
        xlim=None,
        ylim=None,
        expand=True,
        crs=None,
        datum='EPSG:4326',
        default_crs=None,
        label_graticule=None,
        ndiscr=100,
        clip='on',
    ):
        """
        Configure geographic coordinate system for maps.

        Designed for use with geom_map/geom_sf. Provides control over
        projection, geographic bounds, and map display settings.

        Parameters
        ----------
        xlim : tuple, optional
            Longitude limits as (min, max). E.g., (-125, -65) for continental US.
        ylim : tuple, optional
            Latitude limits as (min, max). E.g., (25, 50) for continental US.
        expand : bool, default=True
            Whether to expand limits slightly to prevent data touching edges.
        crs : str, optional
            Coordinate reference system / projection. Options:
            - 'mercator', 'natural earth', 'albers usa', 'orthographic'
            - 'equirectangular', 'robinson', 'miller', 'mollweide'
            - EPSG codes like 'EPSG:4326' (WGS84)
        datum : str, default='EPSG:4326'
            CRS for graticules (ggplot2 compatibility).
        default_crs : str, optional
            Default CRS for non-sf layers. Set to 'EPSG:4326' for lon/lat.
        label_graticule : str, optional
            Which graticule lines to label. E.g., 'NESW', 'NS', 'EW'.
        ndiscr : int, default=100
            Number of segments for discretizing lines (smoother curves).
        clip : str, default='on'
            Whether to clip to panel: 'on' or 'off'.

        Examples
        --------
        >>> coord_sf(xlim=(-125, -65), ylim=(25, 50))  # continental US bounds
        >>> coord_sf(crs='robinson')  # Robinson projection
        >>> coord_sf(crs='orthographic')  # Globe projection
        """
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
        self.crs = crs
        self.datum = datum
        self.default_crs = default_crs
        self.label_graticule = label_graticule
        self.ndiscr = ndiscr
        self.clip = clip

    def _get_projection_type(self, crs):
        """Convert CRS string to Plotly projection type."""
        if crs is None:
            return None

        # Normalize the CRS string
        crs_lower = str(crs).lower().strip()

        # Check the mapping
        if crs_lower in self.PROJECTION_MAP:
            return self.PROJECTION_MAP[crs_lower]

        # If it's already a valid Plotly projection, return as-is
        valid_projections = [
            'mercator', 'natural earth', 'albers usa', 'orthographic',
            'equirectangular', 'robinson', 'miller', 'kavrayskiy7',
            'winkel tripel', 'aitoff', 'sinusoidal', 'mollweide',
            'conic equal area', 'conic conformal', 'stereographic',
            'transverse mercator', 'azimuthal equal area'
        ]
        if crs_lower in valid_projections:
            return crs_lower

        # Return as-is if not recognized (let Plotly handle the error)
        return crs

    def _has_geo_traces(self, fig):
        """Check if figure has geographic traces."""
        geo_types = (
            'scattergeo', 'choropleth',
            'scattermapbox', 'choroplethmapbox',
            'scattermap', 'choroplethmap'
        )
        return any(
            hasattr(trace, 'type') and trace.type in geo_types
            for trace in fig.data
        )

    def _has_mapbox_traces(self, fig):
        """Check if figure uses mapbox-style traces."""
        mapbox_types = (
            'scattermapbox', 'choroplethmapbox',
            'scattermap', 'choroplethmap'
        )
        return any(
            hasattr(trace, 'type') and trace.type in mapbox_types
            for trace in fig.data
        )

    def apply(self, fig):
        """
        Apply the coordinate transformation to the figure.

        For geo figures (scattergeo, choropleth), updates the geo layout.
        For mapbox figures (scattermapbox, etc.), updates mapbox layout.

        Parameters:
            fig (Figure): Plotly figure object.
        """
        if not self._has_geo_traces(fig):
            # Not a geo figure - nothing to do
            return

        if self._has_mapbox_traces(fig):
            self._apply_mapbox(fig)
        else:
            self._apply_geo(fig)

    def _apply_geo(self, fig):
        """Apply coord_sf settings to a geo-based figure."""
        geo_update = {}

        # Set projection if specified
        if self.crs is not None:
            projection_type = self._get_projection_type(self.crs)
            if projection_type:
                geo_update['projection_type'] = projection_type
                # When changing projection from 'albers usa' to something else,
                # we need to remove the 'usa' scope restriction as it doesn't
                # work well with other projections
                if projection_type != 'albers usa':
                    current_scope = getattr(fig.layout.geo, 'scope', None)
                    if current_scope == 'usa':
                        geo_update['scope'] = 'world'

        # Set geographic bounds
        if self.xlim is not None or self.ylim is not None:
            # Calculate bounds with optional expansion
            lon_min, lon_max = self.xlim if self.xlim else (-180, 180)
            lat_min, lat_max = self.ylim if self.ylim else (-90, 90)

            if self.expand:
                # Add ~2% expansion to each side
                lon_range = lon_max - lon_min
                lat_range = lat_max - lat_min
                lon_expand = lon_range * 0.02
                lat_expand = lat_range * 0.02
                lon_min -= lon_expand
                lon_max += lon_expand
                lat_min -= lat_expand
                lat_max += lat_expand
                # Clamp to valid ranges
                lon_min = max(-180, lon_min)
                lon_max = min(180, lon_max)
                lat_min = max(-90, lat_min)
                lat_max = min(90, lat_max)

            geo_update['lonaxis_range'] = [lon_min, lon_max]
            geo_update['lataxis_range'] = [lat_min, lat_max]

            # Calculate center from bounds
            center_lon = (lon_min + lon_max) / 2
            center_lat = (lat_min + lat_max) / 2
            geo_update['center'] = dict(lon=center_lon, lat=center_lat)

        # Handle graticule labels and frame display
        if self.label_graticule:
            # Show lon/lat axes based on label_graticule string
            show_lon = 'E' in self.label_graticule.upper() or 'W' in self.label_graticule.upper()
            show_lat = 'N' in self.label_graticule.upper() or 'S' in self.label_graticule.upper()

            if show_lon:
                geo_update['lonaxis_showgrid'] = True
            if show_lat:
                geo_update['lataxis_showgrid'] = True

        # When bounds are set, show frame with tick labels by default
        if self.xlim is not None or self.ylim is not None:
            geo_update['showframe'] = True
            geo_update['framecolor'] = 'rgba(128, 128, 128, 0.5)'
            geo_update['framewidth'] = 1
            # Show longitude/latitude ticks
            geo_update['lonaxis_showgrid'] = True
            geo_update['lonaxis_gridwidth'] = 0.5
            geo_update['lonaxis_gridcolor'] = 'rgba(128, 128, 128, 0.3)'
            geo_update['lataxis_showgrid'] = True
            geo_update['lataxis_gridwidth'] = 0.5
            geo_update['lataxis_gridcolor'] = 'rgba(128, 128, 128, 0.3)'

        # Apply updates
        if geo_update:
            fig.update_geos(**geo_update)

    def _apply_mapbox(self, fig):
        """Apply coord_sf settings to a mapbox-based figure."""
        # Determine which layout key to use (map vs mapbox)
        # Check which attribute exists on the layout
        if hasattr(fig.layout, 'map') and fig.layout.map is not None:
            layout_key = 'map'
        else:
            layout_key = 'mapbox'

        map_update = {}

        # Set bounds for mapbox
        if self.xlim is not None or self.ylim is not None:
            lon_min, lon_max = self.xlim if self.xlim else (-180, 180)
            lat_min, lat_max = self.ylim if self.ylim else (-90, 90)

            if self.expand:
                lon_range = lon_max - lon_min
                lat_range = lat_max - lat_min
                lon_expand = lon_range * 0.02
                lat_expand = lat_range * 0.02
                lon_min -= lon_expand
                lon_max += lon_expand
                lat_min -= lat_expand
                lat_max += lat_expand

            # Calculate center
            center_lon = (lon_min + lon_max) / 2
            center_lat = (lat_min + lat_max) / 2
            map_update['center'] = dict(lon=center_lon, lat=center_lat)

            # Estimate zoom level from bounds
            lat_range = lat_max - lat_min
            lon_range = lon_max - lon_min
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
            elif max_range > 2:
                zoom = 7
            elif max_range > 1:
                zoom = 8
            else:
                zoom = 9
            map_update['zoom'] = zoom

        # Apply updates
        if map_update:
            fig.update_layout(**{layout_key: map_update})
