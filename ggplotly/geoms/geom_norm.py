# geoms/geom_norm.py

import numpy as np
import plotly.graph_objects as go

from .geom_base import Geom


class geom_norm(Geom):
    """
    Geom for overlaying a normal distribution curve.

    Automatically fits a normal distribution to the data (using mean and std)
    unless mean and sd are explicitly provided. Useful for comparing actual
    data distribution to theoretical normal distribution.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. Uses x aesthetic to determine data range.
    mean : float, optional
        Mean of the normal distribution. If None, computed from data.
    sd : float, optional
        Standard deviation of the normal distribution. If None, computed from data.
    scale : str, optional
        Output scale: 'density' (default) outputs PDF values, 'count' scales
        to match histogram counts (PDF * n * binwidth). When 'count', automatically
        estimates binwidth from data range and number of observations.
    binwidth : float, optional
        Bin width for count scaling. If None, estimated as data_range / 30.
    n : int, optional
        Number of points for the curve. Default is 101.
    color : str, optional
        Color of the line. Default is 'red'.
    size : float, optional
        Width of the line. Default is 2.
    linetype : str, optional
        Line style ('solid', 'dash', etc.). Default is 'solid'.

    Examples
    --------
    >>> # With density-scaled histogram (default)
    >>> ggplot(df, aes(x='x')) + geom_histogram(aes(y=after_stat('density'))) + geom_norm()

    >>> # With count histogram (no density scaling needed on histogram)
    >>> ggplot(df, aes(x='x')) + geom_histogram(bins=30) + geom_norm(scale='count')

    >>> # Explicit parameters
    >>> ggplot(df, aes(x='x')) + geom_histogram(bins=30) + geom_norm(scale='count', mean=0, sd=1)

    >>> # Styled
    >>> ggplot(df, aes(x='x')) + geom_histogram(aes(y=after_stat('density'))) + geom_norm(color='blue', size=3)
    """

    required_aes = ['x']

    default_params = {
        "n": 101,
        "color": "red",
        "size": 2,
        "linetype": "solid",
        "scale": "density",
    }

    def __init__(self, data=None, mapping=None, mean=None, sd=None,
                 scale="density", binwidth=None, **params):
        super().__init__(data, mapping, **params)
        self.mean = mean
        self.sd = sd
        self.scale = scale
        self.binwidth = binwidth

    def _draw_impl(self, fig, data, row, col):
        from scipy.stats import norm

        # Get parameters
        n = self.params.get("n", 101)
        color = self.params.get("color", "red")
        size = self.params.get("size", 2)
        linetype = self.params.get("linetype", "solid")

        # Get x column
        x_col = self.mapping.get('x') if self.mapping else None
        if x_col is None or x_col not in data.columns:
            raise ValueError("geom_norm requires x aesthetic")

        x_data = data[x_col].dropna()
        n_obs = len(x_data)

        # Compute or use provided mean/sd
        mean = self.mean if self.mean is not None else x_data.mean()
        sd = self.sd if self.sd is not None else x_data.std()

        # Generate x range (extend beyond data range)
        x_min, x_max = x_data.min(), x_data.max()
        x_range = x_max - x_min
        x_min -= x_range * 0.05
        x_max += x_range * 0.05

        # Compute normal PDF
        x_vals = np.linspace(x_min, x_max, n)
        y_vals = norm.pdf(x_vals, mean, sd)

        # Scale to counts if requested
        if self.scale == 'count':
            # Estimate binwidth if not provided (default 30 bins like geom_histogram)
            binwidth = self.binwidth if self.binwidth is not None else x_range / 30
            y_vals = y_vals * n_obs * binwidth
            y_label = 'count'
        else:
            y_label = 'density'

        # Map linetype to Plotly dash
        dash_map = {
            'solid': 'solid',
            'dashed': 'dash',
            'dash': 'dash',
            'dotted': 'dot',
            'dot': 'dot',
            'longdash': 'longdash',
            'dashdot': 'dashdot',
            'twodash': 'dashdot',
        }
        dash = dash_map.get(linetype, 'solid')

        # Add trace
        fig.add_trace(
            go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                line=dict(color=color, width=size, dash=dash),
                name=f'Normal(\u03bc={mean:.2f}, \u03c3={sd:.2f})',
                showlegend=True,
                hovertemplate=f'x: %{{x:.2f}}<br>{y_label}: %{{y:.4f}}<extra></extra>',
            ),
            row=row, col=col,
        )
