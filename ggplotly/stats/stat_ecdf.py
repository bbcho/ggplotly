# stats/stat_ecdf.py
"""Empirical Cumulative Distribution Function (ECDF) stat."""

import numpy as np
import pandas as pd


class stat_ecdf:
    """
    Compute the empirical cumulative distribution function.

    The ECDF shows the proportion of data points less than or equal to each
    value. Useful for visualizing distributions without binning like histograms.

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_step(stat='ecdf')
        >>> ggplot(df, aes(x='value')) + geom_line(stat='ecdf')
    """

    def compute(self, x):
        """
        Compute the ECDF for the given data.

        Parameters:
            x (array-like): The input data values.

        Returns:
            DataFrame: DataFrame with 'x' (sorted values) and 'y' (cumulative proportions).
        """
        x = np.sort(x)
        y = np.arange(1, len(x) + 1) / len(x)
        return pd.DataFrame({"x": x, "y": y})
