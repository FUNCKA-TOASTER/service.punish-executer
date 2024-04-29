"""Module "producer".
About:
    Provides a producer client that sends data
    to rabbit.queue-broker service. Using JSON.
"""

from .custom import producer


__all__ = ("producer",)
