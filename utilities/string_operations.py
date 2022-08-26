import uuid

from werkzeug.utils import secure_filename


def change_name(file_name: str) -> str:
    """Creates a new file name based on the UUID4 and previous file extension.

    Args:
        file_name: file.filename from flask form.

    Returns:
        new filename - randomly generated uuid4+extension."""
    new_name = str(uuid.uuid4()) + "." + file_name.rsplit(".", 1)[1].lower()
    return secure_filename(new_name)


def is_data_correct(user_login: str, user_password: str, user_email: str = "") -> bool:
    """Checks if the user has entered login, password, and email address (optional).
    Additionally, it verifies that they are of the correct length and that they do not
    contain forbidden characters.

    Args:
        user_login: string containing login
        user_password: string containing password
        user_email: string containing email

    Returns:
        True if all the data was correct, and False if something goes wrong."""
    forbidden_chars = '"#$%^&*\\()=, „”-/<>|;ąćęłńóśźż{}[]`'

    if user_login is None or user_password is None:
        return False
    if user_login == "" or user_password == "":
        return False
    if len(user_login) > 15 or len(user_password) > 24 or len(user_email) > 64:
        return False

    for i in forbidden_chars:
        if i in user_login or i in user_password or i in user_email:
            return False

    if user_email != "":
        if user_email.count("@") != 1:
            return False

    return True
