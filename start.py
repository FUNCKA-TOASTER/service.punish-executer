"""Service "service.punishment-executer".

File:
    start.py

About:
    This service is responsible for receiving custom
    events from the Redis channel "punishment".
"""

import sys
from loguru import logger
from toaster.broker import (
    Subscriber,
    build_connection,
)
from handler import PunishmentHandler
import config


def setup_logger() -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <red>{module}</red> | <level>{level}</level> | {message}",
        level="DEBUG",
    )


def main():
    """Program entry point."""

    setup_logger()
    subscriber = Subscriber(client=build_connection(config.REDIS_CREDS))
    handler = PunishmentHandler()

    for event in subscriber.listen(channel_name=config.CHANNEL_NAME):
        handler(event)


if __name__ == "__main__":
    main()
