from dataclasses import astuple, fields

from sqlite_to_postgres.sqlite_service import SQLiteService
from sqlite_to_postgres.postgres_service import PostgresService
import settings

import logging

logging.basicConfig(level=logging.INFO)


def load_from_sqlite(sqlite_conn, pg_conn):
    """Основной метод загрузки данных из SQLite в Postgres"""

    mapping_table = settings.mapping_table
    for table, model in mapping_table.items():
        try:
            data_generator = sqlite_service.get_data_from_table(sqlite_conn, table)
            for rows in data_generator:
                data_to_insert, column_names_str = reformat_data(model, rows)
                postgres_service.data_to_postgres(
                    pg_conn, table, column_names_str, data_to_insert
                )
            logging.info(f"Данные из таблицы {table} успешно загружены")
        except Exception as e:
            logging.error(e)


def reformat_data(model, data):
    data_from_db = [(model(**row)) for row in data]
    data_to_insert = [astuple(item) for item in data_from_db]
    column_names = [field.name for field in fields(data_from_db[0])]
    column_names_str = ", ".join(column_names)
    return data_to_insert, column_names_str


if __name__ == "__main__":
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.conn_context(
        settings.SQLITE_DB_PATH
    ) as sqlite_conn, postgres_service.conn_context(
        settings.POSTGRES_DB_DSN
    ) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
