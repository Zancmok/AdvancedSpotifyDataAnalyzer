"""
# TODO: Write Docstring!
"""

import os
from typing import Any, Optional
import SpotifyAnalyzer.config as config
import sqlite3
from sqlite3 import Cursor, Connection


class DatabaseManager:
    """
    # TODO: Write Docstring!
    """

    _connection: Connection = sqlite3.connect(config.DATABASE_PATH)
    _cursor: Cursor = _connection.cursor()

    @staticmethod
    def fget(script: str, **kwargs) -> Any:
        """
        # TODO: Write Docstring!
        """

        path: str = os.path.join(config.SQL_PATH, script)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Script: {script} does not exist.")

        file_contents: str
        with open(path) as file:
            file_contents = file.read()
        
        file_contents = file_contents.format(**kwargs)

        DatabaseManager._cursor.execute(file_contents)

        return DatabaseManager._cursor.fetchall()

    @staticmethod
    def frun(script: str, **kwargs) -> None:
        """
        # TODO: Write Docstring!
        """

        path: str = os.path.join(config.SQL_PATH, script)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Script: {script} does not exist.")

        file_contents: str
        with open(path) as file:
            file_contents = file.read()
        
        file_contents = file_contents.format(**kwargs)

        DatabaseManager._cursor.executescript(file_contents)

        DatabaseManager._connection.commit()
