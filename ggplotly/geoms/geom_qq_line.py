# geoms/geom_qq_line.py

import plotly.graph_objects as go

from ..stats.stat_qq_line import stat_qq_line
from .geom_base import Geom


class geom_qq_line(Geom):
    """
    Geom for drawing the Q-Q reference line.

    Draws a reference line for Q-Q plots that passes through the points
    where the sample and theoretical quantiles match at specified probability
    levels (default: Q1 and Q3, i.e., 25th and 75th percentiles).

    Parameters
    ----------
    distribution : scipy.stats distribution, optional
        A scipy.stats distribution object with a ppf method.
        Default is scipy.stats.norm.
    dparams : dict, optional
        Additional parameters to pass to the distribution's ppf method.
    line_p : tuple of float, optional
        Two probability values (between 0 and 1) specifying which quantiles
        to use for fitting the line. Default is (0.25, 0.75) for Q1 and Q3.
    color : str, optional
        Color of the line. Default is 'red'.
    linetype : str, optional
        Line style ('solid', 'dash', 'dot', 'dashdot'). Default is 'dashed'.
    size : float, optional
        Line width. Default is 1.5.
    alpha : float, optional
        Transparency level for the line. Default is 1.

    Aesthetics
    ----------
    sample : str (required)
        Column name containing the sample data.

    See Also
    --------
    geom_qq : Q-Q plot points
    stat_qq_line : Underlying stat for line computation

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from scipy import stats
    >>>
    >>> # Q-Q plot with default reference line (through Q1 and Q3)
    >>> df = pd.DataFrame({'values': np.random.randn(100)})
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq()
    ...  + geom_qq_line())
    >>>
    >>> # Reference line through 10th and 90th percentiles
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq()
    ...  + geom_qq_line(line_p=(0.10, 0.90)))
    >>>
    >>> # Custom line styling
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq()
    ...  + geom_qq_line(color='blue', linetype='solid', size=2))
    >>>
    >>> # Q-Q plot against t-distribution
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq(distribution=stats.t, dparams={'df': 5})
    ...  + geom_qq_line(distribution=stats.t, dparams={'df': 5}))
    """

    required_aes = ['sample']
    default_params = {"size": 1.5, "color": "red", "linetype": "dashed"}

    def __init__(self, data=None, mapping=None, distribution=None, dparams=None,
                 line_p=(0.25, 0.75), **params):
        super().__init__(data, mapping, **params)
        self.distribution = distribution
        self.dparams = dparams if dparams is not None else {}
        self.line_p = line_p

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the Q-Q reference line on the figure.

        Overrides base draw to create stat with current mapping (after merge).
        """
        data = data if data is not None else self.data

        # Create stat with current mapping (now includes global mapping)
        qq_line_stat = stat_qq_line(
            data=data,
            mapping=self.mapping,
            distribution=self.distribution,
            dparams=self.dparams,
            line_p=self.line_p
        )

        # Apply stat to transform data
        data, self.mapping = qq_line_stat.compute(data)

        # Delegate to implementation
        self._draw_impl(fig, data, row, col)

    def _draw_impl(self, fig, data, row, col):
        """
        Draw Q-Q reference line on the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        data : DataFrame
            Data (already transformed by stat_qq_line).
        row : int
            Row position in subplot.
        col : int
            Column position in subplot.
        """
        # Map linetype to Plotly dash style
        linetype = self.params.get("linetype", "dashed")
        dash_map = {
            "solid": "solid",
            "dashed": "dash",
            "dotted": "dot",
            "dotdash": "dashdot",
            "longdash": "longdash",
            "twodash": "longdashdot",
            # Also accept Plotly names directly
            "dash": "dash",
            "dot": "dot",
            "dashdot": "dashdot",
        }
        line_dash = dash_map.get(linetype, linetype)

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=self.params.get("name", "Q-Q Line"),
        )

        color_targets = dict(
            color="line_color",
            size="line_width",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
