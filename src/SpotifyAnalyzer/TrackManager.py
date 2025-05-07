"""
# TODO: Write Docstring!
"""

from zipfile import ZipFile


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

    @staticmethod
    def process(zip_file: ZipFile) -> None:
        """
        # TODO: Write Docstring!
        """

        TrackManager._zip_file_queue.append(zip_file)
