import sqlite3
from contextlib import contextmanager
import os
from dotenv import load_dotenv
import logging

load_dotenv()

db_path = os.environ.get("DB_PATH")


class SQLiteExtractor:
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
        try:
            curs.execute(f"SELECT * FROM {table_name}")
            data = curs.fetchall()
            return data
        except sqlite3.Error as e:
            logging.error(f"Не удалось забрать данные из таблицы {table_name}: {e}")
