from sqlite3 import Connection

from db import SqliteDB
from db.queries import BaseQuery


class UrlOfVisit(BaseQuery):
    database: SqliteDB

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.database = SqliteDB.get_instance()

    def get_url_id_by_url(self, url: str) -> int:
        url_id = self._select_row(
            table_name='url_of_visit',
            fields=['id'],
            where={
                'url': url
            }
        )
        return url_id

    def add_url(self, url: str, parent_id: int):
        self._insert_row(
            table_name='url_of_visit',
            url=url,
            parent_id=parent_id
        )
        self.connection.commit()
