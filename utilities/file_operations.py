import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app

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


def upload_image(file: FileStorage) -> str:
    """Method used to save file in server. Returns filename."""
    filename = secure_filename(change_name(file.filename))
    file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
    return filename


def download_images(file_name_and_request_object: dict) -> None:
    """Method used to download image to server from another place.

    Args:
        file_name_and_request_object: a dictionary containing the name of the file and the request object of the file we
         want to download."""
    for file_name, file_src in file_name_and_request_object.items():
        with open(
            os.path.join(current_app.config["UPLOAD_FOLDER"], file_name), "wb"
        ) as file:
            file.write(file_src.content)
