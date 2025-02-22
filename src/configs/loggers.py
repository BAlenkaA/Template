import logging
from datetime import datetime
from logging.config import dictConfig

from pydantic import BaseModel
from pythonjsonlogger import jsonlogger

from src.configs.config import settings


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(
            log_record, record, message_dict
        )
        log_record["level"] = record.levelname
        log_record["service-name"] = settings.SERVICE_TITLE
        log_record["timestamp"] = datetime.now()
        # log_record["version"] = app_settings.SERVICE_VERSION
        # log_record["api-version"] = app_settings.API_VERSION


class LogConfig(BaseModel):
    LOGGER_NAME: str = settings.SERVICE_TITLE
    LOG_FORMAT: str = "%(level)s | %(asctime)s | %(message)s | %(filename)s | %(lineno)s | %(funcName)20s"  # noqa: E501
    LOG_LEVEL: str = settings.LOG_LEVEL

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: dict = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {
            "()": CustomJsonFormatter,
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers: dict = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "console": {
            "formatter": "json",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    }
    loggers: dict = {
        LOGGER_NAME: {"handlers": ["console"], "level": LOG_LEVEL},
    }


dictConfig(LogConfig().model_dump())

logger = logging.getLogger(settings.SERVICE_TITLE)
