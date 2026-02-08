import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path


def init_logger() -> None:
    root_logger = logging.getLogger("pythonQEPest")

    log_file: str = os.getenv("LOG_FILE_LOCATION", "logs/app.log")
    level = os.getenv("LOG_LEVEL", "INFO").upper()

    match level:
        case "DEBUG":
            level = logging.DEBUG
        case "INFO":
            level = logging.INFO
        case "WARNING":
            level = logging.WARNING
        case "ERROR":
            level = logging.ERROR
        case _:
            level = logging.INFO

    if root_logger.handlers:
        return

    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=1_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
