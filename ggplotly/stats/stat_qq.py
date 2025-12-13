# stats/stat_qq.py

import numpy as np
import pandas as pd

from .stat_base import Stat


class stat_qq(Stat):
    """
    Stat for computing theoretical vs sample quantiles for Q-Q plots.

    Computes sample quantiles against theoretical quantiles from a specified
    distribution. By default uses the standard normal distribution.

    Default geom: point

    Parameters
    ----------
    distribution : scipy.stats distribution, optional
        A scipy.stats distribution object with a ppf method.
        Default is scipy.stats.norm.
    dparams : dict, optional
        Additional parameters to pass to the distribution's ppf method.
        For example, {'df': 5} for a t-distribution.

    Aesthetics
    ----------
    sample : str (required)
        Column name containing the sample data to compare against
        the theoretical distribution.
    color : str, optional
        Grouping variable for colored points.
    group : str, optional
        Grouping variable for separate Q-Q plots.

    Examples
    --------
    >>> import numpy as np
    >>> import pandas as pd
    >>> from scipy import stats
    >>>
    >>> # Basic Q-Q plot against normal distribution
    >>> df = pd.DataFrame({'values': np.random.randn(100)})
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq())
    >>>
    >>> # Q-Q plot against t-distribution
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq(distribution=stats.t, dparams={'df': 5}))
    >>>
    >>> # Q-Q plot with reference line
    >>> (ggplot(df, aes(sample='values'))
    ...  + stat_qq()
    ...  + stat_qq_line())
    """

    # Default geom for this stat
    geom = 'point'

    def __init__(self, data=None, mapping=None, distribution=None, dparams=None, **params):
        super().__init__(data, mapping, **params)
        self.distribution = distribution
        self.dparams = dparams if dparams is not None else {}

    def compute(self, data):
        """Compute theoretical vs sample quantiles."""
        # Get sample column from mapping
        sample_col = self.mapping.get('sample')
        if sample_col is None:
            raise ValueError("stat_qq requires 'sample' aesthetic mapping")

        if sample_col not in data.columns:
            raise ValueError(f"Sample column '{sample_col}' not found in data")

        # Get and sort sample data
        sample = data[sample_col].dropna().sort_values().reset_index(drop=True)
        n = len(sample)

        if n == 0:
            raise ValueError("No valid sample data for Q-Q plot")

        # Import scipy.stats for default distribution
        if self.distribution is None:
            from scipy.stats import norm
            dist = norm
        else:
            dist = self.distribution

        # Compute theoretical quantiles using Hazen plotting positions
        # This is the same method used by ggplot2
        probs = (np.arange(1, n + 1) - 0.5) / n
        theoretical = dist.ppf(probs, **self.dparams)

        result = pd.DataFrame({
            'theoretical': theoretical,
            'sample': sample.values
        })

        # Update mapping to use computed columns
        new_mapping = dict(self.mapping) if self.mapping else {}
        new_mapping['x'] = 'theoretical'
        new_mapping['y'] = 'sample'
        # Remove 'sample' from mapping as it's been transformed
        new_mapping.pop('sample', None)

        return result, new_mapping
