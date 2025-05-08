"""
# TODO: Write Docstring!
"""

from zipfile import ZipFile
from time import sleep
from celery import Celery
from typing import Optional


class TrackManager:
    """
    # TODO: Write Docstring!
    """

    celery: Celery = Celery('spotify_analyzer')

    @staticmethod
    def process(zip_file: ZipFile) -> None:
        """
        # TODO: Write Docstring!
        """

        TrackManager._thread_loop.apply_async()

    @staticmethod
    @celery.task
    def _thread_loop() -> None:
        """
        # TODO: Write Docstring!
        """
        print(f"Processing zip file", flush=True)
        
        sleep(2)  # Simulate processing time
        print(f"Finished processing", flush=True)
