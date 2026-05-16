import builtins

import pandas as pd
import plotly.graph_objects as go
import pytest

from ggplotly import (
    aes,
    facet_wrap,
    geom_errorbar,
    geom_point,
    geom_rect,
    geom_segment,
    geom_smooth,
    geom_tile,
    ggplot,
    ggsave,
    scale_size,
    scale_y_continuous,
)
from ggplotly.aesthetic_mapper import AestheticMapper
from ggplotly.geoms.geom_searoute import geom_searoute
from ggplotly.stats.stat_base import Stat
from ggplotly.stats.stat_edgebundle import clear_bundling_cache, stat_edgebundle
from ggplotly.stats.stat_smooth import stat_smooth


def test_add_returns_new_plot_without_mutating_original_plot_or_geom():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    base = ggplot(df, aes(x="x", y="y"))
    point = geom_point(color="red")

    updated = base + point

    assert base.layers == []
    assert len(updated.layers) == 1
    assert point.data is None
    assert point.mapping == {}


def test_facet_draw_does_not_shrink_explicit_geom_data_between_panels():
    df = pd.DataFrame({
        "x": [1, 2, 1, 2],
        "y": [1, 2, 3, 4],
        "facet": ["a", "a", "b", "b"],
    })
    segments = pd.DataFrame({
        "x": [1, 1],
        "y": [0, 0],
        "xend": [2, 2],
        "yend": [2, 4],
        "facet": ["a", "b"],
    })

    plot = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + geom_segment(
            data=segments,
            mapping=aes(x="x", y="y", xend="xend", yend="yend"),
            color="black",
        )
        + facet_wrap("facet")
    )

    first = plot.draw()
    second = plot.draw()

    assert len(plot.layers[1].data) == 2
    assert len(first.data) == len(second.data)


class BareDataStat(Stat):
    def compute(self, data):
        return data


def test_bare_stat_results_still_render_through_geom_boundary():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    point = geom_point()
    point.stats = [BareDataStat()]

    fig = (ggplot(df, aes(x="x", y="y")) + point).draw()

    assert len(fig.data) == 1
    assert list(fig.data[0].x) == [1, 2]


def test_show_legend_aliases_are_normalized():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})

    fig = (ggplot(df, aes(x="x", y="y")) + geom_point(**{"show.legend": False})).draw()

    assert fig.data[0].showlegend is False


def test_na_rm_accepts_ggplot2_dotted_alias():
    df = pd.DataFrame({"x": [1, 2], "y": [3.0, None]})

    fig = (ggplot(df, aes(x="x", y="y")) + geom_point(**{"na.rm": True})).draw()

    assert list(fig.data[0].x) == [1]


def test_falsey_group_column_name_is_resolved():
    df = pd.DataFrame({"": ["a", "b"], "x": [1, 2]})

    style = AestheticMapper(df, {"group": ""}, {}).get_style_properties()

    assert list(style["group_series"]) == ["a", "b"]


def test_manual_geoms_accept_continuous_color_without_discrete_legend():
    segments = pd.DataFrame({
        "x": [0, 1, 2],
        "y": [0, 1, 2],
        "xend": [1, 2, 3],
        "yend": [1, 2, 3],
        "value": [0.1, 0.5, 0.9],
    })
    errorbars = pd.DataFrame({
        "x": [1, 2, 3],
        "y": [2, 3, 4],
        "ymin": [1, 2, 3],
        "ymax": [3, 4, 5],
        "value": [0.1, 0.5, 0.9],
    })
    rects = pd.DataFrame({
        "xmin": [0, 1, 2],
        "xmax": [1, 2, 3],
        "ymin": [0, 0, 0],
        "ymax": [1, 2, 3],
        "value": [0.1, 0.5, 0.9],
    })

    segment_fig = (
        ggplot(segments, aes(x="x", y="y", xend="xend", yend="yend", color="value"))
        + geom_segment()
    ).draw()
    errorbar_fig = (
        ggplot(errorbars, aes(x="x", y="y", ymin="ymin", ymax="ymax", color="value"))
        + geom_errorbar()
    ).draw()
    rect_fig = (
        ggplot(rects, aes(xmin="xmin", xmax="xmax", ymin="ymin", ymax="ymax", fill="value"))
        + geom_rect()
    ).draw()

    assert all(trace.showlegend is False for trace in segment_fig.data)
    assert all(trace.showlegend is False for trace in errorbar_fig.data)
    assert all(trace.showlegend is False for trace in rect_fig.data)


def test_smooth_does_not_group_by_continuous_color():
    df = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "y": [1, 4, 9, 16],
        "value": [0.1, 0.2, 0.3, 0.4],
    })

    fig = (
        ggplot(df, aes(x="x", y="y", color="value"))
        + geom_smooth(method="lm")
    ).draw()

    assert len(fig.data) >= 1


def test_categorical_tile_fill_uses_codes_and_does_not_mutate_data():
    df = pd.DataFrame({
        "x": [1, 2, 1],
        "y": [1, 1, 2],
        "fill": ["cold", "hot", "cold"],
    })
    original = df.copy(deep=True)

    fig = (ggplot(df, aes(x="x", y="y", fill="fill")) + geom_tile()).draw()

    pd.testing.assert_frame_equal(df, original)
    assert fig.data[0].z is not None
    assert set(fig.data[0].colorbar.ticktext) == {"cold", "hot"}


def test_sqrt_y_scale_transforms_every_y_trace_and_masks_invalid_values():
    fig = go.Figure()
    fig.add_scatter(x=[1, 2, 3], y=[4, -1, None])
    fig.add_scatter(x=[1, 2], y=[9, 16])

    scale_y_continuous(trans="sqrt").apply(fig)

    assert list(fig.data[0].y) == [2.0, None, None]
    assert list(fig.data[1].y) == [3.0, 4.0]


def test_scale_size_constant_marker_arrays_do_not_divide_by_zero():
    fig = go.Figure()
    fig.add_scatter(x=[1, 2, 3], y=[1, 2, 3], marker={"size": [5, 5, 5]})

    scale_size(range=(2, 10)).apply(fig)

    assert list(fig.data[0].marker.size) == [6.0, 6.0, 6.0]


def test_searoute_import_errors_propagate_without_poisoning_cache(monkeypatch):
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "searoute":
            raise ModuleNotFoundError("forced missing searoute")
        return real_import(name, *args, **kwargs)

    route_geom = geom_searoute()
    monkeypatch.setattr(builtins, "__import__", fake_import)

    with pytest.raises(ImportError):
        route_geom._compute_route((0, 0), (1, 1))

    assert route_geom._route_cache == {}


def test_edge_bundling_cache_returns_copies():
    clear_bundling_cache()
    edges = pd.DataFrame({
        "x": [0.0, 0.0],
        "y": [0.0, 1.0],
        "xend": [1.0, 1.0],
        "yend": [1.0, 0.0],
    })
    stat = stat_edgebundle(C=1, I=1, verbose=False)

    first = stat.compute(edges)
    first.loc[first.index[0], "x"] = 999
    second = stat.compute(edges)

    assert second.loc[second.index[0], "x"] != 999


def test_stat_smooth_invalid_loess_degree_raises_before_fallback():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 4, 9]})
    smoother = stat_smooth(mapping={"x": "x", "y": "y"}, degree=3)

    with pytest.raises(ValueError, match="Degree must be 1 or 2"):
        smoother.compute(df)


def test_ggsave_does_not_print_by_default(tmp_path, capsys):
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4]})
    plot = ggplot(df, aes(x="x", y="y")) + geom_point()

    ggsave(str(tmp_path / "plot.html")).apply(plot)

    captured = capsys.readouterr()
    assert captured.out == ""
