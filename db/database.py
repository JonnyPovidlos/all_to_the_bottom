import sqlite3


class SqliteDB:

    _connection: sqlite3.Connection

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
