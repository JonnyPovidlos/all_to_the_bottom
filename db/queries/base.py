import sqlite3
from sqlite3 import Connection, Row


class BaseQuery:

    connection: Connection

    def __init__(self, connection: Connection):
        self.connection = connection

    @classmethod
    def make_placeholders(cls, n):
        return ', '.join('?' for _ in range(n))

    @classmethod
    def make_query_fields(cls, fields):
        return ', '.join(f'{field}' for field in fields)

    @classmethod
    def make_where_fields(cls, fields: dict):
        return ' WHERE ' + ', '.join(f'{key} = "{value}"' for key, value in fields.items())

    def insert_row(self, table_name, **fields):
        params = self.make_query_fields(fields)
        placeholders = self.make_placeholders(len(fields))
        insert_query = f'INSERT INTO {table_name}({params}) VALUES ({placeholders})'
        try:
            cur = self.connection.execute(insert_query, (*fields.values(),))
        except sqlite3.IntegrityError:
            pass
        else:
            return cur.lastrowid

    def select_row(self, table_name, fields: list, where: dict = None):
        fields_to_select = self.make_query_fields(fields)
        select_query = f'SELECT {fields_to_select} FROM {table_name}'
        if where:
            select_query += self.make_where_fields(where)
        cur = self.connection.execute(select_query)
        row = cur.fetchone()
        return dict(row)

