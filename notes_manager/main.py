"""Точка входу застосунку."""
from notes.logger import setup_logger
from notes.storage import JsonStorage
from notes.manager import NoteManager
from notes import cli


def main():
    logger = setup_logger()
    logger.info("Застосунок запущено")
    manager = NoteManager(JsonStorage("notes.json"), logger)
    cli.run(manager)
    logger.info("Застосунок завершено")


if __name__ == "__main__":
    main()
