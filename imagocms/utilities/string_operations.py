import uuid


def generate_random_string():
    return str(uuid.uuid4())


def change_name(file):
    return generate_random_string()+'.'+file.rsplit('.', 1)[1].lower()


def check_correctness_of_the_data(user_login, user_password, user_email=''):
    forbidden_chars = '"#$%^&*\\()=, „”-/<>|;'

    if user_login is None or user_password is None:
        return False
    elif len(user_login) > 15 or len(user_password) > 256 or len(user_email) > 320:
        return False

    for i in forbidden_chars:
        if i in user_login or i in user_password or i in user_email:
            return False

    return True
