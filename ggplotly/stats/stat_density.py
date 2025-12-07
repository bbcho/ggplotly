"""Density estimation stat for density plots."""

import numpy as np
from scipy.stats import gaussian_kde


class stat_density:
    """
    Compute kernel density estimate for continuous data.

    This stat performs kernel density estimation, useful for visualizing
    the distribution of a continuous variable as a smooth curve.

    Parameters:
        bw (str or float): Bandwidth method or value. Options:
            - 'nrd0' (default): Silverman's rule-of-thumb (R default)
            - 'nrd': Scott's variation of Silverman's rule
            - 'scott': Scott's rule
            - 'silverman': Silverman's rule
            - float: Explicit bandwidth value
        adjust (float): Bandwidth adjustment multiplier. Default is 1.
            Larger values produce smoother curves.
        kernel (str): Kernel function. Default is 'gaussian'.
            Note: scipy only supports gaussian kernel.
        n (int): Number of equally spaced points for density evaluation.
            Default is 512 (matching R's default).
        trim (bool): If True, trim the density curve to the data range.
            Default is False (extend slightly beyond data range).
        na_rm (bool): If True, remove NA values. Default is False.

    Computed variables:
        - x: Evaluation points
        - y: Density estimates (integrate to 1)
        - density: Same as y
        - count: Density * n (useful for histograms)
        - scaled: Density scaled to maximum of 1
        - ndensity: Alias for scaled

    Examples:
        >>> stat_density()  # Default: nrd0 bandwidth, 512 points
        >>> stat_density(bw='scott', adjust=0.5)  # Narrower bandwidth
        >>> stat_density(n=256, trim=True)  # Fewer points, trimmed to data range
    """

    def __init__(self, bw='nrd0', adjust=1, kernel='gaussian', n=512,
                 trim=False, na_rm=False):
        """
        Initialize the density stat.

        Parameters:
            bw (str or float): Bandwidth method or value. Default is 'nrd0'.
            adjust (float): Bandwidth adjustment multiplier. Default is 1.
            kernel (str): Kernel function. Default is 'gaussian'.
            n (int): Number of evaluation points. Default is 512.
            trim (bool): Trim to data range. Default is False.
            na_rm (bool): Remove NA values. Default is False.
        """
        self.bw = bw
        self.adjust = adjust
        self.kernel = kernel
        self.n = n
        self.trim = trim
        self.na_rm = na_rm

    def _compute_bandwidth(self, x):
        """
        Compute bandwidth using specified method.

        Parameters:
            x (array): Input data.

        Returns:
            float: Computed bandwidth value.
        """
        if isinstance(self.bw, (int, float)):
            return float(self.bw) * self.adjust

        x = np.asarray(x)
        n = len(x)
        std = np.std(x, ddof=1)
        iqr = np.subtract(*np.percentile(x, [75, 25]))

        if self.bw in ('nrd0', 'silverman'):
            # Silverman's rule-of-thumb (R's default nrd0)
            # bw = 0.9 * min(sd, IQR/1.34) * n^(-1/5)
            bandwidth = 0.9 * min(std, iqr / 1.34) * n ** (-0.2)
        elif self.bw in ('nrd', 'scott'):
            # Scott's variation
            # bw = 1.06 * min(sd, IQR/1.34) * n^(-1/5)
            bandwidth = 1.06 * min(std, iqr / 1.34) * n ** (-0.2)
        else:
            # Default to scipy's method
            bandwidth = None

        if bandwidth is not None:
            return bandwidth * self.adjust
        return None

    def compute(self, x):
        """
        Estimates density for density plots.

        Parameters:
            x (array-like): Data for density estimation.

        Returns:
            dict: Contains 'x', 'y', 'density', 'count', 'scaled', 'ndensity'.
        """
        x = np.array(x)

        # Remove NA values if requested
        if self.na_rm:
            x = x[~np.isnan(x)]

        if len(x) == 0:
            return {"x": np.array([]), "y": np.array([]), "density": np.array([]),
                    "count": np.array([]), "scaled": np.array([]), "ndensity": np.array([])}

        # Compute bandwidth
        bw = self._compute_bandwidth(x)

        # Create KDE
        if bw is not None:
            density = gaussian_kde(x, bw_method=bw / np.std(x, ddof=1))
        else:
            density = gaussian_kde(x)

        # Generate evaluation points
        x_min, x_max = x.min(), x.max()
        data_range = x_max - x_min

        if self.trim:
            # Trim to data range
            x_vals = np.linspace(x_min, x_max, self.n)
        else:
            # Extend slightly beyond data range (R default behavior)
            extend = data_range * 0.05
            x_vals = np.linspace(x_min - extend, x_max + extend, self.n)

        # Evaluate density
        y_vals = density.evaluate(x_vals)

        # Compute additional variables
        count = y_vals * len(x)
        max_density = y_vals.max() if len(y_vals) > 0 else 1
        scaled = y_vals / max_density if max_density > 0 else y_vals

        return {
            "x": x_vals,
            "y": y_vals,
            "density": y_vals,
            "count": count,
            "scaled": scaled,
            "ndensity": scaled,
        }
