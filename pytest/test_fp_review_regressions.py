import builtins

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pytest

from ggplotly import (
    aes,
    coord_polar,
    facet_grid,
    facet_wrap,
    geom_abline,
    geom_bar,
    geom_boxplot,
    geom_col,
    geom_density,
    geom_errorbar,
    geom_histogram,
    geom_line,
    geom_lines,
    geom_map,
    geom_point,
    geom_rect,
    geom_segment,
    geom_smooth,
    geom_surface,
    geom_text,
    geom_tile,
    ggplot,
    ggsave,
    position_fill,
    position_nudge,
    scale_size,
    scale_y_continuous,
)
from ggplotly.geoms._bar_positioning import compute_bar_trace_specs
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


def test_geom_col_fill_and_outline_are_separate_marker_properties():
    df = pd.DataFrame({"x": ["A", "B"], "y": [2, 3]})

    fig = (
        ggplot(df, aes(x="x", y="y"))
        + geom_col(fill="steelblue", color="black")
    ).draw()

    assert fig.data[0].marker.color == "steelblue"
    assert fig.data[0].marker.line.color == "black"
    assert fig.data[0].marker.line.width == 1


def test_geom_bar_default_stacks_and_dodge_uses_grouped_barmode():
    df = pd.DataFrame({
        "category": ["A", "A", "A", "B", "B", "B"],
        "group": ["X", "Y", "Y", "X", "X", "Y"],
    })

    stacked = (ggplot(df, aes(x="category", fill="group")) + geom_bar()).draw()
    dodged = (
        ggplot(df, aes(x="category", fill="group"))
        + geom_bar(position="dodge")
    ).draw()

    assert stacked.layout.barmode == "relative"
    assert all(trace.offsetgroup is None for trace in stacked.data)
    assert dodged.layout.barmode == "group"
    assert {trace.offsetgroup for trace in dodged.data} == {"X", "Y"}


def test_position_fill_normalizes_each_x_stack_to_one():
    df = pd.DataFrame({
        "category": ["A", "A", "B", "B"],
        "group": ["X", "Y", "X", "Y"],
        "value": [1, 3, 2, 2],
    })

    fig = (
        ggplot(df, aes(x="category", y="value", fill="group"))
        + geom_col(position=position_fill())
    ).draw()

    totals = {"A": 0.0, "B": 0.0}
    for trace in fig.data:
        for x_value, y_value in zip(trace.x, trace.y):
            totals[x_value] += float(y_value)

    assert totals == {"A": 1.0, "B": 1.0}
    assert tuple(fig.layout.yaxis.range) == (0, 1)


def test_histogram_fill_and_outline_follow_ggplot2_roles():
    df = pd.DataFrame({"x": [1, 1, 2, 2, 3, 3]})

    fig = (
        ggplot(df, aes(x="x"))
        + geom_histogram(bins=2, fill="#FF6B6B", color="white")
    ).draw()

    assert fig.data[0].marker.color == "#FF6B6B"
    assert fig.data[0].marker.line.color == "white"
    assert fig.data[0].marker.line.width == 1


def test_density_fill_literal_draws_filled_area():
    df = pd.DataFrame({"x": [-2, -1, -0.5, 0, 0.5, 1, 2]})

    fig = (ggplot(df, aes(x="x")) + geom_density(fill="lightblue")).draw()

    assert fig.data[0].fill == "tozeroy"
    assert fig.data[0].fillcolor == "lightblue"


def test_bar_trace_specs_keep_position_fill_invariants():
    data = pd.DataFrame({
        "x": ["A", "A", "B", "B"],
        "y": [2, 6, 5, 5],
        "group": ["left", "right", "left", "right"],
    })
    style_props = {
        "fill_series": data["group"],
        "fill_map": {"left": "red", "right": "blue"},
        "color_series": None,
        "color_map": None,
        "fill": "group",
        "color": None,
        "default_color": "#1f77b4",
    }

    result = compute_bar_trace_specs(
        data,
        {"x": "x", "y": "y", "fill": "group"},
        {"position": position_fill(), "width": 0.9},
        style_props,
        "Column",
    )

    totals = {"A": 0.0, "B": 0.0}
    for trace in result.traces:
        for x_value, y_value in zip(trace.x, trace.y):
            totals[x_value] += y_value

    assert result.barmode == "relative"
    assert result.yaxis_range == (0.0, 1.0)
    assert totals == {"A": 1.0, "B": 1.0}


def test_abline_uses_finite_data_extent_instead_of_huge_fake_range():
    df = pd.DataFrame({"x": [1, 2, 3], "y": [1, 2, 4]})

    fig = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + geom_abline(slope=1, intercept=0)
    ).draw()

    assert list(fig.data[-1].x) == [1.0, 3.0]


def test_mapped_linetype_creates_distinct_line_dashes():
    df = pd.DataFrame({
        "x": [1, 2, 3, 1, 2, 3],
        "y": [1, 2, 3, 3, 2, 1],
        "style": ["forecast", "forecast", "forecast", "actual", "actual", "actual"],
    })

    fig = (ggplot(df, aes(x="x", y="y", linetype="style")) + geom_line()).draw()

    assert len(fig.data) == 2
    assert {trace.line.dash for trace in fig.data} == {"solid", "dash"}


def test_position_nudge_object_offsets_text_coordinates():
    df = pd.DataFrame({"x": [1, 2], "y": [3, 4], "label": ["a", "b"]})

    fig = (
        ggplot(df, aes(x="x", y="y", label="label"))
        + geom_text(position=position_nudge(x=0.5, y=0.25))
    ).draw()

    assert list(fig.data[0].x) == [1.5, 2.5]
    assert list(fig.data[0].y) == [3.25, 4.25]


def test_size_mapped_points_are_scaled_to_visible_marker_range():
    df = pd.DataFrame({"x": [1, 2], "y": [1, 2], "s": [1, 100]})

    fig = (ggplot(df, aes(x="x", y="y", size="s")) + geom_point()).draw()

    assert list(fig.data[0].marker.size) == [5.0, 20.0]


def test_lm_smooth_confidence_band_is_narrowest_near_x_mean():
    df = pd.DataFrame({
        "x": [0, 1, 2, 3, 4],
        "y": [0.0, 1.2, 1.9, 3.1, 4.0],
    })

    result = stat_smooth(method="lm", se=True).compute_stat(df, x_col="x", y_col="y")
    widths = result["ymax"] - result["ymin"]

    assert widths.iloc[2] < widths.iloc[0]
    assert widths.max() < 1.0


def test_wide_datetime_index_lines_preserve_datetime_values():
    dates = pd.date_range("2024-01-01", periods=3)
    df = pd.DataFrame({"a": [1, 2, 3], "b": [3, 2, 1]}, index=dates)

    fig = (ggplot(df) + geom_lines()).draw()

    assert pd.Timestamp(fig.data[0].x[0]) == dates[0]


def test_grouped_boxplot_uses_grouped_boxmode():
    df = pd.DataFrame({
        "x": ["A"] * 6 + ["B"] * 6,
        "group": ["g1", "g1", "g1", "g2", "g2", "g2"] * 2,
        "y": [1, 2, 3, 2, 3, 4, 3, 4, 5, 4, 5, 6],
    })

    fig = (
        ggplot(df, aes(x="x", y="y", fill="group"))
        + geom_boxplot()
    ).draw()

    assert fig.layout.boxmode == "group"


def test_map_segments_render_as_scattergeo_not_cartesian_scatter():
    df = pd.DataFrame({
        "lon": [-120, -100],
        "lat": [35, 40],
        "lon2": [-110, -90],
        "lat2": [37, 42],
    })

    fig = (
        ggplot(df, aes(x="lon", y="lat", xend="lon2", yend="lat2"))
        + geom_map(map_type="usa")
        + geom_segment()
    ).draw()

    segment_traces = [trace for trace in fig.data if trace.name == "Segment"]
    assert segment_traces
    assert all(trace.type == "scattergeo" for trace in segment_traces)


def test_map_tiles_render_as_geo_polygons_not_heatmap():
    df = pd.DataFrame({
        "lon": [-101, -100],
        "lat": [39, 40],
        "value": [1.0, 2.0],
    })

    fig = (
        ggplot(df, aes(x="lon", y="lat", fill="value"))
        + geom_map(map_type="usa")
        + geom_tile()
    ).draw()

    assert not any(trace.type == "heatmap" for trace in fig.data)
    assert any(trace.type == "scattergeo" and trace.fill == "toself" for trace in fig.data)


def test_facet_grid_auto_height_preserves_multirow_panels():
    df = pd.DataFrame({
        "x": [1, 2] * 6,
        "y": list(range(12)),
        "row": ["r1"] * 4 + ["r2"] * 4 + ["r3"] * 4,
        "col": ["c1", "c1", "c2", "c2"] * 3,
    })

    fig = (
        ggplot(df, aes(x="x", y="y"))
        + geom_point()
        + facet_grid(rows="row", cols="col")
    ).draw()

    assert fig.layout.height >= 780


def test_coord_polar_converts_radian_theta_to_degrees_for_lines():
    df = pd.DataFrame({"theta": [0, np.pi / 2], "r": [1, 1]})

    fig = (
        ggplot(df, aes(x="theta", y="r"))
        + geom_line()
        + coord_polar()
    ).draw()

    assert fig.data[0].type == "scatterpolar"
    assert list(fig.data[0].theta) == [0.0, 90.0]


def test_surface_scene_uses_cube_aspect_and_tight_margins():
    df = pd.DataFrame({
        "x": [0, 1, 0, 1],
        "y": [0, 0, 1, 1],
        "z": [0, 1, 1, 0],
    })

    fig = (ggplot(df, aes(x="x", y="y", z="z")) + geom_surface()).draw()

    assert fig.layout.scene.aspectmode == "cube"
    assert fig.layout.margin.l == 0
