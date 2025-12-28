# geoms/geom_stl.py

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from ..stats.stat_stl import stat_stl
from .geom_base import Geom


class geom_stl(Geom):
    """
    Geom for displaying STL decomposition as a 4-panel chart.

    Performs STL (Seasonal-Trend decomposition using Loess) and displays
    the Observed, Trend, Seasonal, and Residual components as stacked
    line plots with shared x-axis.

    Uses stat_stl internally for the decomposition.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. Requires x and y.
    period : int
        Seasonal period. Required unless data has DatetimeIndex with frequency.
    seasonal : int, optional
        Length of the seasonal smoother. Must be odd. Default is 7.
    trend : int, optional
        Length of the trend smoother. Default is auto-calculated.
    robust : bool, optional
        Use robust fitting to downweight outliers. Default is False.
    color : str, optional
        Line color. Default is 'steelblue'.
    line_width : float, optional
        Width of lines. Default is 1.5.
    rangeslider : bool, optional
        Whether to show a range slider on the bottom subplot. Default is True.

    Examples
    --------
    >>> # Basic STL decomposition
    >>> ggplot(df, aes(x='date', y='value')) + geom_stl(period=12)

    >>> # Robust decomposition for data with outliers
    >>> ggplot(df, aes(x='date', y='value')) + geom_stl(period=12, robust=True)

    >>> # Styled decomposition
    >>> ggplot(df, aes(x='date', y='value')) + geom_stl(period=12, color='coral')
    """

    required_aes = ['x', 'y']

    default_params = {
        "color": "steelblue",
        "line_width": 1.5,
        "seasonal": 7,
        "robust": False,
        "rangeslider": True,
    }

    # Flag to indicate this geom creates its own figure layout
    _creates_subplots = True

    def __init__(self, data=None, mapping=None, period=None, **params):
        super().__init__(data, mapping, **params)
        self.period = period

    def _draw_impl(self, fig, data, row, col):
        # Get parameters
        period = self.period
        seasonal = self.params.get("seasonal", 7)
        trend = self.params.get("trend")
        robust = self.params.get("robust", False)
        color = self.params.get("color", "steelblue")
        line_width = self.params.get("line_width", 1.5)

        # Use stat_stl for computation
        stat = stat_stl(
            mapping=self.mapping,
            period=period,
            seasonal=seasonal,
            trend=trend,
            robust=robust,
        )
        stl_data, _ = stat.compute(data)

        if stl_data.empty:
            return

        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')

        # Get unique components in order
        components = ['Observed', 'Trend', 'Seasonal', 'Residual']

        # Create 4-row subplot figure
        subfig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            subplot_titles=components,
        )

        # Draw each component
        for i, comp in enumerate(components, 1):
            comp_data = stl_data[stl_data['component'] == comp]

            subfig.add_trace(
                go.Scatter(
                    x=comp_data[x_col].values,
                    y=comp_data[y_col].values,
                    mode='lines',
                    line=dict(color=color, width=line_width),
                    name=comp,
                    showlegend=False,
                    hovertemplate=f'{comp}: %{{y:.2f}}<extra></extra>',
                ),
                row=i, col=1,
            )

            # Update y-axis label
            subfig.update_yaxes(title_text=comp, row=i, col=1)

        # Add rangeslider to the bottom x-axis (xaxis4) if enabled
        show_rangeslider = self.params.get("rangeslider", True)
        if show_rangeslider:
            subfig.update_xaxes(
                rangeslider=dict(visible=True, thickness=0.05),
                row=4, col=1,
            )

        # Update layout with enough top margin for main title from labs()
        subfig.update_layout(
            height=700 if show_rangeslider else 600,
            margin=dict(l=60, r=20, t=60, b=40),
            # Position title above the subplot area
            title=dict(y=0.98, yanchor='bottom'),
        )

        # Copy traces and layout to the main figure
        # Clear existing figure and replace with our subplot layout
        fig.data = []
        for trace in subfig.data:
            fig.add_trace(trace)
        fig.update_layout(subfig.layout)

    def before_add(self):
        """
        Called before the geom is added to the plot.

        For geom_stl, we need to signal that this geom will create its own
        subplot structure and should bypass normal faceting.
        """
        return self
