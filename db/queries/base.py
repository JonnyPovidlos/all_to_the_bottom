import sqlite3
from sqlite3 import Connection


class BaseQuery:

    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    @staticmethod
    def __make_placeholders(n: int) -> str:
        return ', '.join('?' for _ in range(n))

    @staticmethod
    def __make_query_fields(fields: list) -> str:
        return ', '.join(f'{field}' for field in fields)

    @staticmethod
    def __make_where_fields(fields: dict) -> str:
        return ' WHERE ' + ', '.join(f'{key} = "{value}"' for key, value in fields.items())

    @staticmethod
    def __return_row(row: dict):
        if len(row) == 1:
            return list(row.values())[0]
        else:
            return list(row.values())

    def _insert_row(self, table_name: str, **fields):
        params = self.__make_query_fields(list(fields.keys()))
        placeholders = self.__make_placeholders(len(fields))
        insert_query = f'INSERT INTO {table_name}({params}) VALUES ({placeholders})'
        try:
            cur = self.connection.execute(insert_query, (*fields.values(),))
        except sqlite3.IntegrityError:
            pass
        else:
            return cur.lastrowid

    def _select_row(self, table_name: str, fields: list, where: dict = None):
        fields_to_select = self.__make_query_fields(fields)
        select_query = f'SELECT {fields_to_select} FROM {table_name}'
        if where:
            select_query += self.__make_where_fields(where)
        cur = self.connection.execute(select_query)
        row = dict(cur.fetchone())
        return self.__return_row(row)
