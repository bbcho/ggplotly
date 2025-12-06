from .stat_base import Stat


class stat_count(Stat):
    """
    Count the number of observations in each group.

    This stat is used internally by geom_bar when you want to display
    counts of categorical data.

    Parameters:
        data (DataFrame, optional): Data to use for this stat.
        mapping (dict, optional): Aesthetic mappings.
        **params: Additional parameters.

    Examples:
        >>> ggplot(df, aes(x='category')) + geom_bar(stat='count')
    """

    __name__ = "count"

    def __init__(self, data=None, mapping=None, **params):
        """
        Initialize the stat_count.

        Parameters:
            data (DataFrame, optional): Data to use for this stat.
            mapping (dict, optional): Aesthetic mappings.
            **params: Additional parameters.
        """
        super().__init__(data, mapping, **params)
        self.aggregator = "count"

    def compute(self, data):
        """
        Compute counts for each group in the data.

        Parameters:
            data (DataFrame): The input data.

        Returns:
            tuple: (transformed DataFrame, updated mapping dict)
        """

        data = data.copy()
        stat = self.aggregator

        grouping = list(set([v for k, v in self.mapping.items()]))
        grouping = [g for g in grouping if g in data.columns]
        grouping_keys = list(set([k for k, v in self.mapping.items()]))

        # if x XOR y in grouping
        # if ("x" in grouping_keys) ^ ("y" in grouping_keys):
        if len(data[grouping].columns) == 1:

            # if len(data.columns)  == 1:
            tf = data[grouping].value_counts()
        else:
            # if both x and y are in the grouping, remove y.
            # Assume that y is the metric we want to summarize
            if ("x" in grouping) & ("y" in grouping):
                grouping.remove("y")
                self.mapping.pop("y")

            tf = data.groupby(grouping).agg(stat).iloc[:, [0]]
            tf.columns = [stat]
            tf = tf.reset_index()

        tf = tf.reset_index()

        if ("x" in self.mapping) & ("y" not in self.mapping):
            dcol = "x"
            # x = list(tf[self.mapping[dcol]])
            # y = list(tf["count"])
            self.mapping["x"] = self.mapping[dcol]
            self.mapping["y"] = stat
        elif ("y" in self.mapping) & ("x" not in self.mapping):
            dcol = "y"
            # y = list(tf[self.mapping[dcol]])
            # x = list(tf["count"])
            self.mapping["y"] = self.mapping[dcol]
            self.mapping["x"] = stat

        return tf, self.mapping
