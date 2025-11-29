class Utils:
    """
    Base class for utility functions that modify ggplot objects.

    Utilities are applied after the plot is constructed to modify its
    appearance or save it to a file.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point() + ggsize(800, 600)
    """

    def apply(self, plot):
        """
        Apply the utility to the plot.

        Parameters:
            plot (ggplot): The ggplot object to apply the utility to.

        Returns:
            None: Modifies the plot in place.
        """
        pass


class ggsize:
    """
    A class to set the size of a ggplot figure.

    Parameters:
        width (int): The width of the plot in pixels.
        height (int): The height of the plot in pixels.
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height

    def apply(self, plot):
        """
        Apply the size to the given plot by setting the width and height.
        """
        plot.fig.update_layout(width=self.width, height=self.height)


class ggsave(Utils):
    """
    A class to save ggplot figures as either HTML or PNG.

    Parameters:
        filename (str): The name of the file to save the figure (including extension).
        width (int, optional): The width of the image in pixels (for PNG). If None, the current figure width is used.
        height (int, optional): The height of the image in pixels (for PNG). If None, the current figure height is used.
        scale (float, optional): Scale the image by this factor (for PNG).
    """

    def __init__(self, filename, width=None, height=None, scale=1.0):
        self.filename = filename
        self.width = width
        self.height = height
        self.scale = scale

    def apply(self, plot):
        """
        Apply the save operation to the given plot.
        """
        # Ensure the plot has been drawn before saving
        # if plot.fig is None:
        plot.draw()

        # Get current width and height from the figure if not provided
        width = self.width if self.width is not None else plot.fig.layout.width
        height = self.height if self.height is not None else plot.fig.layout.height

        # Save based on file extension
        if self.filename.endswith(".html"):
            self.save_html(plot)
        elif self.filename.endswith(".png"):
            self.save_png(plot, width, height)
        else:
            raise ValueError("Unsupported file format. Use either .html or .png.")

    def save_html(self, plot):
        """
        Save the plot as an HTML file.
        """
        plot.fig.write_html(self.filename)
        print(f"Plot saved as HTML: {self.filename}")

    def save_png(self, plot, width, height):
        """
        Save the plot as a PNG file. Requires the `kaleido` package to be installed.
        """
        try:
            # Save as PNG using Plotly's to_image function, with optional custom width and height
            plot.fig.write_image(
                self.filename, width=width, height=height, scale=self.scale
            )
            print(f"Plot saved as PNG: {self.filename}")
        except ValueError as e:
            raise RuntimeError(
                "Failed to save PNG. Ensure that `kaleido` is installed for saving PNG images."
            ) from e
