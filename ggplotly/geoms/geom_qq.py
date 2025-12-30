# geoms/geom_qq.py

import plotly.graph_objects as go

from ..stats.stat_qq import stat_qq
from .geom_base import Geom


class geom_qq(Geom):
    """
    Geom for creating Q-Q (quantile-quantile) plots.

    Displays sample quantiles against theoretical quantiles from a specified
    distribution. By default uses the standard normal distribution.

    Parameters
    ----------
    distribution : scipy.stats distribution, optional
        A scipy.stats distribution object with a ppf method.
        Default is scipy.stats.norm.
    dparams : dict, optional
        Additional parameters to pass to the distribution's ppf method.
        For example, {'df': 5} for a t-distribution.
    color : str, optional
        Color of the points.
    size : float, optional
        Size of the points. Default is 8.
    alpha : float, optional
        Transparency level for the points. Default is 1.
    shape : str, optional
        Shape of the points.

    Aesthetics
    ----------
    sample : str (required)
        Column name containing the sample data to compare against
        the theoretical distribution.
    color : str, optional
        Grouping variable for colored points.
    group : str, optional
        Grouping variable for separate Q-Q plots.

    See Also
    --------
    geom_qq_line : Reference line for Q-Q plots
    stat_qq : Underlying stat for quantile computation

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from scipy import stats
    >>>
    >>> # Basic Q-Q plot against normal distribution
    >>> df = pd.DataFrame({'values': np.random.randn(100)})
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq())
    >>>
    >>> # Q-Q plot with reference line
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq()
    ...  + geom_qq_line())
    >>>
    >>> # Q-Q plot against t-distribution
    >>> (ggplot(df, aes(sample='values'))
    ...  + geom_qq(distribution=stats.t, dparams={'df': 5}))
    >>>
    >>> # Q-Q plot with color grouping
    >>> df = pd.DataFrame({
    ...     'values': np.concatenate([np.random.randn(50), np.random.randn(50) + 2]),
    ...     'group': ['A'] * 50 + ['B'] * 50
    ... })
    >>> (ggplot(df, aes(sample='values', color='group'))
    ...  + geom_qq())
    """

    required_aes = ['sample']
    default_params = {"size": 8}

    def __init__(self, data=None, mapping=None, distribution=None, dparams=None, **params):
        super().__init__(data, mapping, **params)
        self.distribution = distribution
        self.dparams = dparams if dparams is not None else {}

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the Q-Q plot on the figure.

        Overrides base draw to create stat with current mapping (after merge).
        """
        data = data if data is not None else self.data

        # Create stat with current mapping (now includes global mapping)
        qq_stat = stat_qq(
            data=data,
            mapping=self.mapping,
            distribution=self.distribution,
            dparams=self.dparams
        )

        # Apply stat to transform data
        data, self.mapping = qq_stat.compute(data)

        # Delegate to implementation
        self._draw_impl(fig, data, row, col)

    def _draw_impl(self, fig, data, row, col):
        """
        Draw Q-Q plot points on the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        data : DataFrame
            Data (already transformed by stat_qq).
        row : int
            Row position in subplot.
        col : int
            Column position in subplot.
        """
        plot = go.Scatter
        payload = dict(
            mode="markers",
            name=self.params.get("name", "Q-Q"),
        )

        color_targets = dict(
            color="marker_color",
            size="marker_size",
            shape="marker_symbol",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
