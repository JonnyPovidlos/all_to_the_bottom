from .database import SqliteDB


def create_tables_db(database: SqliteDB):

    with database.connection as connection:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS ip_address (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            ip TEXT NOT NULL UNIQUE
            );
            
            CREATE TABLE IF NOT EXISTS time_of_visit (
            time_visit TEXT NOT NULL,
            id_ip      INTEGER NOT NULL,
            PRIMARY KEY (time_visit, id_ip),
            FOREIGN KEY(id_ip) REFERENCES ip_address(ip)
            );
            
            CREATE TABLE IF NOT EXISTS date_of_visit (
            date_visit TEXT NOT NULL,
            id_ip      INTEGER NOT NULL,
            PRIMARY KEY (id_ip, date_visit),
            FOREIGN KEY(id_ip) REFERENCES ip_address(ip)
            );
            
            CREATE TABLE IF NOT EXISTS url_of_visit (
            id        INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            url       TEXT NOT NULL UNIQUE,
            parent_id INTEGER,
            FOREIGN KEY(parent_id) REFERENCES url_of_visit(id) ON DELETE SET NULL
            );
            
            INSERT INTO url_of_visit (url)
            VALUES ('/');
            
            CREATE TABLE IF NOT EXISTS ip_to_url (
            ip_id  INTEGER NOT NULL,
            url_id INTEGER NOT NULL,
            UNIQUE(ip_id, url_id)
            )
        """)
