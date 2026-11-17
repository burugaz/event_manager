"""Класс, представляющий мероприятие."""
from datetime import date


class Event:
    """Мероприятие: название, дата, вместимость."""

    def __init__(self, event_id: int, title: str, event_date: date, capacity: int) -> None:
        self.id = event_id
        self.title = title.strip()
        self.date = event_date
        self.capacity = capacity

    def is_upcoming(self, today: date) -> bool:
        """Проверяет, состоялось ли мероприятие."""
        return self.date >= today

    def has_seats(self, registered_count: int) -> bool:
        """Проверяет, есть ли свободные места."""
        return registered_count < self.capacity

    def to_dict(self) -> dict:
        """Преобразует объект в словарь для сохранения в JSON."""
        return {
            "id": self.id,
            "title": self.title,
            "date": self.date.isoformat(),
            "capacity": self.capacity,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Event":
        """Создает объект Event из словаря (загрузка из JSON)."""
        return cls(
            event_id=data["id"],
            title=data["title"],
            event_date=date.fromisoformat(data["date"]),
            capacity=data["capacity"],
        )

    def __str__(self) -> str:
        return f"{self.title} ({self.date.strftime('%d.%m.%Y')})"