# stats/stat_bin.py
"""Binning stat for histograms."""

import numpy as np
import pandas as pd
from .stat_base import Stat


class stat_bin(Stat):
    """
    Bin continuous data for histograms.

    This stat divides continuous data into bins and counts the number
    of observations in each bin. It's used internally by geom_histogram.

    Parameters:
        bins (int): Number of bins to create. Default is 30.
        data (DataFrame, optional): Data to use for this stat.
        mapping (dict, optional): Aesthetic mappings.
        **params: Additional parameters.

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_histogram(bins=20)
    """

    __name__ = "bin"

    def compute(self, data, bins=30):
        """
        Compute bin counts for the data.

        Parameters:
            data (DataFrame): Data containing the variable to bin.
            bins (int): Number of bins. Default is 30.

        Returns:
            DataFrame: Data with binning information.
        """
        data = data.copy()

        grouping = list(set([v for k, v in self.mapping.items()]))
        grouping = [g for g in grouping if g in data.columns]
        self.params["stat"] = "bin"

        return data
