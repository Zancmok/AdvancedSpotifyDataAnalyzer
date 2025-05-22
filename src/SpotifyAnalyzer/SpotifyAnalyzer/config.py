import os
import dotenv

dotenv.load_dotenv()

DEBUG: bool = True
PORT: int = 5000
HOST: str = "0.0.0.0"
STATIC_PATH: str = "/app/src/static"
TEMPLATES_PATH: str = "/app/src/templates"
SQL_PATH: str = "/app/src/sql"
FLASK_SECRET_KEY: str = "mikudayo"
DEFAULT_ICON_PATH: str = "/app/src/static/img/spotify.png"
UPLOAD_FOLDER: str = '/app/uploads'
SPOTIFY_CLIENT_ID: str = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
