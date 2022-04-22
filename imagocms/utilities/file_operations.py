import os
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import imghdr
from imagocms.utilities.string_operations import change_name


def allowed_file(allowed_extensions: set, file: FileStorage) -> bool:
    """
    Checks if the uploaded file has an extension accepted by the application.
    The set of extensions should be passed as the first argument.
    """
    allowed_extensions = allowed_extensions
    if not imghdr.what(file) in allowed_extensions:
        return False
    return '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions


def upload_image(upload_folder: str, file: FileStorage) -> str:
    """
    Method used to save file in server. Returns filename.
    """
    filename = secure_filename(change_name(file.filename))
    file.save(os.path.join(upload_folder, filename))
    return filename
