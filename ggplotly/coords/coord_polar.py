from .coord_base import Coord


class coord_polar(Coord):
    def apply(self, fig):
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True), angularaxis=dict(visible=True)),
            showlegend=False,
        )
        fig.update_traces(mode="lines")
