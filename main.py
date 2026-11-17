"""ПР1. Начальный сценарий: проверка возможности регистрации
сотрудника на корпоративное мероприятие."""
from datetime import date

event_title = "Осенний тимбилдинг"
event_date = date(2026, 12, 12)
capacity = 50
registered_count = 47
employee_name = "Иван Петров"


def calculate_free_seats(capacity, registered_count):
    """Вернуть количество свободных мест (не меньше нуля)."""
    free_seats = capacity - registered_count
    if free_seats < 0:
        return 0
    return free_seats


def calculate_fill_percent(capacity, registered_count):
    """Вернуть процент заполненности мероприятия (целое число)."""
    return int(registered_count / capacity * 100)


def is_event_upcoming(event_date, today):
    """Проверить, что мероприятие ещё не прошло."""
    return event_date >= today


def get_registration_status(free_seats, is_upcoming):
    """Вернуть текстовый статус регистрации на мероприятие."""
    if not is_upcoming:
        return "Мероприятие уже прошло, регистрация закрыта"
    if free_seats == 0:
        return "Свободных мест нет"
    return "Регистрация открыта"


today = date.today()
free_seats = calculate_free_seats(capacity, registered_count)
fill_percent = calculate_fill_percent(capacity, registered_count)
upcoming = is_event_upcoming(event_date, today)

print(f"Мероприятие: {event_title}")
print(f"Дата: {event_date}")
print(f"Сотрудник: {employee_name}")
print(f"Свободных мест: {free_seats} из {capacity}")
print(f"Заполненность: {fill_percent}%")
print(get_registration_status(free_seats, upcoming))
