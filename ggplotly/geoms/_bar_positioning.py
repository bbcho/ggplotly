from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

from ..positions import position_dodge, position_dodge2, position_fill, position_identity, position_stack


@dataclass(frozen=True)
class BarTraceSpec:
    x: tuple[Any, ...]
    y: tuple[Any, ...]
    name: str
    fill: Any
    outline: Any | None
    width: Any
    offsetgroup: str | None
    legendgroup: str


@dataclass(frozen=True)
class BarPositionResult:
    traces: tuple[BarTraceSpec, ...]
    barmode: str
    yaxis_range: tuple[float, float] | None = None


def resolve_bar_position_kind(position: Any) -> str:
    if position is None:
        return "stack"
    if isinstance(position, str):
        aliases = {"stack": "stack", "dodge": "dodge", "fill": "fill", "identity": "identity"}
        return aliases.get(position, position)
    if isinstance(position, position_fill):
        return "fill"
    if isinstance(position, (position_dodge, position_dodge2)):
        return "dodge"
    if isinstance(position, position_stack):
        return "stack"
    if isinstance(position, position_identity):
        return "identity"
    return "stack"


def compute_bar_trace_specs(
    data: pd.DataFrame,
    mapping: dict[str, Any],
    params: dict[str, Any],
    style_props: dict[str, Any],
    default_name: str,
) -> BarPositionResult:
    x_col = mapping.get("x")
    y_col = mapping.get("y", "count")
    if x_col is None or y_col is None:
        raise ValueError("bar geoms require x and y values after stat computation")

    position_kind = resolve_bar_position_kind(params.get("position"))
    barmode = {
        "dodge": "group",
        "identity": "overlay",
        "fill": "relative",
        "stack": "relative",
    }.get(position_kind, "relative")

    group_col = _first_grouping_column(mapping, data)
    width = params.get("width", 0.9)

    if group_col is None:
        y_values = _normalize_single_stack(data[y_col]) if position_kind == "fill" else data[y_col]
        fill = _literal_fill(style_props)
        outline = _literal_outline(style_props)
        return BarPositionResult(
            traces=(
                BarTraceSpec(
                    x=tuple(data[x_col]),
                    y=tuple(y_values),
                    name=params.get("name", default_name),
                    fill=fill,
                    outline=outline,
                    width=_bar_width(data, width),
                    offsetgroup=None,
                    legendgroup=params.get("name", default_name),
                ),
            ),
            barmode=barmode,
            yaxis_range=(0.0, 1.0) if position_kind == "fill" else None,
        )

    traces = []
    group_values = _group_values(data[group_col], style_props, group_col, mapping)
    working = data.copy()
    if position_kind == "fill":
        totals = working.groupby(x_col, dropna=False)[y_col].transform("sum")
        working[y_col] = working[y_col] / totals.where(totals != 0, 1)

    for group_value in group_values:
        subset = working[working[group_col] == group_value]
        if subset.empty:
            continue

        name = str(group_value)
        traces.append(
            BarTraceSpec(
                x=tuple(subset[x_col]),
                y=tuple(subset[y_col]),
                name=name,
                fill=_fill_for_group(group_value, style_props),
                outline=_outline_for_group(group_value, style_props),
                width=_bar_width(subset, width),
                offsetgroup=name if position_kind == "dodge" else None,
                legendgroup=name,
            )
        )

    return BarPositionResult(
        traces=tuple(traces),
        barmode=barmode,
        yaxis_range=(0.0, 1.0) if position_kind == "fill" else None,
    )


def _first_grouping_column(mapping: dict[str, Any], data: pd.DataFrame) -> str | None:
    for aesthetic in ("fill", "color", "group"):
        value = mapping.get(aesthetic)
        if isinstance(value, str) and value in data.columns:
            return value
    return None


def _group_values(series: pd.Series, style_props: dict[str, Any], group_col: str, mapping: dict[str, Any]) -> tuple[Any, ...]:
    if mapping.get("fill") == group_col and style_props.get("fill_map"):
        return tuple(style_props["fill_map"].keys())
    if mapping.get("color") == group_col and style_props.get("color_map"):
        return tuple(style_props["color_map"].keys())
    return tuple(series.drop_duplicates())


def _literal_fill(style_props: dict[str, Any]) -> Any:
    fill = style_props.get("fill")
    if style_props.get("fill_series") is None and fill is not None:
        return fill
    return style_props["default_color"]


def _literal_outline(style_props: dict[str, Any]) -> Any | None:
    color = style_props.get("color")
    if style_props.get("color_series") is None and color is not None:
        return color
    return None


def _fill_for_group(group_value: Any, style_props: dict[str, Any]) -> Any:
    if style_props.get("fill_series") is not None and style_props.get("fill_map"):
        return style_props["fill_map"].get(group_value, style_props["default_color"])
    if style_props.get("fill_series") is None and style_props.get("fill") is not None:
        return style_props["fill"]
    return style_props["default_color"]


def _outline_for_group(group_value: Any, style_props: dict[str, Any]) -> Any | None:
    if style_props.get("color_series") is not None and style_props.get("color_map"):
        return style_props["color_map"].get(group_value)
    if style_props.get("color_series") is None and style_props.get("color") is not None:
        return style_props["color"]
    return None


def _bar_width(data: pd.DataFrame, width: Any) -> Any:
    if "width" in data.columns:
        return tuple(data["width"])
    return width


def _normalize_single_stack(values: pd.Series) -> pd.Series:
    totals = values.where(values != 0, 1)
    return values / totals
