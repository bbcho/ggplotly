"""Additional scale helpers for ggplot2-style API coverage."""

from __future__ import annotations

import math

import numpy as np
import plotly.express as px

from .scale_base import Scale
from .scale_x_continuous import scale_x_continuous
from .scale_y_continuous import scale_y_continuous


VIRIDIS = px.colors.sequential.Viridis
LINETYPES = ("solid", "dash", "dot", "dashdot", "longdash", "longdashdot")


class _NewScale(Scale):
    _ggplotly_new_scale = True

    def __init__(self, aesthetic):
        self.aesthetic = aesthetic

    def apply(self, fig):
        return None


def new_scale_color():
    """Start a new color scale for subsequent layers."""
    return _NewScale("color")


def new_scale_fill():
    """Start a new fill scale for subsequent layers."""
    return _NewScale("fill")


def new_scale_colour():
    """British spelling alias for new_scale_color."""
    return new_scale_color()


class sec_axis:
    """Secondary axis specification used by continuous position scales."""

    def __init__(self, trans=None, name=None, breaks=None, labels=None):
        self.trans = trans
        self.name = name
        self.breaks = breaks
        self.labels = labels

    def axis_update(self):
        update = {"overlaying": "y", "side": "right"}
        if self.name is not None:
            update["title_text"] = self.name
        if self.breaks is not None:
            update["tickmode"] = "array"
            update["tickvals"] = self.breaks
            if self.labels is not None:
                update["ticktext"] = self.labels(self.breaks) if callable(self.labels) else self.labels
        return update


def dup_axis(name=None, breaks=None, labels=None):
    return sec_axis(name=name, breaks=breaks, labels=labels)


def scale_x_sqrt(**kwargs):
    return scale_x_continuous(trans="sqrt", **kwargs)


def scale_y_sqrt(**kwargs):
    return scale_y_continuous(trans="sqrt", **kwargs)


class _TraceNamePaletteScale(Scale):
    aesthetic = None

    def __init__(self, values=None, name=None, breaks=None, labels=None, guide="legend", na_value=None):
        self.values = values
        self.name = name
        self.breaks = breaks
        self.labels = labels
        self.guide = guide
        self.na_value = na_value

    def _trace_names(self, fig):
        names = []
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            name = getattr(trace, "name", None)
            if name and name not in names:
                names.append(name)
        return names

    def _value_map(self, fig):
        if isinstance(self.values, dict):
            return self.values
        names = self._trace_names(fig)
        values = [] if self.values is None else list(self.values)
        return {name: values[i % len(values)] for i, name in enumerate(names)} if values else {}

    def _rename_breaks(self, fig):
        if self.breaks is None or self.labels is None:
            return
        labels = self.labels(self.breaks) if callable(self.labels) else self.labels
        label_map = dict(zip(self.breaks, labels))
        for trace in fig.data:
            if getattr(trace, "name", None) in label_map:
                trace.name = label_map[trace.name]


class scale_alpha_manual(_TraceNamePaletteScale):
    aesthetic = "alpha"

    def apply(self, fig):
        value_map = self._value_map(fig)
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            value = value_map.get(getattr(trace, "name", None))
            if value is not None:
                trace.opacity = value
            if self.guide == "none":
                trace.showlegend = False
        self._rename_breaks(fig)


class scale_alpha_discrete(scale_alpha_manual):
    def __init__(self, range=(0.35, 1.0), **kwargs):
        values = np.linspace(range[0], range[1], 8)
        super().__init__(values=values, **kwargs)


class scale_alpha_continuous(Scale):
    aesthetic = "alpha"

    def __init__(self, range=(0.1, 1.0), name=None, guide="legend", **kwargs):
        self.range = range
        self.name = name
        self.guide = guide

    def apply(self, fig):
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            if trace.opacity is None:
                trace.opacity = self.range[1]
            else:
                trace.opacity = max(self.range[0], min(self.range[1], float(trace.opacity)))
            if self.guide == "none":
                trace.showlegend = False
        if self.name is not None:
            fig.update_layout(legend_title_text=self.name)


def scale_alpha(range=(0.1, 1.0), **kwargs):
    return scale_alpha_continuous(range=range, **kwargs)


class scale_linetype_manual(_TraceNamePaletteScale):
    aesthetic = "linetype"

    def apply(self, fig):
        value_map = self._value_map(fig)
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            value = value_map.get(getattr(trace, "name", None))
            if value is not None and hasattr(trace, "line"):
                trace.line.dash = value
            if self.guide == "none":
                trace.showlegend = False
        self._rename_breaks(fig)


class scale_linetype_discrete(scale_linetype_manual):
    def __init__(self, **kwargs):
        super().__init__(values=LINETYPES, **kwargs)


def _apply_discrete_palette(fig, scale, update_fill=False):
    names = scale._trace_names(fig)
    color_map = {name: scale.palette[i % len(scale.palette)] for i, name in enumerate(names)}
    for trace in fig.data:
        if not scale._applies_to_trace(trace):
            continue
        color = color_map.get(getattr(trace, "name", None))
        if color is None:
            continue
        if hasattr(trace, "marker") and trace.marker is not None:
            trace.marker.color = color
        if hasattr(trace, "line") and trace.line is not None and not update_fill:
            trace.line.color = color
        if update_fill and hasattr(trace, "fillcolor"):
            trace.fillcolor = color
    if scale.name is not None:
        fig.update_layout(legend_title_text=scale.name)


class scale_color_viridis_d(_TraceNamePaletteScale):
    aesthetic = "color"

    def __init__(self, option="D", direction=1, name=None, **kwargs):
        self.palette = list(VIRIDIS)
        if direction == -1:
            self.palette = list(reversed(self.palette))
        self.option = option
        self.name = name

    def apply(self, fig):
        _apply_discrete_palette(fig, self, update_fill=False)


class scale_colour_viridis_d(scale_color_viridis_d):
    pass


class scale_fill_viridis_d(scale_color_viridis_d):
    aesthetic = "fill"

    def apply(self, fig):
        _apply_discrete_palette(fig, self, update_fill=True)


class _IdentityScale(Scale):
    aesthetic = None

    def __init__(self, guide="none", name=None, **kwargs):
        self.guide = guide
        self.name = name

    def apply(self, fig):
        if self.guide == "none":
            for trace in fig.data:
                if self._applies_to_trace(trace):
                    trace.showlegend = False
        if self.name is not None:
            fig.update_layout(legend_title_text=self.name)


class scale_color_identity(_IdentityScale):
    aesthetic = "color"


class scale_colour_identity(scale_color_identity):
    pass


class scale_fill_identity(_IdentityScale):
    aesthetic = "fill"


class scale_size_identity(_IdentityScale):
    aesthetic = "size"


class scale_alpha_identity(_IdentityScale):
    aesthetic = "alpha"


class scale_shape_identity(_IdentityScale):
    aesthetic = "shape"


class scale_linetype_identity(_IdentityScale):
    aesthetic = "linetype"


class _BinnedGradientScale(Scale):
    aesthetic = None

    def __init__(self, low="#132B43", high="#56B1F7", n_breaks=6, name=None, guide="coloursteps", **kwargs):
        self.low = low
        self.high = high
        self.n_breaks = n_breaks
        self.name = name
        self.guide = guide

    def _colorscale(self):
        steps = max(int(self.n_breaks), 2)
        colors = []
        for i in range(steps):
            p0 = i / steps
            p1 = (i + 1) / steps
            t = i / max(steps - 1, 1)
            color = _interpolate_hex(self.low, self.high, t)
            colors.append([p0, color])
            colors.append([min(p1, 1.0), color])
        return colors

    def apply(self, fig):
        colorscale = self._colorscale()
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            marker = getattr(trace, "marker", None)
            if marker is not None and getattr(marker, "color", None) is not None:
                marker.colorscale = colorscale
                marker.showscale = self.guide != "none"
                if self.name is not None:
                    marker.colorbar = dict(title=self.name)
            if hasattr(trace, "colorscale"):
                trace.colorscale = colorscale
                if self.name is not None and hasattr(trace, "colorbar"):
                    trace.colorbar = dict(title=self.name)


class scale_color_binned(_BinnedGradientScale):
    aesthetic = "color"


class scale_colour_binned(scale_color_binned):
    pass


class scale_fill_binned(_BinnedGradientScale):
    aesthetic = "fill"


def _interpolate_hex(low, high, t):
    def parse(color):
        color = color.lstrip("#")
        if len(color) != 6:
            return (31, 119, 180)
        return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))

    lr, lg, lb = parse(low)
    hr, hg, hb = parse(high)
    return "#{:02x}{:02x}{:02x}".format(
        math.floor(lr + (hr - lr) * t),
        math.floor(lg + (hg - lg) * t),
        math.floor(lb + (hb - lb) * t),
    )


class scale_x_discrete(Scale):
    aesthetic = "x"

    def __init__(self, name=None, limits=None, breaks=None, labels=None, drop=True, expand=None, position="bottom"):
        self.name = name
        self.limits = limits
        self.breaks = breaks
        self.labels = labels
        self.drop = drop
        self.expand = expand
        self.position = position

    def apply(self, fig):
        update = {"type": "category"}
        if self.name is not None:
            update["title_text"] = self.name
        if self.limits is not None:
            update["categoryorder"] = "array"
            update["categoryarray"] = self.limits
        if self.breaks is not None:
            update["tickmode"] = "array"
            update["tickvals"] = self.breaks
            if self.labels is not None:
                update["ticktext"] = self.labels(self.breaks) if callable(self.labels) else self.labels
        if self.position == "top":
            update["side"] = "top"
        fig.update_xaxes(**update)


class scale_y_discrete(scale_x_discrete):
    aesthetic = "y"

    def __init__(self, name=None, limits=None, breaks=None, labels=None, drop=True, expand=None, position="left"):
        super().__init__(name=name, limits=limits, breaks=breaks, labels=labels,
                         drop=drop, expand=expand, position=position)

    def apply(self, fig):
        update = {"type": "category"}
        if self.name is not None:
            update["title_text"] = self.name
        if self.limits is not None:
            update["categoryorder"] = "array"
            update["categoryarray"] = self.limits
        if self.breaks is not None:
            update["tickmode"] = "array"
            update["tickvals"] = self.breaks
            if self.labels is not None:
                update["ticktext"] = self.labels(self.breaks) if callable(self.labels) else self.labels
        if self.position == "right":
            update["side"] = "right"
        fig.update_yaxes(**update)


class scale_pattern_manual(_TraceNamePaletteScale):
    aesthetic = "pattern"

    def apply(self, fig):
        value_map = self._value_map(fig)
        for trace in fig.data:
            if not self._applies_to_trace(trace):
                continue
            shape = value_map.get(getattr(trace, "name", None))
            if shape is None:
                continue
            marker = getattr(trace, "marker", None)
            if marker is not None and hasattr(marker, "pattern"):
                marker.pattern.shape = shape
