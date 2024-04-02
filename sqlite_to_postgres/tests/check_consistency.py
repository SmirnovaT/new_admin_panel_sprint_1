import logging
from dataclasses import astuple
from pathlib import Path
from sqlite_to_postgres.sqlite_service import SQLiteService
from sqlite_to_postgres.models import (
    Genre,
    FilmWork,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)
from sqlite_to_postgres.postgres_service import PostgresService
import os
from dotenv import load_dotenv

load_dotenv()

db_path = os.environ.get("DB_PATH")
dsn = os.environ.get("DB_DSN")

base_path = Path(__file__).resolve().parent.parent
path = base_path / db_path


def compare_data(sqlite_conn, pg_conn):
    """Метод сравнения данных из SQLite и  Postgres."""
    mapping_table = {
        "genre": Genre,
        "film_work": FilmWork,
        "person": Person,
        "person_film_work": PersonFilmWork,
        "genre_film_work": GenreFilmWork,
    }
    for table, model in mapping_table.items():
        count_rows_sqlite = sqlite_service.get_count_data(sqlite_conn, table)
        count_rows_postgres = postgres_service.get_count_data(pg_conn, table)
        try:
            assert count_rows_sqlite == count_rows_postgres
        except AssertionError:
            logging.error(f"Количество строк не совпадает в таблице {table}")

        part_data_sqlite = get_all_from_table_sqlite(sqlite_conn, table, model)

        part_data_postgres = get_data_postgres(pg_conn, table, model)

        try:
            for batch_sqlite, batch_postgres in zip(
                part_data_sqlite, part_data_postgres
            ):
                assert batch_sqlite == batch_postgres
        except AssertionError:
            logging.error(f"Данные не совпадают в таблице {table}")
    print("Все данные сопоставлены, различий нет")


def get_all_from_table_sqlite(sqlite_conn, table, model):
    """Получение данных из SQLite."""
    sqlite_data_generator = sqlite_service.get_data_from_table(sqlite_conn, table)
    for rows in sqlite_data_generator:
        data_from_db = [model(**row).cut_date() for row in rows]
        yield reformat_data(data_from_db)


def get_data_postgres(pg_conn, table, model):
    """Получение данных из Postgres."""
    postgres_data_generator = postgres_service.get_data_from_postgres(pg_conn, table)
    for rows in postgres_data_generator:
        data_from_db = [model(**row).post_init() for row in rows]
        yield reformat_data(data_from_db)


def reformat_data(data_from_db):
    sorted_data = sorted([astuple(item) for item in data_from_db])
    return sorted_data


if __name__ == "__main__":
    sqlite_service = SQLiteService()
    postgres_service = PostgresService()
    with sqlite_service.conn_context(
        path
    ) as sqlite_conn, postgres_service.conn_context(dsn) as pg_conn:
        compare_data(sqlite_conn, pg_conn)
