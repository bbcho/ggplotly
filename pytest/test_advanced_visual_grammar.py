import numpy as np
import pandas as pd

import ggplotly
from ggplotly import (
    aes,
    geom_beeswarm,
    geom_bin2d,
    geom_col_pattern,
    geom_edge_link,
    geom_hex,
    geom_node_point,
    geom_point,
    geom_slabinterval,
    geom_text_repel,
    ggplot,
    graph_layout,
    new_scale_color,
    scale_color_manual,
    scale_linetype_manual,
    scale_pattern_manual,
    scale_y_continuous,
    sec_axis,
    transition_time,
)
from ggplotly.stats import stat_bindot, stat_density_2d, stat_halfeye


def test_advanced_public_api_exports():
    names = [
        "geom_linerange",
        "geom_pointrange",
        "geom_errorbarh",
        "geom_bin2d",
        "geom_hex",
        "geom_slabinterval",
        "geom_density_ridges",
        "geom_alluvium",
        "geom_mosaic",
        "geom_beeswarm",
        "geom_col_pattern",
        "scale_color_viridis_d",
        "scale_colour_viridis_d",
        "scale_alpha_manual",
        "scale_linetype_manual",
        "scale_x_discrete",
        "scale_y_sqrt",
        "new_scale_color",
        "sec_axis",
        "transition_time",
        "graph_layout",
    ]
    assert all(hasattr(ggplotly, name) for name in names)


def test_2d_bin_and_hex_geoms_draw_density_encodings():
    rng = np.random.default_rng(10)
    df = pd.DataFrame({
        "x": rng.normal(size=120),
        "y": rng.normal(size=120),
    })

    bin_fig = (ggplot(df, aes(x="x", y="y")) + geom_bin2d(bins=8)).draw()
    assert len(bin_fig.data) == 1
    assert bin_fig.data[0].type == "heatmap"
    assert np.asarray(bin_fig.data[0].z).sum() == len(df)

    hex_fig = (ggplot(df, aes(x="x", y="y")) + geom_hex(bins=8)).draw()
    assert len(hex_fig.data) == 1
    assert hex_fig.data[0].type == "scatter"
    assert hex_fig.data[0].marker.symbol == "hexagon"
    assert max(hex_fig.data[0].marker.color) > 0


def test_distribution_and_position_geoms_draw_expected_traces():
    rng = np.random.default_rng(11)
    df = pd.DataFrame({
        "group": ["A"] * 80 + ["B"] * 80,
        "value": np.r_[rng.normal(0, 1, 80), rng.normal(2, 0.8, 80)],
        "label": [f"p{i}" for i in range(160)],
    })

    slab_fig = (ggplot(df, aes(x="group", y="value")) + geom_slabinterval()).draw()
    assert len(slab_fig.data) >= 4
    assert any(trace.fill == "toself" for trace in slab_fig.data)

    beeswarm_fig = (ggplot(df, aes(x="group", y="value")) + geom_beeswarm()).draw()
    assert len(beeswarm_fig.data) == 1
    assert len(set(np.round(beeswarm_fig.data[0].x, 3))) > 2

    label_df = df.head(8).assign(x=np.arange(8), y=np.arange(8))
    repel_fig = (
        ggplot(label_df, aes(x="x", y="y", label="label"))
        + geom_point()
        + geom_text_repel(force=0.2)
    ).draw()
    assert any(trace.mode == "text" for trace in repel_fig.data)


def test_new_scale_color_scopes_manual_scales_to_later_layers():
    df = pd.DataFrame({
        "x": [1, 2, 1, 2],
        "y": [1, 2, 3, 4],
        "y2": [4, 3, 2, 1],
        "g1": ["A", "B", "A", "B"],
        "g2": ["C", "D", "C", "D"],
    })

    fig = (
        ggplot(df, aes(x="x"))
        + geom_point(aes(y="y", color="g1"))
        + scale_color_manual({"A": "red", "B": "blue"})
        + new_scale_color()
        + geom_point(aes(y="y2", color="g2"))
        + scale_color_manual({"C": "green", "D": "orange"})
    ).draw()

    colors = {trace.name: trace.marker.color for trace in fig.data}
    assert colors["A"] == "red"
    assert colors["B"] == "blue"
    assert colors["C"] == "green"
    assert colors["D"] == "orange"


def test_pattern_linetype_secondary_axis_and_interactive_metadata():
    bars = pd.DataFrame({
        "x": ["one", "two", "one", "two"],
        "y": [2, 3, 4, 1],
        "group": ["A", "A", "B", "B"],
    })
    bar_fig = (
        ggplot(bars, aes(x="x", y="y", fill="group"))
        + geom_col_pattern(position="dodge")
        + scale_pattern_manual({"A": "/", "B": "x"})
    ).draw()
    assert all(trace.marker.pattern.shape in ("/", "x") for trace in bar_fig.data)

    line_fig = (
        ggplot(bars, aes(x="x", y="y", group="group", linetype="group"))
        + geom_point()
        + scale_linetype_manual({"A": "dash", "B": "dot"})
        + scale_y_continuous(sec_axis=sec_axis(name="secondary"))
    ).draw()
    assert line_fig.layout.yaxis2.title.text == "secondary"

    interactive_fig = (
        ggplot(bars, aes(x="x", y="y", tooltip="group", data_id="group"))
        + geom_point()
        + transition_time("group")
    ).draw()
    assert len(interactive_fig.frames) == 2
    assert list(interactive_fig.data[0].hovertext) == ["A", "A", "B", "B"]
    assert list(interactive_fig.data[0].customdata) == ["A", "A", "B", "B"]


def test_graph_layout_and_geoms_use_mapped_edge_columns():
    edges = pd.DataFrame({"source": ["A", "A", "B"], "target": ["B", "C", "C"]})
    layout = graph_layout(layout="circular").compute(edges, source="source", target="target")

    fig = (
        ggplot(edges, aes(**{"from": "source", "to": "target"}))
        + geom_edge_link(layout=graph_layout(layout="circular"))
        + geom_node_point(layout, aes(x="x", y="y", label="node"))
    ).draw()

    assert set(layout["node"]) == {"A", "B", "C"}
    assert len(fig.data) == 4
    assert all(trace.type == "scatter" for trace in fig.data)


def test_advanced_stats_return_stable_empty_shapes():
    empty = pd.DataFrame({"x": [], "y": []})

    dot_data, dot_mapping = stat_bindot(mapping={"x": "x"}).compute(empty)
    assert list(dot_data.columns) == ["x", "y", "count"]
    assert dot_mapping["size"] == "count"

    density_data, density_mapping = stat_density_2d(mapping={"x": "x", "y": "y"}).compute(empty)
    assert list(density_data.columns) == ["x", "y", "density"]
    assert density_mapping["z"] == "density"

    halfeye_data, halfeye_mapping = stat_halfeye(mapping={"x": "x", "y": "y"}).compute(empty)
    assert {"group", "value", "density", "kind"}.issubset(halfeye_data.columns)
    assert halfeye_mapping["fill"] == "density"
