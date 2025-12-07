# geoms/geom_smooth.py

import plotly.graph_objects as go
import plotly.express as px
from ..stats.stat_smooth import stat_smooth
import numpy as np
from .geom_base import Geom
import pandas as pd


class geom_smooth(Geom):
    """
    Geom for drawing smooth lines (regression/LOESS/etc.).

    Automatically handles categorical variables for color.
    Automatically converts 'group' and 'color' columns to categorical if necessary.

    Parameters:
        method (str, optional): The smoothing method. Options:
                                - 'loess': Custom LOESS with degree-2 polynomials (default, best for R compatibility)
                                - 'lowess': statsmodels lowess with degree-1 (faster)
                                - 'lm': Linear regression
        span (float, optional): The smoothing span for LOESS. Controls the amount of smoothing.
                                Larger values (closer to 1) produce smoother lines. Default is 2/3 (~0.667) to match R.
        se (bool, optional): Whether to display confidence interval ribbon. Default is True to match R.
        level (float, optional): Confidence level for the interval (e.g., 0.95 for 95% CI). Default is 0.95 to match R.
        color (str, optional): Color of the smooth lines. If a categorical variable is mapped to color, different colors will be assigned.
        linetype (str, optional): Line type ('solid', 'dash', etc.). Default is 'solid'.
        alpha (float, optional): Transparency level for the smooth lines. Default is 1.
        group (str, optional): Grouping variable for the smooth lines.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + geom_smooth()
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + geom_smooth(method='lm', se=False)
    """

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw smooth line(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        data = (
            data.copy() if data is not None else self.data.copy()
        )  # Ensuring we are working on a copy

        # Set default line width to 3 for smooth lines if not specified
        if "size" not in self.params:
            self.params["size"] = 3

        # Remove size from mapping if present - smooth lines can't have variable widths
        # Only use size from params (literal values)
        if "size" in self.mapping:
            del self.mapping["size"]

        # Get smoothing parameters
        method = self.params.get("method", "loess")  # Default to 'loess'
        se = self.params.get("se", True)  # Default to True to match R
        level = self.params.get("level", 0.95)  # Default to 95% CI to match R
        span = self.params.get("span", 2/3)  # Default to 2/3 to match R's loess

        # Initialize stat_smooth for statistical smoothing
        smoother = stat_smooth(method=method, span=span, se=se, level=level)

        # Get the actual column names from the mapping
        x_col = self.mapping.get("x", "x")
        y_col = self.mapping.get("y", "y")

        # Handle grouping for confidence intervals
        # If data has groups or colors, compute smooth for each group separately
        from ..aesthetic_mapper import AestheticMapper
        mapper = AestheticMapper(data, self.mapping, self.params, self.theme)
        style_props = mapper.get_style_properties()

        group_col = None
        if style_props['group_series'] is not None:
            group_col = self.mapping.get('group')
        elif style_props['color_series'] is not None:
            group_col = self.mapping.get('color')

        if group_col and group_col in data.columns:
            # Process each group separately
            smoothed_parts = []
            for group_val in data[group_col].unique():
                group_data = data[data[group_col] == group_val].copy()
                group_smoothed = smoother.compute_stat(group_data, x_col=x_col, y_col=y_col)
                smoothed_parts.append(group_smoothed)
            data = pd.concat(smoothed_parts, ignore_index=True)

            # Draw ribbons for each group if se=True
            if se and 'ymin' in data.columns and 'ymax' in data.columns:
                for group_val in data[group_col].unique():
                    group_data = data[data[group_col] == group_val]
                    # Get the color for this group using unified color resolution
                    group_color = mapper.get_color_for_value(group_val, style_props, prefer_fill=False)
                    self._add_ribbon_trace(fig, group_data, x_col, row, col, showlegend=False,
                                         fillcolor=group_color, alpha=0.3)
        else:
            # No grouping - process all data at once
            data = smoother.compute_stat(data, x_col=x_col, y_col=y_col)

            # Draw single ribbon if se=True
            if se and 'ymin' in data.columns and 'ymax' in data.columns:
                # Use the same color as the line with reduced alpha
                ribbon_color = style_props.get('color') or style_props.get('fill') or style_props['default_color']
                self._add_ribbon_trace(fig, data, x_col, row, col, showlegend=False,
                                     fillcolor=ribbon_color, alpha=0.3)

        line_dash = self.params.get("linetype", "solid")
        name = self.params.get("name", "Smooth")

        plot = go.Scatter
        payload = dict(
            mode="lines",
            line_dash=line_dash,
            name=name,
        )

        color_targets = dict(
            color="line_color",
            size="line_width",
        )

        self._transform_fig(plot, fig, data, payload, color_targets, row, col)

    def _add_ribbon_trace(self, fig, data, x_col, row, col, showlegend=False,
                         fillcolor=None, alpha=0.3):
        """
        Add a single ribbon trace to the figure.

        Parameters:
            fig: Plotly figure object
            data: DataFrame with x, ymin, ymax columns
            x_col: Name of x column
            row: Subplot row
            col: Subplot column
            showlegend: Whether to show in legend
            fillcolor: Color for the ribbon fill (if None, uses gray)
            alpha: Alpha transparency for the ribbon (default 0.3)
        """
        x = data[x_col]
        ymin = data['ymin']
        ymax = data['ymax']

        # Create ribbon using filled area between ymin and ymax
        # Use x concatenated with reversed x, and y as ymin + reversed ymax
        x_ribbon = pd.concat([x, x[::-1]], ignore_index=True)
        y_ribbon = pd.concat([ymax, ymin[::-1]], ignore_index=True)

        # Convert color to RGBA if provided
        if fillcolor:
            from ..aesthetic_mapper import AestheticMapper
            # Create a temporary mapper just for color conversion
            temp_mapper = AestheticMapper(data, {}, {}, None)
            fillcolor_rgba = temp_mapper._color_to_rgba(fillcolor, alpha)
        else:
            fillcolor_rgba = f'rgba(128, 128, 128, {alpha})'  # Default gray

        fig.add_trace(
            go.Scatter(
                x=x_ribbon,
                y=y_ribbon,
                fill='toself',
                fillcolor=fillcolor_rgba,
                line=dict(color='rgba(255, 255, 255, 0)'),  # Invisible line
                showlegend=showlegend,
                hoverinfo='skip',
            ),
            row=row,
            col=col,
        )
