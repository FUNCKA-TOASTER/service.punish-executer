"""Module "db".

File:
    instance.py

About:
    File describing the database class instances used.
"""

from funcka_bots.database import Database, build_connection_uri
from config import ALCHEMY_SETUP, DBMS_CREDS


# Database instance
TOASTER_DB = Database(build_connection_uri(ALCHEMY_SETUP, DBMS_CREDS), debug=False)
