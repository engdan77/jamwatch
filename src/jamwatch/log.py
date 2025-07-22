from loguru import logger as loguru_logger

loguru_logger.add("jamwatch.log", rotation="100 MB")


def info(message):
    loguru_logger.info(message)


def warning(message):
    loguru_logger.warning(message)


def error(message):
    loguru_logger.error(message)


def debug(message):
    loguru_logger.debug(message)