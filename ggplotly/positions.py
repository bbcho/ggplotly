import numpy as np


class position_dodge:
    def adjust(self, x, width=0.8):
        """
        Adjust positions by dodging.

        Parameters:
            x (array-like): Original x positions.
            width (float): Total width of the dodge.

        Returns:
            array-like: Adjusted x positions.
        """
        unique_x = np.unique(x)
        n = len(unique_x)
        offsets = np.linspace(-width / 2, width / 2, n)
        x_adj = x.copy()
        for i, val in enumerate(unique_x):
            x_adj[x == val] += offsets[i % n]
        return x_adj


class position_jitter:
    def adjust(self, x, width=0.2):
        """
        Adjust positions by jittering.

        Parameters:
            x (array-like): Original x positions.
            width (float): Width of the jitter.

        Returns:
            array-like: Adjusted x positions.
        """
        jitter = np.random.uniform(-width / 2, width / 2, size=len(x))
        return x + jitter


class position_stack:
    def adjust(self, y):
        """
        Adjust positions by stacking.

        Parameters:
            y (array-like): Original y values.

        Returns:
            array-like: Adjusted y values.
        """
        return np.cumsum(y)
