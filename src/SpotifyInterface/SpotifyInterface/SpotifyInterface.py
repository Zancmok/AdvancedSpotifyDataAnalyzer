import os.path

from .DatabaseManager import DatabaseManager
from os import listdir
import SpotifyInterface.config as config
from time import sleep
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from zipfile import ZipFile, ZipInfo


class SpotifyInterface:
    spotify: Spotify = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET
    ))

    @staticmethod
    def _process_zip_file(user_id: int) -> None:
        path: str = os.path.join(config.UPLOAD_FOLDER, str(user_id), ".zip")

        with ZipFile(path, 'r') as zip_file:
            for file in zip_file.filelist:
                if not file.filename.endswith('.json'):
                    continue

                # _analyze_json(zip_file, file)

        os.remove(path)

    @staticmethod
    def run() -> None:
        zip_file_paths: list[str]
        while True:
            zip_file_paths = listdir(config.UPLOAD_FOLDER)

            if zip_file_paths:
                user_id: int = int(zip_file_paths[0][:-4])

                DatabaseManager.run_query("general/reset-user-data.sql", user_id=user_id)
                DatabaseManager.run_query("general/reset-user-queue.sql", user_id=user_id)

                SpotifyInterface._process_zip_file(user_id)

                continue

            print(DatabaseManager.run_query("general/get-first-queue-element.sql"))

            sleep(config.INACTIVE_INTERVAL)
