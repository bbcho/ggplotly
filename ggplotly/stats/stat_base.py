import copy


class Stat:
    """
    Base class for stats in ggplotly.
    """

    def __init__(self, data=None, mapping=None, **params):
        self.data = data
        self.mapping = mapping if mapping else {}
        self.params = params if params else {}

    def copy(self):
        return copy.deepcopy(self)

    def __radd__(self, other):
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
