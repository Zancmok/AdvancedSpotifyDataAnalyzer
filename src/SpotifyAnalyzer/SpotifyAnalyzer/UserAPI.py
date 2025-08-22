from flask import Blueprint, Response
import SpotifyAnalyzer.config as config

user_data_bp: Blueprint = Blueprint(
    "user-data",
    __name__,
    url_prefix="/user-data/",
    static_folder=config.STATIC_PATH,
    template_folder=config.TEMPLATES_PATH
)


class UserAPI:
    @staticmethod
    @user_data_bp.route("/top-creators/<int:user_id>/<int:page>")
    def top_creators(user_id: int, page: int) -> str | Response:
        return "Hello, World!"

    @staticmethod
    @user_data_bp.route("/top-tracks/<int:user_id>/<int:page>")
    def top_tracks(user_id: int, page: int) -> str | Response:
        return "Hello, World!"

    @staticmethod
    @user_data_bp.route("/top-albums/<int:user_id>/<int:page>")
    def top_albums(user_id: int, page: int) -> str | Response:
        return "Hello, World!"

    @staticmethod
    @user_data_bp.route("/top-genres/<int:user_id>/<int:page>")
    def top_genres(user_id: int, page: int) -> str | Response:
        return "Hello, World!"
