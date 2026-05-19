"""Parity checks for bundled ggplot2-compatible datasets."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from pandas.api.types import (
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
    is_string_dtype,
)

import pytest

from ggplotly import (
    aes,
    data,
    geom_bar,
    geom_line,
    geom_point,
    geom_segment,
    ggplot,
    scale_x_date,
)


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    shape: tuple[int, int]
    columns: tuple[str, ...]
    numeric_columns: tuple[str, ...]
    string_columns: tuple[str, ...] = ()
    datetime_columns: tuple[str, ...] = ()


DATASET_SPECS = (
    DatasetSpec(
        name="diamonds",
        shape=(53940, 10),
        columns=(
            "carat",
            "cut",
            "color",
            "clarity",
            "depth",
            "table",
            "price",
            "x",
            "y",
            "z",
        ),
        numeric_columns=("carat", "depth", "table", "price", "x", "y", "z"),
        string_columns=("cut", "color", "clarity"),
    ),
    DatasetSpec(
        name="economics",
        shape=(574, 6),
        columns=("date", "pce", "pop", "psavert", "uempmed", "unemploy"),
        numeric_columns=("pce", "pop", "psavert", "uempmed", "unemploy"),
        datetime_columns=("date",),
    ),
    DatasetSpec(
        name="economics_long",
        shape=(2870, 4),
        columns=("date", "variable", "value", "value01"),
        numeric_columns=("value", "value01"),
        string_columns=("variable",),
        datetime_columns=("date",),
    ),
    DatasetSpec(
        name="faithfuld",
        shape=(5625, 3),
        columns=("eruptions", "waiting", "density"),
        numeric_columns=("eruptions", "waiting", "density"),
    ),
    DatasetSpec(
        name="luv_colours",
        shape=(657, 4),
        columns=("L", "u", "v", "col"),
        numeric_columns=("L", "u", "v"),
        string_columns=("col",),
    ),
    DatasetSpec(
        name="midwest",
        shape=(437, 28),
        columns=(
            "PID",
            "county",
            "state",
            "area",
            "poptotal",
            "popdensity",
            "popwhite",
            "popblack",
            "popamerindian",
            "popasian",
            "popother",
            "percwhite",
            "percblack",
            "percamerindan",
            "percasian",
            "percother",
            "popadults",
            "perchsd",
            "percollege",
            "percprof",
            "poppovertyknown",
            "percpovertyknown",
            "percbelowpoverty",
            "percchildbelowpovert",
            "percadultpoverty",
            "percelderlypoverty",
            "inmetro",
            "category",
        ),
        numeric_columns=(
            "PID",
            "area",
            "poptotal",
            "popdensity",
            "popwhite",
            "popblack",
            "popamerindian",
            "popasian",
            "popother",
            "percwhite",
            "percblack",
            "percamerindan",
            "percasian",
            "percother",
            "popadults",
            "perchsd",
            "percollege",
            "percprof",
            "poppovertyknown",
            "percpovertyknown",
            "percbelowpoverty",
            "percchildbelowpovert",
            "percadultpoverty",
            "percelderlypoverty",
            "inmetro",
        ),
        string_columns=("county", "state", "category"),
    ),
    DatasetSpec(
        name="mpg",
        shape=(234, 11),
        columns=(
            "manufacturer",
            "model",
            "displ",
            "year",
            "cyl",
            "trans",
            "drv",
            "cty",
            "hwy",
            "fl",
            "class",
        ),
        numeric_columns=("displ", "year", "cyl", "cty", "hwy"),
        string_columns=("manufacturer", "model", "trans", "drv", "fl", "class"),
    ),
    DatasetSpec(
        name="msleep",
        shape=(83, 11),
        columns=(
            "name",
            "genus",
            "vore",
            "order",
            "conservation",
            "sleep_total",
            "sleep_rem",
            "sleep_cycle",
            "awake",
            "brainwt",
            "bodywt",
        ),
        numeric_columns=(
            "sleep_total",
            "sleep_rem",
            "sleep_cycle",
            "awake",
            "brainwt",
            "bodywt",
        ),
        string_columns=("name", "genus", "vore", "order", "conservation"),
    ),
    DatasetSpec(
        name="presidential",
        shape=(12, 4),
        columns=("name", "start", "end", "party"),
        numeric_columns=(),
        string_columns=("name", "party"),
        datetime_columns=("start", "end"),
    ),
    DatasetSpec(
        name="seals",
        shape=(1155, 4),
        columns=("lat", "long", "delta_long", "delta_lat"),
        numeric_columns=("lat", "long", "delta_long", "delta_lat"),
    ),
    DatasetSpec(
        name="txhousing",
        shape=(8602, 9),
        columns=(
            "city",
            "year",
            "month",
            "sales",
            "volume",
            "median",
            "listings",
            "inventory",
            "date",
        ),
        numeric_columns=(
            "year",
            "month",
            "sales",
            "volume",
            "median",
            "listings",
            "inventory",
            "date",
        ),
        string_columns=("city",),
    ),
)


@pytest.mark.parametrize("spec", DATASET_SPECS, ids=lambda spec: spec.name)
def test_ggplot2_dataset_shape_and_columns(spec):
    df = data(spec.name)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == spec.shape
    assert tuple(df.columns) == spec.columns


def test_project_02_datasets_are_available():
    available = set(data())

    assert {spec.name for spec in DATASET_SPECS} <= available


@pytest.mark.parametrize("spec", DATASET_SPECS, ids=lambda spec: spec.name)
def test_ggplot2_dataset_dtype_families(spec):
    df = data(spec.name)

    for column in spec.numeric_columns:
        assert is_numeric_dtype(df[column]), column

    for column in spec.string_columns:
        assert is_object_dtype(df[column]) or is_string_dtype(df[column]), column

    for column in spec.datetime_columns:
        assert is_datetime64_any_dtype(df[column]), column


def test_economics_date_example_draws_on_date_axis():
    economics = data("economics")

    fig = (
        ggplot(economics, aes(x="date", y="unemploy"))
        + geom_line()
        + scale_x_date(date_breaks="10 years", date_labels="%Y")
    ).draw()

    assert fig.layout.xaxis.type == "date"
    assert pd.Timestamp(fig.data[0].x[0]) == economics["date"].iloc[0]


def test_presidential_timeline_example_draws_with_dates():
    presidential = data("presidential")

    fig = (
        ggplot(
            presidential,
            aes(x="start", xend="end", y="name", yend="name", color="party"),
        )
        + geom_segment(linewidth=4)
        + scale_x_date(date_breaks="4 years", date_labels="%Y")
    ).draw()

    assert fig.layout.xaxis.type == "date"
    assert pd.Timestamp(fig.data[0].x[0]) == presidential["start"].iloc[0]


def test_txhousing_date_remains_numeric_for_decimal_year_examples():
    houston = data("txhousing").loc[lambda df: df["city"] == "Houston"]

    fig = (ggplot(houston, aes(x="date", y="sales")) + geom_line()).draw()

    assert is_numeric_dtype(houston["date"])
    assert fig.layout.xaxis.type is None
    assert fig.data[0].x[0] == houston["date"].iloc[0]


def test_representative_categorical_dataset_examples_draw():
    mpg_fig = (
        ggplot(data("mpg"), aes(x="displ", y="hwy", color="class")) + geom_point()
    ).draw()
    diamonds_fig = (ggplot(data("diamonds"), aes(x="cut")) + geom_bar()).draw()

    assert len(mpg_fig.data) > 0
    assert len(diamonds_fig.data) > 0
