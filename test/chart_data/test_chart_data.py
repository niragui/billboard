import datetime
import pytest

from src.chart_data.chart_data import ChartData

TEST_URL = "https://example.com"

@pytest.fixture(autouse=True)
def patch_billboard_url(monkeypatch):
    monkeypatch.setattr("src.chart_data.chart_data.BILLBOARD_URL", TEST_URL)


def test_chart_data_initialization():
    chart = ChartData(abbreviation="hot100", name="Hot 100", link="hot-100")
    assert chart.abbreviation == "HOT100"
    assert chart.name == "Hot 100"
    assert chart.link == "hot-100"


def test_chart_data_get_url_no_date():
    chart = ChartData(abbreviation="hot100", name="Hot 100", link="hot-100")
    expected_url = f"{TEST_URL}/charts/hot-100"
    assert chart.get_url() == expected_url
    assert chart.url == expected_url


def test_chart_data_get_url_with_date():
    chart = ChartData(abbreviation="hot100", name="Hot 100", link="hot-100")
    test_date = datetime.date(2022, 1, 1)
    expected_url = f"{TEST_URL}/charts/hot-100/2022-01-01"
    assert chart.get_url(test_date) == expected_url


def test_chart_data_repr_and_str():
    chart = ChartData(abbreviation="hot100", name="Hot 100", link="hot-100")
    expected = f"BillboardChart(Name: Hot 100 | URL: {TEST_URL}/charts/hot-100)"
    assert repr(chart) == expected
    assert str(chart) == expected
