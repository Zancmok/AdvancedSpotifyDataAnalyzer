import os
import json
from time import sleep
from zipfile import ZipFile, ZipInfo
from typing import Any
from celery import Celery
from SpotifyAnalyzer import SpotifyAnalyzer as config
from SpotifyAnalyzer.SpotifyAnalyzer.DatabaseManager import DatabaseManager
from flask import session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

celery: Celery = Celery(
    'spotify_analyzer',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL
)

spotify: Spotify = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=config.SPOTIFY_CLIENT_ID,
    client_secret=config.SPOTIFY_CLIENT_SECRET
))

_CORRECT_KEYS: list[str] = ['ts', 'platform', 'ms_played', 'conn_country', 'ip_addr', 'master_metadata_track_name',
                            'master_metadata_album_artist_name', 'master_metadata_album_album_name',
                            'spotify_track_uri', 'episode_name', 'episode_show_name', 'spotify_episode_uri',
                            'audiobook_title', 'audiobook_uri', 'audiobook_chapter_uri', 'audiobook_chapter_title',
                            'reason_start', 'reason_end', 'shuffle', 'skipped', 'offline', 'offline_timestamp',
                            'incognito_mode']


def _validate_json_element(json_element: dict[str, Any]) -> bool:
    if list(json_element.keys()) != _CORRECT_KEYS:
        return False

    return True


def _validate_song(json_element: dict[Any, str]) -> None:
    uri: str = json_element.get("spotify_track_uri")

    if not uri:
        return

    if DatabaseManager.run_query("exists_song.sql", spotify_uri=uri)[0][0]:
        return

    song_name: str = json_element["master_metadata_track_name"]

    DatabaseManager.run_query("add_song.sql",
                              album_id=0,
                              name=song_name,
                              spotify_uri=uri,
                              )

    DatabaseManager.run_query("add_queue.sql", data=json.dumps({
        "element_type": "song",
        "element_uri": uri
    }))


def _analyze_json(zip_file: ZipFile, file: ZipInfo) -> None:
    contents: Any = json.loads(zip_file.read(file))

    if type(contents) is not list:
        return

    for json_element in contents:
        if type(json_element) is not dict:
            continue

        json_element: dict[Any, str]

        if not _validate_json_element(json_element):
            continue

        _validate_song(json_element)

        uri: str = json_element.get("spotify_track_uri")

        if not uri:
            continue

        DatabaseManager.run_query("add_song_listen.sql",
                                  user_id=session["user"],
                                  song_id=DatabaseManager.run_query("get_song_from_uri.sql", spotify_uri=uri)[0][0],
                                  timestamp=json_element["ts"],
                                  conn_country=json_element["conn_country"],
                                  ip_address=json_element["ip_addr"],
                                  platform=json_element["platform"],
                                  reason_start=json_element["reason_start"],
                                  reason_end=json_element["reason_end"],
                                  shuffle=json_element["shuffle"],
                                  skipped=json_element["skipped"],
                                  offline=json_element["offline"],
                                  incognito_mode=json_element["incognito_mode"],
                                  offline_timestamp=json_element["offline_timestamp"],
                                  ms_played=json_element["ms_played"]
                                  )


def process(path: str) -> None:
    DatabaseManager.run_query("reset_user_data.sql", user_id=session["user"])

    with ZipFile(path, 'r') as zip_file:
        for file in zip_file.filelist:
            if not file.filename.endswith('.json'):
                continue

            _analyze_json(zip_file, file)

    os.remove(path)


@celery.task
def spotify_api_process() -> None:
    while True:
        elements: list[tuple[int, str]] = DatabaseManager.run_query("get_queue_first.sql")

        if not elements:
            sleep(10)

            continue

        element: dict[str, Any] = json.loads(elements[0][1])

        element_uri: str = element["element_uri"]

        if element["element_type"] == "song":
            try:
                response: dict[str, Any] = spotify.track(element_uri)
            except Exception as e:
                print(e, e.args, flush=True)

                if e.args[0] == 404:
                    DatabaseManager.execute_script("pop_queue.sql")

                sleep(10)
                continue

            if DatabaseManager.run_query("exists_album.sql", spotify_uri=response["album"]["uri"])[0][0]:
                DatabaseManager.run_query("modify_song_album.sql",
                                          album_uri=response["album"]["uri"],
                                          song_uri=element_uri)
            else:
                DatabaseManager.run_query("add_queue.sql", data=json.dumps({
                    "element_type": "album",
                    "element_uri": response["album"]["uri"]
                }))

            DatabaseManager.execute_script("pop_queue.sql")

        elif element["element_type"] == "album":
            try:
                response: dict[str, Any] = spotify.album(element_uri, market='US')
            except Exception as e:
                print(e, e.args, flush=True)

                if e.args[0] == 404:
                    DatabaseManager.execute_script("pop_queue.sql")

                sleep(10)
                continue



            if not DatabaseManager.run_query("exists_album.sql", spotify_uri=element_uri)[0][0]:
                image: str = ""

                if response["images"]:
                    image = response["images"][0]["url"]

                DatabaseManager.run_query("add_album.sql",
                                          author_id=0,
                                          spotify_uri=element_uri,
                                          name=response["name"],
                                          album_type=response["album_type"],
                                          img_url=image)

            for track in response["tracks"]["items"]:
                DatabaseManager.run_query("modify_song_album.sql",
                                          album_uri=response["uri"],
                                          song_uri=track["uri"])

            if DatabaseManager.run_query("exists_author.sql", spotify_uri=response["artists"][0]["uri"])[0][0]:
                DatabaseManager.run_query("modify_album_author.sql",
                                          author_uri=response["artists"][0]["uri"],
                                          album_uri=element_uri)
            else:
                author_id: int = _do_author_thingy(response["artists"][0]["uri"])

                DatabaseManager.run_query("modify_album_author.sql",
                                          author_uri=response["artists"][0]["uri"],
                                          album_uri=element_uri)

            DatabaseManager.execute_script("pop_queue.sql")


def _do_author_thingy(author_uri: str) -> int:
    while True:
        try:
            response: dict[str, Any] = spotify.artist(author_uri)
            break
        except Exception as e:
            print(e, e.args, flush=True)

            if e.args[0] == 404:
                return -1

            sleep(10)

    image: str = ""

    if response["images"]:
        image = response["images"][0]["url"]

    DatabaseManager.run_query("add_author.sql",
                              name=response["name"],
                              spotify_uri=response["uri"],
                              img_url=image)

    author_id: int = DatabaseManager.run_query("get_author.sql", spotify_uri=response["uri"])[0][0]

    for genre in response["genres"]:
        if not DatabaseManager.run_query("exists_genre.sql", name=genre)[0][0]:
            DatabaseManager.run_query("add_genre.sql", name=genre)
        DatabaseManager.run_query("add_author_genre.sql", author_id=author_id,
                                  genre_id=DatabaseManager.run_query("get_genre_id.sql", name=genre)[0][0])

    return author_id
