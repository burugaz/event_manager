"""Функции работы с мероприятиями (объектная модель)."""
from datetime import date
from typing import List, Optional
from models.event import Event


def find_event_by_id(events: List[Event], event_id: int) -> Optional[Event]:
    """Найти мероприятие по ID."""
    for event in events:
        if event.id == event_id:
            return event
    return None


def add_event(
    events: List[Event],
    title: str,
    event_date: date,
    capacity: int,
) -> Event:
    """Добавить новое мероприятие в список."""
    if not title.strip():
        raise ValueError("Название мероприятия не может быть пустым")
    if capacity <= 0:
        raise ValueError("Вместимость должна быть положительным числом")

    new_id = max((e.id for e in events), default=0) + 1

    new_event = Event(
        event_id=new_id,
        title=title.strip(),
        event_date=event_date,
        capacity=capacity
    )
    events.append(new_event)
    return new_event


def find_events_by_title(events: List[Event], query: str) -> List[Event]:
    """Найти мероприятия по подстроке названия."""
    query_lower = query.strip().casefold()
    return [
        event for event in events
        if query_lower in event.title.casefold()
    ]


def sort_events_by_date(events: List[Event]) -> List[Event]:
    """Вернуть отсортированный список мероприятий по дате."""
    return sorted(events, key=lambda e: e.date)


def calculate_fill_percent(event: Event, registered_count: int) -> int:
    """Вернуть процент заполненности мероприятия."""
    if event.capacity == 0:
        return 0
    return int(registered_count / event.capacity * 100)