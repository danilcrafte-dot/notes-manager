"""Налаштування логування подій у файл і консоль."""
import logging


def setup_logger(log_file: str = "notes_app.log") -> logging.Logger:
    """Створює логер, що пише у файл (усі події) і в консоль (попередження)."""
    logger = logging.getLogger("notes_app")
    if logger.handlers:  # не додавати обробники повторно
        return logger
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(fmt)
    logger.addHandler(file_handler)

    console = logging.StreamHandler()
    console.setLevel(logging.WARNING)
    console.setFormatter(fmt)
    logger.addHandler(console)
    return logger
