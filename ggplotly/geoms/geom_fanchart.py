# geoms/geom_fanchart.py

import plotly.graph_objects as go

from ..stats.stat_fanchart import stat_fanchart
from .geom_base import Geom


class geom_fanchart(Geom):
    """
    Geom for displaying fan charts (percentile bands) from T×N matrices.

    Computes percentiles across columns at each time point and displays
    as nested transparent ribbons with an optional median line.

    Uses stat_fanchart internally for percentile computation.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. If x not specified, uses DataFrame index.
    columns : list, optional
        Specific columns to include in percentile calculation.
        Default is all numeric columns.
    percentiles : list, optional
        Percentile levels to display. Default is [10, 25, 50, 75, 90].
    color : str, optional
        Base color for the bands. Default is 'steelblue'.
    alpha : float, optional
        Base transparency for outermost band. Inner bands are more opaque.
        Default is 0.2.
    show_median : bool, optional
        Whether to show the median line. Default is True.
    median_color : str, optional
        Color for median line. Default is same as color.
    median_width : float, optional
        Width of median line. Default is 2.

    Examples
    --------
    >>> # Basic fan chart
    >>> ggplot(df) + geom_fanchart()

    >>> # Custom percentiles
    >>> ggplot(df) + geom_fanchart(percentiles=[5, 25, 50, 75, 95])

    >>> # Styled fan chart
    >>> ggplot(df) + geom_fanchart(color='coral', alpha=0.3)
    """

    required_aes = []  # Flexible - uses columns from DataFrame, x is optional

    default_params = {
        "percentiles": [10, 25, 50, 75, 90],
        "color": "steelblue",
        "alpha": 0.2,
        "show_median": True,
        "median_width": 2,
    }

    def _color_to_rgba(self, color, alpha):
        """Convert color to rgba string."""
        color_map = {
            'steelblue': (70, 130, 180),
            'coral': (255, 127, 80),
            'red': (255, 0, 0),
            'blue': (0, 0, 255),
            'green': (0, 128, 0),
            'orange': (255, 165, 0),
            'purple': (128, 0, 128),
            'pink': (255, 192, 203),
            'gray': (128, 128, 128),
            'grey': (128, 128, 128),
            'black': (0, 0, 0),
            'white': (255, 255, 255),
            'cyan': (0, 255, 255),
            'magenta': (255, 0, 255),
            'yellow': (255, 255, 0),
            'navy': (0, 0, 128),
            'teal': (0, 128, 128),
            'maroon': (128, 0, 0),
            'olive': (128, 128, 0),
            'lime': (0, 255, 0),
            'aqua': (0, 255, 255),
            'silver': (192, 192, 192),
            'fuchsia': (255, 0, 255),
        }

        if color.startswith('#'):
            hex_color = color.lstrip('#')
            if len(hex_color) == 3:
                hex_color = ''.join([c * 2 for c in hex_color])
            rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
        elif color.startswith('rgb'):
            import re
            values = re.findall(r'[\d.]+', color)
            rgb = (int(float(values[0])), int(float(values[1])), int(float(values[2])))
        elif color.lower() in color_map:
            rgb = color_map[color.lower()]
        else:
            rgb = (70, 130, 180)  # Default steelblue

        return f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})'

    def _draw_impl(self, fig, data, row, col):
        # Get parameters
        percentiles = self.params.get("percentiles", [10, 25, 50, 75, 90])
        columns = self.params.get("columns")
        base_color = self.params.get("color", "steelblue")
        base_alpha = self.params.get("alpha", 0.2)
        show_median = self.params.get("show_median", True)
        median_width = self.params.get("median_width", 2)

        # Use stat_fanchart for computation
        stat = stat_fanchart(
            mapping=self.mapping,
            columns=columns,
            percentiles=percentiles,
        )
        pct_data, _ = stat.compute(data)

        if pct_data.empty or 'x' not in pct_data.columns:
            return

        x_values = pct_data['x'].values

        # Sort percentiles to pair outer bands
        sorted_pcts = sorted(percentiles)
        median_pct = 50 if 50 in sorted_pcts else sorted_pcts[len(sorted_pcts) // 2]

        # Create bands from outer to inner
        lower_pcts = [p for p in sorted_pcts if p < median_pct]
        upper_pcts = [p for p in sorted_pcts if p > median_pct]
        bands = list(zip(lower_pcts, list(reversed(upper_pcts))))
        n_bands = len(bands)

        # Draw bands from outer to inner
        for i, (lower, upper) in enumerate(bands):
            if n_bands > 1:
                band_alpha = base_alpha + (base_alpha * 1.5 * i / (n_bands - 1))
            else:
                band_alpha = base_alpha
            band_alpha = min(band_alpha, 0.8)

            fillcolor = self._color_to_rgba(base_color, band_alpha)

            # Lower bound trace
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=pct_data[f'p{lower}'].values,
                    mode='lines',
                    line=dict(width=0),
                    showlegend=False,
                    hoverinfo='skip',
                    legendgroup='fanchart',
                ),
                row=row, col=col,
            )

            # Upper bound trace with fill
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=pct_data[f'p{upper}'].values,
                    mode='lines',
                    line=dict(width=0),
                    fill='tonexty',
                    fillcolor=fillcolor,
                    name=f'{lower}th-{upper}th' if i == 0 else None,
                    showlegend=(i == 0),
                    legendgroup='fanchart',
                    hovertemplate=f'{lower}th-{upper}th percentile<extra></extra>',
                ),
                row=row, col=col,
            )

        # Draw median line
        if show_median and f'p{median_pct}' in pct_data.columns:
            median_color = self.params.get("median_color", base_color)
            fig.add_trace(
                go.Scatter(
                    x=x_values,
                    y=pct_data[f'p{median_pct}'].values,
                    mode='lines',
                    line=dict(color=median_color, width=median_width),
                    name='Median',
                    showlegend=True,
                    legendgroup='fanchart_median',
                    hovertemplate='Median: %{y:.2f}<extra></extra>',
                ),
                row=row, col=col,
            )
