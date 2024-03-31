from dataclasses import astuple, fields

from sqlite_to_postgres.from_sqlite import SQLiteExtractor
from sqlite_to_postgres.models import (
    FilmWork,
    Genre,
    GenreFilmWork,
    PersonFilmWork,
    Person,
)
from sqlite_to_postgres.to_postgres import PostgresSaver

import logging
import os
from dotenv import load_dotenv

load_dotenv()
db_path = os.environ.get("DB_PATH")
dsn = os.environ.get("DB_DSN")


def load_from_sqlite(sqlite_conn, pg_conn):
    """Основной метод загрузки данных из SQLite в Postgres"""

    mapping_table = {
        "genre": Genre,
        "film_work": FilmWork,
        "person": Person,
        "person_film_work": PersonFilmWork,
        "genre_film_work": GenreFilmWork,
    }

    for table, model in mapping_table.items():
        try:
            data = sqlite_extractor.get_data_from_table(sqlite_conn, table)
            data_to_insert, column_names_str = reformat_data(model, data)
            postgres_saver.data_to_postgres(
                pg_conn, table, column_names_str, data_to_insert
            )
            print(f"Данные из таблицы {table} успешно загружены")
        except Exception as e:
            logging.error(e)


def reformat_data(model, data):
    data_from_db = [(model(**row)) for row in data]
    data_to_insert = [astuple(item) for item in data_from_db]
    column_names = [field.name for field in fields(data_from_db[0])]
    column_names_str = ", ".join(column_names)
    return data_to_insert, column_names_str


if __name__ == "__main__":
    sqlite_extractor = SQLiteExtractor()
    postgres_saver = PostgresSaver()
    with sqlite_extractor.conn_context(
        db_path
    ) as sqlite_conn, postgres_saver.conn_context(dsn) as pg_conn:
        load_from_sqlite(sqlite_conn, pg_conn)
