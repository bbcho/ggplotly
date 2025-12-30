# geoms/geom_waterfall.py

import plotly.graph_objects as go

from .geom_base import Geom


class geom_waterfall(Geom):
    """
    Geom for creating waterfall charts.

    Waterfall charts show how an initial value is affected by a series of
    positive or negative values, culminating in a final value. They are
    commonly used to visualize financial statements, budget changes, or
    any cumulative effect analysis.

    Parameters
    ----------
    data : DataFrame, optional
        Data for the geom (overrides plot data).
    mapping : aes, optional
        Aesthetic mappings. Required: x, y.
        Optional: measure (to specify 'relative', 'total', or 'absolute').
    increasing_color : str, default='#2ca02c'
        Color for increasing (positive) values.
    decreasing_color : str, default='#d62728'
        Color for decreasing (negative) values.
    total_color : str, default='#1f77b4'
        Color for total/absolute values.
    connector_color : str, default='rgba(128, 128, 128, 0.5)'
        Color for connector lines between bars.
    connector_width : float, default=1
        Width of connector lines.
    connector_visible : bool, default=True
        Whether to show connector lines.
    text_position : str, default='outside'
        Position of value labels: 'inside', 'outside', 'auto', 'none'.
    text_format : str, optional
        Format string for text labels (e.g., '.2f', ',.0f').
    orientation : str, default='v'
        Orientation: 'v' (vertical) or 'h' (horizontal).
    name : str, default='Waterfall'
        Name for legend.

    Aesthetics
    ----------
    x : str (required)
        Column containing category labels.
    y : str (required)
        Column containing values.
    measure : str, optional
        Column specifying the measure type for each bar:
        - 'relative': Value is added to running total (default behavior)
        - 'total': Bar shows running total up to this point
        - 'absolute': Bar shows absolute value (resets running total)

    Examples
    --------
    >>> import pandas as pd
    >>> from ggplotly import ggplot, aes, geom_waterfall
    >>>
    >>> # Basic waterfall chart
    >>> df = pd.DataFrame({
    ...     'category': ['Start', 'Sales', 'Returns', 'Expenses', 'End'],
    ...     'value': [100, 50, -20, -30, 0],
    ...     'measure': ['absolute', 'relative', 'relative', 'relative', 'total']
    ... })
    >>> (ggplot(df, aes(x='category', y='value', measure='measure'))
    ...  + geom_waterfall())
    >>>
    >>> # Simple waterfall (auto-detect totals by value=0 at start/end)
    >>> df = pd.DataFrame({
    ...     'category': ['Q1', 'Q2', 'Q3', 'Q4'],
    ...     'value': [100, 50, -30, 20]
    ... })
    >>> (ggplot(df, aes(x='category', y='value'))
    ...  + geom_waterfall())
    >>>
    >>> # Financial statement waterfall
    >>> df = pd.DataFrame({
    ...     'item': ['Revenue', 'COGS', 'Gross Profit', 'OpEx', 'Net Income'],
    ...     'amount': [1000, -400, 0, -200, 0],
    ...     'type': ['absolute', 'relative', 'total', 'relative', 'total']
    ... })
    >>> (ggplot(df, aes(x='item', y='amount', measure='type'))
    ...  + geom_waterfall())

    Notes
    -----
    If no 'measure' aesthetic is provided, all values are treated as relative
    changes from the previous value. Use the measure aesthetic to explicitly
    mark starting values ('absolute') and subtotals ('total').
    """

    required_aes = ['x', 'y']

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        # Set default colors
        if 'increasing_color' not in self.params:
            self.params['increasing_color'] = '#2ca02c'  # Green
        if 'decreasing_color' not in self.params:
            self.params['decreasing_color'] = '#d62728'  # Red
        if 'total_color' not in self.params:
            self.params['total_color'] = '#1f77b4'  # Blue

    def _draw_impl(self, fig, data, row, col):
        """
        Draw waterfall chart on the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        data : DataFrame
            Data for the waterfall chart.
        row : int
            Row position in subplot.
        col : int
            Column position in subplot.
        """
        # Validate required aesthetics
        required = ['x', 'y']
        missing = [aes for aes in required if aes not in self.mapping]
        if missing:
            raise ValueError(
                f"geom_waterfall requires aesthetics: {', '.join(required)}. "
                f"Missing: {', '.join(missing)}"
            )

        # Get column names from mapping
        x_col = self.mapping['x']
        y_col = self.mapping['y']
        measure_col = self.mapping.get('measure')

        # Validate columns exist
        if x_col not in data.columns:
            raise ValueError(f"Column '{x_col}' for 'x' not found in data")
        if y_col not in data.columns:
            raise ValueError(f"Column '{y_col}' for 'y' not found in data")

        # Get parameters
        increasing_color = self.params.get('increasing_color', '#2ca02c')
        decreasing_color = self.params.get('decreasing_color', '#d62728')
        total_color = self.params.get('total_color', '#1f77b4')
        connector_color = self.params.get('connector_color', 'rgba(128, 128, 128, 0.5)')
        connector_width = self.params.get('connector_width', 1)
        connector_visible = self.params.get('connector_visible', True)
        text_position = self.params.get('text_position', 'outside')
        text_format = self.params.get('text_format', None)
        orientation = self.params.get('orientation', 'v')
        name = self.params.get('name', 'Waterfall')

        # Extract data
        x_values = data[x_col].tolist()
        y_values = data[y_col].tolist()

        # Determine measure types
        if measure_col and measure_col in data.columns:
            measures = data[measure_col].tolist()
        else:
            # Default: all relative
            measures = ['relative'] * len(y_values)

        # Create text labels
        if text_position != 'none':
            if text_format:
                text_values = [format(v, text_format) for v in y_values]
            else:
                text_values = [str(v) for v in y_values]
        else:
            text_values = None

        # Create Waterfall trace
        trace = go.Waterfall(
            x=x_values,
            y=y_values,
            measure=measures,
            orientation=orientation,
            name=name,
            connector=dict(
                line=dict(
                    color=connector_color,
                    width=connector_width,
                ),
                visible=connector_visible,
            ),
            increasing=dict(marker=dict(color=increasing_color)),
            decreasing=dict(marker=dict(color=decreasing_color)),
            totals=dict(marker=dict(color=total_color)),
            textposition=text_position if text_position != 'none' else None,
            text=text_values,
        )

        fig.add_trace(trace, row=row, col=col)

        # Update layout for better display
        if orientation == 'v':
            fig.update_yaxes(rangemode='tozero', row=row, col=col)
        else:
            fig.update_xaxes(rangemode='tozero', row=row, col=col)
