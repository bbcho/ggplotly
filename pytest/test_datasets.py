import pytest
import pandas as pd
from ggplotly import data
from ggplotly.datasets import (
    mpg,
    diamonds,
    economics,
    economics_long,
    faithfuld,
    luv_colours,
    midwest,
    msleep,
    presidential,
    seals,
    txhousing,
    mtcars,
    iris,
    us_flights,
    us_flights_nodes,
    us_flights_edges,
)


class TestDataFunction:
    def test_data_returns_list_when_no_name(self):
        result = data()
        assert isinstance(result, list)
        assert "mpg" in result
        assert "iris" in result
        assert "diamonds" in result

    def test_data_loads_dataset_by_name(self):
        df = data("mpg")
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 234

    def test_data_raises_on_unknown_dataset(self):
        with pytest.raises(ValueError, match="Unknown dataset"):
            data("nonexistent_dataset")


class TestDatasetLoaders:
    def test_mpg(self):
        df = mpg()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (234, 11)
        assert "manufacturer" in df.columns
        assert "hwy" in df.columns

    def test_diamonds(self):
        df = diamonds()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (53940, 10)
        assert "carat" in df.columns
        assert "price" in df.columns

    def test_economics(self):
        df = economics()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (574, 6)
        assert "date" in df.columns
        assert "unemploy" in df.columns

    def test_economics_long(self):
        df = economics_long()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2870, 4)

    def test_faithfuld(self):
        df = faithfuld()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (5625, 3)
        assert "density" in df.columns

    def test_luv_colours(self):
        df = luv_colours()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (657, 4)

    def test_midwest(self):
        df = midwest()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (437, 28)
        assert "state" in df.columns

    def test_msleep(self):
        df = msleep()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (83, 11)
        assert "sleep_total" in df.columns

    def test_presidential(self):
        df = presidential()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (12, 4)
        assert "party" in df.columns

    def test_seals(self):
        df = seals()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (1155, 4)

    def test_txhousing(self):
        df = txhousing()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (8602, 9)
        assert "city" in df.columns

    def test_mtcars(self):
        df = mtcars()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (32, 12)
        assert "mpg" in df.columns
        assert "cyl" in df.columns

    def test_iris(self):
        df = iris()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (150, 5)
        assert "species" in df.columns
        assert set(df["species"].unique()) == {"setosa", "versicolor", "virginica"}


class TestUSFlightsDatasets:
    def test_us_flights_nodes(self):
        df = us_flights_nodes()
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (276, 6)
        assert "name" in df.columns
        assert "longitude" in df.columns
        assert "latitude" in df.columns

    def test_us_flights_edges(self):
        df = us_flights_edges()
        assert isinstance(df, pd.DataFrame)
        assert df.shape[1] == 2
        assert "V1" in df.columns
        assert "V2" in df.columns

    def test_us_flights_igraph(self):
        pytest.importorskip("igraph")
        import igraph as ig

        g = us_flights()
        assert isinstance(g, ig.Graph)
        assert g.vcount() == 276
        assert g.ecount() > 0
        assert "name" in g.vs.attributes()
        assert "longitude" in g.vs.attributes()
        assert "latitude" in g.vs.attributes()
