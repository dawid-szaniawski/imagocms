import uuid
from typing import IO

from PIL import Image
from werkzeug.utils import secure_filename


def is_valid_image(
    allowed_extensions: set[str, ...], file: IO[bytes], filename: str
) -> bool:
    """Checks if the uploaded file has an extension accepted by the application.

    Args:
        allowed_extensions: set with allowed extensions.
        file: file-like object containing the encoded image.
        filename: string containing full filename.

    Returns:
        True if file extension is in allowed extensions, and False if not."""
    extension_from_name = filename.rsplit(".")[-1].upper()

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


def change_file_name(file_name: str) -> str:
    """Creates a new file name based on the UUID4 and previous file extension.

    Args:
        file_name: file.filename from flask form.

    Returns:
        new filename - randomly generated uuid4+extension."""
    new_name = str(uuid.uuid4()) + "." + file_name.rsplit(".", 1)[1].lower()
    return secure_filename(new_name)
