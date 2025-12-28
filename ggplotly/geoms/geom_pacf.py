# geoms/geom_pacf.py

import numpy as np
import plotly.graph_objects as go

from .geom_base import Geom


class geom_pacf(Geom):
    """
    Geom for displaying Partial Autocorrelation Function (PACF) plots.

    Computes and displays the partial autocorrelation at each lag as vertical
    bars with horizontal confidence interval bands.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. Requires y (the time series values).
    nlags : int, optional
        Number of lags to compute. Default is 40.
    alpha : float, optional
        Significance level for confidence intervals. Default is 0.05.
    method : str, optional
        Method for computing PACF. Options: 'ywm' (Yule-Walker with MLE),
        'yw' (Yule-Walker), 'ols' (OLS), 'ld' (Levinson-Durbin).
        Default is 'ywm'.
    color : str, optional
        Color for the bars. Default is 'steelblue'.
    ci_color : str, optional
        Color for confidence interval bands. Default is 'lightblue'.
    ci_alpha : float, optional
        Transparency of confidence bands. Default is 0.3.
    bar_width : float, optional
        Width of the bars. Default is 0.3.

    Examples
    --------
    >>> # Basic PACF plot
    >>> ggplot(df, aes(y='value')) + geom_pacf()

    >>> # Custom number of lags
    >>> ggplot(df, aes(y='value')) + geom_pacf(nlags=20)

    >>> # Styled PACF
    >>> ggplot(df, aes(y='value')) + geom_pacf(color='coral', nlags=30)
    """

    required_aes = ['y']

    default_params = {
        "nlags": 40,
        "alpha": 0.05,
        "method": "ywm",
        "color": "steelblue",
        "ci_color": "lightblue",
        "ci_alpha": 0.3,
        "bar_width": 0.3,
    }

    def _draw_impl(self, fig, data, row, col):
        from statsmodels.tsa.stattools import pacf

        # Get parameters
        nlags = self.params.get("nlags", 40)
        alpha = self.params.get("alpha", 0.05)
        method = self.params.get("method", "ywm")
        color = self.params.get("color", "steelblue")
        ci_alpha = self.params.get("ci_alpha", 0.3)
        bar_width = self.params.get("bar_width", 0.3)

        # Get y values
        y_col = self.mapping.get('y') if self.mapping else None
        if y_col is None:
            raise ValueError("geom_pacf requires y aesthetic")

        y_values = data[y_col].dropna().values

        # Compute PACF with confidence intervals
        pacf_values, confint = pacf(y_values, nlags=nlags, alpha=alpha, method=method)

        # Skip lag 0 (always 1.0, not informative)
        pacf_values = pacf_values[1:]
        confint = confint[1:]
        lags = np.arange(1, len(pacf_values) + 1)

        # Confidence interval bounds
        ci_lower = confint[:, 0] - pacf_values
        ci_upper = confint[:, 1] - pacf_values

        # Add confidence band (shaded region)
        fig.add_trace(
            go.Scatter(
                x=list(lags) + list(lags[::-1]),
                y=list(ci_upper) + list(ci_lower[::-1]),
                fill='toself',
                fillcolor=f'rgba(173, 216, 230, {ci_alpha})',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip',
                name='95% CI',
            ),
            row=row, col=col,
        )

        # Add horizontal line at y=0
        fig.add_trace(
            go.Scatter(
                x=[1, nlags],
                y=[0, 0],
                mode='lines',
                line=dict(color='black', width=1),
                showlegend=False,
                hoverinfo='skip',
            ),
            row=row, col=col,
        )

        # Add bars for PACF values
        fig.add_trace(
            go.Bar(
                x=lags,
                y=pacf_values,
                marker_color=color,
                width=bar_width,
                name='PACF',
                showlegend=False,
                hovertemplate='Lag %{x}: %{y:.3f}<extra></extra>',
            ),
            row=row, col=col,
        )

        # Update axes
        fig.update_xaxes(title_text='Lag', row=row, col=col)
        fig.update_yaxes(title_text='PACF', row=row, col=col)
