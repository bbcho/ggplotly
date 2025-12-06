"""Identity stat - passes data through unchanged."""


class stat_identity:
    """
    Identity statistical transformation (no transformation).

    This stat passes data through unchanged. It's the default stat for most
    geoms when you want to display raw data values without any aggregation
    or transformation.

    Examples:
        >>> ggplot(df, aes(x='x', y='y')) + geom_point(stat='identity')
    """

    def compute(self, data):
        """
        Return the data unchanged.

        Parameters:
            data (DataFrame): The input data.

        Returns:
            DataFrame: The unchanged data.
        """
        return data
