import os
from typing import Any
import SpotifyAnalyzer.config as config
from functools import lru_cache
from mysql.connector import connect
from mysql.connector.pooling import PooledMySQLConnection
from mysql.connector.abstracts import MySQLConnectionAbstract


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
        return connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME
        )

    @staticmethod
    def run_query(script: str, **kwargs) -> Any:
        sql_query: str = DatabaseManager._load_query(script)

        print(DatabaseManager._get_connection(), flush=True)

        return None

    @staticmethod
    def execute_script(script: str) -> None:
        sql_query: str = DatabaseManager._load_query(script)

        print("test", flush=True)

        print(DatabaseManager._get_connection(), flush=True)
