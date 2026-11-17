from datetime import date

import pytest

from events import add_event
from registrations import (
    calculate_free_seats,
    cancel_registration,
    create_registration,
    get_registration_status,
)

TODAY = date(2026, 11, 17)


def make_events() -> dict[int, dict]:
    events: dict[int, dict] = {}
    add_event(events, "Тимбилдинг", date(2026, 12, 12), 2)
    add_event(events, "Старый семинар", date(2026, 11, 1), 10)
    return events


def test_create_registration():
    registrations: list[dict] = []
    result = create_registration(
        make_events(), registrations, 1, "Иван Петров", TODAY
    )
    assert result["id"] == 1
    assert len(registrations) == 1


def test_duplicate_registration_forbidden():
    events = make_events()
    registrations: list[dict] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)
    with pytest.raises(ValueError):
        create_registration(events, registrations, 1, "иван петров", TODAY)


def test_full_event_forbidden():
    events = make_events()
    registrations: list[dict] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)
    create_registration(events, registrations, 1, "Анна Смирнова", TODAY)
    with pytest.raises(ValueError):
        create_registration(events, registrations, 1, "Олег Орлов", TODAY)


def test_past_event_forbidden():
    with pytest.raises(ValueError):
        create_registration(make_events(), [], 2, "Иван Петров", TODAY)


def test_cancel_registration_frees_seat():
    events = make_events()
    registrations: list[dict] = []
    create_registration(events, registrations, 1, "Иван Петров", TODAY)
    create_registration(events, registrations, 1, "Анна Смирнова", TODAY)
    assert cancel_registration(registrations, 1)
    create_registration(events, registrations, 1, "Олег Орлов", TODAY)
    assert len(registrations) == 2
    assert not cancel_registration(registrations, 99)


def test_free_seats_and_status():
    assert calculate_free_seats(50, 47) == 3
    assert calculate_free_seats(10, 12) == 0
    assert get_registration_status(3, True) == "Регистрация открыта"
    assert get_registration_status(0, True) == "Свободных мест нет"
    assert "прошло" in get_registration_status(3, False)
