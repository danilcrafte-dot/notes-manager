"""Збереження та завантаження нотаток у JSON-файл."""
import json
import os
from .models import Note


class JsonStorage:
    """Файлове сховище нотаток."""

    def __init__(self, path: str = "notes.json"):
        self.path = path

    def load(self) -> list:
        """Читає всі нотатки; якщо файла немає або він пошкоджений - порожній список."""
        if not os.path.exists(self.path):
            return []
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                return [Note.from_dict(item) for item in json.load(f)]
        except (json.JSONDecodeError, TypeError):
            return []

    def save(self, notes: list) -> None:
        """Записує всі нотатки у файл."""
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump([n.to_dict() for n in notes], f, ensure_ascii=False, indent=2)
