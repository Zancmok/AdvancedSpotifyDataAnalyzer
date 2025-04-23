"""
# TODO: Write Docstring!
"""

import bcrypt
import os
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
            
            return function(*args, **kwargs)

        return inner

    @staticmethod
    def run() -> None:
        """
        # Runs the main application.
        """

        SpotifyAnalyzer.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        DatabaseManager.execute_script("create_db.sql")

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
    def login() -> str | Response | dict[str, Any]:
        """
        # TODO: Write Docstring!
        """

        if session.get("key"):
            return redirect("/")

        if request.method == "GET":
            return render_template("loginAndSignup.html")

        data: dict[str, Any] = request.get_json()
        
        if not data or not data.get('type'):
            return {'success': False, 'reason': "Nigga tf you doin"}

        password: str = data.get('password')
        username: str = data.get('name')

        if not password:
            return {'success': False, 'reason': "Men, why no password ):"}

        if not username:
            return {'success': False, 'reason': "You nameless or something?"}

        if data.get('type') == 'SIGNUP':
            if DatabaseManager.run_query("get_user.sql", username=username):
                return {'success': False, 'reason': "User already exists."}  # TODO: Test is this special sauce actually works

            password_bytes: bytes = password.encode('utf-8') 

            salt: bytes = bcrypt.gensalt()

            password_hash: bytes = bcrypt.hashpw(password_bytes, salt)

            decoded_hash: str = password_hash.decode('utf-8')

            DatabaseManager.run_query("add_user.sql", username=username, password=decoded_hash)

            return {'success': True, 'reason': ""}
        else:
            return {'success': False, 'reason': "Code not implemented yet."}
