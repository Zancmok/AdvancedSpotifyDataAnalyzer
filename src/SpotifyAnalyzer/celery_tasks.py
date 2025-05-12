import os
import json
from time import sleep
from zipfile import ZipFile, ZipInfo
from typing import Any
from celery import Celery
import SpotifyAnalyzer.config as config
from SpotifyAnalyzer.DatabaseManager import DatabaseManager
from flask import session

celery: Celery = Celery(
    'spotify_analyzer',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL
)

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
    uri: str = json_element.get("spotify_track_uri") or json_element.get("spotify_episode_uri")

    if not uri:
        return

    if DatabaseManager.run_query("exists_song.sql", spotify_uri=uri)[0][0]:
        return

    song_name: str = json_element["master_metadata_track_name"] or json_element["episode_name"]

    DatabaseManager.run_query("add_song.sql",
                              album_id=0,
                              name=song_name,
                              spotify_uri=uri,
                              img_url="https://icons.veryicon.com/png/o/miscellaneous/hfy/temporary-1.png"
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

        uri: str = json_element.get("spotify_track_uri") or json_element.get("spotify_episode_uri")

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
                                  offline_timestamp=json_element["offline_timestamp"]
                                  )


def process(path: str) -> None:
    with ZipFile(path, 'r') as zip_file:
        for file in zip_file.filelist:
            if not file.filename.endswith('.json'):
                continue

            _analyze_json(zip_file, file)

    os.remove(path)


@celery.task
def spotify_api_process() -> None:
    while True:
        elements: list[tuple[int, dict[str, Any]]] = DatabaseManager.run_query("get_queue_first.sql")

        if not elements:
            sleep(10)

            continue

        element: dict[str, Any] = elements[0][1]

        # print(element, flush=True)

        sleep(.1)
