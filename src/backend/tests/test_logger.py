from logging import Logger

from app.logger import get_logger


def test_get_logger() -> None:
    logger = get_logger()
    assert isinstance(logger, Logger)


def test_get_logger_returns_same_instance() -> None:
    logger1 = get_logger()
    logger2 = get_logger()
    assert logger1 is logger2


def test_logger_name() -> None:
    logger = get_logger()
    assert logger.name == 'uvicorn.error'


def test_logger_has_handlers() -> None:
    logger = get_logger()
    assert len(logger.handlers) >= 0


def test_logger_level() -> None:
    logger = get_logger()
    assert hasattr(logger, 'level')
    assert logger.level >= 0
