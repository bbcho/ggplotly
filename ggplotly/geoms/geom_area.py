# geoms/geom_area.py


import plotly.graph_objects as go

from .geom_base import Geom


class geom_area(Geom):
    """
    Geom for drawing area plots.

    Automatically handles continuous and categorical variables for fill.
    Automatically converts 'group' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        color (str, optional): Color of the area. If a categorical variable is mapped to color, different colors will be assigned.
        linetype (str, optional): Line type ('solid', 'dash', etc.). Default is 'solid'.
        group (str, optional): Grouping variable for the areas.
        fill (str, optional): Fill color for the area. Default is 'lightblue'.
        alpha (float, optional): Transparency level for the fill color. Default is 0.5.
        showlegend (bool, optional): Whether to show legend entries. Default is True.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_area()
        >>> ggplot(df, aes(x='x', y='y', fill='group')) + geom_area(alpha=0.5)
    """

    default_params = {"size": 1}

    def _draw_impl(self, fig, data, row, col):
        """
        Draw area plot(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Data (already transformed by stats).
            row (int): Row position in subplot.
            col (int): Column position in subplot.

        Returns:
            None: Modifies the figure in place.
        """

        # Remove size from mapping if present - area lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        plot = go.Scatter
        payload = dict(
            mode="lines",
            fill="tozeroy",
            line_dash=self.params.get("linetype", "solid"),
            name=self.params.get("name", "Area"),
        )

        color_targets = dict(
            # fill="line",
            fill="fillcolor",
            color="line_color",
            # size="line",
            # marker=dict(color=fill, size=size),
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
