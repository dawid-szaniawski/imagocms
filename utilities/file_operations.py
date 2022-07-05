import os
from pathlib import Path
from typing import IO

from PIL import Image


def is_valid_image(allowed_extensions: set, file: IO[bytes], filename: str) -> bool:
    """Checks if the uploaded file has an extension accepted by the application.
    Args:
        allowed_extensions: set with allowed extensions.
        file: file-like object containing the encoded image.
        filename: string containing full filename."""
    allowed_extensions = allowed_extensions
    extension_from_name = filename.rsplit(".")

    if len(extension_from_name) > 2:
        return False
    else:
        extension_from_name = extension_from_name[1].upper()

    if extension_from_name not in allowed_extensions:
        return False

    try:
        with Image.open(file) as image:
            extension_from_bytes = image.format
    except OSError:
        return False

    if extension_from_bytes not in allowed_extensions:
        return False

    if extension_from_name != extension_from_bytes:
        if extension_from_name == "JPG" and extension_from_bytes == "JPEG":
            return True
        return False

    return True


def download_images(file_name_and_request_object: dict, upload_folder: Path) -> None:
    """Method used to download image to server from another place.
    Args:
        upload_folder: path where the file should be saved.
        file_name_and_request_object: a dictionary containing the name of the file and the request object of the file we
         want to download."""
    for file_name, file_src in file_name_and_request_object.items():
        with open(os.path.join(upload_folder, file_name), "wb") as file:
            file.write(file_src.content)
