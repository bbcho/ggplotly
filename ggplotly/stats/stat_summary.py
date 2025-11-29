# stats/stat_summary.py

import pandas as pd
import numpy as np
from .stat_base import Stat


def mean_se(x):
    """Calculate mean and standard error."""
    n = len(x)
    mean = x.mean()
    se = x.std() / np.sqrt(n) if n > 1 else 0
    return pd.Series({'y': mean, 'ymin': mean - se, 'ymax': mean + se})


def mean_cl_normal(x, conf_level=0.95):
    """Calculate mean and confidence limits assuming normal distribution."""
    from scipy import stats as scipy_stats
    n = len(x)
    mean = x.mean()
    if n > 1:
        se = x.std() / np.sqrt(n)
        t_val = scipy_stats.t.ppf((1 + conf_level) / 2, n - 1)
        margin = t_val * se
    else:
        margin = 0
    return pd.Series({'y': mean, 'ymin': mean - margin, 'ymax': mean + margin})


def mean_sdl(x, mult=1):
    """Calculate mean +/- mult * standard deviation."""
    mean = x.mean()
    sd = x.std()
    return pd.Series({'y': mean, 'ymin': mean - mult * sd, 'ymax': mean + mult * sd})


def median_hilow(x, conf_level=0.95):
    """Calculate median and quantile-based range."""
    alpha = (1 - conf_level) / 2
    return pd.Series({
        'y': x.median(),
        'ymin': x.quantile(alpha),
        'ymax': x.quantile(1 - alpha)
    })


class stat_summary(Stat):
    """
    Summarize y values at each unique x.

    Computes summary statistics (mean, median, etc.) of y for each x value.
    Can compute central tendency and error bars in one step.

    Parameters:
        fun_y (str or callable): Function for the central value. Options:
            - 'mean' (default), 'median', 'min', 'max', 'sum'
            - Or a custom function that takes a Series and returns a scalar
        fun_ymin (str or callable, optional): Function for lower error bar.
        fun_ymax (str or callable, optional): Function for upper error bar.
        fun_data (str or callable, optional): Function that returns y, ymin, ymax together.
            Built-in options:
            - 'mean_se': mean +/- standard error
            - 'mean_cl_normal': mean +/- 95% CI (t-distribution)
            - 'mean_sdl': mean +/- 1 SD
            - 'median_hilow': median with 95% quantile range
        geom (str): Default geom to use. Options: 'pointrange', 'errorbar', 'point'

    Aesthetics computed:
        - y: The central summary value
        - ymin: Lower bound (if fun_ymin or fun_data provided)
        - ymax: Upper bound (if fun_ymax or fun_data provided)

    Examples:
        # Mean with standard error bars
        geom_pointrange(stat='summary', fun_data='mean_se')

        # Median with 95% quantile range
        stat_summary(fun_data='median_hilow')

        # Custom: mean with min/max range
        stat_summary(fun_y='mean', fun_ymin='min', fun_ymax='max')

        # Custom function
        stat_summary(fun_y=lambda x: x.quantile(0.75))
    """

    __name__ = "summary"

    def __init__(self, data=None, mapping=None, fun_y='mean', fun_ymin=None,
                 fun_ymax=None, fun_data=None, geom='pointrange', **params):
        super().__init__(data, mapping, **params)
        self.fun_y = fun_y
        self.fun_ymin = fun_ymin
        self.fun_ymax = fun_ymax
        self.fun_data = fun_data
        self.geom = geom

    def _get_agg_func(self, func_spec):
        """Convert function specification to callable."""
        if func_spec is None:
            return None
        if callable(func_spec):
            return func_spec
        if isinstance(func_spec, str):
            if func_spec == 'mean':
                return lambda x: x.mean()
            elif func_spec == 'median':
                return lambda x: x.median()
            elif func_spec == 'min':
                return lambda x: x.min()
            elif func_spec == 'max':
                return lambda x: x.max()
            elif func_spec == 'sum':
                return lambda x: x.sum()
            elif func_spec == 'sd':
                return lambda x: x.std()
            elif func_spec == 'var':
                return lambda x: x.var()
            elif func_spec == 'se':
                return lambda x: x.std() / np.sqrt(len(x))
            else:
                raise ValueError(f"Unknown function: {func_spec}")
        raise ValueError(f"Invalid function specification: {func_spec}")

    def _get_data_func(self, func_spec):
        """Get function that returns y, ymin, ymax together."""
        if func_spec is None:
            return None
        if callable(func_spec):
            return func_spec
        if isinstance(func_spec, str):
            if func_spec == 'mean_se':
                return mean_se
            elif func_spec == 'mean_cl_normal':
                return mean_cl_normal
            elif func_spec == 'mean_sdl':
                return mean_sdl
            elif func_spec == 'median_hilow':
                return median_hilow
            else:
                raise ValueError(f"Unknown fun_data: {func_spec}")
        raise ValueError(f"Invalid fun_data specification: {func_spec}")

    def compute(self, data):
        """
        Compute summary statistics for each x value.

        Parameters:
            data (DataFrame): Input data with x and y columns.

        Returns:
            tuple: (summarized DataFrame, updated mapping)
        """
        data = data.copy()

        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')

        if x_col is None or y_col is None:
            raise ValueError("stat_summary requires both 'x' and 'y' aesthetics")

        # Group by x
        grouped = data.groupby(x_col)[y_col]

        # Check if we have a fun_data function
        data_func = self._get_data_func(self.fun_data)

        if data_func is not None:
            # Use fun_data to compute y, ymin, ymax together
            result = grouped.apply(data_func).reset_index()
            # Flatten if necessary
            if isinstance(result.columns, pd.MultiIndex):
                result.columns = [x_col] + list(result.columns.droplevel(0)[1:])
        else:
            # Compute y, ymin, ymax separately
            y_func = self._get_agg_func(self.fun_y)
            ymin_func = self._get_agg_func(self.fun_ymin)
            ymax_func = self._get_agg_func(self.fun_ymax)

            result = pd.DataFrame({x_col: grouped.apply(lambda x: x.name).unique()})
            result['y'] = grouped.apply(y_func).values

            if ymin_func is not None:
                result['ymin'] = grouped.apply(ymin_func).values
            if ymax_func is not None:
                result['ymax'] = grouped.apply(ymax_func).values

        # Update mapping
        new_mapping = self.mapping.copy()
        new_mapping['y'] = 'y'
        if 'ymin' in result.columns:
            new_mapping['ymin'] = 'ymin'
        if 'ymax' in result.columns:
            new_mapping['ymax'] = 'ymax'

        return result, new_mapping
