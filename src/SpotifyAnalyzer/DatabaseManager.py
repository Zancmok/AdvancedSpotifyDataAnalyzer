import os
from typing import Any
import SpotifyAnalyzer.config as config
import sqlite3
from sqlite3 import Cursor
from functools import lru_cache


class DatabaseManager:
    @staticmethod
    @lru_cache(maxsize=None)
    def _load_query(script: str) -> str:
        path: str = os.path.join(config.SQL_PATH, script)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Script: {script} does not exist.")

        with open(path) as file:
            contents: str = file.read()

        return contents

    @staticmethod
    def run_query(script: str, **kwargs) -> Any:
        sql_query: str = DatabaseManager._load_query(script)

        with sqlite3.connect(config.DATABASE_PATH) as connector:
            cursor: Cursor = connector.cursor()

            cursor.execute(sql_query, kwargs)

            return cursor.fetchall()

    @staticmethod
    def execute_script(script: str) -> None:
        sql_query: str = DatabaseManager._load_query(script)

        with sqlite3.connect(config.DATABASE_PATH) as connector:
            cursor: sqlite3.Cursor = connector.cursor()

            cursor.executescript(sql_query)

            connector.commit()
