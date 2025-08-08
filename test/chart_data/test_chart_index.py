import os
import pytest

from src.chart_data.chart_data import ChartData
from src.chart_data.chart_index import ChartsIndex

THIS_FOLDER = os.path.dirname(__file__)
TEST_FILE = os.path.join(THIS_FOLDER, "charts_test.json")


def test_charts_index_init():
    index = ChartsIndex(TEST_FILE)
    assert len(index) == 3
    assert isinstance(index.charts[0], ChartData)


def test_charts_index_lookup_by_abbreviation():
    index = ChartsIndex(TEST_FILE)
    chart = index.get_chart("hot100")
    assert chart.name == "Hot 100"


def test_charts_index_lookup_by_name():
    index = ChartsIndex(TEST_FILE)
    chart = index.get_chart("Billboard 200")
    assert chart.abbreviation == "BB200"


def test_charts_index_lookup_by_link():
    index = ChartsIndex(TEST_FILE)
    chart = index.get_chart("hot-100")
    assert chart.abbreviation == "HOT100"


def test_charts_index_getitem():
    index = ChartsIndex(TEST_FILE)
    assert index["global200"].name == "Global 200"


def test_charts_index_invalid_key_type():
    index = ChartsIndex(TEST_FILE)
    with pytest.raises(TypeError):
        index.get_chart(123)  # Not a string


def test_charts_index_key_not_found():
    index = ChartsIndex(TEST_FILE)
    with pytest.raises(KeyError):
        index.get_chart("nonexistent")


def test_charts_index_file_not_found():
    with pytest.raises(OSError):
        ChartsIndex("non_existent_file.json")


def test_charts_index_repr_and_str():
    index = ChartsIndex(TEST_FILE)
    text = str(index)
    assert "ChartsIndex(file=" in text
    assert "Items: 3" in text
