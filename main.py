"""Точка запуска приложения «Система организации корпоративных
мероприятий»."""
import os
from datetime import date

from events import (
    add_event,
    calculate_fill_percent,
    check_event_capacity,
    filter_events_by_capacity,
    find_event,
    sort_events,
)
from registrations import (
    cancel_registration,
    count_registrations,
    create_registration,
    get_event_status,
)
from storage import (
    load_events,
    load_registrations,
    save_events,
    save_registrations,
)
from utils import input_date, input_int

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
EVENTS_FILE = os.path.join(DATA_DIR, "events.json")
REGISTRATIONS_FILE = os.path.join(DATA_DIR, "registrations.json")

MENU = """
=== Система организации корпоративных мероприятий ===
1. Показать мероприятия
2. Найти мероприятие по названию
3. Проверить вместимость
4. Подобрать мероприятия по вместимости
5. Проверить возможность регистрации
6. Зарегистрировать сотрудника
7. Отменить регистрацию
8. Показать регистрации
9. Добавить мероприятие
0. Выход"""


def show_events(events: dict[int, dict], registrations: list[dict]) -> None:
    """Вывести список мероприятий, отсортированный по дате."""
    if not events:
        print("Мероприятий нет")
        return
    for event in sort_events(events):
        registered = count_registrations(registrations, event["id"])
        percent = calculate_fill_percent(event["capacity"], registered)
        print(
            f'{event["id"]}. {event["title"]} | {event["date"]} | '
            f'мест занято: {registered}/{event["capacity"]} ({percent}%)'
        )


def show_registrations(
    events: dict[int, dict],
    registrations: list[dict],
) -> None:
    """Вывести список регистраций с указанием мероприятия."""
    if not registrations:
        print("Регистраций нет")
        return
    for item in registrations:
        event = events.get(item["event_id"])
        title = event["title"] if event else "неизвестное мероприятие"
        print(f'{item["id"]}. {item["employee"]} -> {title}')


def ask_event_id(events: dict[int, dict]) -> int | None:
    """Запросить id мероприятия; вернуть None, если его нет."""
    event_id = input_int("ID мероприятия: ")
    if event_id not in events:
        print("Мероприятие не найдено")
        return None
    return event_id


def search_events(events: dict[int, dict]) -> None:
    """Найти и вывести мероприятия по названию."""
    found = find_event(events, input("Название мероприятия: "))
    if not found:
        print("Ничего не найдено")
    for event in found:
        print(f'{event["id"]}. {event["title"]} | {event["date"]}')


def check_capacity(events: dict[int, dict]) -> None:
    """Проверить, вмещает ли мероприятие заданное число людей."""
    event_id = ask_event_id(events)
    if event_id is None:
        return
    people = input_int("Количество участников: ")
    if check_event_capacity(events, event_id, people):
        print("Вместимости достаточно")
    else:
        print("Вместимости недостаточно")


def select_by_capacity(events: dict[int, dict]) -> None:
    """Вывести мероприятия, вмещающие не меньше заданного числа людей."""
    min_capacity = input_int("Минимальная вместимость: ")
    found = filter_events_by_capacity(events, min_capacity)
    if not found:
        print("Подходящих мероприятий нет")
    for event in found:
        print(f'{event["id"]}. {event["title"]} ({event["capacity"]} мест)')


def check_registration(
    events: dict[int, dict],
    registrations: list[dict],
) -> None:
    """Вывести статус регистрации на выбранное мероприятие."""
    event_id = ask_event_id(events)
    if event_id is not None:
        print(get_event_status(events, registrations, event_id, date.today()))


def register_employee(
    events: dict[int, dict],
    registrations: list[dict],
) -> None:
    """Зарегистрировать сотрудника и сохранить регистрации."""
    event_id = ask_event_id(events)
    if event_id is None:
        return
    employee = input("ФИО сотрудника: ")
    try:
        registration = create_registration(
            events, registrations, event_id, employee, date.today()
        )
    except ValueError as error:
        print(f"Регистрация невозможна: {error}")
        return
    save_registrations(REGISTRATIONS_FILE, registrations)
    print(f'Регистрация создана, ID: {registration["id"]}')


def cancel_employee_registration(registrations: list[dict]) -> None:
    """Отменить регистрацию и сохранить регистрации."""
    registration_id = input_int("ID регистрации: ")
    if cancel_registration(registrations, registration_id):
        save_registrations(REGISTRATIONS_FILE, registrations)
        print("Регистрация отменена")
    else:
        print("Регистрация не найдена")


def create_event(events: dict[int, dict]) -> None:
    """Добавить мероприятие и сохранить мероприятия."""
    title = input("Название мероприятия: ")
    event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    capacity = input_int("Вместимость: ")
    try:
        add_event(events, title, event_date, capacity)
    except ValueError as error:
        print(f"Мероприятие не добавлено: {error}")
        return
    save_events(EVENTS_FILE, events)
    print("Мероприятие добавлено")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    events = load_events(EVENTS_FILE)
    registrations = load_registrations(REGISTRATIONS_FILE)
    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()
        if choice == "1":
            show_events(events, registrations)
        elif choice == "2":
            search_events(events)
        elif choice == "3":
            check_capacity(events)
        elif choice == "4":
            select_by_capacity(events)
        elif choice == "5":
            check_registration(events, registrations)
        elif choice == "6":
            register_employee(events, registrations)
        elif choice == "7":
            cancel_employee_registration(registrations)
        elif choice == "8":
            show_registrations(events, registrations)
        elif choice == "9":
            create_event(events)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()
