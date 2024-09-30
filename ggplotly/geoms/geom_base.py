# geoms/geom_base.py


class Geom:
    """
    Base class for all geoms.
    """

    def __init__(self, mapping=None, **params):
        self.mapping = mapping.mapping if mapping else {}
        self.params = params
        self.data = None  # Will be set during setup_data

    def setup_data(self, data, plot_mapping):
        """
        Combine plot mapping with geom-specific mapping and set data.

        Parameters:
            data (DataFrame): The dataset to use.
            plot_mapping (dict): The global aesthetic mappings from the plot.
        """
        # Merge plot mapping and geom mapping, with geom mapping taking precedence
        combined_mapping = {**plot_mapping, **self.mapping}
        self.mapping = combined_mapping
        self.data = data

    def draw(self, fig, data=None, row=1, col=1):
        """
        Draw the geometry on the figure.

        Parameters:
            fig (Figure): Plotly figure object.
            data (DataFrame): Optional data subset for faceting.
            row (int): Row position in subplot (for faceting).
            col (int): Column position in subplot (for faceting).
        """
        raise NotImplementedError("The draw method must be implemented by subclasses.")
