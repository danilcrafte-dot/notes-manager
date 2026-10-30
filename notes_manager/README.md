# Менеджер нотаток із категоріями та пошуком

Консольний застосунок на Python для ведення нотаток: категорії, теги, пошук, редагування та видалення. Дані зберігаються у JSON, події логуються у файл.

## Технологічний стек
- Python 3.9+ (лише стандартна бібліотека: json, logging, dataclasses, unittest)
- Git / GitHub

## Структура
```
main.py             # точка входу
notes/models.py     # модель Note
notes/storage.py    # робота з JSON-файлом
notes/manager.py    # бізнес-логіка (CRUD, пошук, фільтри)
notes/cli.py        # консольне меню
notes/logger.py     # налаштування логування
tests/              # модульні тести
```

## Запуск
```bash
git clone <URL-репозиторію>
cd notes_manager
python main.py
```

## Тести
```bash
python -m unittest discover tests
```

## Формат даних (notes.json)
Масив об'єктів: `id`, `title`, `content`, `category`, `tags` (масив рядків), `created_at`, `updated_at` (ISO 8601).
