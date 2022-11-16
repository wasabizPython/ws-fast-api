import logging
from logging.handlers import RotatingFileHandler
from decouple import config


def log(name, log_file, log_format, level=logging.INFO):
    fileHandler = RotatingFileHandler(
        filename=log_file,
        maxBytes=int(config('LOG_SIZE')),
        backupCount=int(config('LOG_BACKUP'))
    )
    formatter = logging.Formatter(log_format)
    fileHandler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(fileHandler)
    return logger
