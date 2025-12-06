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
