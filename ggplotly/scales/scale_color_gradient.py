from .scale_base import Scale


class scale_color_gradient(Scale):
    def __init__(self, low="blue", high="red"):
        self.low = low
        self.high = high

    def apply(self, fig):
        for trace in fig.data:
            if "marker" in trace:
                trace.marker.colorscale = [[0, self.low], [1, self.high]]
