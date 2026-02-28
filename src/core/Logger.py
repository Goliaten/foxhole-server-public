from datetime import datetime
import logging
import logging.config
import os
import sys
import config


class exclude_warning(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.WARNING


class Logger(logging.Logger):
    initialised = False

    def __init__(
        self, name=config.LOGGER_NAME_PREFIX, level=config.LOG_LEVEL, *args, **kwargs
    ):
        if not Logger.initialised:
            # logger = logging.getLogger(config.LOGGER_NAME_PREFIX)
            logging.config.dictConfig(dict_config)
            Logger.initialised = True

        super().__init__(name, level, *args, **kwargs)

    def get(self, name="", level=config.LOG_LEVEL):
        name = ".".join([config.LOGGER_NAME_PREFIX, name])

        logger = logging.getLogger(name)
        if (
            logger.level == logging._nameToLevel.get(level)
            if isinstance(level, str)
            else level
        ):
            return logger
        else:
            logger.setLevel(level)
            return logger


dict_config = {
    "version": 1,
    "formatters": {
        "printout": {"format": "[%(asctime)s] %(message)s"},
        "warning": {"format": "[%(asctime)s] [%(levelname)s|%(levelno)s] %(message)s"},
        "full": {
            "format": "[%(asctime)s] [%(levelname)s|%(levelno)s] [%(filename)s:%(funcName)s] %(message)s"
        },
    },
    "filters": {
        "exclude_warning": {
            "()": exclude_warning,
        }
    },
    "handlers": {
        "printout": {
            "class": "logging.StreamHandler",
            "level": config.LOG_LEVEL,
            "formatter": "printout",
            "filters": ["exclude_warning"],
            "stream": sys.stdout,
        },
        "error": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "warning",
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "formatter": "full",
            "filename": os.path.join(
                config.LOG_DIR,
                f"stockpile_scanner_{datetime.strftime(datetime.now(), '%Y%m')}.log",
            ),
            "maxBytes": 4 * 1000 * 1000,
        },
    },
    "loggers": {
        config.LOGGER_NAME_PREFIX: {
            "handlers": ["printout", "error", "file_handler"],
        }
    },
}
