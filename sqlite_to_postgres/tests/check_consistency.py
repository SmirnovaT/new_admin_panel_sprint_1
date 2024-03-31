from dataclasses import astuple
from pathlib import Path
from psycopg2 import sql
import psycopg2

import psycopg2.extras
import logging
from sqlite_to_postgres.from_sqlite import SQLiteExtractor
from sqlite_to_postgres.models import (
    Genre,
    FilmWork,
    Person,
    GenreFilmWork,
    PersonFilmWork,
)
from sqlite_to_postgres.to_postgres import PostgresSaver
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
        len_data_sqlite, sorted_data_sqlite = get_all_from_table_sqlite(
            sqlite_conn, table, model
        )

        len_data_pg, sorted_data_pg = get_all_from_postgres(pg_conn, table, model)

        try:
            assert len_data_sqlite == len_data_pg
        except AssertionError:
            logging.error(f"Длина таблиц {table} не совпадает")
        try:
            assert sorted_data_sqlite == sorted_data_pg
        except AssertionError:
            logging.error(f"Данные не совпадают в таблице {table}")

    print("Все данные сопоставлены, различий нет")


def get_all_from_table_sqlite(sqlite_conn, table, model):
    """Получение данных из SQLite."""
    sqlite_data = sqlite_extractor.get_data_from_table(sqlite_conn, table)
    data_from_db = [model(**row).cut_date() for row in sqlite_data]
    return reformat_data(data_from_db)


def get_all_from_postgres(pg_conn, table, model):
    """Получение данных из Postgres."""
    try:
        cur = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(sql.SQL("SELECT * FROM content.{}").format(sql.Identifier(table)))
        pg_data = cur.fetchall()
        data_from_db = [(model(**row)).post_init() for row in pg_data]
        return reformat_data(data_from_db)
    except (Exception, psycopg2.DatabaseError) as e:
        logging.error(e)


def reformat_data(data_from_db):
    sorted_data = sorted([astuple(item) for item in data_from_db])
    len_data = len(sorted_data)
    return len_data, sorted_data


if __name__ == "__main__":
    sqlite_extractor = SQLiteExtractor()
    postgres_saver = PostgresSaver()
    with sqlite_extractor.conn_context(
        path
    ) as sqlite_conn, postgres_saver.conn_context(dsn) as pg_conn:
        compare_data(sqlite_conn, pg_conn)
