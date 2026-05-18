"""Advanced statistical transforms used by extension-style geoms."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats as scipy_stats
from scipy.stats import gaussian_kde

from .stat_base import Stat


def _clean_numeric(data, columns, na_rm=False):
    frame = data.copy()
    if na_rm:
        frame = frame.dropna(subset=columns)
    for column in columns:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame.dropna(subset=columns)


def _bin_edges(values, bins=30, binwidth=None):
    values = pd.to_numeric(pd.Series(values), errors="coerce").dropna()
    if values.empty:
        return np.array([0, 1], dtype=float)
    lower = float(values.min())
    upper = float(values.max())
    if lower == upper:
        lower -= 0.5
        upper += 0.5
    if binwidth is not None:
        count = max(int(math.ceil((upper - lower) / binwidth)), 1)
        return lower + np.arange(count + 1) * binwidth
    return np.linspace(lower, upper, int(bins) + 1)


class stat_bin2d(Stat):
    """Count observations in rectangular x/y bins."""

    __name__ = "bin2d"

    def __init__(self, data=None, mapping=None, bins=30, binwidth=None, na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.bins = bins
        self.binwidth = binwidth
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        if x_col is None or y_col is None:
            raise ValueError("stat_bin2d requires x and y aesthetics")

        frame = _clean_numeric(data, [x_col, y_col], self.na_rm)
        if frame.empty:
            return pd.DataFrame(columns=["x", "y", "xmin", "xmax", "ymin", "ymax", "count", "density"]), {
                "x": "x",
                "y": "y",
                "fill": "count",
            }

        if isinstance(self.bins, (tuple, list)):
            x_bins, y_bins = self.bins
        else:
            x_bins = y_bins = self.bins
        if isinstance(self.binwidth, (tuple, list)):
            x_width, y_width = self.binwidth
        else:
            x_width = y_width = self.binwidth

        x_edges = _bin_edges(frame[x_col], x_bins, x_width)
        y_edges = _bin_edges(frame[y_col], y_bins, y_width)
        counts, x_edges, y_edges = np.histogram2d(frame[x_col], frame[y_col], bins=[x_edges, y_edges])
        total = counts.sum() or 1

        rows = []
        for xi in range(len(x_edges) - 1):
            for yi in range(len(y_edges) - 1):
                count = float(counts[xi, yi])
                rows.append({
                    "x": (x_edges[xi] + x_edges[xi + 1]) / 2,
                    "y": (y_edges[yi] + y_edges[yi + 1]) / 2,
                    "xmin": x_edges[xi],
                    "xmax": x_edges[xi + 1],
                    "ymin": y_edges[yi],
                    "ymax": y_edges[yi + 1],
                    "count": count,
                    "density": count / total,
                })
        return pd.DataFrame(rows), {"x": "x", "y": "y", "fill": "count"}


class stat_bin_hex(stat_bin2d):
    """Count observations in approximate hexagonal bins."""

    __name__ = "bin_hex"

    def compute(self, data):
        result, mapping = super().compute(data)
        if result.empty:
            return result.assign(radius=[]), mapping
        x_step = float((result["xmax"] - result["xmin"]).replace(0, np.nan).dropna().median() or 1)
        y_step = float((result["ymax"] - result["ymin"]).replace(0, np.nan).dropna().median() or 1)
        result["x"] = result["x"] + (result.groupby("y").ngroup() % 2) * x_step * 0.5
        result["radius"] = min(abs(x_step), abs(y_step)) * 0.45
        return result, mapping


class stat_bindot(Stat):
    """Bin x values and stack dots by count."""

    __name__ = "bindot"

    def __init__(self, data=None, mapping=None, bins=30, binwidth=None, stackdir="up",
                 dotsize=1, na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.bins = bins
        self.binwidth = binwidth
        self.stackdir = stackdir
        self.dotsize = dotsize
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        if x_col is None:
            raise ValueError("stat_bindot requires x aesthetic")
        frame = _clean_numeric(data, [x_col], self.na_rm)
        if frame.empty:
            return pd.DataFrame(columns=["x", "y", "count"]), {"x": "x", "y": "y", "size": "count"}
        edges = _bin_edges(frame[x_col], self.bins, self.binwidth)
        counts, edges = np.histogram(frame[x_col], bins=edges)
        centers = (edges[:-1] + edges[1:]) / 2
        rows = []
        direction = -1 if self.stackdir in ("down", "centerwhole", "center") else 1
        for center, count in zip(centers, counts):
            for rank in range(int(count)):
                rows.append({"x": center, "y": direction * (rank + 1), "count": count})
        return pd.DataFrame(rows, columns=["x", "y", "count"]), {"x": "x", "y": "y", "size": "count"}


class stat_sum(Stat):
    """Count duplicated x/y observations for count plots."""

    __name__ = "sum"

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        if x_col is None or y_col is None:
            raise ValueError("stat_sum requires x and y aesthetics")
        group_cols = [x_col, y_col]
        result = data.groupby(group_cols, dropna=False).size().reset_index(name="n")
        result["prop"] = result["n"] / result["n"].sum()
        return result, {**self.mapping, "size": "n"}


class stat_density_2d(Stat):
    """Compute a 2D kernel density grid."""

    __name__ = "density_2d"

    def __init__(self, data=None, mapping=None, n=80, contour=True, na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.n = n
        self.contour = contour
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        if x_col is None or y_col is None:
            raise ValueError("stat_density_2d requires x and y aesthetics")
        frame = _clean_numeric(data, [x_col, y_col], self.na_rm)
        if len(frame) < 3:
            return pd.DataFrame(columns=["x", "y", "density"]), {"x": "x", "y": "y", "z": "density"}
        x = frame[x_col].to_numpy()
        y = frame[y_col].to_numpy()
        xx, yy = np.mgrid[x.min():x.max():complex(self.n), y.min():y.max():complex(self.n)]
        try:
            kde = gaussian_kde(np.vstack([x, y]))
        except Exception:
            return pd.DataFrame(columns=["x", "y", "density"]), {"x": "x", "y": "y", "z": "density"}
        density = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
        return pd.DataFrame({"x": xx.ravel(), "y": yy.ravel(), "density": density.ravel()}), {
            "x": "x",
            "y": "y",
            "z": "density",
            "fill": "density",
        }


class stat_density_2d_filled(stat_density_2d):
    """Filled 2D density grid."""

    __name__ = "density_2d_filled"


class stat_ellipse(Stat):
    """Compute covariance ellipse paths for grouped x/y observations."""

    __name__ = "ellipse"

    def __init__(self, data=None, mapping=None, level=0.95, segments=100, na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.level = level
        self.segments = segments
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        group_col = self.mapping.get("group") or self.mapping.get("color")
        if x_col is None or y_col is None:
            raise ValueError("stat_ellipse requires x and y aesthetics")
        frame = _clean_numeric(data, [x_col, y_col], self.na_rm)
        groups = [(None, frame)] if group_col is None or group_col not in frame else frame.groupby(group_col)
        theta = np.linspace(0, 2 * np.pi, self.segments)
        circle = np.vstack([np.cos(theta), np.sin(theta)])
        scale = math.sqrt(scipy_stats.chi2.ppf(self.level, 2))
        rows = []
        for group, group_frame in groups:
            if len(group_frame) < 3:
                continue
            points = group_frame[[x_col, y_col]].to_numpy().T
            center = points.mean(axis=1)
            cov = np.cov(points)
            values, vectors = np.linalg.eigh(cov)
            transform = vectors @ np.diag(np.sqrt(np.maximum(values, 0)) * scale)
            ellipse = (transform @ circle).T + center
            for x_val, y_val in ellipse:
                row = {"x": x_val, "y": y_val}
                if group_col is not None:
                    row[group_col] = group
                rows.append(row)
        mapping = {"x": "x", "y": "y"}
        if group_col is not None:
            mapping["group"] = group_col
        return pd.DataFrame(rows), mapping


class stat_quantile(Stat):
    """Fit linear quantile regression lines."""

    __name__ = "quantile"

    def __init__(self, data=None, mapping=None, quantiles=(0.25, 0.5, 0.75), n=100,
                 na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.quantiles = quantiles
        self.n = n
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        if x_col is None or y_col is None:
            raise ValueError("stat_quantile requires x and y aesthetics")
        frame = _clean_numeric(data, [x_col, y_col], self.na_rm)
        if len(frame) < 2:
            return pd.DataFrame(columns=["x", "y", "quantile"]), {"x": "x", "y": "y", "group": "quantile"}
        x_grid = np.linspace(frame[x_col].min(), frame[x_col].max(), self.n)
        rows = []
        for q in self.quantiles:
            try:
                import statsmodels.api as sm
                model = sm.QuantReg(frame[y_col], sm.add_constant(frame[x_col])).fit(q=q)
                y_grid = model.params.iloc[0] + model.params.iloc[1] * x_grid
            except Exception:
                slope, intercept = np.polyfit(frame[x_col], frame[y_col], 1)
                offset = frame[y_col].quantile(q) - frame[y_col].median()
                y_grid = slope * x_grid + intercept + offset
            for x_val, y_val in zip(x_grid, y_grid):
                rows.append({"x": x_val, "y": y_val, "quantile": str(q)})
        return pd.DataFrame(rows), {"x": "x", "y": "y", "group": "quantile", "color": "quantile"}


class stat_summary_bin(Stat):
    """Summarize y values within x bins."""

    __name__ = "summary_bin"

    def __init__(self, data=None, mapping=None, bins=30, fun="mean", na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.bins = bins
        self.fun = fun
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        if x_col is None or y_col is None:
            raise ValueError("stat_summary_bin requires x and y aesthetics")
        frame = _clean_numeric(data, [x_col, y_col], self.na_rm)
        if frame.empty:
            return pd.DataFrame(columns=["x", "y", "ymin", "ymax"]), {
                "x": "x", "y": "y", "ymin": "ymin", "ymax": "ymax",
            }
        edges = _bin_edges(frame[x_col], self.bins, None)
        frame["_bin"] = pd.cut(frame[x_col], edges, include_lowest=True)
        grouped = frame.groupby("_bin", observed=True)[y_col]
        func = getattr(grouped, self.fun) if isinstance(self.fun, str) and hasattr(grouped, self.fun) else grouped.mean
        summary = func().reset_index(name="y")
        summary["x"] = summary["_bin"].apply(lambda interval: interval.mid)
        summary["ymin"] = grouped.min().values
        summary["ymax"] = grouped.max().values
        return summary[["x", "y", "ymin", "ymax"]], {"x": "x", "y": "y", "ymin": "ymin", "ymax": "ymax"}


class stat_summary_2d(stat_bin2d):
    """Summarize z values inside x/y bins."""

    __name__ = "summary_2d"

    def __init__(self, data=None, mapping=None, bins=30, fun="mean", na_rm=False, **params):
        super().__init__(data, mapping, bins=bins, na_rm=na_rm, **params)
        self.fun = fun

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        z_col = self.mapping.get("z") or self.mapping.get("fill")
        if z_col is None:
            return super().compute(data)
        frame = _clean_numeric(data, [x_col, y_col, z_col], self.na_rm)
        if frame.empty:
            return pd.DataFrame(columns=["x", "y", "value"]), {"x": "x", "y": "y", "fill": "value"}
        x_edges = _bin_edges(frame[x_col], self.bins, None)
        y_edges = _bin_edges(frame[y_col], self.bins, None)
        frame["_xbin"] = pd.cut(frame[x_col], x_edges, include_lowest=True)
        frame["_ybin"] = pd.cut(frame[y_col], y_edges, include_lowest=True)
        grouped = frame.groupby(["_xbin", "_ybin"], observed=True)[z_col]
        values = grouped.agg(self.fun).reset_index(name="value")
        values["x"] = values["_xbin"].apply(lambda interval: interval.mid)
        values["y"] = values["_ybin"].apply(lambda interval: interval.mid)
        return values[["x", "y", "value"]], {"x": "x", "y": "y", "fill": "value"}


class stat_halfeye(Stat):
    """Compute density plus interval summaries for half-eye style plots."""

    __name__ = "halfeye"

    def __init__(self, data=None, mapping=None, width=None, n=256, point_interval="median_qi",
                 na_rm=False, **params):
        super().__init__(data, mapping, **params)
        self.width = params.get(".width", width if width is not None else (0.5, 0.8, 0.95))
        self.n = n
        self.point_interval = point_interval
        self.na_rm = na_rm

    def compute(self, data):
        x_col = self.mapping.get("x")
        y_col = self.mapping.get("y")
        value_col = y_col or x_col
        group_col = x_col if y_col is not None else self.mapping.get("group")
        if value_col is None:
            raise ValueError("stat_halfeye requires x or y aesthetic")
        frame = _clean_numeric(data, [value_col], self.na_rm)
        groups = [(None, frame)] if group_col is None or group_col not in frame else frame.groupby(group_col)
        widths = list(self.width) if isinstance(self.width, (tuple, list)) else [self.width]
        rows = []
        for group, group_frame in groups:
            values = group_frame[value_col].dropna()
            if len(values) < 2 or values.std() == 0:
                continue
            density = gaussian_kde(values)
            grid = np.linspace(values.min(), values.max(), self.n)
            dens = density(grid)
            dens = dens / dens.max() if dens.max() else dens
            point = values.median()
            for value, density_value in zip(grid, dens):
                rows.append({"group": group, "value": value, "density": density_value, "kind": "slab"})
            for width in widths:
                lower = values.quantile((1 - width) / 2)
                upper = values.quantile(1 - (1 - width) / 2)
                rows.append({
                    "group": group,
                    "value": point,
                    "lower": lower,
                    "upper": upper,
                    ".width": width,
                    "kind": "interval",
                })
        return pd.DataFrame(
            rows,
            columns=["group", "value", "density", "kind", "lower", "upper", ".width"],
        ), {"x": "group", "y": "value", "fill": "density"}


class stat_dotsinterval(stat_halfeye):
    """Compute dot-interval summaries."""

    __name__ = "dotsinterval"


class stat_alluvium(Stat):
    """Prepare categorical flows between ordered axes."""

    __name__ = "alluvium"

    def compute(self, data):
        return data.copy(), self.mapping.copy()


class stat_mosaic(Stat):
    """Compute rectangular mosaic cells from two categorical variables."""

    __name__ = "mosaic"

    def compute(self, data):
        x_col = self.mapping.get("x")
        fill_col = self.mapping.get("fill") or self.mapping.get("y")
        if x_col is None or fill_col is None:
            raise ValueError("stat_mosaic requires x and fill or y aesthetics")
        counts = data.groupby([x_col, fill_col], dropna=False).size().reset_index(name="count")
        totals = counts.groupby(x_col)["count"].sum()
        grand_total = counts["count"].sum() or 1
        x_start = 0.0
        rows = []
        for x_value, group in counts.groupby(x_col, sort=False):
            x_width = totals.loc[x_value] / grand_total
            y_start = 0.0
            for _, row in group.iterrows():
                height = row["count"] / totals.loc[x_value]
                rows.append({
                    "x": x_value,
                    "fill": row[fill_col],
                    "count": row["count"],
                    "xmin": x_start,
                    "xmax": x_start + x_width,
                    "ymin": y_start,
                    "ymax": y_start + height,
                })
                y_start += height
            x_start += x_width
        return pd.DataFrame(rows), {"xmin": "xmin", "xmax": "xmax", "ymin": "ymin", "ymax": "ymax", "fill": "fill"}
