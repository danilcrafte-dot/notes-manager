"""Бізнес-логіка: CRUD, фільтрація за категорією/тегом, пошук."""
from datetime import datetime
from .models import Note


class NoteManager:
    """Керує колекцією нотаток і зберігає зміни через storage."""

    def __init__(self, storage, logger):
        self.storage = storage
        self.logger = logger
        self.notes = storage.load()

    def _next_id(self) -> int:
        return max((n.id for n in self.notes), default=0) + 1

    @staticmethod
    def _clean_tags(tags) -> list:
        """Нормалізує теги: нижній регістр, без дублікатів і порожніх."""
        result = []
        for t in tags or []:
            t = t.strip().lower()
            if t and t not in result:
                result.append(t)
        return result

    def add(self, title, content, category="Загальне", tags=None) -> Note:
        """Додає нову нотатку."""
        if not title.strip():
            raise ValueError("Заголовок не може бути порожнім")
        note = Note(self._next_id(), title.strip(), content,
                    category.strip() or "Загальне", self._clean_tags(tags))
        self.notes.append(note)
        self.storage.save(self.notes)
        self.logger.info("Додано нотатку #%d '%s'", note.id, note.title)
        return note

    def get(self, note_id: int) -> Note:
        """Повертає нотатку за id або кидає KeyError."""
        for n in self.notes:
            if n.id == note_id:
                return n
        raise KeyError(f"Нотатку #{note_id} не знайдено")

    def update(self, note_id, title=None, content=None, category=None, tags=None) -> Note:
        """Оновлює задані поля нотатки."""
        note = self.get(note_id)
        if title is not None:
            if not title.strip():
                raise ValueError("Заголовок не може бути порожнім")
            note.title = title.strip()
        if content is not None:
            note.content = content
        if category is not None:
            note.category = category.strip() or "Загальне"
        if tags is not None:
            note.tags = self._clean_tags(tags)
        note.updated_at = datetime.now().isoformat(timespec="seconds")
        self.storage.save(self.notes)
        self.logger.info("Оновлено нотатку #%d", note_id)
        return note

    def delete(self, note_id: int) -> None:
        """Видаляє нотатку."""
        note = self.get(note_id)
        self.notes.remove(note)
        self.storage.save(self.notes)
        self.logger.info("Видалено нотатку #%d", note_id)

    def list_all(self, category=None, tag=None) -> list:
        """Повертає нотатки, за потреби відфільтровані за категорією та/або тегом."""
        result = self.notes
        if category:
            result = [n for n in result if n.category.lower() == category.lower()]
        if tag:
            result = [n for n in result if tag.lower() in n.tags]
        return result

    def search(self, query: str) -> list:
        """Пошук без урахування регістру за заголовком, текстом і тегами."""
        q = query.lower().strip()
        self.logger.info("Пошук: '%s'", q)
        return [n for n in self.notes
                if q in n.title.lower() or q in n.content.lower()
                or any(q in t for t in n.tags)]

    def categories(self) -> dict:
        """Статистика: категорія -> кількість нотаток."""
        stats = {}
        for n in self.notes:
            stats[n.category] = stats.get(n.category, 0) + 1
        return stats
