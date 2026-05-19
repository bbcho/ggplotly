# geoms/geom_function.py

from ..stats.stat_function import stat_function
from .geom_line import geom_line


class geom_function(geom_line):
    """Draw a function as a line over the plot x-domain."""

    def __init__(self, data=None, mapping=None, fun=None, xlim=None, n=101, args=None, **params):
        super().__init__(data, mapping, **params)
        self.fun = fun
        self.xlim = xlim
        self.n = n
        self.args = args

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(
                stat_function(
                    mapping=self.mapping,
                    fun=self.fun,
                    xlim=self.xlim,
                    n=self.n,
                    args=self.args,
                )
            )
        return super()._apply_stats(data)
