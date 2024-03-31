import logging
from contextlib import contextmanager
from more_itertools import chunked
import psycopg2
import os
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()
dsn = os.environ.get("DB_DSN")


class PostgresSaver:
    """Установка и закрытие соединения с Postgres. Вставка данных."""

    @contextmanager
    def conn_context(self, dsn: str):
        try:
            conn = psycopg2.connect(dsn)
            yield conn
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(f"Не удалось подключиться к базe: {e}")
        finally:
            conn.close()

    @staticmethod
    def data_to_postgres(pg_conn, table_name: str, column_names_str, data):
        cursor = pg_conn.cursor()
        try:
            for chunk in chunked(data, 100):
                query = f"INSERT INTO content.{table_name} ({column_names_str}) VALUES %s ON CONFLICT (id) DO NOTHING"
                psycopg2.extras.execute_values(cursor, query, chunk)
                pg_conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(f"Не удалось загрудить данные в таблицу {table_name}: {e}")
