"""Функции работы с мероприятиями.

Мероприятия хранятся в словаре: ключ - идентификатор мероприятия,
значение - словарь с данными (title, date, capacity).
Дата хранится строкой в формате ГГГГ-ММ-ДД.
"""
from datetime import date


def calculate_fill_percent(capacity: int, registered_count: int) -> int:
    """Вернуть процент заполненности мероприятия (целое число)."""
    return int(registered_count / capacity * 100)


def is_event_upcoming(event_date: date, today: date) -> bool:
    """Проверить, что мероприятие ещё не прошло."""
    return event_date >= today


def add_event(
    events: dict[int, dict],
    title: str,
    event_date: date,
    capacity: int,
) -> None:
    """Добавить мероприятие в словарь events.

    Идентификатор формируется автоматически.
    При некорректных данных вызывает ValueError.
    """
    if not title.strip():
        raise ValueError("Название мероприятия не может быть пустым")
    if capacity <= 0:
        raise ValueError("Вместимость должна быть положительным числом")
    new_id = max(events, default=0) + 1
    events[new_id] = {
        "title": title.strip(),
        "date": event_date.isoformat(),
        "capacity": capacity,
    }


def find_event(events: dict[int, dict], query: str) -> list[dict]:
    """Найти мероприятия по подстроке названия (без учёта регистра)."""
    query = query.strip().casefold()
    found = []
    for event_id, event in events.items():
        if query in event["title"].casefold():
            found.append({"id": event_id, **event})
    return found


def check_event_capacity(
    events: dict[int, dict],
    event_id: int,
    min_capacity: int,
) -> bool:
    """Проверить, что вместимость мероприятия не меньше min_capacity.

    Если мероприятия с таким идентификатором нет, вернуть False.
    """
    event = events.get(event_id)
    if event is None:
        return False
    return event["capacity"] >= min_capacity


def filter_events_by_capacity(
    events: dict[int, dict],
    min_capacity: int,
) -> list[dict]:
    """Отобрать мероприятия, вмещающие не меньше min_capacity человек."""
    return list(
        {"id": event_id, **event}
        for event_id, event in events.items()
        if event["capacity"] >= min_capacity
    )


def sort_events(events: dict[int, dict]) -> list[dict]:
    """Вернуть мероприятия, упорядоченные по дате проведения."""
    all_events = [
        {"id": event_id, **event} for event_id, event in events.items()
    ]
    return sorted(all_events, key=lambda event: event["date"])
