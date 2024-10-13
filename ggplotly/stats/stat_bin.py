import numpy as np
from .stat_base import Stat
import pandas as pd


class stat_bin(Stat):
    __name__ = "bin"

    def compute(self, data, bins=30):
        """
        Computes counts and bin edges for histograms.

        Parameters:
            data (dataframe): Data to bin.
            bins (int): Number of bins.

        """
        data = data.copy()

        grouping = list(set([v for k, v in self.mapping.items()]))
        grouping = [g for g in grouping if g in data.columns]
        self.params["stat"] = "bin"

        return data
