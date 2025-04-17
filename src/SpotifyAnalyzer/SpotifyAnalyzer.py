"""
# TODO: Write Docstring!
"""

from flask import Flask, render_template, session, redirect, Response, request
from typing import Any, Callable
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
    def required_login(function: Callable) -> Callable:
        """
        # TODO: Write Docstring!
        """

        def inner(*args, **kwargs) -> Any:
            """
            # TODO: Write Docstring!
            """
            
            if not session.get("key"):
                return redirect("/login")
            
            function(*args, **kwargs)

        return inner

    @staticmethod
    def run() -> None:
        """
        # Runs the main application.
        """
        
        SpotifyAnalyzer.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        # DatabaseManager.frun("create_db.sql")

        SpotifyAnalyzer.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG
        )

    @staticmethod
    @app.route("/")
    @required_login
    def index() -> str | Response:
        """
        # TODO: Write Docstring!
        """

        return render_template("index.html")

    @staticmethod
    @app.route("/login", methods=["GET", "POST"])
    def login() -> str | Response:
        """
        # TODO: Write Docstring!
        """

        if session.get("key"):
            return redirect("/")

        if request.method == "GET":
            return render_template("loginAndSignup.html")
