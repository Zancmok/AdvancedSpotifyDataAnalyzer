import base64
import os.path
import bcrypt
import zipfile
from flask import Flask, render_template, session, redirect, Response, request, url_for
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures import ImmutableDict
from typing import Any, Optional
import SpotifyAnalyzer.config as config
from SpotifyAnalyzer.DatabaseManager import DatabaseManager
import filetype


class SpotifyAnalyzer:
    app: Flask = Flask(
        __name__,
        template_folder=config.TEMPLATES_PATH,
        static_folder=config.STATIC_PATH
    )

    @staticmethod
    def run() -> None:
        SpotifyAnalyzer.app.config["SECRET_KEY"] = config.FLASK_SECRET_KEY

        print(DatabaseManager.run_query("general/miku-dayo.sql"), flush=True)

        DatabaseManager.execute_script("general/create-db.sql")

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
            if DatabaseManager.run_query("user-management/get-user.sql", username=username):
                return {'success': False, 'reason': "User already exists."}

            password_bytes: bytes = password.encode('utf-8')

            salt: bytes = bcrypt.gensalt()

            password_hash: bytes = bcrypt.hashpw(password_bytes, salt)

            decoded_hash: str = password_hash.decode('utf-8')

            DatabaseManager.run_query("user-management/add-user.sql", username=username, password_hash=decoded_hash)

            return {'success': True, 'reason': ""}
        else:
            database_user: list[dict[str, Any]] = DatabaseManager.run_query("user-management/get-user.sql", username=username)

            if not database_user:
                return {'success': False, 'reason': "User does not exist."}

            encoded_user_hash: bytes = database_user[0]["password_hash"].encode('utf-8')

            password_bytes: bytes = password.encode('utf-8')

            if bcrypt.checkpw(password_bytes, encoded_user_hash):
                session["user"] = database_user[0]["id"]

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

        data: Optional[dict[str, str]] = request.get_json()

        if not data:
            return {'success': False, 'reason': "Ehh?"}

        data: dict[str, str]

        if not data.get('type'):
            return {'success': False, 'reason': "No type, bahhhh."}

        if not data.get('password'):
            return {'success': False, 'reason': "If no password than no miku for ya."}

        database_user: list[dict[str, Any]] = DatabaseManager.run_query(
            "user-management/get-user.sql",
            username=DatabaseManager.run_query(
                "user-management/get-user-name.sql",
                id=session["user"])[0]["username"]
        )

        encoded_user_hash: bytes = database_user[0]["password_hash"].encode('utf-8')

        password_bytes: bytes = data.get("password").encode('utf-8')

        if not bcrypt.checkpw(password_bytes, encoded_user_hash):
            return {'success': False, 'reason': "Password not correct."}

        data_type: str = data.get('type')

        match data_type:
            case 'name':
                if not data.get("name"):
                    return {'success': False, 'reason': "Why update name when no name?"}

                DatabaseManager.run_query(
                    "user-management/update-data/update-name.sql",
                    username=data.get("name"),
                    id=session["user"]
                )
            case 'password':
                if not data.get("new_password"):
                    return {'success': False, 'reason': "Why update password when no password?"}

                DatabaseManager.run_query(
                    "user-management/update-data/update-password.sql",
                    password=data.get("new_password"),
                    id=session["user"]
                )
            case 'pfp':
                pfp_data: Optional[str] = data.get("pfp")

                if not pfp_data:
                    return {'success': False, 'reason': "Why update password when no pfp?"}
                pfp_data: str

                if not pfp_data.startswith("data:image/"):
                    return {'success': False, 'reason': "That's not an image..."}

                try:
                    # Split off the base64 header and decode
                    header: str
                    encoded: str
                    header, encoded = pfp_data.split(",", 1)

                    pfp_blob: bytes = base64.b64decode(encoded)
                except Exception as e:
                    return {'success': False, 'reason': "Couldn't decode image data."}

                DatabaseManager.run_query(
                    "user-management/update-data/update-pfp.sql",
                    pfp=pfp_blob,
                    id=session["user"]
                )
            case _:
                return {'success': False, 'reason': "Something aint right here..."}

        return {'success': True, 'reason': ""}

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

        except Exception as e:
            print(e, flush=True)

        return {'success': True, 'reason': ""}

    @staticmethod
    @app.route("/avatar/<int:user_id>")
    def avatar(user_id: int) -> str | Response:
        query_result: list[dict[str, bytes]] = DatabaseManager.run_query(
            "user-management/get-user-pfp.sql",
            id=user_id
        )

        if not query_result:
            return ""

        profile_picture: Optional[bytes] = query_result[0]["profile_picture"]

        if not profile_picture:
            return ""
        profile_picture: bytes

        mime_type: str = filetype.guess(profile_picture).MIME

        if not mime_type:
            return ""

        return Response(profile_picture, mimetype=mime_type)
