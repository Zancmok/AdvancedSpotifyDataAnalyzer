import os
from typing import Any
import SpotifyInterface.config as config
from functools import lru_cache
from mysql.connector import connect
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract, MySQLCursorAbstract
from mysql.connector.errors import DatabaseError
from time import sleep


class DatabaseManager:
    @staticmethod
    @lru_cache(maxsize=None)
    def _load_query(script: str) -> str:
        path: str = os.path.join(config.SQL_PATH, script)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Script: {path} does not exist.")

        with open(path) as file:
            contents: str = file.read()

        return contents

    @staticmethod
    def _get_connection() -> PooledMySQLConnection | MySQLConnectionAbstract:
        while True:
            try:
                return connect(
                    host=config.DB_HOST,
                    port=config.DB_PORT,
                    user=config.DB_USER,
                    password=config.DB_PASSWORD,
                    database=config.DB_NAME
                )
            except DatabaseError:
                sleep(.1)

    @staticmethod
    def run_query(script: str, **kwargs) -> Any:
        sql_query: str = DatabaseManager._load_query(script)

        connection: PooledMySQLConnection | MySQLConnectionAbstract = DatabaseManager._get_connection()

        cursor: MySQLCursorAbstract = connection.cursor(dictionary=True, buffered=True)

        cursor.execute(sql_query, kwargs)

        connection.commit()

        data: Any = cursor.fetchall()

        cursor.close()
        connection.close()

        return data

    @staticmethod
    def execute_script(script: str, **kwargs) -> None:
        sql_query: str = DatabaseManager._load_query(script)

        connection: PooledMySQLConnection | MySQLConnectionAbstract = DatabaseManager._get_connection()

        cursor: MySQLCursorAbstract = connection.cursor(dictionary=True, buffered=True)

        statements: list[str] = [stmt.strip() for stmt in sql_query.split(';') if stmt.strip()]

        for statement in statements:
            cursor.execute(statement, kwargs if '%(' in statement else ())

        connection.commit()
        cursor.close()
        connection.close()
