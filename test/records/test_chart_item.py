import datetime
import pytest
from src.records.chart_item import ChartItem


@pytest.fixture
def base_item():
    return ChartItem(
        position=5,
        title="Test Song",
        image="image_url",
        last_week="8",
        peak=5,
        weeks=6,
        debut_date="2023-12-01",
        debut_position=20,
        peak_date="2025-08-07",
        date=datetime.date(2025, 8, 7),
        credits="Artist"
    )


def test_chart_item_initialization(base_item):
    assert base_item.title == "Test Song"
    assert base_item.last_week == 8
    assert base_item.debut_date == datetime.date(2023, 12, 1)
    assert base_item.peak_date == datetime.date(2025, 8, 7)


def test_item_id(base_item):
    assert base_item.item_id == "2023-12-01-20"
    base_item.update_version()
    assert base_item.item_id == "2023-12-01-20-1"


def test_is_new_peak(base_item):
    assert base_item.is_new_peak is True


def test_is_peak(base_item):
    assert base_item.is_peak is True


def test_is_new_false(base_item):
    assert base_item.is_new is False


def test_is_re_entry_false(base_item):
    assert base_item.is_re_entry is False


def test_has_changed_true(base_item):
    assert base_item.has_changed is True


def test_is_repeak_false(base_item):
    assert base_item.is_repeak is False


def test_change_value(base_item):
    assert base_item.change == "+3"


def test_peak_text(base_item):
    assert base_item.peak_text == "NEW PEAK"


def test_text_output(base_item):
    assert "#5 (+3) — Test Song" in base_item.text
    assert "*NEW PEAK*" in base_item.text


def test_to_dict_keys(base_item):
    result = base_item.to_dict()
    assert result["title"] == "Test Song"
    assert result["last_week"] == 8
    assert result["debut_date"] == "2023-12-01"


def test_repr_and_str(base_item):
    r = repr(base_item)
    s = str(base_item)
    assert "ChartItem(Title: Test Song" in r
    assert "#5" in s


def test_new_item_flags():
    item = ChartItem(
        position=1,
        title="Fresh Song",
        image="",
        last_week="",
        peak=1,
        weeks=1,
        debut_date="2025-08-07",
        debut_position=1,
        peak_date="2025-08-07",
        date=datetime.date(2025, 8, 7),
        credits=None
    )
    assert item.is_new is True
    assert item.is_re_entry is False
    assert item.change == "NEW"
    assert item.peak_text == "NEW PEAK"


def test_re_entry_item_flags():
    item = ChartItem(
        position=10,
        title="Re-entry Song",
        image="",
        last_week="",  # Not a digit
        peak=5,
        weeks=10,
        debut_date="2025-01-01",
        debut_position=30,
        peak_date="2025-03-01",
        date=datetime.date(2025, 8, 7),
        credits=None
    )
    assert item.is_new is False
    assert item.is_re_entry is True
    assert item.change == "RE"
    assert item.peak_text is None
