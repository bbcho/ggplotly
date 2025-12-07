# geoms/geom_histogram.py

from .geom_base import Geom
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


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

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw histogram(s) on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame, optional): Data subset for faceting.
            row (int): Row position in subplot. Default is 1.
            col (int): Column position in subplot. Default is 1.

        Returns:
            None: Modifies the figure in place.
        """
        payload = dict()
        data = data if data is not None else self.data

        plot = go.Histogram

        payload["name"] = self.params.get("name", "Histogram")

        # Handle bin specification: binwidth takes precedence over bins
        if self.binwidth is not None:
            # Use xbins with size for binwidth
            xbins_config = {"size": self.binwidth}
            if self.boundary is not None:
                xbins_config["start"] = self.boundary
            elif self.center is not None:
                # Adjust start to align with center
                xbins_config["start"] = self.center - self.binwidth / 2
            payload["xbins"] = xbins_config
        else:
            payload["nbinsx"] = self.bins

        color_targets = dict(
            # fill="marker_fill",
            # fill="fillcolor",
            color="marker_color",
            # size="line",
            # marker=dict(color=fill, size=size),
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
