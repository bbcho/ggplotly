import numpy as np


class position_dodge:
    """
    Adjust positions by dodging overlapping objects side-to-side.

    This is useful for bar charts and other geoms where multiple groups
    would otherwise overlap.

    Examples:
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + geom_bar(position=position_dodge())
    """
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
    """
    Adjust positions by adding random noise.

    This is useful for scatter plots where points would otherwise overlap.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_point(position=position_jitter())
    """

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
    """
    Adjust positions by stacking objects on top of each other.

    This is useful for stacked bar charts and area plots.

    Examples:
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + geom_bar(position=position_stack())
    """

    def adjust(self, y):
        """
        Adjust positions by stacking.

        Parameters:
            y (array-like): Original y values.

        Returns:
            array-like: Adjusted y values.
        """
        return np.cumsum(y)
