"""
Geom for drawing sea routes between ports using the searoute package.

Creates realistic maritime shipping routes with overlap highlighting,
similar to geom_edgebundle but using actual shipping lanes.

Automatically detects geo context and uses Scattergeo when a map is present.
"""

import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .geom_base import Geom

def _get_searoute():
    """Lazy import of searoute package."""
    try:
        import searoute as sr
        return sr
    except (ImportError, ModuleNotFoundError):
        return None


class geom_searoute(Geom):
    """Sea routes for maritime visualization using the searoute package."""

    def __init__(
        self,
        mapping=None,
        data=None,
        units: str = 'km',
        speed_knot: float = None,
        append_orig_dest: bool = False,
        restrictions: list = None,
        include_ports: bool = False,
        port_params: dict = None,
        color: str = '#ff6b35',
        alpha: float = 0.6,
        linewidth: float = 0.8,
        show_highlight: bool = True,
        highlight_color: str = 'white',
        highlight_alpha: float = 0.2,
        highlight_width: float = 0.15,
        show_ports: bool = True,
        port_color: str = '#00ff88',
        port_size: float = 5,
        port_alpha: float = 0.9,
        verbose: bool = False,
        **kwargs
    ):
        """
        Create sea routes for maritime visualization.

        Uses the searoute package to calculate realistic shipping routes
        between ports. Routes follow actual maritime lanes and avoid land.
        Supports overlap highlighting similar to geom_edgebundle.

        Note: This is for visualization purposes only, not for actual
        maritime navigation or routing.

        Parameters
        ----------
        mapping : aes, optional
            Aesthetic mappings. Required: x, y (origin lon/lat),
            xend, yend (destination lon/lat).
        data : DataFrame, optional
            Data containing origin and destination coordinates.
            Each row represents one route.
        units : str, default='km'
            Distance units. Options: 'km', 'm', 'mi', 'naut' (nautical miles),
            'ft', 'in', 'deg', 'rad', 'yd'.
        speed_knot : float, optional
            If provided, calculates estimated duration based on this speed.
        append_orig_dest : bool, default=False
            Whether to append origin and destination to the route path.
        restrictions : list, optional
            List of passages to avoid. Options include:
            'northwest', 'suez', 'panama', 'malacca', 'bering', etc.
        include_ports : bool, default=False
            Whether to include port information in the route calculation.
        port_params : dict, optional
            Additional parameters for port selection.
        color : str, default='#ff6b35'
            Route line color.
        alpha : float, default=0.6
            Route line transparency (0-1).
        linewidth : float, default=0.8
            Route line width.
        show_highlight : bool, default=True
            Add highlight lines on top of routes to emphasize overlaps.
        highlight_color : str, default='white'
            Highlight line color.
        highlight_alpha : float, default=0.2
            Highlight transparency (0-1).
        highlight_width : float, default=0.15
            Highlight line width.
        show_ports : bool, default=True
            Show origin and destination port markers.
        port_color : str, default='#00ff88'
            Port marker color.
        port_size : float, default=5
            Port marker size.
        port_alpha : float, default=0.9
            Port marker transparency (0-1).
        verbose : bool, default=False
            Print progress messages and route statistics.

        Examples
        --------
        >>> # Basic sea route visualization
        >>> routes = pd.DataFrame({
        ...     'x': [0.35, -74.01],      # origin longitudes
        ...     'y': [50.06, 40.71],      # origin latitudes
        ...     'xend': [117.42, 1.29],   # destination longitudes
        ...     'yend': [39.37, 103.85]   # destination latitudes
        ... })
        >>> (ggplot(routes, aes(x='x', y='y', xend='xend', yend='yend'))
        ...  + geom_map(map_type='world')
        ...  + geom_searoute())

        >>> # With custom styling and no Suez Canal
        >>> (ggplot(routes, aes(x='x', y='y', xend='xend', yend='yend'))
        ...  + geom_map(map_type='world')
        ...  + geom_searoute(
        ...      restrictions=['suez'],
        ...      color='steelblue',
        ...      linewidth=1.0,
        ...      highlight_color='yellow'
        ...  ))
        """

        super().__init__(data=data, mapping=mapping, **kwargs)

        # Searoute parameters
        self.units = units
        self.speed_knot = speed_knot
        self.append_orig_dest = append_orig_dest
        self.restrictions = restrictions or []
        self.include_ports = include_ports
        self.port_params = port_params or {}
        self.verbose = verbose

        # Visual parameters
        self.params['color'] = color
        self.params['alpha'] = alpha
        self.params['linewidth'] = linewidth
        self.params['show_highlight'] = show_highlight
        self.params['highlight_color'] = highlight_color
        self.params['highlight_alpha'] = highlight_alpha
        self.params['highlight_width'] = highlight_width
        self.params['show_ports'] = show_ports
        self.params['port_color'] = port_color
        self.params['port_size'] = port_size
        self.params['port_alpha'] = port_alpha

        # Cache for computed routes
        self._route_cache = {}

    def _is_geo_figure(self, fig) -> bool:
        """
        Check if figure has geo context (map traces present).

        Returns True if any Scattergeo or Choropleth traces exist,
        indicating we should render routes as Scattergeo too.
        """
        if not fig.data:
            return False

        geo_types = ('scattergeo', 'choropleth', 'scattermapbox', 'choroplethmapbox')
        return any(
            hasattr(trace, 'type') and trace.type in geo_types
            for trace in fig.data
        )

    def _compute_route(self, origin, destination):
        """
        Compute a single sea route using searoute.

        Parameters
        ----------
        origin : tuple
            (lon, lat) of origin port
        destination : tuple
            (lon, lat) of destination port

        Returns
        -------
        dict or None
            Route GeoJSON feature with coordinates and properties,
            or None if route calculation fails.
        """
        cache_key = (origin, destination, tuple(self.restrictions))
        if cache_key in self._route_cache:
            return self._route_cache[cache_key]

        try:
            # Convert to plain Python floats (searoute doesn't handle numpy types well)
            origin_list = [float(origin[0]), float(origin[1])]
            dest_list = [float(destination[0]), float(destination[1])]

            # Build kwargs dynamically - only include non-None optional params
            kwargs = {
                'units': self.units,
                'append_orig_dest': self.append_orig_dest,
                'include_ports': self.include_ports,
            }

            # Only add optional params if they have values
            if self.speed_knot is not None:
                kwargs['speed_knot'] = self.speed_knot
            if self.restrictions:
                kwargs['restrictions'] = self.restrictions
            if self.port_params:
                kwargs['port_params'] = self.port_params

            try:
                import searoute as sr
            except (ImportError, ModuleNotFoundError):
                raise ImportError("searoute package is required for geom_searoute but is not installed.")

            route = sr.searoute(origin_list, dest_list, **kwargs)
            self._route_cache[cache_key] = route
            return route
        except Exception as e:
            if self.verbose:
                print(f"Warning: Could not compute route from {origin} to {destination}: {e}")
            self._route_cache[cache_key] = None
            return None

    def _extract_route_coords(self, route):
        """
        Extract coordinates from a GeoJSON route feature.

        Parameters
        ----------
        route : dict
            GeoJSON Feature from searoute

        Returns
        -------
        tuple
            (lons, lats) arrays of route coordinates
        """
        if route is None:
            return None, None

        coords = route['geometry']['coordinates']
        lons = [c[0] for c in coords]
        lats = [c[1] for c in coords]
        return np.array(lons), np.array(lats)

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw sea routes on the figure.

        Automatically detects geo context and uses appropriate trace type.
        """
        data = data if data is not None else self.data

        if data is None or (hasattr(data, 'empty') and data.empty):
            return fig

        # Get aesthetic mappings
        x = self.mapping.get('x', 'x')
        y = self.mapping.get('y', 'y')
        xend = self.mapping.get('xend', 'xend')
        yend = self.mapping.get('yend', 'yend')

        # Validate required columns
        required = [x, y, xend, yend]
        missing = [c for c in required if c not in data.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

        # Check if we're in geo context
        is_geo = self._is_geo_figure(fig)

        # Get visual parameters
        color = self.params.get('color', '#ff6b35')
        alpha = self.params.get('alpha', 0.6)
        linewidth = self.params.get('linewidth', 0.8)
        show_highlight = self.params.get('show_highlight', True)
        highlight_color = self.params.get('highlight_color', 'white')
        highlight_alpha = self.params.get('highlight_alpha', 0.2)
        highlight_width = self.params.get('highlight_width', 0.15)

        # Convert colors to rgba
        rgba_color = self._color_to_rgba(color, alpha)
        rgba_highlight = self._color_to_rgba(highlight_color, highlight_alpha)

        # Compute and draw routes
        routes_data = []
        total_distance = 0

        if self.verbose:
            print(f"Computing {len(data)} sea routes...")

        for idx, row_data in data.iterrows():
            origin = (row_data[x], row_data[y])
            destination = (row_data[xend], row_data[yend])

            route = self._compute_route(origin, destination)
            if route is not None:
                lons, lats = self._extract_route_coords(route)
                if lons is not None:
                    routes_data.append({
                        'lons': lons,
                        'lats': lats,
                        'origin': origin,
                        'destination': destination,
                        'distance': route['properties'].get('length', 0),
                        'units': route['properties'].get('units', self.units)
                    })
                    total_distance += route['properties'].get('length', 0)

        if self.verbose:
            print(f"Successfully computed {len(routes_data)} routes")
            print(f"Total distance: {total_distance:.1f} {self.units}")

        # Draw routes (main lines first, then highlights on top)
        if is_geo:
            self._draw_geo_routes(fig, routes_data, rgba_color, linewidth)
            if show_highlight:
                self._draw_geo_routes(fig, routes_data, rgba_highlight, highlight_width)
        else:
            self._draw_cartesian_routes(fig, routes_data, rgba_color, linewidth, row, col)
            if show_highlight:
                self._draw_cartesian_routes(fig, routes_data, rgba_highlight, highlight_width, row, col)

        # Draw port markers
        if self.params.get('show_ports', True):
            self._draw_ports(fig, routes_data, is_geo, row, col)

        return fig

    def _draw_cartesian_routes(self, fig, routes_data, color, width, row, col):
        """Draw routes as Scatter traces (Cartesian coordinates)."""
        for route in routes_data:
            fig.add_trace(
                go.Scatter(
                    x=route['lons'],
                    y=route['lats'],
                    mode='lines',
                    line=dict(color=color, width=width),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=row,
                col=col
            )

    def _draw_geo_routes(self, fig, routes_data, color, width):
        """Draw routes as Scattergeo traces (geographic coordinates)."""
        for route in routes_data:
            fig.add_trace(
                go.Scattergeo(
                    lon=route['lons'],
                    lat=route['lats'],
                    mode='lines',
                    line=dict(color=color, width=width),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )

    def _draw_ports(self, fig, routes_data, is_geo, row, col):
        """Draw port markers at origins and destinations."""
        port_color = self.params.get('port_color', '#00ff88')
        port_size = self.params.get('port_size', 5)
        port_alpha = self.params.get('port_alpha', 0.9)

        rgba_port = self._color_to_rgba(port_color, port_alpha)

        # Collect unique ports
        ports = set()
        for route in routes_data:
            ports.add(route['origin'])
            ports.add(route['destination'])

        if not ports:
            return

        port_lons = [p[0] for p in ports]
        port_lats = [p[1] for p in ports]

        if is_geo:
            fig.add_trace(
                go.Scattergeo(
                    lon=port_lons,
                    lat=port_lats,
                    mode='markers',
                    marker=dict(color=rgba_port, size=port_size),
                    showlegend=False,
                    hoverinfo='skip'
                )
            )
        else:
            fig.add_trace(
                go.Scatter(
                    x=port_lons,
                    y=port_lats,
                    mode='markers',
                    marker=dict(color=rgba_port, size=port_size),
                    showlegend=False,
                    hoverinfo='skip'
                ),
                row=row,
                col=col
            )

    def _color_to_rgba(self, color: str, alpha: float) -> str:
        """Convert color name/hex to RGBA string with alpha."""
        color_map = {
            'steelblue': (70, 130, 180),
            'blue': (0, 0, 255),
            'red': (255, 0, 0),
            'green': (0, 128, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'magenta': (157, 1, 145),
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'yellow': (255, 255, 0),
            'cyan': (0, 255, 255),
            'gold': (255, 215, 0),
            'coral': (255, 127, 80),
            'navy': (0, 0, 128),
            'teal': (0, 128, 128),
        }

        if color.startswith('rgba'):
            return color
        elif color.startswith('#'):
            color = color.lstrip('#')
            if len(color) == 6:
                r, g, b = int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16)
            elif len(color) == 3:
                r, g, b = int(color[0]*2, 16), int(color[1]*2, 16), int(color[2]*2, 16)
            else:
                r, g, b = 255, 107, 53  # Default orange
        elif color.lower() in color_map:
            r, g, b = color_map[color.lower()]
        else:
            r, g, b = 255, 107, 53  # Default orange

        return f'rgba({r},{g},{b},{alpha})'
