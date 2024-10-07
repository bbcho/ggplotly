from .stat_base import Stat
from ..geoms.geom_base import Geom


class stat_count(Stat):
    def __init__(self, data=None, mapping=None, **params):
        self.data = data
        self.mapping = mapping
        self.params = params
        self.aggregator = "count"

    # def __add__(self, other):
    #     print("Adding stat to geom")

    #     if isinstance(other, Geom):
    #         print("Adding stat to geom")
    #         other.add_stat(self)
    #         return other

    def compute(self, data):
        stat = self.aggregator

        grouping = list(set([v for k, v in self.mapping.items()]))
        grouping = [g for g in grouping if g in data.columns]

        if len(data.columns) == 1:
            tf = data.value_counts()
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

        self.data = tf
