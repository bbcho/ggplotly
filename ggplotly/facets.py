import pandas as pd
from plotly.subplots import make_subplots


# facets.py
class Facet:
    def apply(self, plot):
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
                    geom.setup_data(facet_data, plot.mapping)
                    geom.draw(fig, row=row, col=col)

        return fig


class facet_wrap(Facet):
    def __init__(self, facet_var, ncol=None, nrow=None):
        """
        Initialize a facet_wrap object.

        Parameters:
            facet_var (str): The column in the dataframe by which to facet the plot.
            ncol (int): Number of columns to arrange the facets in.
            nrow (int): Number of rows to arrange the facets in (optional).
        """
        self.facet_var = facet_var
        self.ncol = ncol
        self.nrow = nrow

    def apply(self, plot):
        """
        Apply facet wrapping to the plot.

        Parameters:
            plot (ggplot): The ggplot object.

        Returns:
            Figure: A Plotly figure with facets applied.
        """
        import pandas as pd
        from plotly.subplots import make_subplots

        # Determine unique facets and layout
        unique_facets = plot.data[self.facet_var].unique()
        n_facets = len(unique_facets)

        # Calculate number of columns and rows
        if self.ncol is None:
            self.ncol = n_facets
        if self.nrow is None:
            self.nrow = -(-n_facets // self.ncol)  # Ceiling division

        # Create a subplot figure with the required number of rows and columns
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
                geom.setup_data(facet_data, plot.mapping)
                geom.draw(fig, row=row, col=col)

        return fig
