"""ggplot2-compatible 2D density contour geom wrappers."""

from .geom_contour import geom_contour
from .geom_contour_filled import geom_contour_filled


class geom_density_2d(geom_contour):
    """Draw 2D density contour lines."""

    def __init__(
        self,
        data=None,
        mapping=None,
        stat="density_2d",
        position="identity",
        contour=True,
        contour_var="density",
        n=100,
        **params,
    ):
        params.setdefault("gridsize", n)
        params["stat"] = stat
        params["position"] = position
        params["contour"] = contour
        params["contour_var"] = contour_var
        super().__init__(data, mapping, **params)


class geom_density_2d_filled(geom_contour_filled):
    """Draw filled 2D density contours."""

    def __init__(
        self,
        data=None,
        mapping=None,
        stat="density_2d_filled",
        position="identity",
        contour=True,
        contour_var="density",
        n=100,
        **params,
    ):
        params.setdefault("gridsize", n)
        params["stat"] = stat
        params["position"] = position
        params["contour"] = contour
        params["contour_var"] = contour_var
        super().__init__(data, mapping, **params)


geom_density2d = geom_density_2d
geom_density2d_filled = geom_density_2d_filled
