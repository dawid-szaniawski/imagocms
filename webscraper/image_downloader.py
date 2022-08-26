from pathlib import Path
from os.path import join

from requests import get


class Downloader:
    def __init__(self, upload_folder: Path):
        self.upload_folder = upload_folder

    def save_image(self, filename: str, file_src: str) -> None:
        bytes_object = self._convert_string_into_bytes_object(file_src)
        self._write_bytes_to_file(filename, bytes_object)

    def _write_bytes_to_file(self, file_name: str, bytes_object: bytes) -> None:
        with open(join(self.upload_folder, file_name), "wb") as file:
            file.write(bytes_object)

    @staticmethod
    def _convert_string_into_bytes_object(image_src: str) -> bytes:
        return get(image_src).content
