import sqlite3
from contextlib import contextmanager
import logging

from sqlite_to_postgres import settings


class SQLiteService:
    """Установка и закрытие соединения с SQLite. Импорт данных."""

    @contextmanager
    def conn_context(self, db_path: str):
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logging.error(f"Не удалось подключиться к базe: {e}")
        finally:
            conn.close()

    @staticmethod
    def get_data_from_table(conn, table_name: str):
        curs = conn.cursor()
        curs.execute(f"SELECT * FROM {table_name}")
        while rows := curs.fetchmany(settings.BUTCH_SIZE):
            yield rows

    @staticmethod
    def get_count_data(conn, table_name):
        """Получение количества строк из таблицы Sqlite."""
        curs = conn.cursor()
        try:
            curs.execute(f"SELECT count(*) FROM {table_name}")
            row = curs.fetchone()
            return row[0]
        except sqlite3.Error as e:
            logging.error(
                f"Не удалось получить количество строк из таблицы {table_name}: {e}"
            )
