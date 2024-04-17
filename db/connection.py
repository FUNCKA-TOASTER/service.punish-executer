"""Module "db"."""

import MySQLdb


class Connection(object):
    """
    This class provides connection to the MySQL database.
    """

    def __init__(self, host: str, port: int, user: str, password: str):
        try:
            self._connection = MySQLdb.connect(
                host=host, port=port, user=user, password=password
            )
            self._connection.autocommit(True)
            self._cursor = self._connection.cursor()

            print(f"Connected to MySQL Server with <User: {user}>.")

        except MySQLdb.Error as error:
            print(f"Failed to connect to MySQL Server: {error}")

    @property
    def cursor(self):
        """
        Returns database cursor object.
        """
        return self._cursor

    @property
    def connection(self):
        """
        Returns database connection object.
        """
        return self._connection
