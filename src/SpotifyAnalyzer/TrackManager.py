"""
# TODO: Write Docstring!
"""

from zipfile import ZipFile
from threading import Thread
import threading


class TrackManager:
    """
    # TODO: Write Docstring!
    """

    _zip_file_queue: list[ZipFile] = []

    @staticmethod
    def init() -> None:
        """
        # TODO: Write Docstring!
        """

        TrackManager.thread.run()

    @staticmethod
    def process(zip_file: ZipFile) -> None:
        """
        # TODO: Write Docstring!
        """

        TrackManager._zip_file_queue.append(zip_file)

    @staticmethod
    def _thread_loop() -> None:
        """
        # TODO: Write Docstring!
        """

        while True:
            if not TrackManager._zip_file_queue:
                continue

            zip_file: ZipFile = TrackManager._zip_file_queue[0]

            print(zip_file, flush=True)

            TrackManager._zip_file_queue.pop(0)

    thread: Thread = Thread(target=_thread_loop)
