"""Функции работы с регистрациями (объектная модель)."""
from datetime import date
from typing import List
from models.event import Event
from models.registration import Registration
from events import find_event_by_id


def count_registrations_for_event(registrations: List[Registration], event_id: int) -> int:
    """Посчитать количество активных регистраций на мероприятие."""
    return sum(
        1 for reg in registrations
        if reg.event.id == event_id and not reg.is_cancelled
    )


def is_employee_registered(
    registrations: List[Registration],
    event_id: int,
    employee_name: str,
) -> bool:
    """Проверить, зарегистрирован ли сотрудник на мероприятие."""
    name_lower = employee_name.strip().casefold()
    for reg in registrations:
        if (reg.event.id == event_id and
            not reg.is_cancelled and
            reg.employee_name.casefold() == name_lower):
            return True
    return False


def create_registration(
    events: List[Event],
    registrations: List[Registration],
    event_id: int,
    employee_name: str,
    today: date,
) -> Registration:
    """Зарегистрировать сотрудника на мероприятие."""
    # 1. Найти мероприятие
    event = find_event_by_id(events, event_id)
    if event is None:
        raise ValueError("Мероприятие не найдено")

    # 2. Проверки
    if not employee_name.strip():
        raise ValueError("Имя сотрудника не может быть пустым")

    if not event.is_upcoming(today):
        raise ValueError("Мероприятие уже прошло, регистрация закрыта")

    registered_count = count_registrations_for_event(registrations, event_id)
    if not event.has_seats(registered_count):
        raise ValueError("Свободных мест нет")

    if is_employee_registered(registrations, event_id, employee_name):
        raise ValueError("Сотрудник уже зарегистрирован на это мероприятие")

    # 3. Создание объекта
    new_id = max((r.id for r in registrations), default=0) + 1
    new_reg = Registration(
        reg_id=new_id,
        event=event,
        employee_name=employee_name.strip(),
        reg_date=today
    )
    registrations.append(new_reg)
    return new_reg


def cancel_registration(registrations: List[Registration], registration_id: int) -> bool:
    """Отменить регистрацию (пометить как отмененную)."""
    for reg in registrations:
        if reg.id == registration_id and not reg.is_cancelled:
            reg.cancel()
            return True
    return False


def get_event_status_text(event: Event, registrations: List[Registration], today: date) -> str:
    """Вернуть текстовый статус регистрации на мероприятие."""
    if not event.is_upcoming(today):
        return "Мероприятие уже прошло"

    registered_count = count_registrations_for_event(registrations, event.id)
    free_seats = event.capacity - registered_count

    if free_seats <= 0:
        return "Мест нет"
    return f"Открыта ({free_seats} мест)"