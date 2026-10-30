"""Консольний інтерфейс користувача."""

MENU = """
=== Менеджер нотаток ===
1. Додати нотатку
2. Показати всі / фільтр
3. Переглянути нотатку
4. Редагувати нотатку
5. Видалити нотатку
6. Пошук
7. Категорії
0. Вихід
"""


def print_note(n, full=False):
    """Виводить нотатку (коротко або повністю)."""
    tags = ", ".join(n.tags) or "-"
    print(f"#{n.id} [{n.category}] {n.title}  (теги: {tags})")
    if full:
        print(f"  Створено: {n.created_at} | Оновлено: {n.updated_at}")
        print(f"  {n.content}")


def ask_id(prompt="ID нотатки: "):
    """Запитує числовий id; повертає None при помилці."""
    try:
        return int(input(prompt))
    except ValueError:
        print("Потрібне число.")
        return None


def parse_tags(raw: str) -> list:
    return [t for t in raw.split(",")]


def run(manager):
    """Головний цикл меню."""
    while True:
        print(MENU)
        choice = input("Ваш вибір: ").strip()
        try:
            if choice == "1":
                title = input("Заголовок: ")
                content = input("Текст: ")
                cat = input("Категорія (Enter = Загальне): ")
                tags = parse_tags(input("Теги через кому: "))
                n = manager.add(title, content, cat or "Загальне", tags)
                print(f"Додано нотатку #{n.id}")
            elif choice == "2":
                cat = input("Категорія (Enter = всі): ") or None
                tag = input("Тег (Enter = всі): ") or None
                items = manager.list_all(cat, tag)
                if not items:
                    print("Нотаток немає.")
                for n in items:
                    print_note(n)
            elif choice == "3":
                i = ask_id()
                if i is not None:
                    print_note(manager.get(i), full=True)
            elif choice == "4":
                i = ask_id()
                if i is not None:
                    print("Enter - залишити без змін")
                    t = input("Новий заголовок: ") or None
                    c = input("Новий текст: ") or None
                    cat = input("Нова категорія: ") or None
                    raw = input("Нові теги через кому: ")
                    manager.update(i, t, c, cat, parse_tags(raw) if raw else None)
                    print("Оновлено.")
            elif choice == "5":
                i = ask_id()
                if i is not None:
                    manager.delete(i)
                    print("Видалено.")
            elif choice == "6":
                found = manager.search(input("Запит: "))
                if not found:
                    print("Нічого не знайдено.")
                for n in found:
                    print_note(n)
            elif choice == "7":
                for cat, count in manager.categories().items():
                    print(f"{cat}: {count}")
            elif choice == "0":
                print("До побачення!")
                break
            else:
                print("Невірний вибір.")
        except (KeyError, ValueError) as e:
            msg = e.args[0] if e.args else e
            print(f"Помилка: {msg}")
            manager.logger.warning("Помилка: %s", msg)
