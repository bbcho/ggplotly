# datasets.py
"""
Built-in datasets for ggplotly, mirroring those available in ggplot2.
"""

import pandas as pd
from pathlib import Path


_DATA_DIR = Path(__file__).parent / "data"


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
