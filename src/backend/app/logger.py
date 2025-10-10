from logging import Logger

from uvicorn.main import logger


def get_logger() -> Logger:
    return logger
