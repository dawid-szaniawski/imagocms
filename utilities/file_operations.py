import os
from pathlib import Path

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage

import imghdr

from utilities.string_operations import change_name


def allowed_file(allowed_extensions: set, file: FileStorage) -> bool:
    """Checks if the uploaded file has an extension accepted by the application.
    The set of extensions should be passed as the first argument."""
    allowed_extensions = allowed_extensions
    if not imghdr.what(file) in allowed_extensions:
        return False
    return (
        "." in file.filename
        and file.filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )


def upload_image(file: FileStorage, upload_folder: Path) -> str:
    """Method used to save file in server. Returns filename."""
    filename = secure_filename(change_name(file.filename))
    file.save(os.path.join(upload_folder, filename))
    return filename


def download_images(file_name_and_request_object: dict, upload_folder: Path) -> None:
    """Method used to download image to server from another place.
    Args:
        upload_folder: path where the file should be saved.
        file_name_and_request_object: a dictionary containing the name of the file and the request object of the file we
         want to download."""
    for file_name, file_src in file_name_and_request_object.items():
        with open(os.path.join(upload_folder, file_name), "wb") as file:
            file.write(file_src.content)
