from .coord_base import Coord


class coord_flip(Coord):
    def apply(self, fig):
        fig.update_layout(xaxis=dict(autorange="reversed"))
