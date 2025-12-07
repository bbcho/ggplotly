import warnings
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
from plotly.graph_objects import Figure

from .constants import SHAPE_PALETTE, get_color_palette
from .exceptions import FacetColumnNotFoundError, TooManyFacetsWarning


# facets.py
class Facet:
    """
    Base class for faceting operations.

    Faceting creates multiple panels (subplots) based on one or more
    categorical variables, allowing comparison across groups.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + facet_wrap('category')
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + facet_grid('row_var', 'col_var')
    """
    def _compute_global_aesthetic_maps(self, plot):
        """
        Compute global color and shape maps from the full dataset.

        This ensures consistent colors/shapes across all facets.

        Parameters:
            plot (ggplot): The ggplot object with full data.

        Returns:
            Tuple of (global_color_map, global_shape_map)
        """
        data = plot.data
        mapping = plot.mapping

        # Get color palette from theme or default (using shared function)
        palette = get_color_palette(plot.theme)

        # Compute global color map
        global_color_map = None
        color_col = mapping.get('color') or mapping.get('fill')
        if color_col and color_col in data.columns:
            unique_values = data[color_col].dropna().unique()
            global_color_map = {}
            for i, val in enumerate(unique_values):
                global_color_map[val] = palette[i % len(palette)]

        # Compute global shape map
        global_shape_map = None
        shape_col = mapping.get('shape')
        if shape_col and shape_col in data.columns:
            unique_values = data[shape_col].dropna().unique()
            global_shape_map = {}
            for i, val in enumerate(unique_values):
                global_shape_map[val] = SHAPE_PALETTE[i % len(SHAPE_PALETTE)]

        return global_color_map, global_shape_map

    def _apply_global_maps_to_geom(self, geom, global_color_map, global_shape_map):
        """Apply global aesthetic maps to a geom."""
        geom._global_color_map = global_color_map
        geom._global_shape_map = global_shape_map

    def apply(self, plot) -> None | Figure:
        """
        Apply faceting to the plot.

        Parameters:
            plot (ggplot): The ggplot object.

        Returns:
            Figure: A Plotly figure with facets applied.
        """
        pass  # To be implemented by subclasses


# facets/facet_grid.py

from plotly.subplots import make_subplots


class facet_grid(Facet):
    def __init__(self, rows, cols, scales='fixed', space='fixed', labeller=None,
                 margins=False, drop=True, switch=None):
        """
        Initialize a facet_grid object.

        Parameters:
            rows (str): The column in the dataframe by which to facet the rows.
            cols (str): The column in the dataframe by which to facet the columns.
            scales (str): How to handle scales across facets. Options:
                - 'fixed': All facets share the same scale (default)
                - 'free': Each facet has its own scale
                - 'free_x': x-axis is free, y-axis is shared
                - 'free_y': y-axis is free, x-axis is shared
            space (str): How to allocate space for facets. Options:
                - 'fixed': All facets have equal size (default)
                - 'free': Size proportional to data range
                - 'free_x': Width proportional to x-axis range
                - 'free_y': Height proportional to y-axis range
            labeller (callable or str): Function to generate facet labels. Options:
                - None or 'value': Just show the value (default)
                - 'both': Show "variable: value"
                - callable: Function that takes (variable, value) and returns label string
            margins (bool or list): If True, add marginal facets showing all data.
                If a list, specifies which margins to display (e.g., ['rows', 'cols']).
                Default is False.
            drop (bool): If True (default), drop unused factor levels from faceting.
            switch (str): Position to switch strip labels. Options:
                - None: Default positions (top for cols, right for rows)
                - 'x': Switch column labels to bottom
                - 'y': Switch row labels to left
                - 'both': Switch both
        """
        self.rows = rows
        self.cols = cols
        self.scales = scales
        self.space = space
        self.labeller = labeller
        self.margins = margins
        self.drop = drop
        self.switch = switch

    def _get_label(self, row_var, row_val, col_var, col_val):
        """Generate label for a facet based on labeller setting."""
        if self.labeller is None or self.labeller == 'value':
            return f"{row_val}/{col_val}"
        elif self.labeller == 'both':
            return f"{row_var}: {row_val} / {col_var}: {col_val}"
        elif callable(self.labeller):
            row_label = self.labeller(row_var, row_val)
            col_label = self.labeller(col_var, col_val)
            return f"{row_label}/{col_label}"
        else:
            return f"{row_val}/{col_val}"

    def _has_3d_geoms(self, plot):
        """Check if any geom requires 3D layout."""
        geom_3d_types = ('geom_point_3d', 'geom_surface', 'geom_wireframe')
        for geom in plot.layers:
            if geom.__class__.__name__ in geom_3d_types:
                return True
        return False

    def apply(self, plot):
        """
        Apply facet grid to the plot.

        Parameters:
            plot (ggplot): The ggplot object.

        Returns:
            Figure: A Plotly figure with facets applied in a grid.

        Raises:
            FacetColumnNotFoundError: If row or column variable doesn't exist in the data.
        """
        # Validate row facet column exists
        if self.rows not in plot.data.columns:
            raise FacetColumnNotFoundError(
                self.rows,
                list(plot.data.columns),
                facet_type="facet_grid rows"
            )

        # Validate column facet column exists
        if self.cols not in plot.data.columns:
            raise FacetColumnNotFoundError(
                self.cols,
                list(plot.data.columns),
                facet_type="facet_grid cols"
            )

        # Get unique values for the row and column variables
        row_facets = plot.data[self.rows].unique()
        col_facets = plot.data[self.cols].unique()

        nrows = len(row_facets)
        ncols = len(col_facets)

        # Warn if too many facets
        total_facets = nrows * ncols
        if total_facets > 25:
            warnings.warn(
                f"facet_grid will create {total_facets} subplots ({nrows} rows x {ncols} cols). "
                f"This may be slow to render. Consider filtering your data.",
                TooManyFacetsWarning
            )

        # Determine axis sharing based on scales parameter
        shared_x = self.scales in ('fixed', 'free_y')
        shared_y = self.scales in ('fixed', 'free_x')

        # Generate labels
        labels = [self._get_label(self.rows, row, self.cols, col)
                  for row in row_facets for col in col_facets]

        # Calculate column widths and row heights based on space parameter
        column_widths = None
        row_heights = None

        if self.space in ('free', 'free_x'):
            # Calculate width proportional to x-axis data range per column
            x_col = plot.mapping.get('x')
            if x_col and x_col in plot.data.columns:
                col_ranges = []
                for col_val in col_facets:
                    col_data = plot.data[plot.data[self.cols] == col_val][x_col]
                    if len(col_data) > 0:
                        col_ranges.append(col_data.max() - col_data.min())
                    else:
                        col_ranges.append(1)
                total = sum(col_ranges)
                if total > 0:
                    column_widths = [r / total for r in col_ranges]

        if self.space in ('free', 'free_y'):
            # Calculate height proportional to y-axis data range per row
            y_col = plot.mapping.get('y')
            if y_col and y_col in plot.data.columns:
                row_ranges = []
                for row_val in row_facets:
                    row_data = plot.data[plot.data[self.rows] == row_val][y_col]
                    if len(row_data) > 0:
                        row_ranges.append(row_data.max() - row_data.min())
                    else:
                        row_ranges.append(1)
                total = sum(row_ranges)
                if total > 0:
                    row_heights = [r / total for r in row_ranges]

        # Check if we need 3D subplots
        is_3d = self._has_3d_geoms(plot)

        # Build specs for subplots (3D needs type='scene')
        if is_3d:
            specs = [[{"type": "scene"} for _ in range(ncols)] for _ in range(nrows)]
        else:
            specs = None

        # Create a subplot figure with the required number of rows and columns
        fig = make_subplots(
            rows=nrows,
            cols=ncols,
            subplot_titles=labels,
            shared_xaxes=shared_x if not is_3d else False,
            shared_yaxes=shared_y if not is_3d else False,
            column_widths=column_widths,
            row_heights=row_heights,
            specs=specs,
            horizontal_spacing=0.05 if is_3d else 0.2,
            vertical_spacing=0.1 if is_3d else 0.3,
        )

        # Compute global color/shape maps from full dataset for consistent colors across facets
        global_color_map, global_shape_map = self._compute_global_aesthetic_maps(plot)

        # Iterate through each combination of row and column facets and draw geoms
        for row_idx, row_value in enumerate(row_facets):
            for col_idx, col_value in enumerate(col_facets):
                row = row_idx + 1
                col = col_idx + 1

                # For 3D, determine the scene key
                if is_3d:
                    scene_idx = row_idx * ncols + col_idx + 1
                    scene_key = f"scene{scene_idx}" if scene_idx > 1 else "scene"
                else:
                    scene_key = None

                # Subset data for the current facet (row and column combination)
                facet_data = plot.data[
                    (plot.data[self.rows] == row_value)
                    & (plot.data[self.cols] == col_value)
                ]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # Apply global aesthetic maps for consistent colors across facets
                    self._apply_global_maps_to_geom(geom, global_color_map, global_shape_map)

                    # If geom has its own explicit data, use that for faceting instead of plot.data
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[
                            (geom.data[self.rows] == row_value)
                            & (geom.data[self.cols] == col_value)
                        ]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)

                    # Pass scene key for 3D geoms
                    if scene_key:
                        geom.params['_scene_key'] = scene_key

                    geom.draw(fig, row=row, col=col)

        return fig


def label_value(value):
    """Default labeller - just returns the value as string."""
    return str(value)


def label_both(variable, value):
    """Labeller that shows both variable name and value."""
    return f"{variable}: {value}"


class facet_wrap(Facet):
    def __init__(self, facet_var, ncol=None, nrow=None, scales='fixed', dir='h',
                 labeller=None, strip_position='top', drop=True, as_table=True):
        """
        Initialize a facet_wrap object.

        Parameters:
            facet_var (str): The column in the dataframe by which to facet the plot.
            ncol (int): Number of columns to arrange the facets in.
            nrow (int): Number of rows to arrange the facets in (optional).
            scales (str): How to handle scales across facets. Options:
                - 'fixed': All facets share the same scale (default)
                - 'free': Each facet has its own scale
                - 'free_x': x-axis is free, y-axis is shared
                - 'free_y': y-axis is free, x-axis is shared
            dir (str): Direction to wrap facets. Options:
                - 'h': Horizontal (left to right, then down) - default
                - 'v': Vertical (top to bottom, then right)
            labeller (callable or str): Function to generate facet labels. Options:
                - None or 'value': Just show the value (default)
                - 'both': Show "variable: value"
                - callable: Function that takes (variable, value) and returns label string
            strip_position (str): Position of facet labels. Options:
                - 'top': Labels on top (default)
                - 'bottom': Labels on bottom
                - 'left': Labels on left
                - 'right': Labels on right
            drop (bool): If True (default), drop unused factor levels from faceting.
            as_table (bool): If True (default), arrange facets like a table with highest
                values at bottom-right. If False, arrange like a plot with highest
                values at top-right.
        """
        self.facet_var = facet_var
        self.ncol = ncol
        self.nrow = nrow
        self.scales = scales
        self.dir = dir
        self.labeller = labeller
        self.strip_position = strip_position
        self.drop = drop
        self.as_table = as_table

    def _get_label(self, facet_value):
        """Generate label for a facet based on labeller setting."""
        if self.labeller is None or self.labeller == 'value':
            return str(facet_value)
        elif self.labeller == 'both':
            return f"{self.facet_var}: {facet_value}"
        elif callable(self.labeller):
            return self.labeller(self.facet_var, facet_value)
        else:
            return str(facet_value)

    def _get_row_col(self, idx, n_facets):
        """Get row and column for a facet index based on direction."""
        if self.dir == 'v':
            # Vertical: fill columns first (top to bottom, then right)
            col = idx // self.nrow
            row = idx % self.nrow
        else:
            # Horizontal: fill rows first (left to right, then down) - default
            row = idx // self.ncol
            col = idx % self.ncol
        return row, col

    def _has_geo_geoms(self, plot):
        """Check if any geom requires geographic layout."""
        geo_geom_types = ('geom_map', 'geom_point_map')
        for geom in plot.layers:
            if geom.__class__.__name__ in geo_geom_types:
                return True
        return False

    def _has_3d_geoms(self, plot):
        """Check if any geom requires 3D layout."""
        geom_3d_types = ('geom_point_3d', 'geom_surface', 'geom_wireframe')
        for geom in plot.layers:
            if geom.__class__.__name__ in geom_3d_types:
                return True
        return False

    def _get_geo_specs(self, plot):
        """Get map type info from the first geo geom."""
        for geom in plot.layers:
            if geom.__class__.__name__ == 'geom_map':
                return geom.map_type
            elif geom.__class__.__name__ == 'geom_point_map':
                return getattr(geom, 'map_type', 'state')
        return 'state'

    def apply(self, plot):
        """
        Apply facet wrapping to the plot.

        Parameters:
            plot (ggplot): The ggplot object.

        Returns:
            Figure: A Plotly figure with facets applied.

        Raises:
            FacetColumnNotFoundError: If the facet variable doesn't exist in the data.
        """
        # Validate facet column exists
        if self.facet_var not in plot.data.columns:
            raise FacetColumnNotFoundError(
                self.facet_var,
                list(plot.data.columns),
                facet_type="facet_wrap"
            )

        # Determine unique facets and layout
        unique_facets = plot.data[self.facet_var].unique()
        n_facets = len(unique_facets)

        # Warn if too many facets
        if n_facets > 25:
            warnings.warn(
                f"Facet variable '{self.facet_var}' has {n_facets} unique values. "
                f"This will create {n_facets} subplots which may be slow to render. "
                f"Consider filtering your data or using a different faceting variable.",
                TooManyFacetsWarning
            )

        # Calculate number of columns and rows
        if self.ncol is None and self.nrow is None:
            self.ncol = min(n_facets, 3)  # Default to max 3 columns
            self.nrow = -(-n_facets // self.ncol)  # Ceiling division
        elif self.ncol is None:
            self.ncol = -(-n_facets // self.nrow)  # Ceiling division
        elif self.nrow is None:
            self.nrow = -(-n_facets // self.ncol)  # Ceiling division

        # Check if we need special subplot types
        is_geo = self._has_geo_geoms(plot)
        is_3d = self._has_3d_geoms(plot)

        # Compute global color/shape maps from full dataset for consistent colors across facets
        global_color_map, global_shape_map = self._compute_global_aesthetic_maps(plot)

        if is_3d:
            # For 3D subplots, we need to create specs with type='scene'
            from plotly.graph_objects import Figure

            # Generate labels for all facets
            labels = [self._get_label(f) for f in unique_facets]

            # Build specs for 3D subplots
            specs = [[{"type": "scene"} for _ in range(self.ncol)] for _ in range(self.nrow)]

            fig = make_subplots(
                rows=self.nrow,
                cols=self.ncol,
                subplot_titles=labels,
                specs=specs,
                horizontal_spacing=0.05,
                vertical_spacing=0.1,
            )

            # Iterate through each unique facet
            for idx, facet_value in enumerate(unique_facets):
                row, col = self._get_row_col(idx, n_facets)
                row += 1  # Convert to 1-indexed for plotly
                col += 1

                # Determine scene key for this subplot
                scene_idx = (row - 1) * self.ncol + col
                scene_key = f"scene{scene_idx}" if scene_idx > 1 else "scene"

                # Subset the data for the current facet
                facet_data = plot.data[plot.data[self.facet_var] == facet_value]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # Apply global aesthetic maps for consistent colors across facets
                    self._apply_global_maps_to_geom(geom, global_color_map, global_shape_map)

                    # If geom has its own explicit data, use that for faceting
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[geom.data[self.facet_var] == facet_value]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)

                    # Pass scene key for 3D geoms
                    geom.params['_scene_key'] = scene_key
                    geom.draw(fig, row=row, col=col)

        elif is_geo:
            # For geo subplots, we need to manually position each geo
            # Plotly doesn't auto-position geo subplots like xy subplots
            from plotly.graph_objects import Figure
            fig = Figure()

            # Get map type for geo settings
            map_type = self._get_geo_specs(plot)

            # For shared colorbar (scales='fixed'), compute global min/max
            # and pass to geoms for consistent coloring
            global_zmin = None
            global_zmax = None
            fill_col = plot.mapping.get('fill')

            if self.scales == 'fixed' and fill_col and fill_col in plot.data.columns:
                import pandas as pd
                if pd.api.types.is_numeric_dtype(plot.data[fill_col]):
                    global_zmin = plot.data[fill_col].min()
                    global_zmax = plot.data[fill_col].max()

            # Calculate spacing - leave room for title at top and colorbar on right
            h_spacing = 0.02  # horizontal spacing between maps
            v_spacing = 0.08  # vertical spacing between rows
            top_margin = 0.08  # space for main title
            title_height = 0.04  # space for facet titles
            colorbar_width = 0.08 if (self.scales == 'fixed' and global_zmin is not None) else 0

            # Calculate dimensions for each subplot
            available_width = 1.0 - h_spacing * (self.ncol - 1) - colorbar_width
            available_height = 1.0 - top_margin - v_spacing * (self.nrow - 1) - title_height * self.nrow
            plot_width = available_width / self.ncol
            plot_height = available_height / self.nrow

            # Iterate through each unique facet
            for idx, facet_value in enumerate(unique_facets):
                row, col = self._get_row_col(idx, n_facets)
                geo_idx = idx + 1  # geo1, geo2, etc.
                geo_key = f"geo{geo_idx}" if geo_idx > 1 else "geo"

                # Calculate domain for this subplot
                x_start = col * (plot_width + h_spacing)
                x_end = x_start + plot_width
                # Start from top, accounting for title and spacing
                y_end = 1.0 - top_margin - row * (plot_height + v_spacing + title_height)
                y_start = y_end - plot_height

                # Subset the data for the current facet
                facet_data = plot.data[plot.data[self.facet_var] == facet_value]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # Apply global aesthetic maps for consistent colors across facets
                    self._apply_global_maps_to_geom(geom, global_color_map, global_shape_map)

                    # If geom has its own explicit data, use that for faceting
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[geom.data[self.facet_var] == facet_value]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)

                    # Pass geo index and shared scale info
                    geom.params['_geo_key'] = geo_key
                    geom.params['_facet_idx'] = idx
                    geom.params['_facet_count'] = n_facets
                    geom.params['_facet_scales'] = self.scales
                    if global_zmin is not None:
                        geom.params['_global_zmin'] = global_zmin
                        geom.params['_global_zmax'] = global_zmax
                    geom.draw(fig, row=row+1, col=col+1)

                # Set up geo layout for this subplot with domain positioning
                if map_type in ('state', 'usa'):
                    scope = 'usa'
                    projection = 'albers usa'
                elif map_type == 'world':
                    scope = 'world'
                    projection = 'natural earth'
                else:
                    scope = map_type
                    projection = 'natural earth'

                geo_layout = dict(
                    scope=scope,
                    projection_type=projection,
                    showland=True,
                    landcolor='rgb(243, 243, 243)',
                    showocean=False,
                    showlakes=True,
                    lakecolor='rgb(204, 229, 255)',
                    showcountries=True,
                    countrycolor='rgb(204, 204, 204)',
                    showcoastlines=True,
                    coastlinecolor='rgb(204, 204, 204)',
                    domain=dict(
                        x=[x_start, x_end],
                        y=[y_start, y_end]
                    ),
                )
                fig.update_layout(**{geo_key: geo_layout})

                # Add subplot title as annotation
                label = self._get_label(facet_value)
                fig.add_annotation(
                    text=f"<b>{label}</b>",
                    x=(x_start + x_end) / 2,
                    y=y_end + 0.01,
                    xref="paper",
                    yref="paper",
                    showarrow=False,
                    font=dict(size=12),
                    xanchor="center",
                    yanchor="bottom",
                )

        else:
            # Standard non-geo subplots
            # Determine axis sharing based on scales parameter
            shared_x = self.scales in ('fixed', 'free_y')
            shared_y = self.scales in ('fixed', 'free_x')

            # Generate labels for all facets
            labels = [self._get_label(f) for f in unique_facets]

            fig = make_subplots(
                rows=self.nrow,
                cols=self.ncol,
                subplot_titles=labels,
                shared_xaxes=shared_x,
                shared_yaxes=shared_y,
            )

            # Iterate through each unique facet and subset the data accordingly
            for idx, facet_value in enumerate(unique_facets):
                row, col = self._get_row_col(idx, n_facets)
                row += 1  # Convert to 1-indexed for plotly
                col += 1

                # Subset the data for the current facet
                facet_data = plot.data[plot.data[self.facet_var] == facet_value]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # Apply global aesthetic maps for consistent colors across facets
                    self._apply_global_maps_to_geom(geom, global_color_map, global_shape_map)

                    # If geom has its own explicit data, use that for faceting
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[geom.data[self.facet_var] == facet_value]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)
                    geom.draw(fig, row=row, col=col)

        return fig
