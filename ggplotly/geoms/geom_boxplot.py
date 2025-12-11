# geoms/geom_boxplot.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


class geom_boxplot(Geom):
    """Geom for drawing boxplots."""

    def __init__(self, data=None, mapping=None, outlier_colour=None, outlier_color=None,
                 outlier_fill=None, outlier_shape='circle', outlier_size=1.5,
                 outlier_stroke=0.5, outlier_alpha=None, notch=False, varwidth=False,
                 coef=1.5, width=0.75, **params):
        """
        Create a boxplot geom.

        Automatically handles categorical variables for color and fill.
        Automatically converts 'group' and 'fill' columns to categorical if necessary.

        Parameters
        ----------
        data : DataFrame, optional
            Data for this geom.
        mapping : aes, optional
            Aesthetic mappings.
        outlier_colour : str, optional
            Color of outlier points. Default is 'black'. Alias: outlier_color.
        outlier_color : str, optional
            Alias for outlier_colour.
        outlier_fill : str, optional
            Fill color of outlier points. Default is None (same as outlier_colour).
        outlier_shape : str or int, default='circle'
            Shape of outlier points. Plotly marker symbols: 'circle', 'square',
            'diamond', 'cross', etc.
        outlier_size : float, default=1.5
            Size of outlier points.
        outlier_stroke : float, default=0.5
            Stroke width of outlier points.
        outlier_alpha : float, optional
            Alpha transparency of outlier points. Default is None (use main alpha).
        notch : bool, default=False
            If True, draw a notched boxplot. Notches display confidence interval
            around median.
        varwidth : bool, default=False
            If True, vary box width by group size. Note: Limited support in Plotly.
        coef : float, default=1.5
            Length of whiskers as multiple of IQR. Points beyond whiskers are
            plotted as outliers.
        width : float, default=0.75
            Box width.
        **params
            Additional parameters passed to the geom.

        Examples
        --------
        >>> from ggplotly import ggplot, aes, geom_boxplot, data
        >>> mpg = data('mpg')

        >>> # Basic boxplot by vehicle class
        >>> ggplot(mpg, aes(x='class', y='hwy')) + geom_boxplot()

        >>> # Boxplot with fill color by drive type
        >>> ggplot(mpg, aes(x='class', y='hwy', fill='drv')) + geom_boxplot()

        >>> # Notched boxplot showing confidence interval
        >>> ggplot(mpg, aes(x='class', y='hwy')) + geom_boxplot(notch=True)

        >>> # Custom outlier styling
        >>> ggplot(mpg, aes(x='class', y='hwy')) + geom_boxplot(outlier_colour='red', outlier_size=3)
        """
        super().__init__(data, mapping, **params)
        # Support both British and American spelling
        self.outlier_colour = outlier_colour or outlier_color or 'black'
        self.outlier_fill = outlier_fill
        self.outlier_shape = outlier_shape
        self.outlier_size = outlier_size
        self.outlier_stroke = outlier_stroke
        self.outlier_alpha = outlier_alpha
        self.notch = notch
        self.varwidth = varwidth
        self.coef = coef
        self.width = width

    def _shape_to_plotly_symbol(self, shape):
        """Convert ggplot2 shape to Plotly marker symbol."""
        # Map common ggplot2 shapes to Plotly symbols
        shape_map = {
            'circle': 'circle',
            'square': 'square',
            'diamond': 'diamond',
            'triangle': 'triangle-up',
            'cross': 'cross',
            'plus': 'cross',
            'asterisk': 'asterisk',
            'point': 'circle',
            # Numeric shapes from R (0-25)
            0: 'square-open',
            1: 'circle-open',
            2: 'triangle-up-open',
            3: 'cross',
            4: 'x',
            5: 'diamond-open',
            15: 'square',
            16: 'circle',
            17: 'triangle-up',
            18: 'diamond',
            19: 'circle',
        }
        return shape_map.get(shape, 'circle')

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw boxplot(s) on the figure.

        Parameters
        ----------
        fig : Figure
            Plotly figure object.
        data : DataFrame, optional
            Data subset for faceting.
        row : int, default=1
            Row position in subplot.
        col : int, default=1
            Column position in subplot.
        """
        data = data if data is not None else self.data

        plot = go.Box

        payload = dict(
            name=self.params.get("name", "Boxplot"),
            boxpoints='outliers',  # Show outliers
            width=self.width,
        )

        # Configure outlier marker
        outlier_marker = dict(
            color=self.outlier_colour,
            size=self.outlier_size,
            symbol=self._shape_to_plotly_symbol(self.outlier_shape),
            line=dict(width=self.outlier_stroke),
        )
        if self.outlier_fill:
            outlier_marker['color'] = self.outlier_fill
        if self.outlier_alpha is not None:
            outlier_marker['opacity'] = self.outlier_alpha

        payload['marker'] = outlier_marker

        # Configure notch
        if self.notch:
            payload['notched'] = True

        # Configure whisker length (coef * IQR)
        # Plotly doesn't have direct coef parameter, but we can approximate
        # by not using suspectedoutliers when coef != 1.5
        if self.coef != 1.5:
            # Plotly's default is 1.5 IQR, which matches ggplot2 default
            # For other values, we'd need custom calculation
            pass  # Note: Plotly doesn't support custom coef directly

        color_targets = dict(
            fill="fillcolor",
            color="line_color",
        )
        self._transform_fig(plot, fig, data, payload, color_targets, row, col)
