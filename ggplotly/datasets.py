# datasets.py
"""
Built-in datasets for ggplotly, mirroring those available in ggplot2.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List


_DATA_DIR = Path(__file__).parent / "data"


def _list_datasets() -> List[str]:
    """Return sorted list of available dataset names."""
    return sorted([f.stem for f in _DATA_DIR.glob("*.csv")])


def data(name: Optional[str] = None):
    """
    List available datasets or load a dataset by name.

    Parameters:
        name: The name of the dataset to load (without .csv extension).
              If None, returns list of available datasets.

    Returns:
        If name is None: list of available dataset names.
        If name is provided: pandas.DataFrame containing the dataset.

    Raises:
        ValueError: If the dataset name is not found.

    Examples:
        >>> from ggplotly.datasets import data
        >>> data()  # Returns list of available datasets
        ['diamonds', 'economics', 'iris', 'mpg', ...]
        >>> df = data('mpg')  # Load a specific dataset
        >>> df = data('diamonds')
    """
    available = _list_datasets()

    if name is None:
        return available

    if name not in available:
        raise ValueError(
            f"Unknown dataset '{name}'. "
            f"Use data() to see available datasets."
        )
    return pd.read_csv(_DATA_DIR / f"{name}.csv")


def mpg():
    """
    Fuel economy data from 1999 to 2008 for 38 popular models of cars.

    This dataset contains a subset of the fuel economy data that the EPA makes
    available on https://fueleconomy.gov/. It contains only models which had a new
    release every year between 1999 and 2008.

    Returns:
        pandas.DataFrame: A data frame with 234 rows and 11 variables:
            - manufacturer: manufacturer name
            - model: model name
            - displ: engine displacement, in litres
            - year: year of manufacture
            - cyl: number of cylinders
            - trans: type of transmission
            - drv: the type of drive train (f = front-wheel, r = rear-wheel, 4 = 4wd)
            - cty: city miles per gallon
            - hwy: highway miles per gallon
            - fl: fuel type (e = E85, d = diesel, r = regular, p = premium, c = CNG)
            - class: type of car

    Examples:
        >>> from ggplotly import ggplot, aes, geom_point
        >>> from ggplotly.datasets import mpg
        >>> df = mpg()
        >>> p = ggplot(df, aes(x='displ', y='hwy')) + geom_point()
    """
    return pd.read_csv(_DATA_DIR / "mpg.csv")


def diamonds():
    """
    Prices of over 50,000 round cut diamonds.

    Returns:
        pandas.DataFrame: A data frame with 53940 rows and 10 variables.
    """
    return pd.read_csv(_DATA_DIR / "diamonds.csv")


def economics():
    """
    US economic time series data.

    Returns:
        pandas.DataFrame: A data frame with 574 rows and 6 variables.
    """
    return pd.read_csv(_DATA_DIR / "economics.csv")


def economics_long():
    """
    US economic time series data in long format.

    Returns:
        pandas.DataFrame: A data frame with 2870 rows and 4 variables.
    """
    return pd.read_csv(_DATA_DIR / "economics_long.csv")


def faithfuld():
    """
    2D density estimate of Old Faithful eruption data.

    Returns:
        pandas.DataFrame: A data frame with 5625 rows and 3 variables.
    """
    return pd.read_csv(_DATA_DIR / "faithfuld.csv")


def luv_colours():
    """
    Colors in Luv color space.

    Returns:
        pandas.DataFrame: A data frame with 657 rows and 4 variables.
    """
    return pd.read_csv(_DATA_DIR / "luv_colours.csv")


def midwest():
    """
    Midwest demographics data.

    Returns:
        pandas.DataFrame: A data frame with 437 rows and 28 variables.
    """
    return pd.read_csv(_DATA_DIR / "midwest.csv")


def msleep():
    """
    Mammal sleep data.

    Returns:
        pandas.DataFrame: A data frame with 83 rows and 11 variables.
    """
    return pd.read_csv(_DATA_DIR / "msleep.csv")


def presidential():
    """
    Terms of 12 presidents from Eisenhower to Trump.

    Returns:
        pandas.DataFrame: A data frame with 12 rows and 4 variables.
    """
    return pd.read_csv(_DATA_DIR / "presidential.csv")


def seals():
    """
    Vector field of seal movements.

    Returns:
        pandas.DataFrame: A data frame with 1155 rows and 4 variables.
    """
    return pd.read_csv(_DATA_DIR / "seals.csv")


def txhousing():
    """
    Housing sales in Texas.

    Returns:
        pandas.DataFrame: A data frame with 8602 rows and 9 variables.
    """
    return pd.read_csv(_DATA_DIR / "txhousing.csv")


def mtcars():
    """
    Motor Trend car road tests.

    Returns:
        pandas.DataFrame: A data frame with 32 rows and 12 variables.
    """
    return pd.read_csv(_DATA_DIR / "mtcars.csv")


def iris():
    """
    Edgar Anderson's Iris data.

    Returns:
        pandas.DataFrame: A data frame with 150 rows and 5 variables.
    """
    return pd.read_csv(_DATA_DIR / "iris.csv")


def us_flights_nodes():
    """
    US flights network node data (airports).

    Returns:
        pandas.DataFrame: A data frame with 276 rows and 6 variables.
    """
    return pd.read_csv(_DATA_DIR / "us_flights_nodes.csv")


def us_flights_edges():
    """
    US flights network edge data (routes).

    Returns:
        pandas.DataFrame: A data frame with route connections.
    """
    return pd.read_csv(_DATA_DIR / "us_flights_edges.csv")


def us_flights():
    """
    US flights network as an igraph Graph object.

    Requires the igraph package to be installed.

    Returns:
        igraph.Graph: A graph object with airport nodes and flight edges.
    """
    try:
        import igraph as ig
    except ImportError:
        raise ImportError(
            "The igraph package is required for us_flights(). "
            "Install it with: pip install igraph"
        )

    nodes = us_flights_nodes()
    edges = us_flights_edges()

    g = ig.Graph.TupleList(
        edges.itertuples(index=False),
        directed=False,
    )

    # Add node attributes
    node_names = [v["name"] for v in g.vs]
    for col in nodes.columns:
        if col != "name":
            attr_map = dict(zip(nodes["name"], nodes[col]))
            g.vs[col] = [attr_map.get(name) for name in node_names]

    return g
