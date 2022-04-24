import uuid

import bs4.element


def change_name(file: str) -> str:
    """
    Creates a new file name based on the UUID4 and previous file extension.

    Args:
        file: file.filename from flask form.

    Returns:
        new filename - randomly generated uuid4+extension.
    """
    return str(uuid.uuid4())+'.'+file.rsplit('.', 1)[1].lower()


def check_correctness_of_the_data(user_login: str, user_password: str, user_email: str = '') -> bool:
    """
    Checks if the user has entered login, password, and email address (optional).
    Additionally, it verifies that they are of the correct length and that they do not contain forbidden characters.
    """
    forbidden_chars = '"#$%^&*\\()=, „”-/<>|;ąćęłńóśźż{}[]`'

    if user_login is None or user_password is None:
        return False
    if len(user_login) > 15 or len(user_password) > 256 or len(user_email) > 320:
        return False

    for i in forbidden_chars:
        if i in user_login or i in user_password or i in user_email:
            return False

    return True


def prepare_src_and_alt(images_data: bs4.element.ResultSet) -> dict:
    """
    A method that extracts the source of the image and its alt from the bs4.element.ResultSet object.
    """
    return {image['src']: image['alt'] for image in images_data}
