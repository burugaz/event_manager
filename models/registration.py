"""Класс, представляющий регистрацию сотрудника."""
from datetime import date
from models.event import Event


class Registration:
    """Регистрация сотрудника на мероприятие."""

    def __init__(self, reg_id: int, event: Event, employee_name: str, reg_date: date) -> None:
        self.id = reg_id
        self.event = event  # Ссылка на объект Event
        self.employee_name = employee_name.strip()
        self.reg_date = reg_date
        self.is_cancelled = False

    def cancel(self) -> None:
        """Отменяет регистрацию."""
        self.is_cancelled = True

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "event_id": self.event.id,
            "employee": self.employee_name,
            "is_cancelled": self.is_cancelled,
        }

    @classmethod
    def from_dict(cls, data: dict, events_map: dict[int, Event]) -> "Registration":
        """Создает объект Registration из словаря, связывая с Event."""
        event_id = data["event_id"]
        event = events_map.get(event_id)

        if event is None:
            raise ValueError(f"Мероприятие с ID {event_id} не найдено")

        # Дату регистрации можно брать из данных или ставить текущую,
        # если в старом JSON её нет. Для совместимости с ПР2 ставим заглушку или дату из данных.
        reg_date_str = data.get("date")
        reg_date = date.fromisoformat(reg_date_str) if reg_date_str else date.today()

        reg = cls(
            reg_id=data["id"],
            event=event,
            employee_name=data["employee"],
            reg_date=reg_date
        )
        if data.get("is_cancelled"):
            reg.cancel()
        return reg

    def __str__(self) -> str:
        status = "Отменена" if self.is_cancelled else "Активна"
        return f"Регистрация #{self.id}: {self.employee_name} на '{self.event.title}' [{status}]"