import pandas as pd
from plotly.subplots import make_subplots
from plotly.graph_objects import Figure


# facets.py
class Facet:
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
    def __init__(self, rows, cols):
        """
        Initialize a facet_grid object.

        Parameters:
            rows (str): The column in the dataframe by which to facet the rows.
            cols (str): The column in the dataframe by which to facet the columns.
        """
        self.rows = rows
        self.cols = cols

    def apply(self, plot):
        """
        Apply facet grid to the plot.

        Parameters:
            plot (ggplot): The ggplot object.

        Returns:
            Figure: A Plotly figure with facets applied in a grid.
        """
        # Get unique values for the row and column variables
        row_facets = plot.data[self.rows].unique()
        col_facets = plot.data[self.cols].unique()

        nrows = len(row_facets)
        ncols = len(col_facets)

        # Create a subplot figure with the required number of rows and columns
        fig = make_subplots(
            rows=nrows,
            cols=ncols,
            subplot_titles=[f"{row}/{col}" for row in row_facets for col in col_facets],
        )

        # Iterate through each combination of row and column facets and draw geoms
        for row_idx, row_value in enumerate(row_facets):
            for col_idx, col_value in enumerate(col_facets):
                row = row_idx + 1
                col = col_idx + 1

                # Subset data for the current facet (row and column combination)
                facet_data = plot.data[
                    (plot.data[self.rows] == row_value)
                    & (plot.data[self.cols] == col_value)
                ]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # If geom has its own explicit data, use that for faceting instead of plot.data
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[
                            (geom.data[self.rows] == row_value)
                            & (geom.data[self.cols] == col_value)
                        ]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)
                    geom.draw(fig, row=row, col=col)

        return fig


class facet_wrap(Facet):
    def __init__(self, facet_var, ncol=None, nrow=None, scales='fixed'):
        """
        Initialize a facet_wrap object.

        Parameters:
            facet_var (str): The column in the dataframe by which to facet the plot.
            ncol (int): Number of columns to arrange the facets in.
            nrow (int): Number of rows to arrange the facets in (optional).
            scales (str): How to handle scales across facets. Options:
                - 'fixed': All facets share the same scale (default for geo)
                - 'free': Each facet has its own scale
        """
        self.facet_var = facet_var
        self.ncol = ncol
        self.nrow = nrow
        self.scales = scales

    def _has_geo_geoms(self, plot):
        """Check if any geom requires geographic layout."""
        geo_geom_types = ('geom_map', 'geom_point_map')
        for geom in plot.layers:
            if geom.__class__.__name__ in geo_geom_types:
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
        """
        # Determine unique facets and layout
        unique_facets = plot.data[self.facet_var].unique()
        n_facets = len(unique_facets)

        # Calculate number of columns and rows
        if self.ncol is None:
            self.ncol = min(n_facets, 3)  # Default to max 3 columns for geo
        if self.nrow is None:
            self.nrow = -(-n_facets // self.ncol)  # Ceiling division

        # Check if we need geo subplots
        is_geo = self._has_geo_geoms(plot)

        if is_geo:
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
                row = idx // self.ncol  # 0-indexed row
                col = idx % self.ncol   # 0-indexed col
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
                fig.add_annotation(
                    text=f"<b>{facet_value}</b>",
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
            fig = make_subplots(
                rows=self.nrow,
                cols=self.ncol,
                subplot_titles=[str(f) for f in unique_facets],
            )

            # Iterate through each unique facet and subset the data accordingly
            for idx, facet_value in enumerate(unique_facets):
                row = (idx // self.ncol) + 1
                col = (idx % self.ncol) + 1

                # Subset the data for the current facet
                facet_data = plot.data[plot.data[self.facet_var] == facet_value]

                # Draw each geom on the subplot for the current facet
                for geom in plot.layers:
                    # If geom has its own explicit data, use that for faceting
                    if hasattr(geom, '_has_explicit_data') and geom._has_explicit_data:
                        geom_facet_data = geom.data[geom.data[self.facet_var] == facet_value]
                        geom.setup_data(geom_facet_data, plot.mapping)
                    else:
                        geom.setup_data(facet_data, plot.mapping)
                    geom.draw(fig, row=row, col=col)

        return fig
