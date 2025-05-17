import os.path
import bcrypt
import zipfile
from flask import Flask, render_template, session, redirect, Response, request
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures import ImmutableDict
from typing import Any, Callable
import SpotifyAnalyzer.config as config
from SpotifyAnalyzer.DatabaseManager import DatabaseManager
import SpotifyAnalyzer.celery_tasks as celery_tasks


class SpotifyAnalyzer:
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

        DatabaseManager.execute_script("create_db.sql")

        DatabaseManager.execute_script("create_base_values.sql")

        print(DatabaseManager.run_query("miku_dayo.sql"), flush=True)

        celery_tasks.spotify_api_process.delay()

        SpotifyAnalyzer.app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )

    @staticmethod
    @app.route("/")
    def index() -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("index.html")

    @staticmethod
    @app.route("/login", methods=["GET", "POST"])
    def login() -> str | Response | dict[str, Any]:
        if session.get("user"):
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
                return {'success': False, 'reason': "User already exists."}

            password_bytes: bytes = password.encode('utf-8')

            salt: bytes = bcrypt.gensalt()

            password_hash: bytes = bcrypt.hashpw(password_bytes, salt)

            decoded_hash: str = password_hash.decode('utf-8')

            image: bytes
            with open(config.DEFAULT_ICON_PATH, 'rb') as file:
                image = file.read()

            DatabaseManager.run_query("add_user.sql", username=username, password=decoded_hash, profile_picture=image)

            return {'success': True, 'reason': ""}
        else:
            database_user: list[tuple[int | str, ...]] = DatabaseManager.run_query("get_user.sql", username=username)

            if not database_user:
                return {'success': False, 'reason': "User does not exist."}

            # [0] is the first and only field, [2] is the password in the said user field 
            encoded_user_hash: bytes = database_user[0][2].encode('utf-8')

            password_bytes: bytes = password.encode('utf-8')

            if bcrypt.checkpw(password_bytes, encoded_user_hash):
                # [0] is the first and only field, [0] is the user_id in the said user field
                session["user"] = database_user[0][0]

                return {'success': True, 'reason': ""}
            else:
                return {'success': False, 'reason': "Password not correct."}

    @staticmethod
    @app.route("/logout", methods=["POST"])
    def logout() -> Response | dict[str, Any]:
        session["user"] = None

        return {'success': True, 'reason': ""}

    @staticmethod
    @app.route("/settings", methods=["GET", "POST"])
    def settings() -> str | Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        if request.method == "GET":
            return render_template("settings.html")

        files: ImmutableDict = request.files
        data: dict[Any, str] = request.form

        old_password: str = data.get("old_password")
        new_username: str = data.get("new_username")
        username_changed: bool = bool(data.get("username_changed"))
        new_password: str = data.get("new_password")
        password_changed: bool = bool(data.get("password_changed"))
        pfp_changed: bool = bool(data.get("pfp_changed"))
        pfp: FileStorage = files.get("pfp")
 
        database_user: list[tuple[int | str, ...]] = DatabaseManager.run_query("get_user_by_id.sql", id=session.get("user"))

        encoded_user_hash: bytes = database_user[0][2].encode('utf-8')

        password_bytes: bytes = old_password.encode('utf-8')

        if not bcrypt.checkpw(password_bytes, encoded_user_hash):
            return {'success': False, 'reason': "Password not correct"}

        if username_changed and not DatabaseManager.run_query("user_already_exists.sql", username=new_username)[0][0]:
            DatabaseManager.run_query("change_username.sql", username=new_username, id=session.get("user"))

        if password_changed:
            password_bytes: bytes = new_password.encode('utf-8')

            salt: bytes = bcrypt.gensalt()

            password_hash: bytes = bcrypt.hashpw(password_bytes, salt)

            decoded_hash: str = password_hash.decode('utf-8')

            DatabaseManager.run_query("change_password.sql", password=decoded_hash, id=session.get("user"))

        if pfp_changed:
            DatabaseManager.run_query("change_pfp.sql", profile_picture=pfp)  # DO THIS AT HOUZM

        return {'success': False, 'reason': "Not implemented yet"}

    @staticmethod
    @app.route("/data-upload", methods=["POST"])
    def data_upload() -> Response | dict[str, Any]:
        if 'file' not in request.files:
            return {'success': False, 'reason': "No file part"}

        file: FileStorage = request.files['file']

        if not zipfile.is_zipfile(file.stream):
            return {'success': False, 'reason': "Not a zip file"}
        file.stream.seek(0)

        user_id: int = session.get("user")

        try:
            filename: str = f"{user_id}.zip"

            file_path: str = os.path.join(config.UPLOAD_FOLDER, filename)

            if os.path.exists(file_path):
                return {'success': False, 'reason': "Your file is already in processing!"}

            file.save(file_path)

            # celery_tasks.process.delay(file_path)

            celery_tasks.process(file_path)

        except Exception as e:
            print(e, flush=True)

        return {'success': True, 'reason': ""}

    @staticmethod
    @app.route("/get-main-page-data", methods=["POST"])
    def get_main_page_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")
        
        data: dict[Any, str] = request.get_json()

        if "start_date" not in data or "end_date" not in data:
            return {}

        return DatabaseManager.run_query("get_user_listen_times.sql", start_date=data["start_date"], end_date=data["end_date"])
