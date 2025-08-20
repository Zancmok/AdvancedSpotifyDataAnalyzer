import os
import dotenv

dotenv.load_dotenv()

INACTIVE_INTERVAL: int = 5
ERROR_SLEEP_INTERVAL: int = 1
UPLOAD_FOLDER: str = '/app/uploads'
DB_HOST: str = "mysql"
DB_PORT: str = "3306"
DB_USER: str = "spotify"
DB_PASSWORD: str = "spotifypass"
DB_NAME: str = "spotifydb"
SQL_PATH: str = "/app/sql"
SPOTIFY_CLIENT_ID: str = os.getenv("CLIENT_ID")
SPOTIFY_CLIENT_SECRET: str = os.getenv("CLIENT_SECRET")
