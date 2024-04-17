"""Module "consumer".
About:
    The module provides a consumer class
    to listen to RabbitMQ queue
    and getting the byte data in JSON formats
    string.
"""

from .custom import consumer


__all__ = ("consumer",)
