# stats/stat_stl.py

import pandas as pd

from .stat_base import Stat


class stat_stl(Stat):
    """
    Stat for STL (Seasonal-Trend decomposition using Loess).

    Decomposes a time series into observed, trend, seasonal, and residual
    components. Returns a stacked DataFrame with a 'component' column
    suitable for use with facet_wrap().

    Parameters
    ----------
    period : int, optional
        Seasonal period. Required unless data has DatetimeIndex with frequency.
    seasonal : int, optional
        Length of the seasonal smoother. Must be odd. Default is 7.
    trend : int, optional
        Length of the trend smoother. Default is auto-calculated.
    robust : bool, optional
        Use robust fitting to downweight outliers. Default is False.

    Examples
    --------
    >>> # STL with faceting
    >>> (ggplot(df, aes(x='date', y='value'))
    ...  + stat_stl(period=12)
    ...  + geom_line()
    ...  + facet_wrap('component', ncol=1, scales='free_y'))

    >>> # Color by component
    >>> (ggplot(df, aes(x='date', y='value', color='component'))
    ...  + stat_stl(period=12)
    ...  + geom_line())
    """

    # Default geom for this stat (used when stat added directly to plot)
    geom = 'line'

    def __init__(self, data=None, mapping=None, period=None, seasonal=7,
                 trend=None, robust=False, **params):
        super().__init__(data, mapping, **params)
        self.period = period
        self.seasonal = seasonal
        self.trend = trend
        self.robust = robust

    def _infer_period(self, index):
        """Try to infer period from DatetimeIndex."""
        if not hasattr(index, 'freq') or index.freq is None:
            return None

        freq = index.freq.name if hasattr(index.freq, 'name') else str(index.freq)

        freq_map = {
            'D': 7, 'W': 52, 'M': 12, 'ME': 12, 'MS': 12,
            'Q': 4, 'QE': 4, 'QS': 4, 'H': 24, 'h': 24,
        }

        for key, period in freq_map.items():
            if freq.startswith(key):
                return period
        return None

    def compute(self, data):
        """Compute STL decomposition and return stacked DataFrame."""
        from statsmodels.tsa.seasonal import STL

        x_col = self.mapping.get('x') if self.mapping else None
        y_col = self.mapping.get('y') if self.mapping else None

        if y_col is None:
            raise ValueError("stat_stl requires y aesthetic")

        y_values = data[y_col].values

        # Get period
        period = self.period
        if period is None:
            period = self._infer_period(data.index)
        if period is None:
            raise ValueError("period must be specified for STL decomposition")

        # Perform STL
        stl = STL(y_values, period=period, seasonal=self.seasonal,
                  trend=self.trend, robust=self.robust)
        result = stl.fit()

        # Build stacked DataFrame
        components = [
            ('Observed', result.observed),
            ('Trend', result.trend),
            ('Seasonal', result.seasonal),
            ('Residual', result.resid),
        ]

        result_frames = []
        for comp_name, comp_values in components:
            comp_df = data.copy()
            comp_df[y_col] = comp_values
            comp_df['component'] = comp_name
            result_frames.append(comp_df)

        result_data = pd.concat(result_frames, ignore_index=True)

        # Preserve component order for faceting
        result_data['component'] = pd.Categorical(
            result_data['component'],
            categories=['Observed', 'Trend', 'Seasonal', 'Residual'],
            ordered=True
        )

        return result_data, self.mapping
