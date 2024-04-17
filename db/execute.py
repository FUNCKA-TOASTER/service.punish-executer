"""Module "db" """


class Executer(object):
    """Class providing functions
    for basic SQL queries.
    """

    _ops = {"__le": "<=", "__lt": "<", "__ge": ">=", "__gt": ">", "__nt": "!="}

    def __init__(self, connection, cursor):
        self.con = connection
        self.cur = cursor

    def select(self, schema: str, table: str, fields: tuple = None, **rows) -> tuple:
        """
        Accepts arguments for fields, comparisons, etc.,
        forms a database select query from them and returns the result of its execution.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10

        Args:
            fields (tuple, optional): Fields for which it is necessary to obtain data
            in the database. Defaults to None.

        Returns:
            str: MySQL query string.
        """
        if fields:
            summary_fields = ", ".join(fields)
        else:
            summary_fields = "*"

        query = f"SELECT {summary_fields} FROM {table}"

        if rows:
            summary_rows = " AND ".join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute(f"USE {schema};")
        self.cur.execute(query)
        result = self.cur.fetchall()
        return result

    def insert(self, schema: str, table: str, on_duplicate=None, **rows):
        """
        Takes arguments for fields, comparisons, etc.,
        forms a database insert query from them and inserts data when it is executed.

        Args:
            on_duplicate (str, optional): On duplicate action.
            Can be "ignore" or "update". Defaults to None.
        """
        if not rows:
            return

        summary_keys = ", ".join(rows.keys())  # Might be incorrect
        summary_values = ", ".join([f"'{value}'" for value in rows.values()])
        query = f""" INSERT INTO {table} ({summary_keys})
                     VALUES ({summary_values})
                """

        if on_duplicate == "ignore":
            query += " ON DUPLICATE KEY UPDATE id=id"

        if on_duplicate == "update":
            query += f""" ON DUPLICATE KEY UPDATE {', '.join(
                            [f"{key}='{value}'" for key, value in rows.items()]
                        )}
                     """

        query += ";"

        self.cur.execute(f"USE {schema};")
        self.cur.execute(query)

    def update(self, schema: str, table: str, new_data: dict, **rows):
        """
        Accepts arguments for fields, comparisons, etc.,
        forms a query from them to update the database
        and updates the data according to the dictionary
        of correspondences received as input when executing the request.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10

        Args:
            new_data (dict): Dict of correspondences for replacing variable values.
        """
        if not new_data:
            return

        summary_fields = ", ".join(
            [f"{key}='{value}'" for key, value in new_data.items()]
        )
        query = f"UPDATE {table} SET {summary_fields}"

        if rows:
            summary_rows = " AND ".join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute(f"USE {schema};")
        self.cur.execute(query)

    def delete(self, schema: str, table: str, **rows):
        """
        Takes arguments for fields, comparisons, etc.,
        forms a request from them to delete from the
        database and deletes data according to the
        conditions specified by the comparison operators.
        Keys that mimic comparison operators:
            1) __le -> <= \n
            2) __lt -> <  \n
            3) __ge -> >= \n
            4) __gt -> >  \n
            5) __nt -> != \n

        Example rows:
            id__lt=10 -> id<10
        """
        query = f"DELETE FROM {table}"

        if rows:
            summary_rows = " AND ".join(self._get_ratio(rows))
            query += f" WHERE {summary_rows}"

        query += ";"

        self.cur.execute(f"USE {schema};")
        self.cur.execute(query)

    def raw(self, schema: str, query: str):
        """Raw query executer.

        Args:
            schema (str): Schema name.
            query (str): Query string.

        Returns:
            object: MySQL cursor object.
        """
        self.cur.execute(f"USE {schema};")
        self.cur.execute(query)

        return self.cur

    def _get_ratio(self, rows: dict) -> list:
        """
        When specifying a method for comparing variables in an ORM query method,
        you must use keywords. Key characters are transformed by this
        method into comparison operators. The function returns a list
        of strings that are arranged according to the desired pattern.

        Args:
            rows (dict): rows with transformation keys into comparison operators

        Returns:
            list: list of args with sql somprassion operators.
        """
        summary = []
        for key, value in rows.items():
            op = key[-4:-1] + key[-1]
            op = self._ops.get(op, "=")

            if op != "=":
                key = key[0:-4]

            summary.append(f"{key} {op} '{value}'")

        return summary
