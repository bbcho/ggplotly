import copy


class Stat:
    """
    Base class for statistical transformations in ggplotly.

    Stats transform data before it is rendered by a geom. For example,
    stat_count counts the number of observations in each group.

    Parameters:
        data (DataFrame, optional): Data to use for this stat.
        mapping (dict, optional): Aesthetic mappings.
        **params: Additional parameters for the stat.

    Examples:
        >>> ggplot(df, aes(x='category')) + geom_bar() + stat_count()
    """

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the stat.

        Parameters:
            data (DataFrame, optional): Data to use for this stat.
            mapping (dict, optional): Aesthetic mappings.
            **params: Additional parameters for the stat.
        """
        self.data = data
        self.mapping = mapping if mapping else {}
        self.params = params if params else {}

    def copy(self):
        """
        Create a deep copy of this stat.

        Returns:
            Stat: A new stat instance with copied data.
        """
        return copy.deepcopy(self)

    def __radd__(self, other):
        """
        Right-add operator to combine stat with a geom.

        Parameters:
            other (Geom): The geom to combine with.

        Returns:
            Geom: A new geom with this stat applied.
        """
        # if isinstance(other, Geom):
        # other.add_stat(self)
        self.mapping = {**self.mapping, **other.mapping}
        self.params = {**self.params, **other.params}
        self.data = other.data.copy()

        new = other.copy()
        new.stats = [*other.stats.copy()]
        new.stats.append(self.copy())
        return new

    def compute(self, data):
        """
        Computes the stat, modifying the data as needed.

        Parameters:
            data (DataFrame): The input data.

        Returns:
            DataFrame: Modified data.
        """
        raise NotImplementedError(
            "compute_stat method must be implemented in subclasses."
        )
