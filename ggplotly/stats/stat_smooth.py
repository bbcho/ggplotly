# stats/stat_smooth.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.nonparametric.smoothers_lowess import lowess


class stat_smooth:
    """
    Stat for computing smoothed lines (LOESS, linear regression, etc.).

    Handles the computation of smoothed values, which are then passed to geom_smooth for visualization.
    """

    def __init__(self, method="loess", frac=0.3):
        """
        Initializes the smoothing stat.

        Parameters:
            method (str): The smoothing method ('loess', 'lm'). Default is 'loess'.
            frac (float): The smoothing parameter for LOESS. Default is 0.3.
        """
        self.method = method
        self.frac = frac

    def apply_smoothing(self, x, y):
        """
        Applies smoothing based on the chosen method (LOESS or linear regression).

        Parameters:
            x (array-like): The x-values.
            y (array-like): The y-values.

        Returns:
            Smoothed y-values.
        """
        if self.method == "lm":
            # Linear regression using scikit-learn
            model = LinearRegression()
            x_reshaped = np.array(x).reshape(-1, 1)  # Reshaping x for sklearn
            model.fit(x_reshaped, y)
            return model.predict(x_reshaped)

        elif self.method == "loess":
            # LOESS smoothing using statsmodels' lowess
            smoothed = lowess(y, x, frac=self.frac)
            return smoothed[:, 1]  # Return smoothed y-values

        else:
            raise ValueError(f"Unsupported method: {self.method}")

    def compute_stat(self, data):
        """
        Computes the stat for smoothing, modifying the data with smoothed values.

        Parameters:
            data (DataFrame): The input data containing 'x' and 'y'.

        Returns:
            DataFrame: Modified data with smoothed 'y' values.
        """
        x = data["x"]
        y = data["y"]

        # Apply smoothing
        smoothed_y = self.apply_smoothing(x, y)

        # Replace original 'y' with smoothed 'y' in the DataFrame
        data["y"] = smoothed_y
        return data
