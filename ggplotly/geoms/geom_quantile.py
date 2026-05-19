# geoms/geom_quantile.py

from ..stats.stat_advanced import stat_quantile
from .geom_line import geom_line


class geom_quantile(geom_line):
    """Draw linear quantile regression lines."""

    def __init__(
        self,
        data=None,
        mapping=None,
        quantiles=(0.25, 0.5, 0.75),
        formula=None,
        method="rq",
        n=100,
        **params,
    ):
        super().__init__(data, mapping, **params)
        self.quantiles = quantiles
        self.formula = formula
        self.method = method
        self.n = n

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(
                stat_quantile(
                    mapping=self.mapping,
                    quantiles=self.quantiles,
                    formula=self.formula,
                    method=self.method,
                    n=self.n,
                    na_rm=self.params.get("na_rm", False),
                )
            )
        return super()._apply_stats(data)
