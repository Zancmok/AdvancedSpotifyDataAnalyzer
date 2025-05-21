import os.path
import bcrypt
import zipfile
from flask import Flask, render_template, session, redirect, Response, request, url_for
from werkzeug.datastructures.file_storage import FileStorage
from werkzeug.datastructures import ImmutableDict
from typing import Any
from SpotifyAnalyzer import SpotifyAnalyzer as config
from SpotifyAnalyzer.SpotifyAnalyzer.DatabaseManager import DatabaseManager
import SpotifyAnalyzer.SpotifyAnalyzer.celery_tasks as celery_tasks
import filetype


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

        return render_template("../templates/index.html")

    @staticmethod
    @app.route("/login", methods=["GET", "POST"])
    def login() -> str | Response | dict[str, Any]:
        if session.get("user"):
            return redirect("/")

        if request.method == "GET":
            return render_template("../templates/loginAndSignup.html")

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
            return render_template("../templates/settings.html", picture_path=url_for("avatar", user_id=session["user"]))

        files: ImmutableDict = request.files
        data: dict[Any, str] = request.form

        old_password: str = data.get("old_password")
        new_username: str = data.get("new_username")
        username_changed: bool = data.get("username_changed") == "true"
        new_password: str = data.get("new_password")
        password_changed: bool = data.get("password_changed") == "true"
        pfp_changed: bool = data.get("pfp_changed") == "true"
        pfp: FileStorage = files.get("pfp")

        database_user: list[tuple[int | str, ...]] = DatabaseManager.run_query("get_user_by_id.sql",
                                                                               id=session.get("user"))

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
            DatabaseManager.run_query("change_pfp.sql", profile_picture=pfp.stream.read(), id=session.get("user"))

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

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "users": DatabaseManager.run_query("get_user_listen_times.sql", start_date=in_data["start_date"],
                                               end_date=in_data["end_date"]),
            "genres": DatabaseManager.run_query("get_genre_listen_times.sql", start_date=in_data["start_date"],
                                                end_date=in_data["end_date"]),
            "tracks": DatabaseManager.run_query("get_track_listen_times.sql", start_date=in_data["start_date"],
                                                end_date=in_data["end_date"]),
            "authors": DatabaseManager.run_query("get_author_listen_times.sql", start_date=in_data["start_date"],
                                                 end_date=in_data["end_date"]),
            "albums": DatabaseManager.run_query("get_album_listen_times.sql", start_date=in_data["start_date"],
                                                end_date=in_data["end_date"])
        }

        return out_data

    @staticmethod
    @app.route("/avatar/<int:user_id>")
    def avatar(user_id: int) -> str | Response:
        query_result: list = DatabaseManager.run_query("get_user_pfp.sql", id=user_id)

        if not query_result:
            return ""

        profile_picture: bytes = query_result[0][0]
        mime_type: str = filetype.guess(profile_picture).MIME

        if not mime_type:
            return ""

        return Response(profile_picture, mimetype=mime_type)

    @staticmethod
    @app.route("/user/<int:user_id>")
    def user(user_id: int) -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("../templates/user.html", user_id=user_id)

    @staticmethod
    @app.route("/song/<int:song_id>")
    def song(song_id: int) -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("../templates/trackPage.html", song_id=song_id)

    @staticmethod
    @app.route("/genre/<int:genre_id>")
    def genre(genre_id: int) -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("../templates/genre.html", genre_id=genre_id)

    @staticmethod
    @app.route("/author/<int:author_id>")
    def author(author_id: int) -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("../templates/creator.html", author_id=author_id)

    @staticmethod
    @app.route("/album/<int:album_id>")
    def album(album_id: int) -> str | Response:
        if not session.get("user"):
            return redirect("/login")

        return render_template("../templates/album.html", album_id=album_id)

    @staticmethod
    @app.route("/get-user-data", methods=["POST"])
    def get_user_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data or "user_id" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "main": DatabaseManager.run_query("user_page/main.sql", user_id=in_data["user_id"]),
            "genres": DatabaseManager.run_query("user_page/get_genre_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], user_id=in_data["user_id"]),
            "tracks": DatabaseManager.run_query("user_page/get_track_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], user_id=in_data["user_id"]),
            "authors": DatabaseManager.run_query("user_page/get_author_listen_times.sql",
                                                 start_date=in_data["start_date"],
                                                 end_date=in_data["end_date"], user_id=in_data["user_id"]),
            "albums": DatabaseManager.run_query("user_page/get_album_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], user_id=in_data["user_id"])
        }

        return out_data

    @staticmethod
    @app.route("/get-genre-data", methods=["POST"])
    def get_genre_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data or "genre_id" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "main": DatabaseManager.run_query("genre_page/main.sql", genre_id=in_data["genre_id"]),
            "users": DatabaseManager.run_query("genre_page/get_user_listen_times.sql", start_date=in_data["start_date"],
                                               end_date=in_data["end_date"], genre_id=in_data["genre_id"]),
            "tracks": DatabaseManager.run_query("genre_page/get_track_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], genre_id=in_data["genre_id"]),
            "authors": DatabaseManager.run_query("genre_page/get_author_listen_times.sql",
                                                 start_date=in_data["start_date"],
                                                 end_date=in_data["end_date"], genre_id=in_data["genre_id"]),
            "albums": DatabaseManager.run_query("genre_page/get_album_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], genre_id=in_data["genre_id"])
        }

        return out_data

    @staticmethod
    @app.route("/get-song-data", methods=["POST"])
    def get_song_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data or "song_id" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "main": DatabaseManager.run_query("song_page/main.sql", song_id=in_data["song_id"]),
            "users": DatabaseManager.run_query("song_page/get_user_listen_times.sql", start_date=in_data["start_date"],
                                               end_date=in_data["end_date"], song_id=in_data["song_id"])
        }

        return out_data


    @staticmethod
    @app.route("/get-author-data", methods=["POST"])
    def get_author_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data or "author_id" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "main": DatabaseManager.run_query("author_page/main.sql", author_id=in_data["author_id"]),
            "users": DatabaseManager.run_query("author_page/get_user_listen_times.sql", start_date=in_data["start_date"],
                                               end_date=in_data["end_date"], author_id=in_data["author_id"]),
            "tracks": DatabaseManager.run_query("author_page/get_track_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], author_id=in_data["author_id"]),
            "albums": DatabaseManager.run_query("author_page/get_album_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], author_id=in_data["author_id"])
        }

        return out_data

    @staticmethod
    @app.route("/get-album-data", methods=["POST"])
    def get_album_data() -> Response | dict[str, Any]:
        if not session.get("user"):
            return redirect("/login")

        in_data: dict[Any, str] = request.get_json()

        if "start_date" not in in_data or "end_date" not in in_data or "album_id" not in in_data:
            return {}

        out_data: dict[str, Any] = {
            "main": DatabaseManager.run_query("album_page/main.sql", album_id=in_data["album_id"]),
            "users": DatabaseManager.run_query("album_page/get_user_listen_times.sql", start_date=in_data["start_date"],
                                               end_date=in_data["end_date"], album_id=in_data["album_id"]),
            "tracks": DatabaseManager.run_query("album_page/get_track_listen_times.sql",
                                                start_date=in_data["start_date"],
                                                end_date=in_data["end_date"], album_id=in_data["album_id"])
        }

        return out_data
