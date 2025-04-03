"""
# TODO: Write Docstring!
"""

import SpotifyAnalyzer.config as config
import sqlite3


class DatabaseManager:
    """
    # TODO: Write Docstring!
    """

    _connection = sqlite3.connect(config.DATABASE_PATH)
    _cursor = _connection.cursor()
