# scales/__init__.py
from .scale_base import Scale
from .scale_advanced import (
    dup_axis,
    new_scale_color,
    new_scale_colour,
    new_scale_fill,
    scale_alpha,
    scale_alpha_continuous,
    scale_alpha_discrete,
    scale_alpha_identity,
    scale_alpha_manual,
    scale_color_binned,
    scale_color_identity,
    scale_color_viridis_d,
    scale_colour_binned,
    scale_colour_identity,
    scale_colour_viridis_d,
    scale_fill_binned,
    scale_fill_identity,
    scale_fill_viridis_d,
    scale_linetype_discrete,
    scale_linetype_identity,
    scale_linetype_manual,
    scale_pattern_manual,
    scale_shape_identity,
    scale_size_identity,
    scale_x_discrete,
    scale_x_sqrt,
    scale_y_discrete,
    scale_y_sqrt,
    sec_axis,
)
from .scale_color_brewer import scale_color_brewer
from .scale_color_gradient import scale_color_gradient
from .scale_color_manual import scale_color_manual
from .scale_fill_brewer import scale_fill_brewer
from .scale_fill_gradient import scale_fill_gradient
from .scale_fill_manual import scale_fill_manual
from .scale_fill_viridis import scale_fill_viridis_c
from .scale_shape_manual import scale_shape_manual
from .scale_size import scale_size
from .scale_x_continuous import scale_x_continuous
from .scale_x_date import scale_x_date, scale_x_datetime
from .scale_x_log10 import scale_x_log10
from .scale_x_rangeselector import scale_x_rangeselector
from .scale_x_rangeslider import scale_x_rangeslider
from .scale_x_reverse import scale_x_reverse
from .scale_y_continuous import scale_y_continuous
from .scale_y_log10 import scale_y_log10
from .scale_y_reverse import scale_y_reverse

scale_colour_manual = scale_color_manual
scale_colour_gradient = scale_color_gradient
scale_colour_brewer = scale_color_brewer

__all__ = [
    "Scale",
    "scale_x_continuous",
    "scale_y_continuous",
    "scale_x_log10",
    "scale_y_log10",
    "scale_x_reverse",
    "scale_y_reverse",
    "scale_x_date",
    "scale_x_datetime",
    "scale_x_rangeslider",
    "scale_x_rangeselector",
    "scale_color_manual",
    "scale_colour_manual",
    "scale_color_gradient",
    "scale_colour_gradient",
    "scale_color_brewer",
    "scale_colour_brewer",
    "scale_fill_gradient",
    "scale_fill_manual",
    "scale_fill_brewer",
    "scale_fill_viridis_c",
    "scale_shape_manual",
    "scale_size",
    "scale_alpha",
    "scale_alpha_continuous",
    "scale_alpha_discrete",
    "scale_alpha_manual",
    "scale_alpha_identity",
    "scale_linetype_manual",
    "scale_linetype_discrete",
    "scale_linetype_identity",
    "scale_color_viridis_d",
    "scale_colour_viridis_d",
    "scale_fill_viridis_d",
    "scale_x_sqrt",
    "scale_y_sqrt",
    "scale_color_identity",
    "scale_colour_identity",
    "scale_fill_identity",
    "scale_size_identity",
    "scale_shape_identity",
    "scale_color_binned",
    "scale_colour_binned",
    "scale_fill_binned",
    "scale_x_discrete",
    "scale_y_discrete",
    "scale_pattern_manual",
    "new_scale_color",
    "new_scale_colour",
    "new_scale_fill",
    "sec_axis",
    "dup_axis",
]
