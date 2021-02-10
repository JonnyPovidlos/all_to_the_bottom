from sqlite3 import Connection

from db import SqliteDB
from db.queries import BaseQuery


class IpToUrl(BaseQuery):
    database: SqliteDB
    
    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.database = SqliteDB.get_instance()

    def add_ip_to_url(self, ip_id: int, url_id: int, date: str, time: str):
        self._insert_row(
            table_name='ip_to_url',
            ip_id=ip_id,
            url_id=url_id,
            date_visit=date,
            time_visit=time
        )
        self.connection.commit()
