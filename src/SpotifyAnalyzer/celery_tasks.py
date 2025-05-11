"""
# TODO: Write Docstring!
"""

from zipfile import ZipFile
from celery import Celery
import SpotifyAnalyzer.config as config


celery: Celery = Celery(
    'spotify_analyzer',
    broker=config.CELERY_BROKER_URL,
    backend=config.CELERY_BACKEND_URL
)


@celery.task
def process(path: str) -> None:
    """
    # TODO: Write Docstring!
    """

    print(path, flush=True)
