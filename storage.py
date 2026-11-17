"""Загрузка и сохранение данных в JSON-файлах."""
import json
import os


def _read_json(filename: str) -> list[dict]:
    """Прочитать список записей из JSON-файла.

    Если файла нет или он повреждён, вернуть пустой список.
    """
    try:
        with open(filename, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден, данные начаты с нуля")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} повреждён, данные начаты с нуля")
        return []
    if not isinstance(data, list):
        print(f"Файл {filename} имеет неверный формат")
        return []
    return data


def _write_json(filename: str, data: list[dict]) -> None:
    """Записать список записей в JSON-файл."""
    folder = os.path.dirname(filename)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_events(filename: str) -> dict[int, dict]:
    """Загрузить мероприятия: список из JSON -> словарь по id."""
    events = {}
    for item in _read_json(filename):
        try:
            events[item["id"]] = {
                "title": item["title"],
                "date": item["date"],
                "capacity": item["capacity"],
            }
        except KeyError as error:
            print(f"В записи мероприятия нет поля {error}, запись пропущена")
    return events


def save_events(filename: str, events: dict[int, dict]) -> None:
    """Сохранить мероприятия: словарь по id -> список в JSON."""
    data = [{"id": event_id, **event} for event_id, event in events.items()]
    _write_json(filename, data)


def load_registrations(filename: str) -> list[dict]:
    """Загрузить регистрации из JSON-файла."""
    return _read_json(filename)


def save_registrations(filename: str, registrations: list[dict]) -> None:
    """Сохранить регистрации в JSON-файл."""
    _write_json(filename, registrations)
