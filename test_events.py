from datetime import date

import pytest

from events import (
    add_event,
    calculate_fill_percent,
    check_event_capacity,
    filter_events_by_capacity,
    find_event,
    is_event_upcoming,
    sort_events,
)


def make_events() -> dict[int, dict]:
    events: dict[int, dict] = {}
    add_event(events, "Осенний тимбилдинг", date(2026, 12, 12), 50)
    add_event(events, "Семинар", date(2026, 12, 3), 30)
    return events


def test_add_event():
    events = make_events()
    assert len(events) == 2
    assert events[1]["date"] == "2026-12-12"


def test_add_event_invalid_capacity():
    with pytest.raises(ValueError):
        add_event({}, "Семинар", date(2026, 12, 3), 0)


def test_find_event_ignores_case():
    found = find_event(make_events(), "ТИМБИЛДИНГ")
    assert [event["id"] for event in found] == [1]


def test_check_event_capacity():
    events = make_events()
    assert check_event_capacity(events, 1, 50)
    assert not check_event_capacity(events, 2, 31)
    assert not check_event_capacity(events, 99, 1)


def test_filter_events_by_capacity():
    found = filter_events_by_capacity(make_events(), 40)
    assert [event["id"] for event in found] == [1]


def test_sort_events_by_date():
    ordered = sort_events(make_events())
    assert [event["id"] for event in ordered] == [2, 1]


def test_is_event_upcoming():
    assert is_event_upcoming(date(2026, 12, 12), date(2026, 11, 17))
    assert not is_event_upcoming(date(2026, 11, 1), date(2026, 11, 17))


def test_calculate_fill_percent():
    assert calculate_fill_percent(50, 47) == 94
