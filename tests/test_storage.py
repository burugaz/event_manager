import pytest
from datetime import date
from models.event import Event
from models.registration import Registration
from storage import (
    load_events,
    load_registrations,
    save_events,
    save_registrations,
)


def test_events_roundtrip(tmp_path):
    filename = str(tmp_path / "events.json")
    events_list = []
    e1 = Event(1, "Семинар", date(2026, 12, 3), 30)
    events_list.append(e1)

    # Сохраняем как список, но функция ждет dict[int, Event] для сохранения в старом формате?
    # Нет, в новом storage.save_events принимает dict[int, Event].
    # Давайте адаптируем тест под новый storage.

    events_dict = {1: e1}
    save_events(filename, events_dict)

    loaded_dict = load_events(filename)
    assert 1 in loaded_dict
    assert loaded_dict[1].title == "Семинар"


def test_registrations_roundtrip(tmp_path):
    filename = str(tmp_path / "registrations.json")

    # Создаем событие для связи
    event = Event(1, "Семинар", date(2026, 12, 3), 30)
    events_map = {1: event}

    reg = Registration(1, event, "Иван Петров", date(2026, 11, 17))
    items = [reg]

    save_registrations(filename, items)

    loaded_items = load_registrations(filename, events_map)
    assert len(loaded_items) == 1
    assert loaded_items[0].employee_name == "Иван Петров"


def test_missing_and_broken_file(tmp_path):
    assert load_events(str(tmp_path / "none.json")) == {}

    broken = tmp_path / "broken.json"
    broken.write_text("{не json", encoding="utf-8")
    assert load_registrations(str(broken), {}) == []