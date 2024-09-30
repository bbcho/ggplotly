import numpy as np


class stat_bin:
    def compute(self, x, bins=30):
        """
        Computes counts and bin edges for histograms.

        Parameters:
            x (array-like): Data to bin.
            bins (int): Number of bins.

        Returns:
            dict: Contains 'counts' and 'edges'.
        """
        counts, edges = np.histogram(x, bins=bins)
        return {"counts": counts, "edges": edges}
