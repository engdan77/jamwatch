import loguru

loguru.logger.level("DEBUG")


class Logger:
    def info(self, message):
        loguru.logger.info(message)

    def warning(self, message):
        loguru.logger.warning(message)

    def error(self, message):
        loguru.logger.error(message)

    def debug(self, message):
        loguru.logger.debug(message)


logger = Logger()
