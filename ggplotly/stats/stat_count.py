from .stat_base import Stat


class stat_count(Stat):
    __name__ = "count"

    def __init__(self, data=None, mapping=None, **params):
        super().__init__(data, mapping, **params)
        # self.data = data
        # self.mapping = mapping if mapping else {}
        # self.params = params if params else {}
        self.aggregator = "count"

    def compute(self, data):

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
