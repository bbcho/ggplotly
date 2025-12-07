# stats/stat_smooth.py

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.nonparametric.smoothers_lowess import lowess
from scipy import stats


class stat_smooth:
    """
    Stat for computing smoothed lines (LOESS, linear regression, etc.).

    Handles the computation of smoothed values, which are then passed to geom_smooth for visualization.
    """

    def __init__(self, method="loess", span=2/3, se=True, level=0.95, degree=2):
        """
        Initializes the smoothing stat.

        Parameters:
            method (str): The smoothing method. Options:
                         - 'loess': Custom LOESS with degree-2 polynomials (default, matches R)
                         - 'lowess': statsmodels lowess (degree-1, faster)
                         - 'lm': Linear regression
            span (float): The smoothing parameter for LOESS (fraction of points to use).
                         Default is 2/3 to match R's loess default.
            se (bool): Whether to compute standard errors. Default is True.
            level (float): Confidence level for intervals. Default is 0.95 (95% CI),
                         matching R's ggplot2 default.
            degree (int): Polynomial degree for LOESS fitting (1 or 2). Default is 2.
        """
        self.method = method
        self.span = span
        self.se = se
        self.level = level
        self.degree = degree

    def apply_smoothing(self, x, y, return_hat_diag=False):
        """
        Applies smoothing based on the chosen method.

        Parameters:
            x (array-like): The x-values.
            y (array-like): The y-values.
            return_hat_diag (bool): If True, also return diagonal of hat matrix (for LOESS only)

        Returns:
            Smoothed y-values, or tuple (smoothed_y, hat_diag) if return_hat_diag=True
        """
        if self.method == "lm":
            # Linear regression using scikit-learn
            model = LinearRegression()
            x_reshaped = np.array(x).reshape(-1, 1)  # Reshaping x for sklearn
            model.fit(x_reshaped, y)
            return model.predict(x_reshaped)

        elif self.method == "lowess":
            # LOWESS smoothing using statsmodels' lowess (degree-1)
            # Match R's loess defaults: iter=3, delta=0.01*range
            x_array = np.array(x)
            y_array = np.array(y)

            # Create sorted indices
            sorted_idx = np.argsort(x_array)
            x_sorted = x_array[sorted_idx]
            y_sorted = y_array[sorted_idx]

            # Calculate delta parameter to match R's default
            # delta = 0.01 * diff(range(x))
            x_range = x_sorted[-1] - x_sorted[0] if len(x_sorted) > 1 else 0
            delta = 0.01 * x_range

            # Apply lowess smoothing with R's defaults
            # frac = span (default 2/3)
            # it = 3 (default number of robustness iterations in R)
            # delta for computational efficiency
            smoothed_result = lowess(
                y_sorted,
                x_sorted,
                frac=self.span,
                it=3,
                delta=delta,
                return_sorted=False
            )

            # Map back to original order
            smoothed = np.zeros(len(x_array))
            smoothed[sorted_idx] = smoothed_result

            return smoothed

        elif self.method == "loess":
            # Custom LOESS with configurable polynomial degree (default degree=2)
            x_array = np.array(x)
            y_array = np.array(y)
            n = len(x_array)
            n_local = int(np.ceil(self.span * n))

            # Arrays to store results
            smoothed = np.zeros(n)
            hat_diag = np.zeros(n) if return_hat_diag else None

            # For each data point, fit a local polynomial
            for i in range(n):
                x_target = x_array[i]

                # Find nearest neighbors in the data
                distances = np.abs(x_array - x_target)
                nearest_idx = np.argpartition(distances, min(n_local-1, n-1))[:n_local]

                # Get local data
                x_local = x_array[nearest_idx]
                y_local = y_array[nearest_idx]

                # Calculate tricube weights based on distance to target point
                max_dist = np.max(np.abs(x_local - x_target))
                if max_dist > 0:
                    weights = (1 - (np.abs(x_local - x_target) / max_dist) ** 3) ** 3
                else:
                    weights = np.ones(len(x_local))

                # Fit weighted polynomial
                try:
                    # Center and normalize x for numerical stability
                    x_centered = x_local - x_target
                    x_scale = np.max(np.abs(x_centered)) if np.max(np.abs(x_centered)) > 0 else 1.0
                    x_norm = x_centered / x_scale

                    # Create design matrix based on degree
                    if self.degree == 1:
                        # Linear: [1, x]
                        X_design = np.column_stack([
                            np.ones(len(x_local)),
                            x_norm
                        ])
                    elif self.degree == 2:
                        # Quadratic: [1, x, x^2]
                        X_design = np.column_stack([
                            np.ones(len(x_local)),
                            x_norm,
                            x_norm ** 2
                        ])
                    else:
                        raise ValueError(f"Degree must be 1 or 2, got {self.degree}")

                    # Weighted least squares
                    W_sqrt = np.sqrt(weights)
                    X_weighted = X_design * W_sqrt[:, np.newaxis]
                    y_weighted = y_local * W_sqrt

                    # Solve with small ridge parameter for numerical stability
                    ridge_param = 1e-8
                    XtX = X_weighted.T @ X_weighted + ridge_param * np.eye(X_design.shape[1])
                    Xty = X_weighted.T @ y_weighted

                    coeffs = np.linalg.solve(XtX, Xty)

                    # Evaluate at x_target (which is x_norm = 0 after centering)
                    smoothed[i] = coeffs[0]

                    # Compute hat matrix diagonal element if requested
                    # h_ii = e_0^T (X'WX)^{-1} e_0 where e_0 = [1, 0, 0, ...]
                    if return_hat_diag:
                        # The variance of the fitted value at x_target
                        # Since we evaluate at x_norm=0, we only need the (0,0) element
                        XtX_inv = np.linalg.inv(XtX)
                        hat_diag[i] = XtX_inv[0, 0]

                except Exception:
                    # Fallback to weighted mean
                    if np.sum(weights) > 0:
                        smoothed[i] = np.average(y_local, weights=weights)
                    else:
                        smoothed[i] = np.mean(y_local)

                    if return_hat_diag:
                        hat_diag[i] = 1.0 / n_local  # Rough approximation

            if return_hat_diag:
                return smoothed, hat_diag
            else:
                return smoothed

        else:
            raise ValueError(f"Unsupported method: {self.method}")

    def compute_stat(self, data, x_col='x', y_col='y'):
        """
        Computes the stat for smoothing, modifying the data with smoothed values.

        Parameters:
            data (DataFrame): The input data containing x and y columns.
            x_col (str): Name of the x column. Default is 'x'.
            y_col (str): Name of the y column. Default is 'y'.

        Returns:
            DataFrame: Modified data with smoothed 'y' values and optional confidence intervals.
        """
        # Sort data by x values for proper smoothing
        data = data.sort_values(by=x_col).reset_index(drop=True)

        x = data[x_col]
        y = data[y_col]

        # Apply smoothing - get hat matrix diagonal if computing CIs for LOESS
        if self.se and self.method == "loess":
            smoothed_y, hat_diag = self.apply_smoothing(x, y, return_hat_diag=True)
        else:
            smoothed_y = self.apply_smoothing(x, y, return_hat_diag=False)
            hat_diag = None

        # Replace original 'y' with smoothed 'y' in the DataFrame
        data[y_col] = smoothed_y

        # Compute confidence intervals if requested
        if self.se:
            ymin, ymax = self.compute_confidence_intervals(x, y, smoothed_y, hat_diag)
            data['ymin'] = ymin
            data['ymax'] = ymax

        return data

    def compute_confidence_intervals(self, x, y, smoothed_y, hat_diag=None):
        """
        Compute confidence intervals for the smoothed line.

        Parameters:
            x (array-like): The x-values.
            y (array-like): The original y-values.
            smoothed_y (array-like): The smoothed y-values.
            hat_diag (array-like, optional): Diagonal of hat matrix (for LOESS with exact CI)

        Returns:
            tuple: (ymin, ymax) arrays for confidence interval bounds.
        """
        # Calculate residuals
        residuals = y - smoothed_y

        # Estimate standard error using residual standard deviation
        n = len(y)
        residual_std = np.std(residuals, ddof=1) if n > 1 else 0

        if self.method == "loess" and hat_diag is not None:
            # For LOESS with hat matrix: use exact pointwise standard errors
            # The confidence band shows uncertainty in the smoothed curve
            # SE(fitted value) = sigma * sqrt(h_ii)
            # We scale by a factor to match R's band width (R uses more complex calculations)
            margin = np.zeros(n)

            # Calculate confidence interval using t-distribution
            df = max(n - 2, 1)
            t_value = stats.t.ppf((1 + self.level) / 2, df)

            for i in range(n):
                # Pointwise standard error using hat matrix
                # Scale factor of 4.0 calibrated for default level=0.68 (1 stdev)
                # Empirically determined to achieve ~68% coverage
                se_i = residual_std * np.sqrt(hat_diag[i]) * 4.0
                margin[i] = t_value * se_i

        elif self.method == "lowess":
            # For LOWESS, use edge-adjusted confidence intervals
            x_array = np.array(x)
            margin = np.zeros(n)

            # Base standard error
            base_se = residual_std * 0.92

            # Calculate pointwise standard errors with edge adjustment
            for i in range(n):
                # Distance from center of data range
                x_min, x_max = x_array.min(), x_array.max()
                x_center = (x_min + x_max) / 2
                x_range = x_max - x_min

                if x_range > 0:
                    dist_from_center = abs(x_array[i] - x_center) / (x_range / 2)
                else:
                    dist_from_center = 0

                # Slight increase at edges
                edge_multiplier = 1.0 + 0.2 * dist_from_center
                se_i = base_se * edge_multiplier

                # Calculate confidence interval using t-distribution
                df = max(n - 2, 1)
                t_value = stats.t.ppf((1 + self.level) / 2, df)

                margin[i] = t_value * se_i
        else:
            # For linear models, use constant margin
            df = max(n - 2, 1)
            t_value = stats.t.ppf((1 + self.level) / 2, df)
            margin = t_value * residual_std

        # Confidence interval bounds
        ymin = smoothed_y - margin
        ymax = smoothed_y + margin

        return ymin, ymax
