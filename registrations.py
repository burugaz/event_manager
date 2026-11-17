"""Функции работы с регистрациями сотрудников на мероприятия.

Регистрации хранятся в списке словарей:
{"id": ..., "event_id": ..., "employee": ...}.
"""
from datetime import date

from events import is_event_upcoming


def calculate_free_seats(capacity: int, registered_count: int) -> int:
    """Вернуть количество свободных мест (не меньше нуля)."""
    free_seats = capacity - registered_count
    if free_seats < 0:
        return 0
    return free_seats


def get_registration_status(free_seats: int, is_upcoming: bool) -> str:
    """Вернуть текстовый статус регистрации на мероприятие."""
    if not is_upcoming:
        return "Мероприятие уже прошло, регистрация закрыта"
    if free_seats == 0:
        return "Свободных мест нет"
    return "Регистрация открыта"


def count_registrations(registrations: list[dict], event_id: int) -> int:
    """Посчитать регистрации на мероприятие."""
    return sum(1 for item in registrations if item["event_id"] == event_id)


def get_event_status(
    events: dict[int, dict],
    registrations: list[dict],
    event_id: int,
    today: date,
) -> str:
    """Вернуть статус регистрации на мероприятие с учётом даты и мест."""
    event = events[event_id]
    registered = count_registrations(registrations, event_id)
    free_seats = calculate_free_seats(event["capacity"], registered)
    upcoming = is_event_upcoming(date.fromisoformat(event["date"]), today)
    return get_registration_status(free_seats, upcoming)


def is_employee_registered(
    registrations: list[dict],
    event_id: int,
    employee: str,
) -> bool:
    """Проверить, зарегистрирован ли сотрудник на мероприятие."""
    name = employee.strip().casefold()
    for item in registrations:
        same_name = item["employee"].casefold() == name
        if item["event_id"] == event_id and same_name:
            return True
    return False


def create_registration(
    events: dict[int, dict],
    registrations: list[dict],
    event_id: int,
    employee: str,
    today: date,
) -> dict:
    """Зарегистрировать сотрудника на мероприятие.

    Регистрация невозможна, если мероприятия нет, оно уже прошло,
    мест не осталось или сотрудник уже зарегистрирован - в этих случаях
    вызывается ValueError с описанием причины.
    """
    if event_id not in events:
        raise ValueError("Мероприятие не найдено")
    if not employee.strip():
        raise ValueError("Имя сотрудника не может быть пустым")
    status = get_event_status(events, registrations, event_id, today)
    if status != "Регистрация открыта":
        raise ValueError(status)
    if is_employee_registered(registrations, event_id, employee):
        raise ValueError("Сотрудник уже зарегистрирован на мероприятие")
    registration = {
        "id": max((item["id"] for item in registrations), default=0) + 1,
        "event_id": event_id,
        "employee": employee.strip(),
    }
    registrations.append(registration)
    return registration


def cancel_registration(
    registrations: list[dict],
    registration_id: int,
) -> bool:
    """Отменить регистрацию: удалить её из списка.

    Возвращает True, если регистрация найдена и отменена.
    """
    for index, item in enumerate(registrations):
        if item["id"] == registration_id:
            registrations.pop(index)
            return True
    return False
