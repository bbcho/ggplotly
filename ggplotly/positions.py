import numpy as np
import pandas as pd


class position_dodge:
    """
    Dodge overlapping objects side-to-side.

    Dodging preserves the vertical position of a geom while adjusting the
    horizontal position. This is useful for bar charts, boxplots, and other
    geoms where multiple groups would otherwise overlap at the same x position.

    Unlike position_jitter, position_dodge requires a grouping variable to
    determine which objects should be dodged relative to each other.

    Parameters:
        width (float): Total width of the dodged area. Default is None,
            which uses the width of the elements. For most cases, 0.9 works well.
        preserve (str): Should dodging preserve the "total" width of all elements
            at a position, or the width of a "single" element? Default is "total".

    Examples:
        >>> # Dodged bar chart
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + \\
        ...     geom_bar(stat='identity', position=position_dodge())

        >>> # Dodged points with explicit width
        >>> ggplot(df, aes(x='category', y='value', color='group')) + \\
        ...     geom_point(position=position_dodge(width=0.5))
    """

    def __init__(self, width=None, preserve="total"):
        """
        Initialize position_dodge.

        Parameters:
            width (float, optional): Total width of the dodged area.
            preserve (str): "total" or "single" - how to calculate widths.
        """
        self.width = width
        self.preserve = preserve

    def adjust(self, x, group=None, width=None):
        """
        Adjust x positions by dodging based on group.

        Parameters:
            x (array-like): Original x positions.
            group (array-like, optional): Group labels for each point.
                Points with the same x but different groups will be dodged.
            width (float, optional): Total width of the dodge. Overrides
                instance width if provided.

        Returns:
            array-like: Adjusted x positions with groups dodged side-by-side.
        """
        x = np.asarray(x, dtype=float)
        dodge_width = width if width is not None else (self.width if self.width is not None else 0.9)

        # If no group provided, return unchanged
        if group is None:
            return x

        group = np.asarray(group)

        # Get unique groups (maintain order of first appearance)
        _, idx = np.unique(group, return_index=True)
        unique_groups = group[np.sort(idx)]
        n_groups = len(unique_groups)

        if n_groups <= 1:
            return x

        # Create mapping from group to index
        group_to_idx = {g: i for i, g in enumerate(unique_groups)}

        # Calculate offset for each point based on its group
        x_adj = x.copy()

        # Width of each individual element
        element_width = dodge_width / n_groups

        for i, g in enumerate(group):
            group_idx = group_to_idx[g]
            # Center the groups: offset from -dodge_width/2 to +dodge_width/2
            # Each group gets positioned at its slot center
            offset = -dodge_width / 2 + element_width * (group_idx + 0.5)
            x_adj[i] += offset

        return x_adj

    def compute_dodged_positions(self, data, x_col, group_col, width=None):
        """
        Compute dodged positions for a DataFrame.

        This is a convenience method for dodging positions in a DataFrame,
        handling the grouping automatically.

        Parameters:
            data (DataFrame): Data containing x and group columns.
            x_col (str): Name of the x position column.
            group_col (str): Name of the grouping column.
            width (float, optional): Total dodge width.

        Returns:
            array-like: Adjusted x positions.
        """
        x = data[x_col].values
        group = data[group_col].values
        return self.adjust(x, group=group, width=width)


class position_dodge2(position_dodge):
    """
    Dodge overlapping objects side-to-side (version 2).

    Unlike position_dodge(), position_dodge2() works without a grouping
    variable in a layer. It's particularly useful for arranging box plots,
    which can have variable widths.

    Parameters:
        width (float): Total width of the dodged area. Default is None.
        preserve (str): "total" or "single". Default is "total".
        padding (float): Padding between elements. Default is 0.1.
        reverse (bool): Reverse the order of dodging. Default is False.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + \\
        ...     geom_boxplot(position=position_dodge2(padding=0.2))
    """

    def __init__(self, width=None, preserve="total", padding=0.1, reverse=False):
        super().__init__(width=width, preserve=preserve)
        self.padding = padding
        self.reverse = reverse


class position_jitter:
    """
    Adjust positions by adding random noise.

    This is useful for scatter plots where points would otherwise overlap,
    particularly when one or both axes are categorical or discrete.

    Parameters:
        width (float): Amount of horizontal jitter. Default is 0.4.
            The jitter is added in both directions, so the total spread is width.
        height (float): Amount of vertical jitter. Default is 0.
        seed (int, optional): Random seed for reproducibility.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + \\
        ...     geom_point(position=position_jitter())

        >>> # Control jitter amount
        >>> ggplot(df, aes(x='category', y='value')) + \\
        ...     geom_point(position=position_jitter(width=0.2, height=0.1))
    """

    def __init__(self, width=0.4, height=0, seed=None):
        self.width = width
        self.height = height
        self.seed = seed

    def adjust(self, x, y=None, width=None, height=None):
        """
        Adjust positions by jittering.

        Parameters:
            x (array-like): Original x positions.
            y (array-like, optional): Original y positions.
            width (float, optional): Override horizontal jitter width.
            height (float, optional): Override vertical jitter height.

        Returns:
            If y is None: adjusted x positions.
            If y is provided: tuple of (adjusted x, adjusted y).
        """
        if self.seed is not None:
            np.random.seed(self.seed)

        w = width if width is not None else self.width
        h = height if height is not None else self.height

        x = np.asarray(x, dtype=float)
        x_jitter = np.random.uniform(-w / 2, w / 2, size=len(x))
        x_adj = x + x_jitter

        if y is None:
            return x_adj

        y = np.asarray(y, dtype=float)
        y_jitter = np.random.uniform(-h / 2, h / 2, size=len(y))
        y_adj = y + y_jitter

        return x_adj, y_adj


class position_stack:
    """
    Stack overlapping objects on top of each other.

    This is useful for stacked bar charts and area plots where you want
    to show how parts contribute to a whole.

    Parameters:
        vjust (float): Vertical adjustment for position. Default is 1.
        reverse (bool): Reverse stacking order. Default is False.

    Examples:
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + \\
        ...     geom_bar(stat='identity', position=position_stack())
    """

    def __init__(self, vjust=1, reverse=False):
        self.vjust = vjust
        self.reverse = reverse

    def adjust(self, y, group=None):
        """
        Adjust y positions by stacking.

        Parameters:
            y (array-like): Original y values.
            group (array-like, optional): Group labels. If provided,
                stacking is done within each x position based on groups.

        Returns:
            array-like: Adjusted y values (cumulative).
        """
        y = np.asarray(y, dtype=float)

        if self.reverse:
            y = y[::-1]

        result = np.cumsum(y)

        if self.reverse:
            result = result[::-1]

        return result

    def compute_stacked_positions(self, data, x_col, y_col, group_col):
        """
        Compute stacked positions for a DataFrame.

        Stacks y values within each unique x position, ordered by group.

        Parameters:
            data (DataFrame): Data containing position columns.
            x_col (str): Name of the x position column.
            y_col (str): Name of the y value column.
            group_col (str): Name of the grouping column.

        Returns:
            tuple: (y_bottom, y_top) arrays for each bar.
        """
        data = data.copy()

        # Sort by x then group for consistent stacking
        data = data.sort_values([x_col, group_col])

        y_bottom = []
        y_top = []

        for x_val in data[x_col].unique():
            mask = data[x_col] == x_val
            x_data = data[mask]

            cumsum = 0
            for _, row in x_data.iterrows():
                y_bottom.append(cumsum)
                cumsum += row[y_col]
                y_top.append(cumsum)

        return np.array(y_bottom), np.array(y_top)


class position_fill(position_stack):
    """
    Stack overlapping objects and standardize to have equal height.

    This is useful for showing proportions rather than absolute values.
    Each stack is normalized to sum to 1 (or 100%).

    Parameters:
        vjust (float): Vertical adjustment. Default is 1.
        reverse (bool): Reverse stacking order. Default is False.

    Examples:
        >>> ggplot(df, aes(x='category', y='value', fill='group')) + \\
        ...     geom_bar(stat='identity', position=position_fill())
    """

    def compute_stacked_positions(self, data, x_col, y_col, group_col):
        """
        Compute normalized stacked positions for a DataFrame.

        Each x position's values are normalized to sum to 1.

        Parameters:
            data (DataFrame): Data containing position columns.
            x_col (str): Name of the x position column.
            y_col (str): Name of the y value column.
            group_col (str): Name of the grouping column.

        Returns:
            tuple: (y_bottom, y_top) arrays normalized to [0, 1].
        """
        data = data.copy()
        data = data.sort_values([x_col, group_col])

        y_bottom = []
        y_top = []

        for x_val in data[x_col].unique():
            mask = data[x_col] == x_val
            x_data = data[mask]
            total = x_data[y_col].sum()

            if total == 0:
                total = 1  # Avoid division by zero

            cumsum = 0
            for _, row in x_data.iterrows():
                proportion = row[y_col] / total
                y_bottom.append(cumsum)
                cumsum += proportion
                y_top.append(cumsum)

        return np.array(y_bottom), np.array(y_top)


class position_identity:
    """
    Don't adjust position.

    This is the default position adjustment - it leaves the data unchanged.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + \\
        ...     geom_point(position=position_identity())
    """

    def adjust(self, x, **kwargs):
        """Return positions unchanged."""
        return np.asarray(x)


class position_nudge:
    """
    Nudge points a fixed distance.

    This is useful for moving labels or points away from their anchors
    by a fixed amount.

    Parameters:
        x (float): Horizontal distance to nudge. Default is 0.
        y (float): Vertical distance to nudge. Default is 0.

    Examples:
        >>> ggplot(df, aes(x='x', y='y', label='name')) + \\
        ...     geom_point() + \\
        ...     geom_text(position=position_nudge(x=0.1, y=0.1))
    """

    def __init__(self, x=0, y=0):
        self.x_nudge = x
        self.y_nudge = y

    def adjust(self, x, y=None):
        """
        Nudge positions by fixed amounts.

        Parameters:
            x (array-like): Original x positions.
            y (array-like, optional): Original y positions.

        Returns:
            If y is None: adjusted x positions.
            If y is provided: tuple of (adjusted x, adjusted y).
        """
        x = np.asarray(x, dtype=float) + self.x_nudge

        if y is None:
            return x

        y = np.asarray(y, dtype=float) + self.y_nudge
        return x, y
