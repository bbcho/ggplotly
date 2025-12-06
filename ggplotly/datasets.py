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


def _load_us_flights():
    """Load US flights as an igraph Graph object."""
    try:
        import igraph as ig
    except ImportError:
        raise ImportError(
            "The igraph package is required for data('us_flights'). "
            "Install it with: pip install igraph"
        )

    nodes = pd.read_csv(_DATA_DIR / "us_flights_nodes.csv")
    edges = pd.read_csv(_DATA_DIR / "us_flights_edges.csv")

    g = ig.Graph.TupleList(
        edges.itertuples(index=False),
        directed=False,
    )

    # Add node attributes - vertex names are integer IDs from edge list
    # Map from integer ID to node attributes using the 'id' column
    id_to_row = {row['id']: row for _, row in nodes.iterrows()}

    # First, collect the vertex IDs before we overwrite 'name'
    vertex_ids = [v["name"] for v in g.vs]

    # Now add all attributes
    for col in nodes.columns:
        attr_values = []
        for node_id in vertex_ids:
            if node_id in id_to_row:
                attr_values.append(id_to_row[node_id][col])
            else:
                attr_values.append(None)
        g.vs[col] = attr_values

    return g


def data(name: Optional[str] = None):
    """
    List available datasets or load a dataset by name.

    Parameters:
        name: The name of the dataset to load (without .csv extension).
              If None, returns list of available datasets.
              Special case: 'us_flights' returns an igraph Graph object.

    Returns:
        If name is None: list of available dataset names.
        If name is 'us_flights': igraph.Graph object.
        Otherwise: pandas.DataFrame containing the dataset.

    Raises:
        ValueError: If the dataset name is not found.

    Examples:
        >>> from ggplotly.datasets import data
        >>> data()  # Returns list of available datasets
        ['diamonds', 'economics', 'iris', 'mpg', 'us_flights', ...]
        >>> df = data('mpg')  # Load a specific dataset
        >>> g = data('us_flights')  # Load as igraph Graph
    """
    available = _list_datasets() + ["us_flights"]

    if name is None:
        return sorted(available)

    if name == "us_flights":
        return _load_us_flights()

    if name not in available:
        raise ValueError(
            f"Unknown dataset '{name}'. "
            f"Use data() to see available datasets."
        )
    return pd.read_csv(_DATA_DIR / f"{name}.csv")
