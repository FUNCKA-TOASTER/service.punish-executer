"""Module "config".

File:
    __init__.py

About:
    Initializing the "config" module.
"""

from .config import (
    REDIS_CREDS,
    CHANNEL_NAME,
    TOKEN,
    GROUP_ID,
    API_VERSION,
    ALCHEMY_SETUP,
    DBMS_CREDS,
)


__all__ = (
    "REDIS_CREDS",  # Redis (broker) credentials
    "CHANNEL_NAME",  # Broker subscription channel name
    "TOKEN",  # API token
    "GROUP_ID",  # ID of the group
    "API_VERSION",  # API Version use
    "ALCHEMY_SETUP",  # Setup for sqlalchemy. Driver, Database and DBMS.
    "DBMS_CREDS",  # DBMS credentials includes host, port, user, password.
)
