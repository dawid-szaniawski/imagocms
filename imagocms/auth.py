import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug.security import check_password_hash, generate_password_hash

from imagocms.db import get_db
from imagocms.sql_queries import (
    select_id_password_by_name,
    insert_user,
    select_all_user_data_by_id
)


bp = Blueprint("auth", __name__, url_prefix="/login")


@bp.route("/", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        error = None

        if not is_login_data_correct(username, password):
            error = "Wprowadzone dane są nieprawidłowe."

        user = get_db().execute(select_id_password_by_name, (username,)).fetchone()

        if user is None:
            error = "Użytkownik o takim loginie nie istnieje."

        if error is None:
            if check_password_hash(user["password"], password):
                session.clear()
                session["user_id"] = user["id"]
                return redirect(url_for("index"))
            error = "Nieprawidłowe hasło"

        flash(error)

    return render_template("auth/login.html")


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        error = None

        if not is_login_data_correct(username, password, email):
            error = "Wprowadzone dane są nieprawidłowe."
        elif email == "":
            email = None

        if error is None:
            db = get_db()
            try:
                db.execute(
                    insert_user, (username, generate_password_hash(password), email)
                )
                db.commit()
            except db.IntegrityError:
                error = "Użytkownik o takim loginie lub adresie mailowym już istnieje!"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(select_all_user_data_by_id, (user_id,)).fetchone()


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(**kwargs)

    return wrapped_view


def is_login_data_correct(
    user_login: str, user_password: str, user_email: str | None = None
) -> bool:
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
    if len(user_login) > 15 or len(user_password) > 24:
        return False

    for i in forbidden_chars:
        if i in user_login or i in user_password:
            return False

    if user_email and user_email != "":
        if user_email.count("@") != 1:
            return False

    return True
