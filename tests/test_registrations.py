from datetime import date
import pytest
from models.event import Event
from models.registration import Registration
from events import add_event
from registrations import (
    create_registration,
    cancel_registration,
    count_registrations_for_event,
    is_employee_registered,
    get_event_status_text,
)

TODAY = date(2026, 11, 17)


def make_events() -> list[Event]:
    events: list[Event] = []
    add_event(events, "Тимбилдинг", date(2026, 12, 12), 2)
    add_event(events, "Старый семинар", date(2026, 11, 1), 10)
    return events


def test_create_registration():
    registrations: list[Registration] = []
    events = make_events()
    result = create_registration(events, registrations, 1, "Иван Петров", TODAY)

    assert result.id == 1
    assert len(registrations) == 1
    assert result.employee_name == "Иван Петров"
    assert result.event.id == 1


def test_duplicate_registration_forbidden():
    events = make_events()
    registrations: list[Registration] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)

    with pytest.raises(ValueError):
        create_registration(events, registrations, 1, "иван петров", TODAY)


def test_full_event_forbidden():
    events = make_events()
    registrations: list[Registration] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)
    create_registration(events, registrations, 1, "Анна Смирнова", TODAY)

    with pytest.raises(ValueError):
        create_registration(events, registrations, 1, "Олег Орлов", TODAY)


def test_past_event_forbidden():
    events = make_events()
    with pytest.raises(ValueError):
        create_registration(events, [], 2, "Иван Петров", TODAY)


def test_cancel_registration_frees_seat():
    events = make_events()
    registrations: list[Registration] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)
    create_registration(events, registrations, 1, "Анна Смирнова", TODAY)

    assert cancel_registration(registrations, 1)

    # Теперь должно быть место для третьего
    create_registration(events, registrations, 1, "Олег Орлов", TODAY)
    assert len(registrations) == 3 # Все 3 записи есть, одна отменена

    assert not cancel_registration(registrations, 99)


def test_free_seats_and_status():
    events = make_events()
    registrations: list[Registration] = []
    event = events[0] # Тимбилдинг, вместимость 2

    assert get_event_status_text(event, registrations, TODAY) == "Открыта (2 мест)"

    create_registration(events, registrations, 1, "Иван", TODAY)
    assert get_event_status_text(event, registrations, TODAY) == "Открыта (1 мест)"

    create_registration(events, registrations, 1, "Анна", TODAY)
    assert get_event_status_text(event, registrations, TODAY) == "Мест нет"