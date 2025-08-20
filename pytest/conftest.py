import sys
import os
import pytest
import pandas as pd
import numpy as np

# Add the parent directory to the path so we can import ggplotly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 1, 5, 3],
        'category': ['A', 'B', 'A', 'B', 'A'],
        'group': ['X', 'X', 'Y', 'Y', 'X'],
        'value': [10, 20, 15, 25, 18],
        'size_var': [10, 20, 15, 25, 18],
        'color_var': ['red', 'blue', 'green', 'red', 'blue']
    })

@pytest.fixture
def sample_data_large():
    """Provide larger sample data for tests."""
    np.random.seed(42)
    return pd.DataFrame({
        'x': np.linspace(0, 10, 100),
        'y': np.sin(np.linspace(0, 10, 100)),
        'category': np.random.choice(['A', 'B', 'C'], 100),
        'group': np.random.choice(['X', 'Y'], 100),
        'angle': np.linspace(0, 2*np.pi, 100),
        'radius': np.random.uniform(0.5, 2, 100)
    })

@pytest.fixture
def sample_data_grid():
    """Provide grid data for tile plots."""
    return pd.DataFrame({
        'x': [1, 2, 3, 1, 2, 3, 1, 2, 3],
        'y': [1, 1, 1, 2, 2, 2, 3, 3, 3],
        'value': [0.1, 0.5, 0.9, 0.3, 0.7, 0.2, 0.8, 0.4, 0.6]
    })

@pytest.fixture
def sample_data_error():
    """Provide data with error bars."""
    df = pd.DataFrame({
        'x': [1, 2, 3, 4, 5],
        'y': [2, 4, 1, 5, 3],
        'ymin': [1.5, 3.5, 0.5, 4.5, 2.5],
        'ymax': [2.5, 4.5, 1.5, 5.5, 3.5]
    })
    return df

@pytest.fixture
def sample_data_ribbon():
    """Provide data for ribbon plots."""
    x = np.linspace(0, 10, 50)
    y = np.sin(x)
    return pd.DataFrame({
        'x': x,
        'ymin': y - 0.2,
        'ymax': y + 0.2
    })

@pytest.fixture
def empty_dataframe():
    """Provide empty dataframe for edge case testing."""
    return pd.DataFrame()

@pytest.fixture
def single_row_data():
    """Provide single row data for edge case testing."""
    return pd.DataFrame({'x': [1], 'y': [1]})

@pytest.fixture
def single_column_data():
    """Provide single column data for edge case testing."""
    return pd.DataFrame({'x': [1, 2, 3, 4, 5]})

