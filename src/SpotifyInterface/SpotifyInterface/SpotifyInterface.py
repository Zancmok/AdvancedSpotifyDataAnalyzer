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
import datetime


class SpotifyInterface:
    spotify: Spotify = Spotify(auth_manager=SpotifyClientCredentials(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET
    ))

    _fields_required: list[str] = ["spotify_track_uri", "ts", "ms_played", "conn_country", "ip_addr",
                                   "incognito_mode", "offline", "skipped", "shuffle", "reason_end",
                                   "reason_start"]
    _fields_not_null: list[str] = ["spotify_track_uri", "ts", "ms_played"]

    @staticmethod
    def _listen_valid(listen: dict[str, Any]) -> bool:
        for field in SpotifyInterface._fields_required:
            if field not in listen:
                return False

            if field in SpotifyInterface._fields_not_null and field is None:
                return False

        return True

    @staticmethod
    def _analyze_json(user_id: int, zip_file: ZipFile, file: ZipInfo) -> None:
        contents: Any = json.loads(zip_file.read(file))

        if type(contents) is not list:
            return
        contents: list

        CHUNK_SIZE: int = 500
        for bundle in [contents[i:i + CHUNK_SIZE] for i in range(0, len(contents), CHUNK_SIZE)]:
            valid_elements: list[dict[str, Any]] = []
            for json_element in bundle:
                if type(json_element) is not dict:
                    continue
                json_element: dict[str, Any]

                if not SpotifyInterface._listen_valid(json_element):
                    continue

                valid_elements.append({
                    "owner": user_id,
                    "song_uri": json_element["spotify_track_uri"],
                    "timestamp": datetime.datetime.fromisoformat(json_element["ts"].replace("Z", "+00:00")).replace(
                        tzinfo=None),
                    "ms_played": json_element["ms_played"],
                    "conn_country": json_element["conn_country"],
                    "ip_addr": json_element["ip_addr"],
                    "incognito_mode": json_element["incognito_mode"],
                    "offline": json_element["offline"],
                    "skipped": json_element["skipped"],
                    "shuffle": json_element["shuffle"],
                    "reason_end": json_element["reason_end"],
                    "reason_start": json_element["reason_start"]
                })

            DatabaseManager.execute_many("queue/insert-into-queue.sql", valid_elements)

    @staticmethod
    def _process_zip_file(user_id: int) -> None:
        path: str = os.path.join(config.UPLOAD_FOLDER, f"{user_id}.zip")

        with ZipFile(path, 'r') as zip_file:
            for file in zip_file.filelist:
                if not file.filename.endswith('.json'):
                    continue

                SpotifyInterface._analyze_json(user_id, zip_file, file)

        os.remove(path)

    @staticmethod
    def _new_tracks(song_uris: list[str]) -> None:
        while True:
            try:
                processed_tracks: list[dict[str, Any]] = SpotifyInterface.spotify.tracks(song_uris)
            except Exception as e:
                print(e, flush=True)
                sleep(1)
                continue

            # Ya are here mate

            break

    @staticmethod
    def _process_tracks(tracks: list[dict[str, Any]]) -> None:
        def _format_listens(listens: list[dict[str, Any]]) -> list[dict[str, Any]]:
            return [{
                "user_id": l["owner"],
                "song_uri": l["song_uri"],
                "timestamp": l["timestamp"],
                "ms_played": l["ms_played"],
                "conn_country": l["conn_country"],
                "ip_addr": l["ip_addr"],
                "reason_start": l["reason_start"],
                "reason_end": l["reason_end"],
                "shuffle": l["shuffle"],
                "skipped": l["skipped"],
                "offline": l["offline"],
                "incognito_mode": l["incognito_mode"]
            } for l in listens]

        existing_tracks: list[dict[str, Any]] = DatabaseManager.execute_with_list(
            "song-processing/get-existing-songs.sql",
            [t["song_uri"] for t in tracks]
        )

        DatabaseManager.execute_many(
            "song-processing/add-song-listens.sql",
            _format_listens(existing_tracks)
        )

        existing_uris: set = {t["song_uri"] for t in existing_tracks}
        new_tracks_listens: list[dict[str, Any]] = [t for t in tracks if t["song_uri"] not in existing_uris]

        if new_tracks_listens:
            SpotifyInterface._new_tracks([t["song_uri"] for t in new_tracks_listens])

            DatabaseManager.execute_many(
                "song-processing/add-song-listens.sql",
                _format_listens(new_tracks_listens)
            )

        DatabaseManager.execute_with_list(
            "song-processing/remove-queue-elements.sql",
            [t["song_uri"] for t in tracks]
        )

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

            tracks: list[dict[str, Any]] = DatabaseManager.run_query("queue/get-first-50-queue-elements.sql")
            if tracks:
                SpotifyInterface._process_tracks(tracks)

            sleep(config.INACTIVE_INTERVAL)
