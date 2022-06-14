import uuid

from bs4.element import ResultSet


def change_name(file_name: str) -> str:
    """Creates a new file name based on the UUID4 and previous file extension.

    Args:
        file_name: file.filename from flask form.

    Returns:
        new filename - randomly generated uuid4+extension."""
    return str(uuid.uuid4()) + "." + file_name.rsplit(".", 1)[1].lower()


def is_data_correct(user_login: str, user_password: str, user_email: str = "") -> bool:
    """Checks if the user has entered login, password, and email address (optional).
    Additionally, it verifies that they are of the correct length and that they do not contain forbidden characters."""
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


def prepare_src_and_alt(images_data: ResultSet) -> dict:
    """A method that extracts the source of the image and its alt from the ResultSet object.

    Args:
        images_data: bs4.element.ResultSet. Subclass of list with HTML IMG objects."""
    return {image["src"]: image["alt"] for image in images_data}
