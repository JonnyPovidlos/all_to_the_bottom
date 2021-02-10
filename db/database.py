import sqlite3


class SqliteDB:

    _connection: sqlite3.Connection
    __instance__ = None

    def __init__(self):
        if not SqliteDB.__instance__:
            SqliteDB.__instance__ = self
        else:
            raise Exception(f'Экземпляр класса {self.__class__.__name__} уже был создан')

    def close_connection(self):
        self._connection.close()

    @staticmethod
    def get_instance():
        if not SqliteDB.__instance__:
            return SqliteDB()
        return SqliteDB.__instance__

    @property
    def connection(self) -> sqlite3.Connection:
        self._connect()
        return self._connection

    def _connect(self):
        connection_string = 'db.db'
        self._connection = sqlite3.connect(
            connection_string,
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        self._connection.row_factory = sqlite3.Row

    def check_connection(self) -> dict:
        with self.connection as con:
            cur = con.execute('SELECT 1')
            return dict(cur.fetchone())
