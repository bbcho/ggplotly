# geoms/geom_lines.py

import numpy as np
import plotly.graph_objects as go

from .geom_base import Geom


class geom_lines(Geom):
    """
    Geom for efficiently plotting many line series.

    Designed for T×N matrices where each column is a separate series.
    Uses a single Plotly trace with None separators for performance.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. If x not specified, uses DataFrame index.
    columns : list, optional
        Specific columns to plot. Default is all numeric columns.
    color : str, optional
        Line color. Default is theme color. Ignored if multicolor=True.
    alpha : float, optional
        Line transparency. Default is 0.5.
    size : float, optional
        Line width. Default is 1.
    showlegend : bool, optional
        Whether to show legend. Default is False.
    multicolor : bool, optional
        If True, each series gets a different color from the palette.
        Default is False.
    palette : str or list, optional
        Color palette to use when multicolor=True. Can be a Plotly
        colorscale name ('Viridis', 'Plasma', etc.) or a list of colors.
        Default is 'Plotly'.

    Examples
    --------
    >>> # Plot all columns (single color)
    >>> ggplot(df) + geom_lines()

    >>> # Multi-colored lines
    >>> ggplot(df) + geom_lines(multicolor=True)

    >>> # Multi-colored with custom palette
    >>> ggplot(df) + geom_lines(multicolor=True, palette='Viridis')
    """

    required_aes = []  # Flexible - uses columns from DataFrame, x is optional

    default_params = {"size": 1, "alpha": 0.5, "showlegend": False, "multicolor": False}

    def _get_color_palette(self, n_colors):
        """Get a list of colors for multicolor mode."""
        import plotly.express as px

        palette_name = self.params.get("palette", "Plotly")

        # If palette is already a list, use it directly
        if isinstance(palette_name, list):
            colors = palette_name
        # Check qualitative palettes first
        elif hasattr(px.colors.qualitative, palette_name):
            colors = getattr(px.colors.qualitative, palette_name)
        # Check sequential palettes (need to sample from continuous scale)
        elif hasattr(px.colors.sequential, palette_name):
            colorscale = getattr(px.colors.sequential, palette_name)
            colors = px.colors.sample_colorscale(colorscale, n_colors)
        # Default to Plotly palette
        else:
            colors = px.colors.qualitative.Plotly

        return colors

    def _draw_impl(self, fig, data, row, col):
        # Determine x values
        x_col = self.mapping.get("x") if self.mapping else None
        if x_col and x_col in data.columns:
            x_values = data[x_col].values
        else:
            x_values = data.index.values

        # Determine which columns to plot
        columns = self.params.get("columns")
        if columns is None:
            # All numeric columns except x
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            if x_col and x_col in numeric_cols:
                numeric_cols.remove(x_col)
            columns = numeric_cols

        # Filter to only existing columns
        columns = [c for c in columns if c in data.columns]

        alpha = self.params.get("alpha", 0.5)
        size = self.params.get("size", 1)
        showlegend = self.params.get("showlegend", False)
        multicolor = self.params.get("multicolor", False)

        if multicolor and columns:
            # Multicolor mode: one trace per series with different colors
            colors = self._get_color_palette(len(columns))

            for i, col_name in enumerate(columns):
                color = colors[i % len(colors)]
                fig.add_trace(
                    go.Scatter(
                        x=x_values,
                        y=data[col_name].values,
                        mode='lines',
                        line=dict(color=color, width=size),
                        opacity=alpha,
                        showlegend=showlegend,
                        name=str(col_name),
                        legendgroup=str(col_name),
                        hoverinfo='skip',
                    ),
                    row=row,
                    col=col,
                )
        else:
            # Single color mode: use None separators for performance
            color = self.params.get("color")
            if color is None and hasattr(self, 'theme') and self.theme:
                import plotly.express as px
                palette = getattr(self.theme, 'color_map', None) or px.colors.qualitative.Plotly
                color = palette[0]
            elif color is None:
                color = '#636EFA'  # Plotly default blue

            # Build single trace with None separators for performance
            all_x = []
            all_y = []

            for col_name in columns:
                all_x.extend(x_values.tolist())
                all_x.append(None)  # Separator
                all_y.extend(data[col_name].values.tolist())
                all_y.append(None)  # Separator

            # Single trace for all lines
            fig.add_trace(
                go.Scatter(
                    x=all_x,
                    y=all_y,
                    mode='lines',
                    line=dict(color=color, width=size),
                    opacity=alpha,
                    showlegend=showlegend,
                    name=self.params.get('name', 'Lines'),
                    hoverinfo='skip',
                ),
                row=row,
                col=col,
            )
