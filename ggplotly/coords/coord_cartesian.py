# coords/coord_cartesian.py
from .coord_base import Coord


class coord_cartesian(Coord):
    def __init__(self, xlim=None, ylim=None):
        self.xlim = xlim
        self.ylim = ylim

    def apply(self, fig):
        if self.xlim:
            fig.update_xaxes(range=self.xlim)
        if self.ylim:
            fig.update_yaxes(range=self.ylim)
