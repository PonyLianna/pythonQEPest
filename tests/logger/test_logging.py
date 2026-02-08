import logging
from pythonQEPest.logger import init_logger


def _reset_logger():
    logger = logging.getLogger("pythonQEPest")
    for h in list(logger.handlers):
        logger.removeHandler(h)
        h.close()
    logger.setLevel(logging.NOTSET)
    return logger


def test_logger_initialization():
    _reset_logger()
    try:
        init_logger()
        assert True  # If no exception is raised, the test passes
    except Exception as e:
        assert False, f"Logger initialization failed with exception: {e}"

def test_default_configuration(monkeypatch):
    _reset_logger()
    monkeypatch.delenv("LOG_FILE_LOCATION", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("APP_DEBUG_ENABLE", raising=False)

    init_logger()

    logger = logging.getLogger("pythonQEPest")
    assert logger.level == logging.INFO
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
    assert file_handlers, "File handler should be configured"
    assert file_handlers[0].baseFilename.endswith(
        "\\logs\\app.log"
    ), "Default LOG_FILE_LOCATION should be logs/app.log"

def _logger_levels(monkeypatch, level: str, assert_level):
    _reset_logger()

    monkeypatch.setenv("LOG_LEVEL", level)
    init_logger()

    logger = logging.getLogger("pythonQEPest")
    assert logger.level == assert_level


def test_logger_levels(monkeypatch):
    """ Logger levels testing"""
    _logger_levels(monkeypatch, level="DEBUG", assert_level=logging.DEBUG)
    _logger_levels(monkeypatch, level="INFO", assert_level=logging.INFO)
    _logger_levels(monkeypatch, level="WARNING", assert_level=logging.WARNING)
    _logger_levels(monkeypatch, level="ERROR", assert_level=logging.ERROR)
    _logger_levels(monkeypatch, level="", assert_level=logging.INFO)


def test_file_location(monkeypatch):
    """ LOG_FILE_LOCATION testing"""

    # Test with custom LOG_FILE_LOCATION
    _reset_logger()
    monkeypatch.setenv("LOG_FILE_LOCATION", "test_logs/app.log")

    init_logger()

    logger = logging.getLogger("pythonQEPest")
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

    assert file_handlers, "File handler should be configured"
    assert file_handlers[0].baseFilename.endswith(
        "\\test_logs\\app.log"
    ), "File handler should use LOG_FILE_LOCATION"

    # Test with default LOG_FILE_LOCATION
    _reset_logger()
    monkeypatch.delenv("LOG_FILE_LOCATION", raising=False)

    init_logger()

    logger = logging.getLogger("pythonQEPest")
    file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]

    assert file_handlers, "File handler should be configured"
    assert file_handlers[0].baseFilename.endswith(
        "\\logs\\app.log"
    ), "File handler should use LOG_FILE_LOCATION"


def test_debug_option(monkeypatch):
    """ Debug switch testing"""
    _reset_logger()
    monkeypatch.setenv("APP_DEBUG_ENABLE", "false")

    init_logger()

    logger = logging.getLogger("pythonQEPest")
    assert len(logger.handlers) == 0

    _reset_logger()
    monkeypatch.setenv("APP_DEBUG_ENABLE", "true")

    init_logger()

    logger = logging.getLogger("pythonQEPest")
    assert len(logger.handlers) != 0
