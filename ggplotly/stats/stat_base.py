class Stat:
    """
    Base class for stats in ggplotly.
    """

    def __init__(self):
        pass

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
