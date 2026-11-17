from datetime import date
import pytest
from models.event import Event
from events import (
    add_event,
    calculate_fill_percent,
    find_event_by_id,
    sort_events_by_date,
)


def make_events() -> list[Event]:
    events: list[Event] = []
    add_event(events, "Осенний тимбилдинг", date(2026, 12, 12), 50)
    add_event(events, "Семинар", date(2026, 12, 3), 30)
    return events


def test_add_event():
    events = make_events()
    assert len(events) == 2
    assert events[0].date == date(2026, 12, 12)


def test_add_event_invalid_capacity():
    with pytest.raises(ValueError):
        add_event([], "Семинар", date(2026, 12, 3), 0)


def test_find_event_by_id():
    events = make_events()
    found = find_event_by_id(events, 1)
    assert found is not None
    assert found.title == "Осенний тимбилдинг"


def test_find_event_not_found():
    events = make_events()
    assert find_event_by_id(events, 99) is None


def test_sort_events_by_date():
    ordered = sort_events_by_date(make_events())
    # Семинар (3 декабря) должен быть раньше Тимбилдинга (12 декабря)
    assert ordered[0].title == "Семинар"
    assert ordered[1].title == "Осенний тимбилдинг"


def test_is_event_upcoming():
    event = Event(1, "Test", date(2026, 12, 12), 10)
    assert event.is_upcoming(date(2026, 11, 17))
    assert not event.is_upcoming(date(2027, 1, 1))


def test_calculate_fill_percent():
    event = Event(1, "Test", date(2026, 12, 12), 50)
    assert calculate_fill_percent(event, 47) == 94