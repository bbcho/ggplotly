"""Project 04 ggplot2 core-stat and wrapper coverage."""

import numpy as np
import pandas as pd
import pytest

import ggplotly
from ggplotly import (
    aes,
    geom_area,
    geom_blank,
    geom_function,
    geom_hex,
    geom_point,
    geom_quantile,
    ggplot,
    stat_align,
    stat_quantile,
    stat_summary_hex,
    stat_unique,
    stat_ydensity,
)


def test_project04_public_exports_are_available():
    for name in (
        "geom_blank",
        "geom_function",
        "geom_quantile",
        "stat_align",
        "stat_summary_hex",
        "stat_unique",
        "stat_ydensity",
    ):
        assert name in ggplotly.__all__
        assert hasattr(ggplotly, name)


def test_stat_unique_keeps_first_row_per_mapped_key_and_drops_missing_when_requested():
    frame = pd.DataFrame({
        "x": [1, 1, 2, None],
        "y": [3, 3, 4, 5],
        "group": ["A", "A", "B", "C"],
        "label": ["first", "second", "third", "missing"],
    })

    result, mapping = stat_unique(mapping={"x": "x", "y": "y", "color": "group"}).compute(frame)
    assert result["label"].tolist() == ["first", "third", "missing"]
    assert mapping == {"x": "x", "y": "y", "color": "group"}

    result, _ = stat_unique(mapping={"x": "x", "y": "y", "color": "group"}, na_rm=True).compute(frame)
    assert result["label"].tolist() == ["first", "third"]


def test_stat_align_interpolates_grouped_area_data_to_shared_x_domain():
    frame = pd.DataFrame({
        "x": [1, 3, 2, 3],
        "y": [1, 3, 10, 20],
        "group": ["A", "A", "B", "B"],
    })

    result, mapping = stat_align(mapping={"x": "x", "y": "y", "fill": "group"}).compute(frame)

    assert mapping == {"x": "x", "y": "y", "fill": "group"}
    assert result.groupby("group")["x"].apply(list).to_dict() == {"A": [1.0, 2.0, 3.0], "B": [1.0, 2.0, 3.0]}
    assert result[result["group"] == "A"]["y"].tolist() == pytest.approx([1, 2, 3])
    assert result[result["group"] == "B"]["y"].tolist() == pytest.approx([0, 10, 20])


def test_geom_area_uses_align_by_default_and_identity_preserves_rows():
    frame = pd.DataFrame({
        "x": [1, 3, 2, 3],
        "y": [1, 3, 10, 20],
        "group": ["A", "A", "B", "B"],
    })

    aligned = (ggplot(frame, aes(x="x", y="y", fill="group")) + geom_area()).draw()
    assert [len(trace.x) for trace in aligned.data] == [3, 3]

    identity = (ggplot(frame, aes(x="x", y="y", fill="group")) + geom_area(stat="identity")).draw()
    assert [len(trace.x) for trace in identity.data] == [2, 2]


def test_stat_summary_hex_aggregates_values_and_geom_hex_draws_value_scale():
    frame = pd.DataFrame({
        "x": [0.1, 0.2, 0.9, 0.95],
        "y": [0.1, 0.2, 0.9, 0.95],
        "z": [1, 3, 10, 14],
    })

    result, mapping = stat_summary_hex(mapping={"x": "x", "y": "y", "z": "z"}, bins=2).compute(frame)

    assert mapping == {"x": "x", "y": "y", "fill": "value"}
    assert sorted(result["value"].tolist()) == pytest.approx([2, 12])
    assert sorted(result["count"].tolist()) == [2, 2]
    assert "radius" in result

    fig = (ggplot(frame, aes(x="x", y="y", z="z")) + stat_summary_hex(bins=2)).draw()
    assert len(fig.data) == 1
    assert sorted(list(fig.data[0].marker.color)) == pytest.approx([2, 12])
    assert fig.data[0].marker.colorbar.title.text == "value"


def test_stat_ydensity_outputs_violin_compatible_columns_and_scale_modes():
    frame = pd.DataFrame({
        "category": ["A"] * 20 + ["B"] * 40,
        "value": np.r_[np.linspace(-1, 1, 20), np.linspace(-2, 2, 40)],
    })

    result, mapping = stat_ydensity(
        mapping={"x": "category", "y": "value"},
        n=32,
        scale="width",
    ).compute(frame)

    assert mapping == {"x": "x", "y": "y", "group": "group"}
    assert {
        "x",
        "y",
        "density",
        "scaled",
        "ndensity",
        "count",
        "n",
        "violinwidth",
        "width",
        "group",
    }.issubset(result.columns)
    assert result.groupby("group")["violinwidth"].max().to_dict() == pytest.approx({"A": 1, "B": 1})

    count_scaled, _ = stat_ydensity(
        mapping={"x": "category", "y": "value"},
        n=32,
        scale="count",
    ).compute(frame)
    assert count_scaled[count_scaled["group"] == "B"]["violinwidth"].max() > count_scaled[
        count_scaled["group"] == "A"
    ]["violinwidth"].max()


def test_geom_blank_adds_invisible_scale_training_trace():
    bounds = pd.DataFrame({"x": [0, 10], "y": [-5, 5]})
    point = pd.DataFrame({"x": [5], "y": [0]})

    fig = (
        ggplot(point, aes(x="x", y="y"))
        + geom_blank(data=bounds, mapping=aes(x="x", y="y"))
        + geom_point()
    ).draw()

    assert len(fig.data) == 2
    assert list(fig.data[0].x) == [0, 10]
    assert list(fig.data[0].y) == [-5, 5]
    assert fig.data[0].opacity == 0
    assert fig.data[0].showlegend is False
    assert fig.data[0].hoverinfo == "skip"


def test_geom_function_draws_line_with_keyword_args_and_no_data():
    fig = (
        ggplot()
        + geom_function(fun=lambda x, shift=0: x + shift, xlim=(0, 1), n=3, args={"shift": 2})
    ).draw()

    assert len(fig.data) == 1
    assert list(fig.data[0].y) == pytest.approx([x + 2 for x in fig.data[0].x])
    assert fig.data[0].mode == "lines"


def test_geom_quantile_draws_quantile_lines_and_rejects_unsupported_options():
    frame = pd.DataFrame({"x": np.arange(10, dtype=float), "y": np.arange(10, dtype=float) * 2 + 1})

    fig = (ggplot(frame, aes(x="x", y="y")) + geom_quantile(n=12)).draw()
    assert len(fig.data) == 3
    assert {trace.mode for trace in fig.data} == {"lines"}
    assert {trace.name for trace in fig.data} == {"0.25", "0.5", "0.75"}

    single = (ggplot(frame, aes(x="x", y="y")) + geom_quantile(quantiles=0.5, n=8)).draw()
    assert len(single.data) == 1

    with pytest.raises(NotImplementedError, match="method='rq'"):
        stat_quantile(mapping={"x": "x", "y": "y"}, method="lm")
    with pytest.raises(NotImplementedError, match="y ~ x"):
        stat_quantile(mapping={"x": "x", "y": "y"}, formula="y ~ poly(x, 2)")


def test_geom_hex_still_counts_when_no_summary_stat_is_attached():
    frame = pd.DataFrame({"x": [0, 0, 1], "y": [0, 0, 1]})

    fig = (ggplot(frame, aes(x="x", y="y")) + geom_hex(bins=2)).draw()

    assert len(fig.data) == 1
    assert fig.data[0].marker.colorbar.title.text == "count"
