import os

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)

from imagocms.db import get_db
from imagocms.auth import login_required
from utilities.file_operations import is_valid_image
from utilities.string_operations import change_name

bp = Blueprint("create", __name__, url_prefix="/create")


@bp.route("/", methods=("GET", "POST"))
@login_required
def create():
    """The route to add posts (usually images). Checks whether the user has inserted
    the title and added graphics or description. Verifies the correctness of the data
    and uploads it to the database. If the user has added an image, it also calls
    the method that saves the attachment on the server."""
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        file = request.files["image"]
        error = None
        allowed_extensions = current_app.config["ALLOWED_EXTENSIONS"]

        if not title:
            error = "Tytuł jest wymagany."
        elif len(title) > 80:
            error = "Tytuł może mieć maksymalnie 80 znaków."
        elif not file and description == "":
            error = "Załącz plik lub uzupełnij pole opis."
        elif file:
            if not is_valid_image(allowed_extensions, file.stream, file.filename):
                file.close()
                extensions = ", ".join(allowed_extensions)
                error = f"Nieprawidłowe rozszerzenie pliku. Spróbuj użyć: {extensions}"

        elif error is None and description == "":
            description = None

        if error is None:
            db = get_db()
            if file:
                file.stream.seek(0)
                filename = change_name(file.filename)
                file.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                file.close()
            else:
                filename = None
            db.execute(
                """
                INSERT INTO images (title, author_id, description, filename, accepted)
                VALUES (?, ?, ?, ?, 0)""",
                (title, g.user["id"], description, filename),
            )
            db.commit()
            return redirect(url_for("homepage.index"))

        flash(error)
    return render_template("add_image/create.html")


@bp.errorhandler(413)
def request_entity_too_large(error):
    """If the file is too large, we will flash an error instead of redirect
    to the error page."""
    flash("Maksymalna wielkość pliku to 2MB")
    return redirect(request.url)
