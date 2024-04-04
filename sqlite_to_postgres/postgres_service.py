import logging
from contextlib import contextmanager
import psycopg2
import psycopg2.extras
from psycopg2 import sql

from sqlite_to_postgres import settings


class PostgresService:
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
        query = f"INSERT INTO content.{table_name} ({column_names_str}) VALUES %s ON CONFLICT (id) DO NOTHING"
        psycopg2.extras.execute_values(cursor, query, data)
        pg_conn.commit()

    @staticmethod
    def get_data_from_postgres(pg_conn, table):
        """Получение данных из Postgres."""
        cur = pg_conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:
            cur.execute(
                sql.SQL("SELECT * FROM content.{}").format(sql.Identifier(table))
            )
            while rows := cur.fetchmany(settings.BUTCH_SIZE):
                yield rows
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(e)

    @staticmethod
    def get_count_data(pg_conn, table):
        """Получение количества строк из таблицы Postgres."""
        cur = pg_conn.cursor()
        try:
            cur.execute(
                sql.SQL("SELECT count(*) FROM content.{}").format(sql.Identifier(table))
            )
            row = cur.fetchone()
            return row[0]
        except (Exception, psycopg2.DatabaseError) as e:
            logging.error(e)
