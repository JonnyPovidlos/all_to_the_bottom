from sqlite3 import Connection

from db import SqliteDB
from db.queries import BaseQuery


class IpAddress(BaseQuery):
    database: SqliteDB

    def __init__(self, connection: Connection):
        super().__init__(connection)
        self.database = SqliteDB.get_instance()

    def add_ip(self, ip_address: str):
        self._insert_row(
            table_name='ip_address',
            ip=ip_address
        )
        self.connection.commit()

    def get_ip_id_by_ip_address(self, ip_address: str) -> int:
        id_ip = self._select_row(
            table_name='ip_address',
            fields=['id'],
            where={
                'ip': ip_address
            }
        )
        return id_ip



