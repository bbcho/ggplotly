# stats/stat_ecdf.py
"""Empirical Cumulative Distribution Function (ECDF) stat."""

import numpy as np
import pandas as pd

from .stat_base import Stat


class stat_ecdf(Stat):
    """
    Compute the empirical cumulative distribution function.

    The ECDF shows the proportion of data points less than or equal to each
    value. Useful for visualizing distributions without binning like histograms.

    Parameters:
        data (DataFrame, optional): Data to use for this stat.
        mapping (dict, optional): Aesthetic mappings.
        n (int, optional): Number of points to evaluate. Default uses all unique values.
        pad (bool): If True, pad the ECDF with (min-eps, 0) and (max+eps, 1). Default False.
        **params: Additional parameters for the stat.

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_step(stat='ecdf')
        >>> ggplot(df, aes(x='value')) + geom_line(stat='ecdf')
    """

    __name__ = "ecdf"

    def __init__(self, data=None, mapping=None, n=None, pad=False, **params):
        """
        Initialize the stat_ecdf.

        Parameters:
            data (DataFrame, optional): Data to use for this stat.
            mapping (dict, optional): Aesthetic mappings.
            n (int, optional): Number of evaluation points.
            pad (bool): Whether to pad ECDF at ends. Default False.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)
        self.n = n
        self.pad = pad

    def compute(self, data):
        """
        Compute the ECDF for the given data.

        Parameters:
            data (DataFrame or array-like): The input data. If DataFrame,
                uses the column specified in mapping['x'].

        Returns:
            tuple: (DataFrame with 'x' and 'y' columns, updated mapping dict)
        """
        # Handle both DataFrame and array input for backward compatibility
        if isinstance(data, pd.DataFrame):
            x_col = self.mapping.get('x')
            if x_col is None:
                raise ValueError("stat_ecdf requires 'x' aesthetic mapping")
            x = data[x_col].values
        else:
            x = np.asarray(data)

        # Sort and compute ECDF
        x_sorted = np.sort(x)
        y = np.arange(1, len(x_sorted) + 1) / len(x_sorted)

        # Optionally pad the ECDF
        if self.pad:
            eps = (x_sorted[-1] - x_sorted[0]) * 0.01 if len(x_sorted) > 1 else 0.1
            x_sorted = np.concatenate([[x_sorted[0] - eps], x_sorted, [x_sorted[-1] + eps]])
            y = np.concatenate([[0], y, [1]])

        result = pd.DataFrame({"x": x_sorted, "y": y})

        # Update mapping to reflect computed columns
        new_mapping = self.mapping.copy()
        new_mapping['x'] = 'x'
        new_mapping['y'] = 'y'

        return result, new_mapping

    def compute_array(self, x):
        """
        Compute the ECDF values for a given array of x values.

        This is a convenience method for direct array computation.

        Parameters:
            x (array-like): The input data values.

        Returns:
            tuple: (x_sorted, y_values) arrays
        """
        x_sorted = np.sort(x)
        y_values = np.arange(1, len(x_sorted) + 1) / len(x_sorted)
        return x_sorted, y_values
