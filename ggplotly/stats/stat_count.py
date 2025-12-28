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

        # Get the actual column names mapped to x and y
        x_col = self.mapping.get('x')
        y_col = self.mapping.get('y')

        # Use value_counts when we only have one grouping column
        # OR when all data columns would be used for grouping (nothing left to count)
        non_grouping_cols = [c for c in data.columns if c not in grouping]

        if len(grouping) == 1 or len(non_grouping_cols) == 0:
            # Use value_counts - works when grouping by all columns
            tf = data[grouping].value_counts()
        else:
            # If both x and y columns are in the grouping, remove y
            # (y will become the count result)
            if x_col in grouping and y_col in grouping:
                grouping.remove(y_col)
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
