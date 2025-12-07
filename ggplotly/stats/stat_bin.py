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
            Ignored if binwidth is specified.
        binwidth (float, optional): Width of each bin. Overrides bins.
        boundary (float, optional): Bin boundary. One bin edge will be at this value.
        center (float, optional): Bin center. One bin center will be at this value.
            Mutually exclusive with boundary.
        breaks (array-like, optional): Explicit bin breaks. Overrides bins and binwidth.
        closed (str): Which side of bins is closed. Options:
            - 'right' (default): bins are (a, b]
            - 'left': bins are [a, b)
        pad (bool): If True, add empty bins at start and end. Default is False.
        na_rm (bool): If True, remove NA values. Default is False.

    Computed variables:
        - count: Number of observations in bin
        - density: Density of observations (count / total / width)
        - ncount: Count scaled to maximum of 1
        - ndensity: Density scaled to maximum of 1
        - width: Width of each bin
        - x: Bin center
        - xmin: Bin left edge
        - xmax: Bin right edge

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_histogram(bins=20)
        >>> ggplot(df, aes(x='value')) + geom_histogram(binwidth=0.5)
        >>> ggplot(df, aes(x='value')) + geom_histogram(boundary=0)
    """

    __name__ = "bin"

    def __init__(self, data=None, mapping=None, bins=30, binwidth=None,
                 boundary=None, center=None, breaks=None, closed='right',
                 pad=False, na_rm=False, **params):
        """
        Initialize the binning stat.

        Parameters:
            data (DataFrame, optional): Data to use.
            mapping (dict, optional): Aesthetic mappings.
            bins (int): Number of bins. Default is 30.
            binwidth (float, optional): Width of bins.
            boundary (float, optional): Bin boundary position.
            center (float, optional): Bin center position.
            breaks (array-like, optional): Explicit bin breaks.
            closed (str): Which side is closed ('right' or 'left'). Default is 'right'.
            pad (bool): Add empty edge bins. Default is False.
            na_rm (bool): Remove NA values. Default is False.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)
        self.bins = bins
        self.binwidth = binwidth
        self.boundary = boundary
        self.center = center
        self.breaks = breaks
        self.closed = closed
        self.pad = pad
        self.na_rm = na_rm

    def _compute_bins(self, x, bins, binwidth, boundary, center, breaks):
        """
        Compute bin edges based on parameters.

        Parameters:
            x (array): Data values.
            bins (int): Number of bins.
            binwidth (float): Width of bins.
            boundary (float): Bin boundary.
            center (float): Bin center.
            breaks (array): Explicit breaks.

        Returns:
            array: Bin edges.
        """
        x_min, x_max = np.nanmin(x), np.nanmax(x)
        x_range = x_max - x_min

        # If explicit breaks provided, use them
        if breaks is not None:
            return np.asarray(breaks)

        # Determine binwidth
        if binwidth is not None:
            width = binwidth
        else:
            width = x_range / bins

        # Adjust for boundary or center
        if boundary is not None:
            # Shift to align with boundary
            shift = (x_min - boundary) % width
            bin_min = x_min - shift
        elif center is not None:
            # Shift to align with center
            shift = (x_min - center + width / 2) % width
            bin_min = x_min - shift
        else:
            # Use data minimum as starting point
            bin_min = x_min

        # Generate bin edges
        n_bins = int(np.ceil((x_max - bin_min) / width)) + 1
        bin_edges = bin_min + np.arange(n_bins + 1) * width

        return bin_edges

    def compute(self, data, bins=None):
        """
        Compute bin counts for the data.

        Parameters:
            data (DataFrame): Data containing the variable to bin.
            bins (int, optional): Number of bins. Default is self.bins.

        Returns:
            DataFrame: Data with binning information including:
                - x: bin centers
                - count: counts per bin
                - density: density per bin
                - ncount: normalized count
                - ndensity: normalized density
                - width: bin width
                - xmin: bin left edge
                - xmax: bin right edge
        """
        if bins is None:
            bins = self.bins

        x_col = self.mapping.get('x')
        if x_col is None:
            # Return unchanged if no x mapping
            return data

        x = data[x_col].values.copy()

        # Remove NA values if requested
        if self.na_rm:
            x = x[~np.isnan(x)]

        if len(x) == 0:
            return pd.DataFrame({
                'x': [], 'count': [], 'density': [], 'ncount': [],
                'ndensity': [], 'width': [], 'xmin': [], 'xmax': []
            })

        # Compute bin edges
        bin_edges = self._compute_bins(x, bins, self.binwidth, self.boundary,
                                       self.center, self.breaks)

        # Compute histogram
        # Note: np.histogram has right-closed bins by default [(, ])
        # For left-closed bins, we need to handle this differently
        if self.closed == 'left':
            # Reverse the data and edges, compute, then reverse back
            counts, _ = np.histogram(-x, bins=-bin_edges[::-1])
            counts = counts[::-1]
        else:
            counts, _ = np.histogram(x, bins=bin_edges)

        # Compute bin properties
        widths = np.diff(bin_edges)
        centers = (bin_edges[:-1] + bin_edges[1:]) / 2
        xmin = bin_edges[:-1]
        xmax = bin_edges[1:]

        # Compute density (integrates to 1)
        total = len(x)
        density = counts / (total * widths) if total > 0 else counts * 0

        # Normalized count and density (max = 1)
        max_count = counts.max() if counts.max() > 0 else 1
        max_density = density.max() if density.max() > 0 else 1
        ncount = counts / max_count
        ndensity = density / max_density

        # Add padding if requested
        if self.pad:
            # Add empty bins at start and end
            avg_width = np.mean(widths)
            centers = np.concatenate([[centers[0] - avg_width], centers, [centers[-1] + avg_width]])
            counts = np.concatenate([[0], counts, [0]])
            density = np.concatenate([[0], density, [0]])
            ncount = np.concatenate([[0], ncount, [0]])
            ndensity = np.concatenate([[0], ndensity, [0]])
            widths = np.concatenate([[avg_width], widths, [avg_width]])
            xmin = np.concatenate([[xmin[0] - avg_width], xmin, [xmax[-1]]])
            xmax = np.concatenate([[xmin[1]], xmax, [xmax[-1] + avg_width]])

        result = pd.DataFrame({
            'x': centers,
            'count': counts,
            'density': density,
            'ncount': ncount,
            'ndensity': ndensity,
            'width': widths,
            'xmin': xmin,
            'xmax': xmax,
        })

        # Store stat info
        self.params["stat"] = "bin"

        return result
