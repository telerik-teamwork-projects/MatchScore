from mariadb import connect
from mariadb.connections import Connection
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> Connection:
    return connect(
        user=os.environ['db_user'],
        password=os.environ['db_password'],
        host=os.environ['db_host'],
        port=int(os.environ['db_port']),
        database=os.environ['db_name'],
        # ssl=os.environ['db_ssl']
    )


def read_query(sql: str, sql_params=()):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)

        return list(cursor)


def insert_query(sql: str, sql_params=()) -> int:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.lastrowid


def update_query(sql: str, sql_params=()) -> bool:
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(sql, sql_params)
        conn.commit()

        return cursor.rowcount