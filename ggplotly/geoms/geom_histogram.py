# geoms/geom_histogram.py

import pandas as pd
import plotly.graph_objects as go

from ..stats.stat_bin import stat_bin
from .geom_base import Geom


class geom_histogram(Geom):
    """
    Geom for drawing histograms.

    Automatically handles categorical variables for color and fill.
    Automatically converts 'group' and 'fill' columns to categorical if necessary.

    Parameters:
        mapping (aes): Aesthetic mappings created by aes().
        bins (int, optional): Number of bins. Default is 30. Overridden by binwidth if specified.
        binwidth (float, optional): Width of each bin. Overrides bins if specified.
            In ggplot2, this is the preferred way to specify bin size.
        boundary (float, optional): A boundary between bins. Shifts bin edges to align with
            this value. For example, boundary=0 ensures a bin edge at 0.
        center (float, optional): The center of one of the bins. Alternative to boundary.
        color (str, optional): Color of the histogram bars. If a categorical variable is
            mapped to color, different colors will be assigned.
        group (str, optional): Grouping variable for the histogram bars.
        fill (str, optional): Fill color for the bars.
        alpha (float, optional): Transparency level for the fill color. Default is 1.
        showlegend (bool, optional): Whether to show legend entries. Default is True.
        position (str, optional): Position adjustment: 'stack' (default), 'dodge', 'identity'.
        na_rm (bool, optional): If True, silently remove missing values. Default is False.

    Examples:
        >>> ggplot(df, aes(x='value')) + geom_histogram()
        >>> ggplot(df, aes(x='value')) + geom_histogram(bins=20)
        >>> ggplot(df, aes(x='value')) + geom_histogram(binwidth=5)
        >>> ggplot(df, aes(x='value', fill='category')) + geom_histogram(alpha=0.5)
    """

    def __init__(self, data=None, mapping=None, bins=30, binwidth=None, boundary=None,
                 center=None, barmode="stack", bin=None, **params):
        """
        Initialize the histogram geom.

        Parameters:
            data (DataFrame, optional): Data for this geom.
            mapping (aes, optional): Aesthetic mappings.
            bins (int): Number of bins. Default is 30. Overridden by binwidth if specified.
            binwidth (float, optional): Width of each bin. Overrides bins if specified.
            boundary (float, optional): A boundary between bins.
            center (float, optional): The center of one of the bins.
            barmode (str): Bar mode ('stack', 'overlay', 'group'). Default is 'stack'.
            bin (int, optional): Deprecated alias for bins. Use bins instead.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)
        # Support deprecated 'bin' parameter for backward compatibility
        if bin is not None:
            self.bins = bin
        else:
            self.bins = bins
        self.binwidth = binwidth
        self.boundary = boundary
        self.center = center
        self.barmode = barmode

    def _apply_stats(self, data):
        """
        Apply stat_bin to compute histogram bins.

        Handles grouping by fill/color/group aesthetics automatically.
        """
        na_rm = self.params.get("na_rm", False)
        x_col = self.mapping.get("x")

        # Determine grouping column from fill, color, or group mapping
        group_col = None
        for aesthetic in ['fill', 'color', 'group']:
            if aesthetic in self.mapping:
                potential_col = self.mapping[aesthetic]
                if potential_col in data.columns:
                    group_col = potential_col
                    break

        # Create stat_bin with our parameters
        bin_stat = stat_bin(
            mapping={'x': x_col},
            bins=self.bins,
            binwidth=self.binwidth,
            boundary=self.boundary,
            center=self.center,
            na_rm=na_rm
        )

        # Compute bins - either grouped or ungrouped
        if group_col is not None:
            # Grouped histogram: compute separate bins for each group
            binned_frames = []
            for group_value in data[group_col].unique():
                group_data = data[data[group_col] == group_value].copy()
                binned_data = bin_stat.compute(group_data)
                binned_data[group_col] = group_value
                binned_frames.append(binned_data)

            if binned_frames:
                data = pd.concat(binned_frames, ignore_index=True)
            else:
                data = pd.DataFrame({'x': [], 'count': [], 'width': [], group_col: []})
        else:
            # Ungrouped histogram
            data = bin_stat.compute(data)

        # Update mapping for bar chart rendering
        self.mapping["x"] = "x"

        # Resolve y mapping (after_stat expressions, ..var.., etc.)
        data = self._resolve_y_mapping(data)

        # Apply any additional stats
        return super()._apply_stats(data)

    def _resolve_y_mapping(self, data):
        """
        Resolve the y aesthetic mapping to a computed stat variable.

        Handles:
        - after_stat('density')
        - after_stat('count / count.sum()')  # expressions
        - '..density..'  # R-style syntax
        """
        from ..aes import after_stat
        y_mapping = self.mapping.get("y", "")

        if isinstance(y_mapping, after_stat):
            if y_mapping.is_expression():
                # Evaluate expression and store result in new column
                data['_after_stat_y'] = y_mapping.evaluate(data)
                self.mapping["y"] = '_after_stat_y'
            elif y_mapping.expr in data.columns:
                self.mapping["y"] = y_mapping.expr
            else:
                self.mapping["y"] = "count"
        elif isinstance(y_mapping, str):
            # Handle R-style ..var.. syntax or direct column name
            if y_mapping.startswith("..") and y_mapping.endswith(".."):
                stat_var = y_mapping[2:-2]  # Strip the dots
            else:
                stat_var = y_mapping

            if stat_var in data.columns:
                self.mapping["y"] = stat_var
            else:
                self.mapping["y"] = "count"
        else:
            self.mapping["y"] = "count"

        return data

    def _draw_impl(self, fig, data, row, col):
        """
        Draw histogram(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Data (already transformed by _apply_stats).
            row (int): Row position in subplot.
            col (int): Column position in subplot.

        Returns:
            None: Modifies the figure in place.
        """
        payload = dict()
        payload["name"] = self.params.get("name", "Histogram")

        # Use Bar trace with width from stat_bin
        plot = go.Bar

        color_targets = dict(
            color="marker_color",
        )

        self._transform_fig(
            plot,
            fig,
            data,
            payload,
            color_targets,
            row,
            col,
            barmode=self.barmode,
        )
