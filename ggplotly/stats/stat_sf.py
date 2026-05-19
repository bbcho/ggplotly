"""Simple-feature stat used by geom_sf-compatible layers."""

from .stat_base import Stat


class stat_sf(Stat):
    """Pass through simple-feature data unchanged."""

    __name__ = "sf"

    def __init__(
        self,
        data=None,
        mapping=None,
        geom="sf",
        position="identity",
        na_rm=False,
        show_legend=None,
        inherit_aes=True,
        **params,
    ):
        super().__init__(data, mapping, **params)
        self.geom = geom
        self.position = position
        self.na_rm = na_rm
        self.show_legend = show_legend
        self.inherit_aes = inherit_aes

    def compute(self, data):
        return data.copy(), self.mapping.copy()
