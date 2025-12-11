import numpy as np
import pandas as pd


class position_dodge:
    """Dodge overlapping objects side-to-side."""

    def __init__(self, width=None, preserve="total"):
        """
        Dodge overlapping objects side-to-side.

        Dodging preserves the vertical position of a geom while adjusting the
        horizontal position. This is useful for bar charts, boxplots, and other
        geoms where multiple groups would otherwise overlap at the same x position.

        Unlike position_jitter, position_dodge requires a grouping variable to
        determine which objects should be dodged relative to each other.

        Parameters
        ----------
        width : float, optional
            Total width of the dodged area. Default is None, which uses the width
            of the elements. For most cases, 0.9 works well.
        preserve : str, default='total'
            Should dodging preserve the 'total' width of all elements at a position,
            or the width of a 'single' element?

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_bar, geom_point, data
        >>> from ggplotly.positions import position_dodge
        >>> mpg = data('mpg')

        >>> # Dodged bar chart showing cylinder counts by drive type
        >>> ggplot(mpg, aes(x='cyl', fill='drv')) + \\
        ...     geom_bar(position=position_dodge())

        >>> # Dodged points with explicit width
        >>> ggplot(mpg, aes(x='cyl', y='hwy', color='drv')) + \\
        ...     geom_point(position=position_dodge(width=0.5))
        """
        self.width = width
        self.preserve = preserve

    def adjust(self, x, group=None, width=None):
        """
        Adjust x positions by dodging based on group.

        Parameters
        ----------
        x : array-like
            Original x positions.
        group : array-like, optional
            Group labels for each point. Points with the same x but different
            groups will be dodged.
        width : float, optional
            Total width of the dodge. Overrides instance width if provided.

        Returns
        -------
        array-like
            Adjusted x positions with groups dodged side-by-side.
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

        Parameters
        ----------
        data : DataFrame
            Data containing x and group columns.
        x_col : str
            Name of the x position column.
        group_col : str
            Name of the grouping column.
        width : float, optional
            Total dodge width.

        Returns
        -------
        array-like
            Adjusted x positions.
        """
        x = data[x_col].values
        group = data[group_col].values
        return self.adjust(x, group=group, width=width)


class position_dodge2(position_dodge):
    """Dodge overlapping objects side-to-side (version 2)."""

    def __init__(self, width=None, preserve="total", padding=0.1, reverse=False):
        """
        Dodge overlapping objects side-to-side (version 2).

        Unlike position_dodge(), position_dodge2() works without a grouping
        variable in a layer. It's particularly useful for arranging box plots,
        which can have variable widths.

        Parameters
        ----------
        width : float, optional
            Total width of the dodged area.
        preserve : str, default='total'
            Whether to preserve 'total' or 'single' element width.
        padding : float, default=0.1
            Padding between elements.
        reverse : bool, default=False
            Reverse the order of dodging.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_boxplot, data
        >>> from ggplotly.positions import position_dodge2
        >>> mpg = data('mpg')

        >>> # Boxplots with custom padding
        >>> ggplot(mpg, aes(x='class', y='hwy')) + \\
        ...     geom_boxplot(position=position_dodge2(padding=0.2))
        """
        super().__init__(width=width, preserve=preserve)
        self.padding = padding
        self.reverse = reverse


class position_jitter:
    """Adjust positions by adding random noise."""

    def __init__(self, width=0.4, height=0, seed=None):
        """
        Adjust positions by adding random noise.

        This is useful for scatter plots where points would otherwise overlap,
        particularly when one or both axes are categorical or discrete.

        Parameters
        ----------
        width : float, default=0.4
            Amount of horizontal jitter. The jitter is added in both directions,
            so the total spread is width.
        height : float, default=0
            Amount of vertical jitter.
        seed : int, optional
            Random seed for reproducibility.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, data
        >>> from ggplotly.positions import position_jitter
        >>> mpg = data('mpg')

        >>> # Jittered points to reduce overplotting
        >>> ggplot(mpg, aes(x='cyl', y='hwy')) + \\
        ...     geom_point(position=position_jitter())

        >>> # Control jitter amount
        >>> ggplot(mpg, aes(x='cyl', y='hwy')) + \\
        ...     geom_point(position=position_jitter(width=0.2, height=0.5))
        """
        self.width = width
        self.height = height
        self.seed = seed

    def adjust(self, x, y=None, width=None, height=None):
        """
        Adjust positions by jittering.

        Parameters
        ----------
        x : array-like
            Original x positions.
        y : array-like, optional
            Original y positions.
        width : float, optional
            Override horizontal jitter width.
        height : float, optional
            Override vertical jitter height.

        Returns
        -------
        array-like or tuple
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
    """Stack overlapping objects on top of each other."""

    def __init__(self, vjust=1, reverse=False):
        """
        Stack overlapping objects on top of each other.

        This is useful for stacked bar charts and area plots where you want
        to show how parts contribute to a whole.

        Parameters
        ----------
        vjust : float, default=1
            Vertical adjustment for position.
        reverse : bool, default=False
            Reverse stacking order.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_bar, data
        >>> from ggplotly.positions import position_stack
        >>> mpg = data('mpg')

        >>> # Stacked bar chart
        >>> ggplot(mpg, aes(x='class', fill='drv')) + \\
        ...     geom_bar(position=position_stack())
        """
        self.vjust = vjust
        self.reverse = reverse

    def adjust(self, y, group=None):
        """
        Adjust y positions by stacking.

        Parameters
        ----------
        y : array-like
            Original y values.
        group : array-like, optional
            Group labels. If provided, stacking is done within each x position
            based on groups.

        Returns
        -------
        array-like
            Adjusted y values (cumulative).
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

        Parameters
        ----------
        data : DataFrame
            Data containing position columns.
        x_col : str
            Name of the x position column.
        y_col : str
            Name of the y value column.
        group_col : str
            Name of the grouping column.

        Returns
        -------
        tuple
            (y_bottom, y_top) arrays for each bar.
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
    """Stack and normalize to equal height for proportions."""

    def __init__(self, vjust=1, reverse=False):
        """
        Stack overlapping objects and standardize to have equal height.

        This is useful for showing proportions rather than absolute values.
        Each stack is normalized to sum to 1 (or 100%).

        Parameters
        ----------
        vjust : float, default=1
            Vertical adjustment.
        reverse : bool, default=False
            Reverse stacking order.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_bar, data
        >>> from ggplotly.positions import position_fill
        >>> mpg = data('mpg')

        >>> # Proportional stacked bar chart (100% stacked)
        >>> ggplot(mpg, aes(x='class', fill='drv')) + \\
        ...     geom_bar(position=position_fill())
        """
        super().__init__(vjust=vjust, reverse=reverse)

    def compute_stacked_positions(self, data, x_col, y_col, group_col):
        """
        Compute normalized stacked positions for a DataFrame.

        Each x position's values are normalized to sum to 1.

        Parameters
        ----------
        data : DataFrame
            Data containing position columns.
        x_col : str
            Name of the x position column.
        y_col : str
            Name of the y value column.
        group_col : str
            Name of the grouping column.

        Returns
        -------
        tuple
            (y_bottom, y_top) arrays normalized to [0, 1].
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
    """Don't adjust position (identity transformation)."""

    def __init__(self):
        """
        Don't adjust position.

        This is the default position adjustment - it leaves the data unchanged.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, data
        >>> from ggplotly.positions import position_identity
        >>> mpg = data('mpg')

        >>> # Points with no position adjustment (default behavior)
        >>> ggplot(mpg, aes(x='displ', y='hwy')) + \\
        ...     geom_point(position=position_identity())
        """
        pass

    def adjust(self, x, **kwargs):
        """Return positions unchanged."""
        return np.asarray(x)


class position_nudge:
    """Nudge points a fixed distance."""

    def __init__(self, x=0, y=0):
        """
        Nudge points a fixed distance.

        This is useful for moving labels or points away from their anchors
        by a fixed amount.

        Parameters
        ----------
        x : float, default=0
            Horizontal distance to nudge.
        y : float, default=0
            Vertical distance to nudge.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_point, geom_text, data
        >>> from ggplotly.positions import position_nudge
        >>> mtcars = data('mtcars')

        >>> # Nudge text labels away from points
        >>> ggplot(mtcars.head(10), aes(x='wt', y='mpg', label='model')) + \\
        ...     geom_point() + \\
        ...     geom_text(position=position_nudge(x=0.1, y=0.5))
        """
        self.x_nudge = x
        self.y_nudge = y

    def adjust(self, x, y=None):
        """
        Nudge positions by fixed amounts.

        Parameters
        ----------
        x : array-like
            Original x positions.
        y : array-like, optional
            Original y positions.

        Returns
        -------
        array-like or tuple
            If y is None: adjusted x positions.
            If y is provided: tuple of (adjusted x, adjusted y).
        """
        x = np.asarray(x, dtype=float) + self.x_nudge

        if y is None:
            return x

        y = np.asarray(y, dtype=float) + self.y_nudge
        return x, y
