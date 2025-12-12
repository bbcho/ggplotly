"""Identity stat - passes data through unchanged."""

from .stat_base import Stat


class stat_identity(Stat):
    """
    Identity statistical transformation (no transformation).

    This stat passes data through unchanged. It's the default stat for most
    geoms when you want to display raw data values without any aggregation
    or transformation.

    Parameters:
        data (DataFrame, optional): Data to use for this stat.
        mapping (dict, optional): Aesthetic mappings.
        **params: Additional parameters for the stat.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point(stat='identity')
    """

    __name__ = "identity"

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the stat_identity.

        Parameters:
            data (DataFrame, optional): Data to use for this stat.
            mapping (dict, optional): Aesthetic mappings.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)

    def compute(self, data):
        """
        Return the data unchanged.

        Parameters:
            data (DataFrame): The input data.

        Returns:
            tuple: (unchanged data, unchanged mapping)
        """
        return data, self.mapping
