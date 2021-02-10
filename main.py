import os

from db import(
    SqliteDB,
    IpAddress,
    UrlOfVisit,
    IpToUrl,
    create_tables_db,
)
from helpers import parse_log_file, parse_url

if __name__ == '__main__':

    database = SqliteDB()
    if not os.path.exists(os.path.join(os.getcwd(), 'db.db')):
        create_tables_db(database)
    rows = parse_log_file('tmp.txt')

    for row in rows:
        connection = database.connection
        IpAddress(connection).add_ip(row['ip'])
        ip_id = IpAddress(connection).get_ip_id_by_ip_address(row['ip'])

        parsed_url = parse_url(row['url'])
        for url in parsed_url:
            parent_url_id = UrlOfVisit(connection).get_url_id_by_url(url['parent'])
            UrlOfVisit(connection).add_url(url['cur_url'], parent_url_id)

        url_id = UrlOfVisit(connection).get_url_id_by_url(parsed_url[-1]['cur_url'])
        IpToUrl(connection).add_ip_to_url(ip_id, url_id, row['date'], row['time'])

    database.close_connection()