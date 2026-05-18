"""Extension-style geoms that build on the core grammar."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
import plotly.graph_objects as go

from ..aes import aes
from ..positions import position_beeswarm, position_quasirandom
from ..stats.stat_advanced import (
    stat_bin2d,
    stat_bin_hex,
    stat_bindot,
    stat_density_2d,
    stat_density_2d_filled,
    stat_halfeye,
    stat_mosaic,
    stat_sum,
)
from .geom_bar import geom_bar
from .geom_base import Geom
from .geom_col import geom_col
from .geom_label import geom_label
from .geom_text import geom_text
from .geom_tile import geom_tile


def _line_color(style_props, params, default="#1f77b4"):
    return params.get("color") or style_props.get("color") or style_props.get("default_color") or default


def _fill_color(style_props, params, default="#1f77b4"):
    return params.get("fill") or style_props.get("fill") or params.get("color") or style_props.get("default_color") or default


def _category_positions(values):
    categories = _ordered_unique(values)
    category_index = {value: i for i, value in enumerate(categories)}
    return pd.Series(values.map(category_index), index=values.index), categories


def _ordered_unique(values):
    return list(pd.Series(values).dropna().unique())


def _with_names(fig, axis, tickvals, ticktext):
    updater = fig.update_xaxes if axis == "x" else fig.update_yaxes
    updater(tickmode="array", tickvals=tickvals, ticktext=ticktext)


class geom_linerange(Geom):
    """Draw vertical intervals from ymin to ymax at x."""

    required_aes = ["x", "ymin", "ymax"]
    default_params = {"size": 2}

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        x = data[self.mapping["x"]]
        ymin = data[self.mapping["ymin"]]
        ymax = data[self.mapping["ymax"]]
        color = _line_color(style, self.params)
        for i, idx in enumerate(data.index):
            fig.add_trace(
                go.Scatter(
                    x=[x.loc[idx], x.loc[idx]],
                    y=[ymin.loc[idx], ymax.loc[idx]],
                    mode="lines",
                    line=dict(color=color, width=self.params.get("size", 2), dash=style["linetype"]),
                    name=self.params.get("name", "Linerange"),
                    showlegend=self._show_legend() and i == 0,
                    legendgroup="linerange",
                    opacity=style["alpha"],
                ),
                row=row,
                col=col,
            )


class geom_pointrange(geom_linerange):
    """Draw vertical intervals with a point at y."""

    required_aes = ["x", "y", "ymin", "ymax"]

    def _draw_impl(self, fig, data, row, col):
        super()._draw_impl(fig, data, row, col)
        style = self._get_style_props(data)
        color = _line_color(style, self.params)
        fig.add_trace(
            go.Scatter(
                x=data[self.mapping["x"]],
                y=data[self.mapping["y"]],
                mode="markers",
                marker=dict(color=color, size=self.params.get("point_size", self.params.get("size", 8))),
                name=self.params.get("name", "Pointrange"),
                showlegend=False,
                opacity=style["alpha"],
            ),
            row=row,
            col=col,
        )


class geom_crossbar(Geom):
    """Draw a range box with a horizontal middle bar."""

    required_aes = ["x", "y", "ymin", "ymax"]
    default_params = {"width": 0.5, "size": 1}

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        color = _line_color(style, self.params, "black")
        fill = _fill_color(style, self.params, "rgba(31,119,180,0.25)")
        width = self.params.get("width", 0.5)
        for i, idx in enumerate(data.index):
            x = data.loc[idx, self.mapping["x"]]
            y = data.loc[idx, self.mapping["y"]]
            ymin = data.loc[idx, self.mapping["ymin"]]
            ymax = data.loc[idx, self.mapping["ymax"]]
            fig.add_trace(
                go.Scatter(
                    x=[x - width / 2, x + width / 2, x + width / 2, x - width / 2, x - width / 2],
                    y=[ymin, ymin, ymax, ymax, ymin],
                    mode="lines",
                    fill="toself",
                    fillcolor=fill,
                    line=dict(color=color, width=self.params.get("size", 1)),
                    name=self.params.get("name", "Crossbar"),
                    showlegend=self._show_legend() and i == 0,
                    legendgroup="crossbar",
                    opacity=style["alpha"],
                ),
                row=row,
                col=col,
            )
            fig.add_trace(
                go.Scatter(
                    x=[x - width / 2, x + width / 2],
                    y=[y, y],
                    mode="lines",
                    line=dict(color=color, width=self.params.get("size", 1)),
                    showlegend=False,
                ),
                row=row,
                col=col,
            )


class geom_errorbarh(Geom):
    """Draw horizontal error bars."""

    required_aes = ["x", "y"]
    default_params = {"height": 4}

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        x = data[self.mapping["x"]]
        y = data[self.mapping["y"]]
        if "xerr" in self.mapping:
            xerr = data[self.mapping["xerr"]]
            xmin = x - xerr
            xmax = x + xerr
        else:
            xmin = data[self.mapping["xmin"]]
            xmax = data[self.mapping["xmax"]]
        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                error_x=dict(
                    type="data",
                    array=xmax - x,
                    arrayminus=x - xmin,
                    width=self.params.get("height", 4),
                ),
                marker_color=_line_color(style, self.params),
                opacity=style["alpha"],
                name=self.params.get("name", "Errorbarh"),
                showlegend=self._show_legend(),
            ),
            row=row,
            col=col,
        )


class geom_freqpoly(Geom):
    """Draw frequency polygons from binned x values."""

    required_aes = ["x"]
    default_params = {"bins": 30, "size": 2}

    def _draw_impl(self, fig, data, row, col):
        x_col = self.mapping["x"]
        groups = [(None, data)]
        group_col = self.mapping.get("color") or self.mapping.get("group")
        if group_col in data.columns:
            groups = data.groupby(group_col)
        style = self._get_style_props(data)
        for group, frame in groups:
            values = pd.to_numeric(frame[x_col], errors="coerce").dropna()
            counts, edges = np.histogram(values, bins=self.params.get("bins", 30))
            centers = (edges[:-1] + edges[1:]) / 2
            trace_props = self._apply_color_targets(dict(color="line_color"), style, value_key=group)
            fig.add_trace(
                go.Scatter(
                    x=centers,
                    y=counts,
                    mode="lines",
                    line_width=self.params.get("size", 2),
                    name=str(group) if group is not None else self.params.get("name", "Freqpoly"),
                    showlegend=self._show_legend(),
                    **trace_props,
                ),
                row=row,
                col=col,
            )


class geom_dotplot(Geom):
    """Draw stacked dot plots."""

    required_aes = ["x"]

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_bindot(mapping=self.mapping, bins=self.params.get("bins", 30)))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        fig.add_trace(
            go.Scatter(
                x=data[self.mapping["x"]],
                y=data[self.mapping["y"]],
                mode="markers",
                marker=dict(
                    color=_line_color(style, self.params),
                    size=self.params.get("dotsize", 8),
                ),
                name=self.params.get("name", "Dotplot"),
                showlegend=self._show_legend(),
                opacity=style["alpha"],
            ),
            row=row,
            col=col,
        )


class geom_count(Geom):
    """Draw points sized by duplicate x/y count."""

    required_aes = ["x", "y"]

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_sum(mapping=self.mapping))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        n = pd.to_numeric(data.get("n", pd.Series([1] * len(data))), errors="coerce").fillna(1)
        size = 6 + 18 * (n - n.min()) / ((n.max() - n.min()) or 1)
        fig.add_trace(
            go.Scatter(
                x=data[self.mapping["x"]],
                y=data[self.mapping["y"]],
                mode="markers",
                marker=dict(color=_line_color(style, self.params), size=size),
                name=self.params.get("name", "Count"),
                showlegend=self._show_legend(),
                opacity=style["alpha"],
            ),
            row=row,
            col=col,
        )


class geom_bin2d(Geom):
    """Draw rectangular 2D bin counts."""

    required_aes = ["x", "y"]

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_bin2d(mapping=self.mapping, bins=self.params.get("bins", 30)))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        pivot = data.pivot_table(index="y", columns="x", values="count", aggfunc="sum")
        fig.add_trace(
            go.Heatmap(
                x=list(pivot.columns),
                y=list(pivot.index),
                z=pivot.values,
                colorscale=self.params.get("palette", "Viridis"),
                colorbar=dict(title=self.params.get("name", "count")),
                name=self.params.get("name", "Bin2d"),
            ),
            row=row,
            col=col,
        )


class geom_hex(geom_bin2d):
    """Draw approximate hexagonal bin counts."""

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_bin_hex(mapping=self.mapping, bins=self.params.get("bins", 30)))
        return Geom._apply_stats(self, data)

    def _draw_impl(self, fig, data, row, col):
        count = pd.to_numeric(data["count"], errors="coerce").fillna(0)
        size = 8 + 22 * (count - count.min()) / ((count.max() - count.min()) or 1)
        fig.add_trace(
            go.Scatter(
                x=data["x"],
                y=data["y"],
                mode="markers",
                marker=dict(
                    symbol="hexagon",
                    size=size,
                    color=count,
                    colorscale=self.params.get("palette", "Viridis"),
                    showscale=True,
                    colorbar=dict(title="count"),
                ),
                name=self.params.get("name", "Hex"),
                showlegend=False,
            ),
            row=row,
            col=col,
        )


class geom_raster(geom_tile):
    """Raster-like tile plot; implemented as contiguous Plotly heatmap cells."""


class geom_slabinterval(Geom):
    """Draw half-eye slab intervals."""

    required_aes = ["x", "y"]

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_halfeye(mapping=self.mapping, **self.params))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        if data.empty:
            return
        alpha = self.params.get("alpha", 0.45)
        groups = [g for g in data["group"].dropna().unique()]
        if not groups:
            groups = [None]
        for group_index, group in enumerate(groups):
            slab = data[(data["group"] == group) & (data["kind"] == "slab")] if group is not None else data[data["kind"] == "slab"]
            intervals = data[(data["group"] == group) & (data["kind"] == "interval")] if group is not None else data[data["kind"] == "interval"]
            if slab.empty:
                continue
            x_base = group_index + 1
            x_shape = x_base + slab["density"] * self.params.get("scale", 0.35)
            fig.add_trace(
                go.Scatter(
                    x=list([x_base] * len(slab)) + list(x_shape[::-1]),
                    y=list(slab["value"]) + list(slab["value"][::-1]),
                    mode="lines",
                    fill="toself",
                    fillcolor=self.params.get("fill", "rgba(31,119,180,0.35)"),
                    line=dict(color=self.params.get("color", "#1f77b4")),
                    opacity=alpha,
                    name=str(group),
                    showlegend=self._show_legend(),
                ),
                row=row,
                col=col,
            )
            for _, interval in intervals.iterrows():
                fig.add_trace(
                    go.Scatter(
                        x=[x_base, x_base],
                        y=[interval["lower"], interval["upper"]],
                        mode="lines+markers",
                        marker=dict(size=6),
                        line=dict(color=self.params.get("interval_color", "black"), width=2),
                        showlegend=False,
                    ),
                    row=row,
                    col=col,
                )
        _with_names(fig, "x", list(range(1, len(groups) + 1)), [str(g) for g in groups])


class geom_density_ridges(Geom):
    """Draw ridgeline densities by group."""

    required_aes = ["x", "y"]

    def _draw_impl(self, fig, data, row, col):
        x_col = self.mapping["x"]
        y_col = self.mapping["y"]
        categories = _ordered_unique(data[y_col])
        colors = self.params.get("colors")
        for i, category in enumerate(categories):
            values = pd.to_numeric(data.loc[data[y_col] == category, x_col], errors="coerce").dropna()
            if len(values) < 2 or values.std() == 0:
                continue
            grid = np.linspace(values.min(), values.max(), self.params.get("n", 256))
            from scipy.stats import gaussian_kde
            density = gaussian_kde(values)(grid)
            density = density / density.max() * self.params.get("scale", 0.8)
            baseline = i
            upper = baseline + density
            fig.add_trace(
                go.Scatter(
                    x=list(grid) + list(grid[::-1]),
                    y=list(upper) + [baseline] * len(grid),
                    mode="lines",
                    fill="toself",
                    fillcolor=(colors[i % len(colors)] if colors else self.params.get("fill", "rgba(31,119,180,0.35)")),
                    line=dict(color=self.params.get("color", "#1f77b4")),
                    name=str(category),
                    showlegend=self._show_legend(),
                ),
                row=row,
                col=col,
            )
        _with_names(fig, "y", list(range(len(categories))), [str(c) for c in categories])


class geom_text_repel(geom_text):
    """Text labels with deterministic point-index offsets to reduce overlap."""

    def _draw_impl(self, fig, data, row, col):
        frame = data.copy()
        x_col = self.mapping["x"]
        y_col = self.mapping["y"]
        radius = self.params.get("force", 0.08)
        angles = np.linspace(0, 2 * np.pi, len(frame), endpoint=False)
        frame[x_col] = frame[x_col] + np.cos(angles) * radius
        frame[y_col] = frame[y_col] + np.sin(angles) * radius
        super()._draw_impl(fig, frame, row, col)


class geom_label_repel(geom_label):
    """Label boxes with deterministic point-index offsets to reduce overlap."""

    def _draw_impl(self, fig, data, row, col):
        frame = data.copy()
        x_col = self.mapping["x"]
        y_col = self.mapping["y"]
        radius = self.params.get("force", 0.08)
        angles = np.linspace(0, 2 * np.pi, len(frame), endpoint=False)
        frame[x_col] = frame[x_col] + np.cos(angles) * radius
        frame[y_col] = frame[y_col] + np.sin(angles) * radius
        super()._draw_impl(fig, frame, row, col)


class geom_textpath(Geom):
    """Draw a line and place labels along path midpoints."""

    required_aes = ["x", "y", "label"]

    def _draw_impl(self, fig, data, row, col):
        group_col = self.mapping.get("group")
        groups = [(None, data)] if group_col not in data else data.groupby(group_col)
        color = self.params.get("color", "#1f77b4")
        for group, frame in groups:
            frame = frame.sort_values(self.mapping["x"])
            fig.add_trace(
                go.Scatter(
                    x=frame[self.mapping["x"]],
                    y=frame[self.mapping["y"]],
                    mode="lines",
                    line=dict(color=color, width=self.params.get("size", 2)),
                    name=str(group) if group is not None else self.params.get("name", "Textpath"),
                    showlegend=self._show_legend(),
                ),
                row=row,
                col=col,
            )
            mid = frame.iloc[len(frame) // 2]
            fig.add_annotation(
                x=mid[self.mapping["x"]],
                y=mid[self.mapping["y"]],
                text=str(mid[self.mapping["label"]]),
                showarrow=False,
                font=dict(color=color, size=self.params.get("text_size", 12)),
                row=row,
                col=col,
            )


class geom_labelpath(geom_textpath):
    """Textpath with a light label background."""

    def _draw_impl(self, fig, data, row, col):
        super()._draw_impl(fig, data, row, col)
        for annotation in fig.layout.annotations[-1:]:
            annotation.bgcolor = self.params.get("fill", "white")
            annotation.bordercolor = self.params.get("color", "#1f77b4")


class geom_alluvium(Geom):
    """Draw categorical alluvial paths across ordered x stages."""

    required_aes = ["x", "stratum", "alluvium"]

    def _draw_impl(self, fig, data, row, col):
        x_col = self.mapping["x"]
        stratum_col = self.mapping["stratum"]
        alluvium_col = self.mapping["alluvium"]
        stages = _ordered_unique(data[x_col])
        strata = _ordered_unique(data[stratum_col])
        stage_pos = {stage: i for i, stage in enumerate(stages)}
        stratum_pos = {stratum: i for i, stratum in enumerate(strata)}
        for alluvium, frame in data.groupby(alluvium_col):
            frame = frame.sort_values(x_col, key=lambda s: s.map(stage_pos))
            fig.add_trace(
                go.Scatter(
                    x=[stage_pos[v] for v in frame[x_col]],
                    y=[stratum_pos[v] for v in frame[stratum_col]],
                    mode="lines",
                    line=dict(width=self.params.get("size", 10), color=self.params.get("color", "rgba(31,119,180,0.25)")),
                    opacity=self.params.get("alpha", 0.35),
                    name=str(alluvium),
                    showlegend=False,
                ),
                row=row,
                col=col,
            )
        _with_names(fig, "x", list(range(len(stages))), [str(v) for v in stages])
        _with_names(fig, "y", list(range(len(strata))), [str(v) for v in strata])


class geom_stratum(Geom):
    """Draw stacked stratum blocks for alluvial examples."""

    required_aes = ["x", "stratum"]

    def _draw_impl(self, fig, data, row, col):
        counts = data.groupby([self.mapping["x"], self.mapping["stratum"]]).size().reset_index(name="count")
        for stratum, frame in counts.groupby(self.mapping["stratum"]):
            fig.add_trace(
                go.Bar(
                    x=frame[self.mapping["x"]],
                    y=frame["count"],
                    name=str(stratum),
                    opacity=self.params.get("alpha", 0.7),
                ),
                row=row,
                col=col,
            )
        fig.update_layout(barmode="stack")


class geom_mosaic(Geom):
    """Draw mosaic rectangles for two categorical variables."""

    required_aes = ["x"]

    def _apply_stats(self, data):
        if not self.stats:
            self.stats.append(stat_mosaic(mapping=self.mapping))
        return super()._apply_stats(data)

    def _draw_impl(self, fig, data, row, col):
        style = self._get_style_props(data)
        for i, (_, cell) in enumerate(data.iterrows()):
            fill = self._apply_color_targets(dict(fill="fillcolor"), style, value_key=cell.get("fill")).get(
                "fillcolor",
                "#1f77b4",
            )
            fig.add_trace(
                go.Scatter(
                    x=[cell["xmin"], cell["xmax"], cell["xmax"], cell["xmin"], cell["xmin"]],
                    y=[cell["ymin"], cell["ymin"], cell["ymax"], cell["ymax"], cell["ymin"]],
                    mode="lines",
                    fill="toself",
                    fillcolor=fill,
                    line=dict(color="white", width=1),
                    name=str(cell.get("fill", "Mosaic")),
                    showlegend=self._show_legend() and i == 0,
                ),
                row=row,
                col=col,
            )


class geom_beeswarm(Geom):
    """Categorical scatter with deterministic beeswarm packing."""

    required_aes = ["x", "y"]

    def _draw_impl(self, fig, data, row, col):
        frame = data.copy()
        x_codes, categories = _category_positions(frame[self.mapping["x"]])
        x_adj, y_adj = position_beeswarm(width=self.params.get("width", 0.4)).adjust(
            x_codes,
            frame[self.mapping["y"]],
            group=x_codes,
        )
        style = self._get_style_props(data)
        fig.add_trace(
            go.Scatter(
                x=x_adj,
                y=y_adj,
                mode="markers",
                marker=dict(color=_line_color(style, self.params), size=self.params.get("size", 7)),
                name=self.params.get("name", "Beeswarm"),
                showlegend=self._show_legend(),
                opacity=style["alpha"],
            ),
            row=row,
            col=col,
        )
        _with_names(fig, "x", list(range(len(categories))), [str(c) for c in categories])


class geom_quasirandom(geom_beeswarm):
    """Alias for deterministic quasirandom categorical point packing."""

    def _draw_impl(self, fig, data, row, col):
        frame = data.copy()
        x_codes, categories = _category_positions(frame[self.mapping["x"]])
        x_adj, y_adj = position_quasirandom(width=self.params.get("width", 0.4)).adjust(
            x_codes,
            frame[self.mapping["y"]],
            group=x_codes,
        )
        style = self._get_style_props(data)
        fig.add_trace(
            go.Scatter(
                x=x_adj,
                y=y_adj,
                mode="markers",
                marker=dict(color=_line_color(style, self.params), size=self.params.get("size", 7)),
                name=self.params.get("name", "Quasirandom"),
                showlegend=self._show_legend(),
                opacity=style["alpha"],
            ),
            row=row,
            col=col,
        )
        _with_names(fig, "x", list(range(len(categories))), [str(c) for c in categories])


class geom_col_pattern(geom_col):
    """Column geom with Plotly marker patterns."""

    default_params = {**geom_col.default_params, "pattern": "/"}


class geom_bar_pattern(geom_bar):
    """Bar geom with Plotly marker patterns."""

    default_params = {"pattern": "/"}


class geom_tile_pattern(geom_tile):
    """Tile geom alias that accepts pattern parameters for API parity."""


class graph_layout:
    """Compute deterministic node coordinates for graph geoms."""

    def __init__(self, layout="spring", seed=1, **kwargs):
        self.layout = layout
        self.seed = seed
        self.kwargs = kwargs

    def compute(self, edges, source="from", target="to"):
        try:
            import networkx as nx
        except ImportError as exc:
            raise ImportError("graph_layout requires networkx") from exc
        graph = nx.from_pandas_edgelist(edges, source=source, target=target)
        if self.layout == "circular":
            positions = nx.circular_layout(graph)
        elif self.layout == "kamada_kawai":
            positions = nx.kamada_kawai_layout(graph)
        else:
            positions = nx.spring_layout(graph, seed=self.seed, **self.kwargs)
        return pd.DataFrame([
            {"node": node, "x": xy[0], "y": xy[1]}
            for node, xy in positions.items()
        ])


class geom_edge_link(Geom):
    """Draw graph edges from an edge list with from/to columns."""

    required_aes = []

    def _draw_impl(self, fig, data, row, col):
        source_col = self.mapping.get("from", "from")
        target_col = self.mapping.get("to", "to")
        layout = self.params.get("layout") or graph_layout()
        nodes = layout.compute(data, source=source_col, target=target_col)
        pos = nodes.set_index("node")[["x", "y"]].to_dict("index")
        for i, edge in data.iterrows():
            start = pos[edge[source_col]]
            end = pos[edge[target_col]]
            fig.add_trace(
                go.Scatter(
                    x=[start["x"], end["x"]],
                    y=[start["y"], end["y"]],
                    mode="lines",
                    line=dict(color=self.params.get("color", "rgba(80,80,80,0.35)"), width=self.params.get("size", 1)),
                    showlegend=False,
                    name=self.params.get("name", "Edge"),
                ),
                row=row,
                col=col,
            )


class geom_node_point(Geom):
    """Draw graph nodes from a node layout dataframe."""

    required_aes = ["x", "y"]

    def _draw_impl(self, fig, data, row, col):
        label_col = self.mapping.get("label")
        style = self._get_style_props(data)
        fig.add_trace(
            go.Scatter(
                x=data[self.mapping["x"]],
                y=data[self.mapping["y"]],
                mode="markers",
                text=data[label_col] if label_col in data else None,
                marker=dict(color=_line_color(style, self.params), size=self.params.get("size", 10)),
                name=self.params.get("name", "Node"),
                showlegend=self._show_legend(),
            ),
            row=row,
            col=col,
        )


class geom_node_text(geom_text):
    """Text labels for graph nodes."""


def geom_dotsinterval(data=None, mapping=None, **params):
    """Convenience wrapper for dot-interval summaries."""
    geom = geom_slabinterval(data=data, mapping=mapping, **params)
    return geom
