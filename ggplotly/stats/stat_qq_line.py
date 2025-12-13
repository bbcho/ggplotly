# stats/stat_qq_line.py

import numpy as np
import pandas as pd

from .stat_base import Stat


class stat_qq_line(Stat):
    """
    Stat for computing the Q-Q reference line through specified quantiles.

    Computes a reference line for Q-Q plots that passes through the points
    where the sample and theoretical quantiles match at specified probability
    levels (default: Q1 and Q3, i.e., 25th and 75th percentiles).

    Default geom: line

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

    Aesthetics
    ----------
    sample : str (required)
        Column name containing the sample data.
    color : str, optional
        Line color.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from scipy import stats
    >>>
    >>> # Q-Q plot with default reference line (through Q1 and Q3)
    >>> df = pd.DataFrame({'values': np.random.randn(100)})
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq()
    ...  + stat_qq_line())
    >>>
    >>> # Reference line through 10th and 90th percentiles
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq()
    ...  + stat_qq_line(line_p=(0.10, 0.90)))
    >>>
    >>> # Q-Q plot against t-distribution
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq(distribution=stats.t, dparams={'df': 5})
    ...  + stat_qq_line(distribution=stats.t, dparams={'df': 5}))
    """

    # Default geom for this stat
    geom = 'line'

    def __init__(self, data=None, mapping=None, distribution=None, dparams=None,
                 line_p=(0.25, 0.75), **params):
        super().__init__(data, mapping, **params)
        self.distribution = distribution
        self.dparams = dparams if dparams is not None else {}
        self.line_p = line_p

    def compute(self, data):
        """Compute Q-Q reference line through specified quantiles."""
        # Get sample column from mapping
        sample_col = self.mapping.get('sample')
        if sample_col is None:
            raise ValueError("stat_qq_line requires 'sample' aesthetic mapping")

        if sample_col not in data.columns:
            raise ValueError(f"Sample column '{sample_col}' not found in data")

        # Get sample data
        sample = data[sample_col].dropna()
        n = len(sample)

        if n == 0:
            raise ValueError("No valid sample data for Q-Q line")

        # Import scipy.stats for default distribution
        if self.distribution is None:
            from scipy.stats import norm
            dist = norm
        else:
            dist = self.distribution

        # Compute sample quantiles at line_p positions
        sample_q = np.quantile(sample, self.line_p)

        # Compute theoretical quantiles at same positions
        theoretical_q = dist.ppf(self.line_p, **self.dparams)

        # Calculate line parameters: y = slope * x + intercept
        slope = (sample_q[1] - sample_q[0]) / (theoretical_q[1] - theoretical_q[0])
        intercept = sample_q[0] - slope * theoretical_q[0]

        # Generate line points spanning the theoretical quantile range
        # Use Hazen plotting positions to match stat_qq
        probs = (np.arange(1, n + 1) - 0.5) / n
        x_range = dist.ppf(probs, **self.dparams)
        x_min, x_max = x_range.min(), x_range.max()

        # Extend slightly beyond data range
        x_extend = (x_max - x_min) * 0.05
        x_vals = np.array([x_min - x_extend, x_max + x_extend])
        y_vals = slope * x_vals + intercept

        result = pd.DataFrame({
            'theoretical': x_vals,
            'sample': y_vals
        })

        # Update mapping to use computed columns
        new_mapping = dict(self.mapping) if self.mapping else {}
        new_mapping['x'] = 'theoretical'
        new_mapping['y'] = 'sample'
        # Remove 'sample' from mapping as it's been transformed
        new_mapping.pop('sample', None)

        return result, new_mapping
