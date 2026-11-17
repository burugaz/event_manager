"""Вспомогательные функции безопасного ввода."""
from datetime import date, datetime


def input_int(prompt: str) -> int:
    """Запросить целое число; при ошибке ввода повторить запрос."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите целое число")


def input_date(prompt: str) -> date:
    """Запросить дату в формате ДД.ММ.ГГГГ; при ошибке повторить запрос."""
    while True:
        try:
            return datetime.strptime(input(prompt).strip(), "%d.%m.%Y").date()
        except ValueError:
            print("Ошибка: введите дату в формате ДД.ММ.ГГГГ")
