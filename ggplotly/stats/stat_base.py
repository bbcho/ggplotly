import copy


def coerce_stat_result(result):
    """
    Normalize stat outputs to the internal (data, mapping_updates) contract.

    Older direct stat consumers returned bare data. Keep that public behavior
    usable while giving render paths one explicit boundary.
    """
    if isinstance(result, tuple) and len(result) == 2:
        data, mapping = result
        return data, mapping or {}
    return result, {}


class Stat:
    """
    Base class for statistical transformations in ggplotly.

    Stats transform data before it is rendered by a geom. For example,
    stat_count counts the number of observations in each group.

    Subclasses must implement the `compute()` method which transforms data
    and returns a tuple of (transformed_data, mapping_updates).

    Return Type Contract:
        The compute() method MUST return a tuple of:
        - data (DataFrame): The transformed data
        - mapping (dict): Updated aesthetic mappings (e.g., {'y': 'count'})

        Example implementation:
            def compute(self, data):
                # Transform data
                result = data.groupby('x').size().reset_index(name='count')
                # Return data and any mapping updates
                return result, {'y': 'count'}

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
        new_stat = self.copy()
        new_stat.mapping = {**new_stat.mapping, **other.mapping}
        new_stat.params = {**new_stat.params, **other.params}
        new_stat.data = other.data.copy() if other.data is not None else None
        new = other.copy()
        new.stats = [*new.stats, new_stat]
        return new

    def compute(self, data):
        """
        Compute the statistical transformation on the data.

        This method must be implemented by all stat subclasses.

        Parameters:
            data (DataFrame): The input data to transform.

        Returns:
            tuple: A tuple of (transformed_data, mapping_updates) where:
                - transformed_data (DataFrame): The transformed data
                - mapping_updates (dict): Dictionary of aesthetic mapping updates
                  (e.g., {'y': 'count'} to update the y aesthetic)

        Raises:
            NotImplementedError: If not implemented by subclass.

        Example:
            >>> class stat_example(Stat):
            ...     def compute(self, data):
            ...         result = data.groupby('x').mean().reset_index()
            ...         return result, {'y': 'mean_value'}
        """
        raise NotImplementedError(
            "compute() method must be implemented in subclasses."
        )
