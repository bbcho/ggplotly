# stats/stat_fanchart.py

import numpy as np
import pandas as pd

from .stat_base import Stat


class stat_fanchart(Stat):
    """
    Stat for computing percentile bands from T×N matrices.

    Computes percentiles across columns at each row (time point) and returns
    a DataFrame with percentile columns suitable for ribbon plotting.

    Parameters
    ----------
    columns : list, optional
        Specific columns to include in percentile calculation.
        Default is all numeric columns.
    percentiles : list, optional
        Percentile levels to compute. Default is [10, 25, 50, 75, 90].

    Returns
    -------
    DataFrame with columns:
        - x (from index or x aesthetic)
        - p{N} for each percentile (e.g., p10, p25, p50, p75, p90)
        - median (alias for p50)

    Examples
    --------
    >>> # Use with geom_ribbon
    >>> (ggplot(df)
    ...  + stat_fanchart()
    ...  + geom_ribbon(aes(ymin='p10', ymax='p90'), alpha=0.3)
    ...  + geom_ribbon(aes(ymin='p25', ymax='p75'), alpha=0.3)
    ...  + geom_line(aes(y='median')))
    """

    def __init__(self, data=None, mapping=None, columns=None,
                 percentiles=None, **params):
        super().__init__(data, mapping, **params)
        self.columns = columns
        self.percentiles = percentiles or [10, 25, 50, 75, 90]

    def compute(self, data):
        """Compute percentiles across columns."""
        x_col = self.mapping.get('x') if self.mapping else None

        # Determine which columns to use
        columns = self.columns
        if columns is None:
            numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
            if x_col and x_col in numeric_cols:
                numeric_cols.remove(x_col)
            columns = numeric_cols

        # Filter to existing columns
        columns = [c for c in columns if c in data.columns]

        if not columns:
            return pd.DataFrame({'x': data.index.values}), self.mapping

        # Get x values
        if x_col and x_col in data.columns:
            x_values = data[x_col].values
        else:
            x_values = data.index.values

        # Compute percentiles across columns for each row
        matrix = data[columns].values  # T x N matrix
        pct_values = np.percentile(matrix, self.percentiles, axis=1)

        # Build result DataFrame
        result = pd.DataFrame({'x': x_values})

        for i, p in enumerate(self.percentiles):
            result[f'p{p}'] = pct_values[i]

        # Add median alias if 50 is in percentiles
        if 50 in self.percentiles:
            result['median'] = result['p50']

        # Update mapping
        new_mapping = dict(self.mapping) if self.mapping else {}
        new_mapping['x'] = 'x'

        return result, new_mapping
