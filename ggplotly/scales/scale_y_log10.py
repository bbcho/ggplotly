from .scale_base import Scale


class scale_y_log10(Scale):
    def apply(self, fig):
        fig.update_yaxes(type="log")
