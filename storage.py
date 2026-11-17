"""Загрузка и сохранение данных в JSON-файлах через объекты."""
import json
import os
from models.event import Event
from models.registration import Registration


def _read_json(filename: str) -> list[dict]:
    """Прочитать список записей из JSON-файла."""
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []
    return data


def _write_json(filename: str, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_events(filename: str) -> dict[int, Event]:
    """Загружает мероприятия и возвращает словарь {id: Event}."""
    raw_data = _read_json(filename)
    events = {}
    for item in raw_data:
        try:
            event = Event.from_dict(item)
            events[event.id] = event
        except (KeyError, ValueError):
            continue
    return events


def save_events(filename: str, events: dict[int, Event]) -> None:
    """Сохраняет мероприятия из словаря объектов в JSON."""
    data = [event.to_dict() for event in events.values()]
    _write_json(filename, data)


def load_registrations(filename: str, events_map: dict[int, Event]) -> list[Registration]:
    """Загружает регистрации и связывает их с объектами Event."""
    raw_data = _read_json(filename)
    registrations = []
    for item in raw_data:
        try:
            reg = Registration.from_dict(item, events_map)
            registrations.append(reg)
        except (KeyError, ValueError):
            continue
    return registrations


def save_registrations(filename: str, registrations: list[Registration]) -> None:
    """Сохраняет список объектов Registration в JSON."""
    data = [reg.to_dict() for reg in registrations]
    _write_json(filename, data)