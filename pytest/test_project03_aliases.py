"""Project 03 ggplot2 alias and thin-wrapper coverage."""

import numpy as np
import pandas as pd

import ggplotly
from ggplotly import (
    aes,
    geom_density2d,
    geom_density2d_filled,
    geom_density_2d,
    geom_density_2d_filled,
    ggplot,
)
from ggplotly.geoms import geom_bin2d, geom_bin_2d
from ggplotly.guides import guide_colorbar, guide_colourbar
from ggplotly.stats import (
    stat_bin2d,
    stat_bin_2d,
    stat_contour_filled,
    stat_density2d,
    stat_density_2d,
    stat_sf,
)


def _density_points(seed=31, size=120):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "x": np.r_[rng.normal(-1, 0.45, size), rng.normal(1, 0.5, size)],
        "y": np.r_[rng.normal(0, 0.55, size), rng.normal(1.2, 0.45, size)],
    })


def test_project03_direct_aliases_resolve_to_canonical_objects():
    assert geom_bin_2d is geom_bin2d
    assert ggplotly.geom_bin_2d is ggplotly.geom_bin2d
    assert stat_bin_2d is stat_bin2d
    assert ggplotly.stat_bin_2d is ggplotly.stat_bin2d
    assert stat_density2d is stat_density_2d
    assert ggplotly.stat_density2d is ggplotly.stat_density_2d
    assert guide_colourbar is guide_colorbar
    assert ggplotly.guide_colourbar is ggplotly.guide_colorbar
    assert geom_density2d is geom_density_2d
    assert geom_density2d_filled is geom_density_2d_filled


def test_geom_density2d_draws_contour_lines():
    fig = (
        ggplot(_density_points(), aes(x="x", y="y"))
        + geom_density2d(bins=7, n=35, color="black")
    ).draw()

    assert len(fig.data) == 1
    assert fig.data[0].type == "contour"
    assert fig.data[0].ncontours == 7
    assert fig.data[0].contours.coloring == "lines"
    assert fig.data[0].line.color == "black"


def test_geom_density2d_filled_draws_filled_contours():
    fig = (
        ggplot(_density_points(), aes(x="x", y="y"))
        + geom_density2d_filled(bins=6, n=30, palette="Plasma")
    ).draw()

    assert len(fig.data) == 1
    assert fig.data[0].type == "contour"
    assert fig.data[0].ncontours == 6
    assert fig.data[0].contours.coloring == "heatmap"
    assert fig.data[0].colorscale is not None


def test_stat_contour_filled_uses_contour_grid_contract():
    result, mapping = stat_contour_filled(
        mapping={"x": "x", "y": "y"},
        gridsize=24,
    ).compute(_density_points(size=60))

    assert result["x"].shape == (24,)
    assert result["y"].shape == (24,)
    assert result["z"].shape == (24, 24)
    assert mapping["z"] == "z"


def test_stat_sf_is_noop_for_geom_sf_owned_geometry_handling():
    frame = pd.DataFrame({"geometry": ["POINT (0 0)", "POINT (1 1)"], "value": [1, 2]})
    result, mapping = stat_sf(mapping={"geometry": "geometry"}).compute(frame)

    assert result.equals(frame)
    assert result is not frame
    assert mapping == {"geometry": "geometry"}
