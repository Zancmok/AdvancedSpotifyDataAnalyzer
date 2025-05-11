import os
import json
from zipfile import ZipFile, ZipInfo
from typing import Any
from celery import Celery
import SpotifyAnalyzer.config as config
from SpotifyAnalyzer.DatabaseManager import DatabaseManager

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


def _analyze_json(zip_file: ZipFile, file: ZipInfo) -> None:
    contents: Any = json.loads(zip_file.read(file))

    if type(contents) is not list:
        return

    for json_element in contents:
        if type(json_element) is not dict:
            continue

        json_element: dict

        if not _validate_json_element(json_element):
            continue

        DatabaseManager.run_query("add_queue.sql", data=json.dumps(json_element))  # This is not what you should be doin


@celery.task
def process(path: str) -> None:
    with ZipFile(path, 'r') as zip_file:
        for file in zip_file.filelist:
            if not file.filename.endswith('.json'):
                continue

            _analyze_json(zip_file, file)

    os.remove(path)
