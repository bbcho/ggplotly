from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass(frozen=True)
class GeoTilePolygonSpec:
    lon: tuple[float, ...]
    lat: tuple[float, ...]
    fill: str
    z: Any
    name: str


def has_geo_context(fig) -> bool:
    return any(
        hasattr(trace, "type") and trace.type in ("choropleth", "scattergeo")
        for trace in fig.data
    )


def infer_tile_polygons(x: pd.Series, y: pd.Series, fills: pd.Series, colors: pd.Series) -> tuple[GeoTilePolygonSpec, ...]:
    x_half = _half_spacing(x)
    y_half = _half_spacing(y)
    specs = []
    for idx in x.index:
        lon = float(x.loc[idx])
        lat = float(y.loc[idx])
        specs.append(
            GeoTilePolygonSpec(
                lon=(lon - x_half, lon + x_half, lon + x_half, lon - x_half, lon - x_half),
                lat=(lat - y_half, lat - y_half, lat + y_half, lat + y_half, lat - y_half),
                fill=str(colors.loc[idx]),
                z=fills.loc[idx],
                name=str(fills.loc[idx]),
            )
        )
    return tuple(specs)


def _half_spacing(values: pd.Series) -> float:
    unique = pd.Series(values.dropna().unique()).sort_values()
    if len(unique) < 2:
        return 0.5
    diffs = unique.diff().dropna()
    positive = diffs[diffs > 0]
    if positive.empty:
        return 0.5
    return float(positive.min()) / 2
