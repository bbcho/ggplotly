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

    required_aes = ['x']  # y is computed by stat_bin

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
        # Store original x column name (mapping may have been modified by previous facet panel)
        if not hasattr(self, '_original_x_col'):
            self._original_x_col = self.mapping.get("x")
        x_col = self._original_x_col

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
            # Grouped histogram: compute bins using SAME edges for all groups
            # First, compute bin edges from ALL data so groups align for stacking
            import numpy as np
            all_x = data[x_col].dropna().values
            x_min, x_max = np.nanmin(all_x), np.nanmax(all_x)
            x_range = x_max - x_min

            # Determine bin width
            if self.binwidth is not None:
                width = self.binwidth
            else:
                width = x_range / self.bins

            # Compute shared bin edges
            if self.boundary is not None:
                shift = (x_min - self.boundary) % width
                bin_min = x_min - shift
            elif self.center is not None:
                shift = (x_min - self.center + width / 2) % width
                bin_min = x_min - shift
            else:
                bin_min = x_min

            n_bins = int(np.ceil((x_max - bin_min) / width)) + 1
            shared_breaks = bin_min + np.arange(n_bins + 1) * width

            # Now compute bins for each group using the shared breaks
            binned_frames = []
            for group_value in data[group_col].unique():
                group_data = data[data[group_col] == group_value].copy()
                # Create a new stat_bin with the shared breaks
                group_bin_stat = stat_bin(
                    mapping={'x': x_col},
                    breaks=shared_breaks,
                    na_rm=na_rm
                )
                binned_data = group_bin_stat.compute(group_data)
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
        # Get style properties for color mapping
        style_props = self._get_style_props(data)
        alpha = style_props['alpha']

        # Determine grouping column from fill, color, or group mapping
        group_col = None
        for aesthetic in ['fill', 'color', 'group']:
            if aesthetic in self.mapping:
                potential_col = self.mapping[aesthetic]
                if potential_col in data.columns:
                    group_col = potential_col
                    break

        # Get x and y column names from mapping
        x_col = self.mapping.get("x", "x")
        y_col = self.mapping.get("y", "count")

        # Initialize legend tracking on figure if not present
        if not hasattr(fig, '_ggplotly_shown_legendgroups'):
            fig._ggplotly_shown_legendgroups = set()

        if group_col is not None:
            # Grouped histogram - one trace per group with proper width
            cat_map = style_props.get('color_map') or style_props.get('fill_map', {})
            if not cat_map:
                # Build a color map from unique values
                import plotly.express as px
                unique_vals = data[group_col].unique()
                colors = px.colors.qualitative.Plotly
                cat_map = {val: colors[i % len(colors)] for i, val in enumerate(unique_vals)}

            for cat_value in cat_map.keys():
                cat_mask = data[group_col] == cat_value
                if not cat_mask.any():
                    continue

                subset = data[cat_mask]
                legend_name = str(cat_value)

                # Check if we should show this legend entry
                show_legend = legend_name not in fig._ggplotly_shown_legendgroups
                if show_legend:
                    fig._ggplotly_shown_legendgroups.add(legend_name)

                fig.add_trace(
                    go.Bar(
                        x=subset[x_col],
                        y=subset[y_col],
                        width=subset['width'] if 'width' in subset.columns else None,
                        marker_color=cat_map.get(cat_value, style_props['default_color']),
                        opacity=alpha,
                        name=legend_name,
                        showlegend=show_legend,
                        legendgroup=legend_name,
                    ),
                    row=row,
                    col=col,
                )
        else:
            # Single histogram - one trace
            color = style_props.get('color') or style_props.get('fill') or style_props['default_color']
            fig.add_trace(
                go.Bar(
                    x=data[x_col],
                    y=data[y_col],
                    width=data['width'] if 'width' in data.columns else None,
                    marker_color=color,
                    opacity=alpha,
                    name=self.params.get("name", "Histogram"),
                    showlegend=self.params.get("showlegend", True),
                ),
                row=row,
                col=col,
            )

        fig.update_yaxes(rangemode="tozero")
        fig.update_layout(barmode=self.barmode)
