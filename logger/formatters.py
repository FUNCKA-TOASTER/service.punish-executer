"""Module "logger"."""

import logging
from colorama import Fore


class LoggingFormatters(object):
    """Formatting set class."""

    def get_formatter_colored(self, color: str):
        """Provides a formatter with color output.
        Required primarily for console output.

        Args:
            color (str): Main information text color.

        Returns:
            Formatter: Formatter object for the logger.
        """
        colors = {"red": Fore.RED, "blue": Fore.BLUE, "light_green": Fore.LIGHTGREEN_EX}

        formatter = logging.Formatter(
            colors[color]
            + "[ %(name)s | %(levelname)s | %(asctime)s ] "
            + Fore.WHITE
            + "Message: %(message)s"
        )

        return formatter

    def get_formatter(self):
        """Provides a formatter with color output.
        Required primarily for file output.

        Args:
            color (str): Main information text color.

        Returns:
            Formatter: Formatter object for the logger.
        """
        formatter = logging.Formatter(
            "[ %(name)s | %(levelname)s | %(asctime)s ] " + "Message: %(message)s"
        )

        return formatter
