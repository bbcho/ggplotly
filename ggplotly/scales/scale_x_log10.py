from .scale_base import Scale


class scale_x_log10(Scale):
    def apply(self, fig):
        fig.update_xaxes(type="log")
