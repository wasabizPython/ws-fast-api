import logging
from logging.handlers import RotatingFileHandler


def log(name, log_file, log_format, level=logging.INFO):
    fileHandler = RotatingFileHandler(
        filename=log_file,
        maxBytes=50 * 1024 * 1024,
        backupCount=200
    )
    formatter = logging.Formatter(log_format)
    fileHandler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(fileHandler)
    return logger