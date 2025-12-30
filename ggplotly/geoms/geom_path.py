# geoms/geom_path.py

import plotly.graph_objects as go

from .geom_base import Geom


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
        colour (str, optional): Alias for color (British spelling).
        size (float, optional): Line width. Default is 2.
        linewidth (float, optional): Alias for size (ggplot2 3.4+ compatibility).
        linetype (str, optional): Line style ('solid', 'dash', 'dot', 'dashdot'). Default is 'solid'.
        alpha (float, optional): Transparency level. Default is 1.
        na_rm (bool, optional): If True, remove missing values. Default is False.
        show_legend (bool, optional): Whether to show in legend. Default is True.

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

    required_aes = ['x', 'y']
    default_params = {"size": 2}

    def _draw_impl(self, fig, data, row, col):
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
