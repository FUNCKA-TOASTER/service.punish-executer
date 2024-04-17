"""Module "logger"."""

import logging
import config
from tools import msk_now
from .formatters import LoggingFormatters


class Logger(LoggingFormatters):
    """Logger class, creator of a new instance,
    Let's start registering. Provides basic
    logging functionality.
    """

    def __init__(self):
        self._setup_logger(name=config.SERVICE_NAME, date=msk_now())

    def _setup_logger(self, name: str, date: str):
        self.logger = logging.getLogger(name)

        date = date.replace("-", ".")
        date = date.replace(":", "-")

        stream_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(
            filename="./logs/" + date + ".log", encoding="utf-8", mode="w"
        )

        stream_handler.setFormatter(self.get_formatter_colored("red"))
        file_handler.setFormatter(self.get_formatter())

        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

        self.logger.setLevel(logging.DEBUG)

    async def info(self, text: str):
        """Logs a message as info.

        Args:
            text (str): Text of log message.
        """
        self.logger.info(text)

    async def debug(self, text: str):
        """Logs a message as debug.

        Args:
            text (str): Text of log message.
        """
        self.logger.debug(text)

    async def warning(self, text: str):
        """Logs a message as warning.

        Args:
            text (str): Text of log message.
        """
        self.logger.warning(text)

    async def error(self, text: str):
        """Logs a message as error.

        Args:
            text (str): Text of log message.
        """
        self.logger.error(text)

    async def critical(self, text: str):
        """Logs a message as critical.

        Args:
            text (str): Text of log message.
        """
        self.logger.critical(text)


logger = Logger()
