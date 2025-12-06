import pytest
import pandas as pd
from ggplotly import data


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
        df = data("mpg")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (234, 11)
        assert "manufacturer" in df.columns
        assert "hwy" in df.columns

    def test_diamonds(self):
        df = data("diamonds")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (53940, 10)
        assert "carat" in df.columns
        assert "price" in df.columns

    def test_economics(self):
        df = data("economics")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (574, 6)
        assert "date" in df.columns
        assert "unemploy" in df.columns

    def test_economics_long(self):
        df = data("economics_long")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (2870, 4)

    def test_faithfuld(self):
        df = data("faithfuld")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (5625, 3)
        assert "density" in df.columns

    def test_luv_colours(self):
        df = data("luv_colours")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (657, 4)

    def test_midwest(self):
        df = data("midwest")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (437, 28)
        assert "state" in df.columns

    def test_msleep(self):
        df = data("msleep")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (83, 11)
        assert "sleep_total" in df.columns

    def test_presidential(self):
        df = data("presidential")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (12, 4)
        assert "party" in df.columns

    def test_seals(self):
        df = data("seals")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (1155, 4)

    def test_txhousing(self):
        df = data("txhousing")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (8602, 9)
        assert "city" in df.columns

    def test_mtcars(self):
        df = data("mtcars")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (32, 12)
        assert "mpg" in df.columns
        assert "cyl" in df.columns

    def test_iris(self):
        df = data("iris")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (150, 5)
        assert "species" in df.columns
        assert set(df["species"].unique()) == {"setosa", "versicolor", "virginica"}


class TestUSFlightsDatasets:
    def test_us_flights_nodes(self):
        df = data("us_flights_nodes")
        assert isinstance(df, pd.DataFrame)
        assert df.shape == (276, 6)
        assert "name" in df.columns
        assert "longitude" in df.columns
        assert "latitude" in df.columns

    def test_us_flights_edges(self):
        df = data("us_flights_edges")
        assert isinstance(df, pd.DataFrame)
        assert df.shape[1] == 2
        assert "V1" in df.columns
        assert "V2" in df.columns

    def test_us_flights_igraph(self):
        pytest.importorskip("igraph")
        import igraph as ig

        g = data("us_flights")
        assert isinstance(g, ig.Graph)
        assert g.vcount() == 276
        assert g.ecount() > 0
        assert "name" in g.vs.attributes()
        assert "longitude" in g.vs.attributes()
        assert "latitude" in g.vs.attributes()

    def test_us_flights_in_list(self):
        available = data()
        assert "us_flights" in available
