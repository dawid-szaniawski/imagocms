import uuid
import os
from werkzeug.utils import secure_filename


def allowed_file(allowed_extensions, filename):
    allowed_extensions = allowed_extensions
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def generate_random_string():
    return str(uuid.uuid4())


def change_name(file):
    return generate_random_string()+'.'+file.rsplit('.', 1)[1].lower()


def upload_image(upload_folder, file):
    filename = secure_filename(change_name(file.filename))
    file.save(os.path.join(upload_folder, filename))
    return filename
