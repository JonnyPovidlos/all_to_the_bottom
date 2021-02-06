import os

from db import SqliteDB, create_tables_db, queries
from helpers import parse_log_file, parse_url

if __name__ == '__main__':
    db = SqliteDB()
    if not os.path.exists(os.path.join(os.getcwd(), 'db.db')):
        create_tables_db(db)
    rows = parse_log_file('logs.txt')

    for row in rows:
        with db.connection as connection:
            query = queries.BaseQuery(connection)

            query.insert_row(
                table_name='ip_address',
                ip=row['ip']
            )

            ip_id = query.select_row(
                table_name='ip_address',
                fields=['id'],
                where={
                    'ip': row['ip']
                }
            )['id']

            query.insert_row(
                table_name='date_of_visit',
                date_visit=row['date'],
                id_ip=ip_id
            )

            query.insert_row(
                table_name='time_of_visit',
                time_visit=row['time'],
                id_ip=ip_id
            )
            url = parse_url(row['url'])

            for u in url:
                parent_id = query.select_row(
                    table_name='url_of_visit',
                    fields=['id'],
                    where={
                        'url': u['parent']
                    }
                )['id']
                query.insert_row(
                    table_name='url_of_visit',
                    url=u['url'],
                    parent_id=parent_id
                )
            url_id = query.select_row(
                table_name='url_of_visit',
                fields=['id'],
                where={
                    'url': url[len(url) - 1]['url']
                }
            )['id']

            query.insert_row(
                table_name='ip_to_url',
                ip_id=ip_id,
                url_id=url_id
            )
