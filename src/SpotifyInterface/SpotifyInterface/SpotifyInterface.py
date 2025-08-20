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

            if field in SpotifyInterface._fields_not_null and listen[field] is None:
                return False

        return True

    @staticmethod
    def _analyze_json(user_id: int, zip_file: ZipFile, file: ZipInfo) -> None:
        contents: Any = json.loads(zip_file.read(file))

        if type(contents) is not list:
            return
        contents: list

        valid_elements: list[dict[str, Any]] = []
        for json_element in contents:
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

        SpotifyInterface._process_tracks(valid_elements)

    @staticmethod
    def _process_genres(genres: list[str]) -> None:
        unique_genres: set[str] = set(genres)

        existing_genres: set[str] = set(DatabaseManager.execute_with_list("artist-processing/get-existing-genres.sql", list(unique_genres)))
        new_genres: set[str] = unique_genres - existing_genres

        DatabaseManager.execute_many("artist-processing/add-genres.sql", [{"name": genre} for genre in new_genres])

    @staticmethod
    def _process_artists(artist_uris: list[str]) -> None:
        unique_artist_uris: set[str] = set(artist_uris)

        existing_artist_uris: set[str] = set(DatabaseManager.execute_with_list("artist-processing/get-existing-artists.sql", list(unique_artist_uris)))
        artists_to_process: set[str] = unique_artist_uris - existing_artist_uris

        processed_artists: list[dict[str, Any]] = []
        BATCH_STACK_SIZE: int = 50
        batches: list[list[str]] = [list(artists_to_process)[i:i+BATCH_STACK_SIZE] for i in range(0, len(artists_to_process), BATCH_STACK_SIZE)]
        for batch in batches:
            while True:
                try:
                    api_response: list[dict[str, Any]] = SpotifyInterface.spotify.artists(batch)["artists"]

                    for processed_artist in api_response:
                        image: dict[str, Any] = processed_artist["images"][0] if processed_artist["images"] else {
                            "url": None,
                            "height": None,
                            "width": None
                        }

                        processed_artists.append({
                            "uri": processed_artist["uri"],
                            "image_url": image["url"],
                            "image_height": image["height"],
                            "image_width": image["width"],
                            "name": processed_artist["name"],
                            "genres": processed_artist["genres"]
                        })

                    break
                except Exception as e:
                    print(f"Failed processing a batch of artists due to an error: {e}", flush=True)
                    print(batch, flush=True)
                    sleep(config.ERROR_SLEEP_INTERVAL)

        genres: list[str] = []
        for artist in processed_artists:
            for genre in artist["genres"]:
                genres.append(genre)
        SpotifyInterface._process_genres(genres)

        DatabaseManager.execute_many("artist-processing/add-artists.sql", processed_artists)

        genre_map: dict[str, int] = {row["name"]: row["id"] for row in DatabaseManager.run_query("artist-processing/get-genres.sql")}

        DatabaseManager.execute_many("artist-processing/add-genre-artist.sql", [
            {"genre_id": genre_map[genre], "artist_uri": artist["uri"]}
            for artist in processed_artists
            for genre in artist["genres"]
        ])

    @staticmethod
    def _process_albums(album_uris: list[str]) -> None:
        unique_album_uris: set[str] = set(album_uris)

        existing_album_uris: set[str] = set(DatabaseManager.execute_with_list("album-processing/get-existing-albums.sql", list(unique_album_uris)))
        albums_to_process: set[str] = unique_album_uris - existing_album_uris

        processed_albums: list[dict[str, Any]] = []
        BATCH_STACK_SIZE: int = 20
        batches: list[list[str]] = [list(albums_to_process)[i:i+BATCH_STACK_SIZE] for i in range(0, len(albums_to_process), BATCH_STACK_SIZE)]
        for batch in batches:
            while True:
                try:
                    api_response: list[dict[str, Any]] = SpotifyInterface.spotify.albums(batch)["albums"]

                    for processed_album in api_response:
                        image: dict[str, Any] = processed_album["images"][0] if processed_album["images"] else {
                            "url": None,
                            "height": None,
                            "width": None
                        }

                        processed_albums.append({
                            "uri": processed_album["uri"],
                            "album_type": processed_album["album_type"],
                            "total_tracks": processed_album["total_tracks"],
                            "image_url": image["url"],
                            "image_height": image["height"],
                            "image_width": image["width"],
                            "name": processed_album["name"],
                            "artists": [artist['uri'] for artist in processed_album["artists"]]
                        })

                    break
                except Exception as e:
                    print(f"Failed processing a batch of albums due to an error: {e}", flush=True)
                    print(batch, flush=True)
                    sleep(config.ERROR_SLEEP_INTERVAL)

        artist_uris: list[str] = []
        for album in processed_albums:
            for artist_uri in album["artists"]:
                artist_uris.append(artist_uri)
        SpotifyInterface._process_artists(artist_uris)

        DatabaseManager.execute_many("album-processing/add-albums.sql", processed_albums)
        DatabaseManager.execute_many("album-processing/add-album-artist.sql", [{
            "artist_uri": artist,
            "album_uri": album["uri"]
        } for album in processed_albums for artist in album["artists"]])

    @staticmethod
    def _process_tracks(tracks: list[dict[str, Any]]) -> None:
        unique_track_uris: set[str] = set(track["song_uri"] for track in tracks)

        existing_song_uris: set[str] = set(DatabaseManager.execute_with_list("song-processing/get-existing-songs.sql", list(unique_track_uris)))
        songs_to_process: set[str] = unique_track_uris - existing_song_uris

        processed_tracks: list[dict[str, Any]] = []
        BATCH_STACK_SIZE: int = 50
        batches: list[list[str]] = [list(songs_to_process)[i:i+BATCH_STACK_SIZE] for i in range(0, len(songs_to_process), BATCH_STACK_SIZE)]
        for batch in batches:
            while True:
                try:
                    api_response: list[dict[str, Any]] = SpotifyInterface.spotify.tracks(batch)["tracks"]

                    for processed_track in api_response:
                        processed_tracks.append({
                            "uri": processed_track["uri"],
                            "album_uri": processed_track["album"]["uri"],
                            "duration": processed_track["duration_ms"],
                            "explicit": processed_track["explicit"],
                            "name": processed_track["name"],
                            "preview_url": processed_track.get("preview_url"),
                            "is_local": processed_track["is_local"],
                            "artists": [artist['uri'] for artist in processed_track["artists"]]
                        })

                    break
                except Exception as e:
                    print(f"Failed processing a batch of tracks due to an error: {e}", flush=True)
                    print(batch, flush=True)
                    sleep(config.ERROR_SLEEP_INTERVAL)

        SpotifyInterface._process_albums([
            track["album_uri"] for track in processed_tracks
        ])

        artist_uris: list[str] = []
        for track in processed_tracks:
            for artist_uri in track["artists"]:
                artist_uris.append(artist_uri)
        SpotifyInterface._process_artists(artist_uris)

        DatabaseManager.execute_many("song-processing/add-song.sql", processed_tracks)
        DatabaseManager.execute_many("song-processing/add-song-artist.sql", [{
            "song_uri": song["uri"],
            "artist_uri": artist
        } for song in processed_tracks for artist in song["artists"]])

    @staticmethod
    def _process_zip_file(user_id: int) -> None:
        path: str = os.path.join(config.UPLOAD_FOLDER, f"{user_id}.zip")

        with ZipFile(path, 'r') as zip_file:
            for file in zip_file.filelist:
                if not file.filename.endswith('.json'):
                    continue

                SpotifyInterface._analyze_json(user_id, zip_file, file)

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

                SpotifyInterface._process_zip_file(user_id)

                os.remove(os.path.join(config.UPLOAD_FOLDER, f"{user_id}.zip"))

                print(f"Data of user with id of '{user_id}' processed successfully!", flush=True)

                continue

            sleep(config.INACTIVE_INTERVAL)
