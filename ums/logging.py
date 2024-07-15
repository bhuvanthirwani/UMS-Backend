#!/usr/bin/env python3

import sys
import logging
from typing import Union
from loguru import logger
from ums.settings import settings


class InterceptHandler(logging.Handler):
    """
    Default handler from examples in loguru documentation.

    This handler intercepts all log requests and
    passes them to loguru.

    For more info see:
    https://loguru.readthedocs.io/en/stable/overview.html#entirely-compatible-with-standard-logging
    """

    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        """
        Propagates logs to loguru.

        :param record: record to log.
        """
        try:
            level: Union[str, int] = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back  # type: ignore
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def init_logger(config: dict = {}):  # noqa
    log_level: str = "INFO"
    log_fmt: str = "[%(levelname)s] - %(message)s"
    # TODO: {name}:{function}:{line} -> does not gives log file name debugging needed.
    # trunk-ignore(flake8/E501)
    loguru_format = "{time} - <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{level.icon} [{level}] - {message}</level>"
    date_fmt: str = "%Y-%m-%d %H:%M:%S"

    if config is not None:
        log_level = config.get("log_level", "INFO")
        numeric_level = getattr(logging, log_level.upper(), None)
        if not isinstance(numeric_level, int):
            numeric_level = getattr(logging, "INFO", None)
        log_fmt = config.get("logging_format", log_fmt)
        date_fmt = config.get("logging_datefmt", date_fmt)

    if "loguru" in sys.modules:
        loguru_format = config.get("loguru_format", loguru_format)
        loguru_config = {
            "handlers": [
                {"sink": sys.stdout, "format": loguru_format, "colorize": True},
                {
                    "sink": "server.log",
                    "serialize": True,
                    "enqueue": True,
                    "rotation": "512MB",
                },
            ],
        }
        logger.configure(**loguru_config)
        logging.basicConfig(
            handlers=[InterceptHandler()],
            level=numeric_level,
            format=log_fmt,
            datefmt=date_fmt,
            force=True,
        )
    else:
        # use standard logger
        logging.basicConfig(
            level=numeric_level,
            format=log_fmt,
            datefmt=date_fmt,
            force=True,
        )

    # "Register" new logging level to be compatible with loguru's success level
    SUCCESS = 35
    logging.addLevelName(SUCCESS, "SUCCESS")
    logging.Logger.success = success


def success(self, msg, *args, **kwargs):
    SUCCESS = 35
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, msg, args, **kwargs)


def configure_logging(**kwargs) -> None:  # pragma: no cover
    """Configures logging."""
    intercept_handler = InterceptHandler()
    if flask_app := kwargs.get('app', None):
        flask_app.logger.addHandler(intercept_handler)

    logging.basicConfig(handlers=[intercept_handler], level=logging.NOTSET)

    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("uvicorn."):
            logging.getLogger(logger_name).handlers = []

    # change handler for default uvicorn logger
    logging.getLogger("uvicorn").handlers = [intercept_handler]
    logging.getLogger("uvicorn.access").handlers = [intercept_handler]

    # set logs output, level and format
    logger.remove()
    logger.add(
        sys.stdout,
        level=settings.log_level.value,
    )
    init_logger(kwargs)
