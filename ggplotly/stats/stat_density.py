import numpy as np
from scipy.stats import gaussian_kde


class stat_density:
    def compute(self, x):
        """
        Estimates density for density plots.

        Parameters:
            x (array-like): Data for density estimation.

        Returns:
            dict: Contains 'x' and 'y' for the density estimate.
        """
        x = np.array(x)
        density = gaussian_kde(x)
        x_vals = np.linspace(x.min(), x.max(), 100)
        y_vals = density.evaluate(x_vals)
        return {"x": x_vals, "y": y_vals}
