import os.path
from typing import Any
from .DatabaseManager import DatabaseManager
from os import listdir
import SpotifyInterface.config as config
from time import sleep
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from zipfile import ZipFile, ZipInfo
import json


class SpotifyInterface:
    spotify: Spotify = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET
    ))

    _fields_required: list[str] = ["spotify_track_uri", "ms_played", "conn_country", "ip_addr",
                                   "incognito_mode", "offline", "skipped", "shuffle", "reason_end",
                                   "reason_start"]
    @staticmethod
    def _listen_valid(listen: dict[str, Any]) -> bool:
        for field in SpotifyInterface._fields_required:
            if field not in listen:

                return False

        return True

    @staticmethod
    def _analyze_json(zip_file: ZipFile, file: ZipInfo) -> None:
        contents: Any = json.loads(zip_file.read(file))

        if type(contents) is not list:
            return
        contents: list

        for json_element in contents:
            if type(json_element) is not dict:
                continue
            json_element: dict[str, Any]

            if not SpotifyInterface._listen_valid(json_element):
                continue

            # Hia

    @staticmethod
    def _process_zip_file(user_id: int) -> None:
        path: str = os.path.join(config.UPLOAD_FOLDER, f"{user_id}.zip")

        with ZipFile(path, 'r') as zip_file:
            for file in zip_file.filelist:
                if not file.filename.endswith('.json'):
                    continue

                SpotifyInterface._analyze_json(zip_file, file)

        os.remove(path)

    @staticmethod
    def run() -> None:
        print("Spotify Interface started!", flush=True)

        zip_file_paths: list[str]
        while True:
            zip_file_paths = listdir(config.UPLOAD_FOLDER)

            if zip_file_paths:
                user_id: int = int(zip_file_paths[0][:-4])

                print(f"Started processing data of user with id of '{user_id}'!", flush=True)

                DatabaseManager.run_query("general/reset-user-data.sql", user_id=user_id)
                DatabaseManager.run_query("general/reset-user-queue.sql", user_id=user_id)

                SpotifyInterface._process_zip_file(user_id)

                print(f"Data of user with id of '{user_id}' processed successfully!", flush=True)

                continue

            print(DatabaseManager.run_query("general/get-first-queue-element.sql"), flush=True)

            sleep(config.INACTIVE_INTERVAL)
