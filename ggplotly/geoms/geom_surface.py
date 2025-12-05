# geoms/geom_surface.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper
import pandas as pd
import numpy as np


class geom_surface(Geom):
    """Geom for drawing 3D surface plots."""

    def __init__(self, data=None, mapping=None, **params):
        """
        Create a 3D surface plot.

        Visualizes functions z = f(x, y) or grid data as continuous surfaces.
        Data can be long format (x, y, z columns) or grid format.

        Parameters
        ----------
        data : DataFrame, optional
            Data for the geom (overrides plot data).
        mapping : aes, optional
            Aesthetic mappings. Required: x, y, z.
        colorscale : str, default='Viridis'
            Plotly colorscale: 'Viridis', 'Plasma', 'Inferno', 'Blues', 'RdBu', etc.
        alpha : float, default=1
            Surface opacity (0-1).
        showscale : bool, default=True
            Show the colorbar.
        contours : dict, optional
            Contour settings for x, y, z projections.
        hidesurface : bool, default=False
            Hide surface and show only contours.
        reversescale : bool, default=False
            Reverse the colorscale.
        lighting : dict, optional
            Lighting settings for 3D effect.

        Examples
        --------
        >>> # Basic surface
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_surface()

        >>> # Custom colorscale
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_surface(colorscale='Plasma')
        """
        super().__init__(data, mapping, **params)
        # Set default colorscale
        if 'colorscale' not in self.params:
            self.params['colorscale'] = 'Viridis'

    def _prepare_grid_data(self, data):
        """
        Convert long-format data to grid format for surface plotting.

        Parameters:
            data: DataFrame with x, y, z columns

        Returns:
            tuple: (x_unique, y_unique, z_grid) where z_grid is 2D array

        Raises:
            ValueError: If data does not form a regular grid
        """
        x_col = self.mapping['x']
        y_col = self.mapping['y']
        z_col = self.mapping['z']

        x_vals = data[x_col]
        y_vals = data[y_col]
        z_vals = data[z_col]

        # Get unique sorted values for x and y
        x_unique = np.sort(x_vals.unique())
        y_unique = np.sort(y_vals.unique())

        # Validate that data forms a regular grid
        expected_size = len(x_unique) * len(y_unique)
        if len(data) != expected_size:
            raise ValueError(
                f"geom_surface requires data on a regular x-y grid where z = f(x, y). "
                f"Data has {len(data)} points but a {len(x_unique)}x{len(y_unique)} grid "
                f"expects {expected_size} points. For parametric surfaces (like torus, "
                f"sphere, helicoid), use Plotly's go.Surface directly with 2D arrays."
            )

        # Create a pivot table to get z values as a 2D grid
        # Use pivot_table to handle potential duplicates by averaging
        pivot_df = data.pivot_table(
            values=z_col,
            index=y_col,
            columns=x_col,
            aggfunc='mean'
        )

        # Reindex to ensure proper ordering
        pivot_df = pivot_df.reindex(index=y_unique, columns=x_unique)

        z_grid = pivot_df.values

        return x_unique, y_unique, z_grid

    def _prepare_fill_data(self, data, x_unique, y_unique):
        """
        Prepare surfacecolor data if fill aesthetic is mapped.

        Parameters:
            data: DataFrame
            x_unique: Unique x values
            y_unique: Unique y values

        Returns:
            2D array of fill values or None
        """
        if 'fill' not in self.mapping:
            return None

        fill_col = self.mapping['fill']
        x_col = self.mapping['x']
        y_col = self.mapping['y']

        # Pivot the fill column
        pivot_df = data.pivot_table(
            values=fill_col,
            index=y_col,
            columns=x_col,
            aggfunc='mean'
        )

        pivot_df = pivot_df.reindex(index=y_unique, columns=x_unique)

        return pivot_df.values

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        # Validate required aesthetics
        if 'x' not in self.mapping or 'y' not in self.mapping or 'z' not in self.mapping:
            raise ValueError("geom_surface requires 'x', 'y', and 'z' aesthetics")

        # Prepare grid data
        x_unique, y_unique, z_grid = self._prepare_grid_data(data)

        # Check for fill aesthetic (surfacecolor)
        surfacecolor = self._prepare_fill_data(data, x_unique, y_unique)

        # Get parameters
        alpha = self.params.get('alpha', 1.0)
        colorscale = self.params.get('colorscale', 'Viridis')
        showscale = self.params.get('showscale', True)
        reversescale = self.params.get('reversescale', False)
        hidesurface = self.params.get('hidesurface', False)
        contours = self.params.get('contours', None)
        lighting = self.params.get('lighting', None)
        name = self.params.get('name', 'Surface')

        # Get scene key for faceting support
        scene_key = self.params.get('_scene_key', 'scene')

        # Build surface trace
        surface_kwargs = dict(
            x=x_unique,
            y=y_unique,
            z=z_grid,
            colorscale=colorscale,
            opacity=alpha,
            showscale=showscale,
            reversescale=reversescale,
            hidesurface=hidesurface,
            name=name,
            scene=scene_key,
        )

        # Add surfacecolor if fill is mapped
        if surfacecolor is not None:
            surface_kwargs['surfacecolor'] = surfacecolor

        # Add contours if specified
        if contours is not None:
            surface_kwargs['contours'] = contours

        # Add lighting if specified
        if lighting is not None:
            surface_kwargs['lighting'] = lighting

        # Handle colorbar settings
        colorbar_params = {}
        if 'colorbar_title' in self.params:
            colorbar_params['title'] = self.params['colorbar_title']
        if colorbar_params:
            surface_kwargs['colorbar'] = colorbar_params

        # Create and add trace
        trace = go.Surface(**surface_kwargs)
        fig.add_trace(trace)

        # Update 3D scene layout with axis labels
        scene_dict = {}
        if 'x' in self.mapping:
            scene_dict['xaxis_title'] = self.mapping['x']
        if 'y' in self.mapping:
            scene_dict['yaxis_title'] = self.mapping['y']
        if 'z' in self.mapping:
            scene_dict['zaxis_title'] = self.mapping['z']

        if scene_dict:
            fig.update_layout(**{scene_key: scene_dict})


class geom_wireframe(Geom):
    """
    Geom for drawing 3D wireframe plots.

    Creates a wireframe (mesh) representation of a surface using Plotly's Scatter3d
    with lines connecting grid points.

    Parameters:
        x (str): Column name for x-axis values (via aes mapping).
        y (str): Column name for y-axis values (via aes mapping).
        z (str): Column name for z-axis values (via aes mapping).
        color (str, optional): Wire color. Default is '#1f77b4'.
        linewidth (float, optional): Width of wireframe lines. Default is 1.
        alpha (float, optional): Line opacity. Default is 1.

    Examples:
        >>> # Basic wireframe
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_wireframe()

        >>> # Wireframe with custom color
        >>> ggplot(df, aes(x='x', y='y', z='z')) + geom_wireframe(color='red', linewidth=2)
    """

    def _prepare_grid_data(self, data):
        """Convert long-format data to grid format.

        Raises:
            ValueError: If data does not form a regular grid
        """
        x_col = self.mapping['x']
        y_col = self.mapping['y']
        z_col = self.mapping['z']

        x_vals = data[x_col]
        y_vals = data[y_col]

        x_unique = np.sort(x_vals.unique())
        y_unique = np.sort(y_vals.unique())

        # Validate that data forms a regular grid
        expected_size = len(x_unique) * len(y_unique)
        if len(data) != expected_size:
            raise ValueError(
                f"geom_wireframe requires data on a regular x-y grid where z = f(x, y). "
                f"Data has {len(data)} points but a {len(x_unique)}x{len(y_unique)} grid "
                f"expects {expected_size} points. For parametric surfaces (like torus, "
                f"sphere, helicoid), use Plotly's go.Surface directly with 2D arrays."
            )

        pivot_df = data.pivot_table(
            values=z_col,
            index=y_col,
            columns=x_col,
            aggfunc='mean'
        )

        pivot_df = pivot_df.reindex(index=y_unique, columns=x_unique)

        return x_unique, y_unique, pivot_df.values

    def draw(self, fig, data=None, row=1, col=1):
        data = data if data is not None else self.data

        if 'x' not in self.mapping or 'y' not in self.mapping or 'z' not in self.mapping:
            raise ValueError("geom_wireframe requires 'x', 'y', and 'z' aesthetics")

        x_unique, y_unique, z_grid = self._prepare_grid_data(data)

        # Get parameters
        color = self.params.get('color', '#1f77b4')
        linewidth = self.params.get('linewidth', 1)
        alpha = self.params.get('alpha', 1.0)
        scene_key = self.params.get('_scene_key', 'scene')

        # Create meshgrid
        X, Y = np.meshgrid(x_unique, y_unique)

        # Create wireframe lines
        # Lines along x direction
        for i in range(len(y_unique)):
            fig.add_trace(go.Scatter3d(
                x=X[i, :],
                y=Y[i, :],
                z=z_grid[i, :],
                mode='lines',
                line=dict(color=color, width=linewidth),
                opacity=alpha,
                showlegend=False,
                scene=scene_key,
            ))

        # Lines along y direction
        for j in range(len(x_unique)):
            fig.add_trace(go.Scatter3d(
                x=X[:, j],
                y=Y[:, j],
                z=z_grid[:, j],
                mode='lines',
                line=dict(color=color, width=linewidth),
                opacity=alpha,
                showlegend=False,
                scene=scene_key,
            ))

        # Update scene layout
        scene_dict = {}
        if 'x' in self.mapping:
            scene_dict['xaxis_title'] = self.mapping['x']
        if 'y' in self.mapping:
            scene_dict['yaxis_title'] = self.mapping['y']
        if 'z' in self.mapping:
            scene_dict['zaxis_title'] = self.mapping['z']

        if scene_dict:
            fig.update_layout(**{scene_key: scene_dict})
