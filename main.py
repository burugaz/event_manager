"""Точка запуска приложения «Система организации корпоративных мероприятий» (ООП)."""
import os
from datetime import date
from models.event import Event
from models.registration import Registration
from events import (
    add_event,
    calculate_fill_percent,
    find_event_by_id,
    sort_events_by_date,
)
from registrations import (
    cancel_registration,
    count_registrations_for_event,
    create_registration,
    get_event_status_text,
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
3. Проверить статус регистрации
4. Зарегистрировать сотрудника
5. Отменить регистрацию
6. Показать регистрации
7. Добавить мероприятие
0. Выход"""


def show_events(events: list[Event], registrations: list[Registration]) -> None:
    """Вывести список мероприятий."""
    if not events:
        print("Мероприятий нет")
        return

    sorted_events = sort_events_by_date(events)
    for event in sorted_events:
        registered = count_registrations_for_event(registrations, event.id)
        percent = calculate_fill_percent(event, registered)
        print(
            f'{event.id}. {event.title} | {event.date.strftime("%d.%m.%Y")} | '
            f'мест занято: {registered}/{event.capacity} ({percent}%)'
        )


def show_registrations(registrations: list[Registration]) -> None:
    """Вывести список активных регистраций."""
    active_regs = [r for r in registrations if not r.is_cancelled]
    if not active_regs:
        print("Активных регистраций нет")
        return

    for reg in active_regs:
        print(f'{reg.id}. {reg.employee_name} -> {reg.event.title} ({reg.event.date.strftime("%d.%m.%Y")})')


def ask_event_id(events: list[Event]) -> int | None:
    """Запросить ID мероприятия."""
    event_id = input_int("ID мероприятия: ")
    if find_event_by_id(events, event_id) is None:
        print("Мероприятие не найдено")
        return None
    return event_id


def search_events(events: list[Event]) -> None:
    """Найти и вывести мероприятия по названию."""
    found = []
    query = input("Название мероприятия: ")
    if query.strip():
        query_lower = query.strip().casefold()
        found = [e for e in events if query_lower in e.title.casefold()]

    if not found:
        print("Ничего не найдено")
    for event in found:
        print(f'{event.id}. {event.title} | {event.date.strftime("%d.%m.%Y")}')


def check_registration_status(
    events: list[Event],
    registrations: list[Registration],
) -> None:
    """Вывести статус регистрации на выбранное мероприятие."""
    event_id = ask_event_id(events)
    if event_id is not None:
        event = find_event_by_id(events, event_id)
        if event:
            print(get_event_status_text(event, registrations, date.today()))


def register_employee(
    events: list[Event],
    registrations: list[Registration],
) -> None:
    """Зарегистрировать сотрудника и сохранить регистрации."""
    event_id = ask_event_id(events)
    if event_id is None:
        return
    employee = input("ФИО сотрудника: ")
    try:
        reg = create_registration(events, registrations, event_id, employee, date.today())
        save_registrations(REGISTRATIONS_FILE, registrations)
        print(f'Регистрация создана, ID: {reg.id}')
    except ValueError as error:
        print(f"Ошибка: {error}")


def cancel_employee_registration(registrations: list[Registration]) -> None:
    """Отменить регистрацию и сохранить изменения."""
    registration_id = input_int("ID регистрации: ")
    if cancel_registration(registrations, registration_id):
        save_registrations(REGISTRATIONS_FILE, registrations)
        print("Регистрация отменена")
    else:
        print("Регистрация не найдена или уже отменена")


def create_event(events: list[Event]) -> None:
    """Добавить мероприятие и сохранить мероприятия."""
    title = input("Название мероприятия: ")
    event_date = input_date("Дата (ДД.ММ.ГГГГ): ")
    capacity = input_int("Вместимость: ")
    try:
        add_event(events, title, event_date, capacity)
        save_events(EVENTS_FILE, events)
        print("Мероприятие добавлено")
    except ValueError as error:
        print(f"Ошибка: {error}")


def main() -> None:
    """Точка запуска: цикл меню и вызов функций проекта."""
    # Загрузка данных как списков/словарей объектов
    events_dict = load_events(EVENTS_FILE)
    events_list = list(events_dict.values())

    registrations = load_registrations(REGISTRATIONS_FILE, events_dict)

    while True:
        print(MENU)
        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_events(events_list, registrations)
        elif choice == "2":
            search_events(events_list)
        elif choice == "3":
            check_registration_status(events_list, registrations)
        elif choice == "4":
            register_employee(events_list, registrations)
        elif choice == "5":
            cancel_employee_registration(registrations)
        elif choice == "6":
            show_registrations(registrations)
        elif choice == "7":
            create_event(events_list)
        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неизвестный пункт меню")


if __name__ == "__main__":
    main()