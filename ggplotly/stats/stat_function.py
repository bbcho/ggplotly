# stats/stat_function.py

import numpy as np
import pandas as pd

from .stat_base import Stat


class stat_function(Stat):
    """
    Stat for computing y values from a function over the x range.

    Evaluates a user-provided function over a grid of x values within
    the data range, returning x and y columns for line plotting.

    Default geom: line

    Parameters
    ----------
    fun : callable
        Function that takes an array of x values and returns y values.
    n : int, optional
        Number of points to evaluate. Default is 101.
    xlim : tuple, optional
        (min, max) range for x values. If None, uses data range.
    args : tuple, optional
        Additional positional arguments to pass to fun.

    Examples
    --------
    >>> from scipy import stats
    >>>
    >>> # Standard normal distribution
    >>> stat_function(fun=lambda x: stats.norm.pdf(x, loc=0, scale=1))
    >>>
    >>> # Normal with custom mean and std
    >>> stat_function(fun=lambda x: stats.norm.pdf(x, loc=5, scale=2))
    >>>
    >>> # Exponential distribution (lambda=1)
    >>> stat_function(fun=lambda x: stats.expon.pdf(x, scale=1))
    >>>
    >>> # Gamma distribution (shape=2, scale=1)
    >>> stat_function(fun=lambda x: stats.gamma.pdf(x, a=2, scale=1))
    >>>
    >>> # Beta distribution (a=2, b=5)
    >>> stat_function(fun=lambda x: stats.beta.pdf(x, a=2, b=5), xlim=(0, 1))
    >>>
    >>> # Student's t distribution (df=3)
    >>> stat_function(fun=lambda x: stats.t.pdf(x, df=3))
    >>>
    >>> # Chi-squared distribution (df=5)
    >>> stat_function(fun=lambda x: stats.chi2.pdf(x, df=5))
    >>>
    >>> # Custom polynomial function
    >>> stat_function(fun=lambda x: x**2 - 2*x + 1, n=50)
    >>>
    >>> # Plot without data - must provide xlim (uses geom_line by default)
    >>> (ggplot()
    ...  + stat_function(fun=lambda x: stats.norm.pdf(x), xlim=(-4, 4)))
    """

    # Default geom for this stat
    geom = 'line'

    def __init__(self, data=None, mapping=None, fun=None, n=101,
                 xlim=None, args=(), **params):
        super().__init__(data, mapping, **params)
        if fun is None:
            raise ValueError("stat_function requires 'fun' parameter")
        self.fun = fun
        self.n = n
        self.xlim = xlim
        self.args = args

    def compute(self, data):
        """Compute function values over x range."""
        x_col = self.mapping.get('x') if self.mapping else None

        # Determine x range
        if self.xlim is not None:
            x_min, x_max = self.xlim
        elif x_col and x_col in data.columns:
            x_min, x_max = data[x_col].min(), data[x_col].max()
        else:
            x_min, x_max = 0, 1

        # Extend range slightly for smooth curve
        x_range = x_max - x_min
        x_min -= x_range * 0.05
        x_max += x_range * 0.05

        # Generate x grid and compute y values
        x_vals = np.linspace(x_min, x_max, self.n)
        y_vals = self.fun(x_vals, *self.args)

        result = pd.DataFrame({'x': x_vals, 'y': y_vals})

        new_mapping = dict(self.mapping) if self.mapping else {}
        new_mapping['x'] = 'x'
        new_mapping['y'] = 'y'

        return result, new_mapping
