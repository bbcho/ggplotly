# geoms/geom_path.py

import plotly.graph_objects as go
from .geom_base import Geom
from ..aesthetic_mapper import AestheticMapper


class geom_path(Geom):
    """
    Geom for drawing paths connecting points in data order.

    Unlike geom_line which sorts points by x-axis value, geom_path connects
    points in the order they appear in the data. This is useful for:
    - Trajectories and movement paths
    - Time series with non-monotonic x values
    - Connected scatterplots
    - Drawing arbitrary shapes

    Parameters:
        color (str, optional): Color of the path. Can be a column name for grouping.
        size (float, optional): Line width. Default is 2.
        linetype (str, optional): Line style ('solid', 'dash', 'dot', 'dashdot'). Default is 'solid'.
        alpha (float, optional): Transparency level. Default is 1.
        lineend (str, optional): Line end style. Default is 'round'.
        linejoin (str, optional): Line join style. Default is 'round'.
        arrow (bool, optional): Whether to add arrow at end. Default is False.

    Aesthetics:
        - x: x-axis values
        - y: y-axis values
        - color: Grouping variable for colored paths
        - group: Grouping variable for separate paths

    Examples:
        # Simple path (connects points in data order)
        ggplot(trajectory, aes(x='x', y='y')) + geom_path()

        # Spiral (x is not monotonic)
        ggplot(spiral_data, aes(x='x', y='y')) + geom_path()

        # Connected scatterplot with time
        ggplot(data, aes(x='gdp', y='life_exp', group='country')) + geom_path()

        # Multiple colored trajectories
        ggplot(tracks, aes(x='x', y='y', color='track_id')) + geom_path()
    """

    __name__ = "geom_path"

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw path(s) on the figure, connecting points in data order.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = data if data is not None else self.data

        # Set default line width
        if "size" not in self.params:
            self.params["size"] = 2

        # Remove size from mapping - paths use constant width
        if "size" in self.mapping:
            del self.mapping["size"]

        line_dash = self.params.get("linetype", "solid")
        name = self.params.get("name", "Path")

        # Handle Plotly's fill parameter separately from fill aesthetic
        fill_param = self.params.get("fill", None)
        plotly_fill = None
        if fill_param in ['tonexty', 'tozeroy', 'tonextx', 'tozerox', 'toself', 'tonext']:
            plotly_fill = fill_param
            original_fill = self.params.pop("fill", None)

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
            fill=plotly_fill,
        )

        color_targets = dict(
            fill="line_color",
            color="line_color",
            size="line_width",
        )

        # Key difference from geom_line: NO sorting by x
        # Data is drawn in the order it appears
        self._transform_fig(plot, fig, data, payload, color_targets, row, col)

        # Restore fill parameter
        if plotly_fill is not None:
            self.params["fill"] = original_fill
