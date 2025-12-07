from .coord_base import Coord


class coord_flip(Coord):
    """
    Flip cartesian coordinates so x becomes y and y becomes x.

    This is useful for horizontal bar charts and other cases where
    you want to swap the axes.

    Parameters:
        xlim: Limits for the x-axis (after flipping, this controls the vertical axis).
        ylim: Limits for the y-axis (after flipping, this controls the horizontal axis).
        expand: If True (default), adds a small expansion factor to the limits.
        clip: Whether to clip points that fall outside the plotting area.
            "on" (default) clips to panel, "off" allows drawing outside.

    Examples:
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_flip()
        >>> ggplot(df, aes(x='category', y='value')) + geom_bar() + coord_flip(xlim=(0, 100))
    """

    def __init__(self, xlim=None, ylim=None, expand=True, clip="on"):
        """
        Initialize coord_flip.

        Parameters:
            xlim: Limits for the x-axis (after flipping).
            ylim: Limits for the y-axis (after flipping).
            expand: Whether to expand limits (default True).
            clip: Clipping mode ("on" or "off").
        """
        self.xlim = xlim
        self.ylim = ylim
        self.expand = expand
        self.clip = clip

    def apply(self, fig):
        """
        Apply coordinate flip to the figure by swapping x and y data.

        This swaps the x and y values in all traces, effectively rotating
        the plot 90 degrees. Also swaps axis titles and settings.

        Parameters:
            fig (Figure): The Plotly figure to modify.

        Returns:
            None: Modifies the figure in place.
        """
        # Swap x and y data in all traces
        for trace in fig.data:
            # Get current x and y values
            x_data = trace.x
            y_data = trace.y

            # Swap them
            trace.x = y_data
            trace.y = x_data

            # For bar traces, swap orientation
            if hasattr(trace, 'orientation'):
                if trace.orientation == 'v' or trace.orientation is None:
                    trace.orientation = 'h'
                elif trace.orientation == 'h':
                    trace.orientation = 'v'

            # Handle error bars if present - swap the error bar data
            # Note: error_x and error_y are different types in Plotly, so we need
            # to convert the properties rather than swapping the objects directly
            if hasattr(trace, 'error_x') and hasattr(trace, 'error_y'):
                error_x_dict = trace.error_x.to_plotly_json() if trace.error_x else {}
                error_y_dict = trace.error_y.to_plotly_json() if trace.error_y else {}
                # Only swap if there's actual error bar data
                if error_x_dict or error_y_dict:
                    # Convert error_x data to error_y format and vice versa
                    trace.error_x = error_y_dict if error_y_dict else None
                    trace.error_y = error_x_dict if error_x_dict else None

        # Swap axis titles
        layout = fig.layout
        xaxis_title = layout.xaxis.title.text if layout.xaxis.title else None
        yaxis_title = layout.yaxis.title.text if layout.yaxis.title else None

        if xaxis_title or yaxis_title:
            fig.update_layout(
                xaxis_title=yaxis_title,
                yaxis_title=xaxis_title
            )

        # Apply limits if specified (note: limits are applied after flipping)
        if self.xlim is not None:
            fig.update_xaxes(range=list(self.xlim))
        if self.ylim is not None:
            fig.update_yaxes(range=list(self.ylim))
