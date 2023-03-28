import logging


class LoggerProvider:
    @staticmethod
    def get_logger() -> logging.Logger:
        return logging.getLogger()
