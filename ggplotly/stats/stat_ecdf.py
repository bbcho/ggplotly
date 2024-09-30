# stats/stat_ecdf.py
import numpy as np
import pandas as pd


class stat_ecdf:
    def compute(self, x):
        x = np.sort(x)
        y = np.arange(1, len(x) + 1) / len(x)
        return pd.DataFrame({"x": x, "y": y})
