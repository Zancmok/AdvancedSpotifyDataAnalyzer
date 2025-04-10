"""
# TODO: Write Docstring!
"""

from flask import Flask, render_template
import SpotifyAnalyzer.config as config
from SpotifyAnalyzer.DatabaseManager import DatabaseManager


class SpotifyAnalyzer:
    """
    # TODO: Write Docstring!
    """

    app: Flask = Flask(
        __name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    @staticmethod
    def run() -> None:
        """
        # Runs the main application.
        """
        
        SpotifyAnalyzer.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        DatabaseManager.fget("make_bobr_db.sql")

        DatabaseManager.fget("get_specific_bobr.sql", bobr_id=2)

        """SpotifyAnalyzer.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )"""

    @staticmethod
    @app.route("/")
    def index() -> str:
        """
        # TODO: Write Docstring!
        """

        return render_template("index.html")
