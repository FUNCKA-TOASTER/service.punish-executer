"""Module "db"."""

import config
from .connection import Connection
from .execute import Executer


class DataBase(object):
    """
    The main class is the database view.
    Organizes a connection and implements
    access to table properties using
    object-relational methods of the base table.
    """

    def __init__(self, host: str, port: int, user: str, password: str):
        self._tunnel = Connection(host=host, port=port, user=user, password=password)

        self._execute = Executer(
            connection=self._tunnel.connection, cursor=self._tunnel.cursor
        )

    @property
    def execute(self):
        return self._execute

    @property
    def preset(self):
        pass


db = DataBase(
    host=config.MY_SQL_HOST,
    port=config.MY_SQL_PORT,
    user=config.MY_SQL_USER,
    password=config.MY_SQL_PSWD,
)
