"""Модель даних: нотатка."""
from dataclasses import dataclass, field, asdict
from datetime import datetime


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class Note:
    """Нотатка з категорією та тегами."""
    id: int
    title: str
    content: str
    category: str = "Загальне"
    tags: list = field(default_factory=list)
    created_at: str = field(default_factory=_now)
    updated_at: str = field(default_factory=_now)

    def to_dict(self) -> dict:
        """Перетворює нотатку на словник для запису в JSON."""
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Note":
        """Створює нотатку зі словника."""
        return Note(**data)
