from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
)
from werkzeug.exceptions import abort

from imagocms.db import get_db
from imagocms.sql_queries import (
    select_images_with_offset,
    select_author_images_with_offset,
    select_single_image,
    select_comments_on_img,
    insert_comment
)

bp = Blueprint("homepage", __name__)


@bp.route("/")
def index():
    """Route for the home page. It can take optional argument.
    Shows the newest post with its title, description, image,
    and the number of comments."""
    author = request.args.get("author", None)
    page = int(request.args.get("page", 1))

    images_data = get_db().execute(
        select_author_images_with_offset if author else select_images_with_offset,
        (author, (page * 10) - 10) if author else ((page * 10) - 10,)
    ).fetchall()
    images = images_data[:10]

    if not images:
        if author or page != 1:
            abort(404)

    return render_template(
        "homepage/index.html",
        images=images,
        author=author,
        page=page,
        next_page=set_next_page(images_data[10:], page),
    )


@bp.route("/img/<int:img_id>", methods=("GET", "POST"))
def image_page(img_id: int):
    """Route for single post page. It takes one argument and shows the post and all the
    comments related to the post.

    Args:
        img_id: int. Unique ID number from the database."""
    if request.method == "POST":
        body = request.form["comment"]
        error = None

        if not body:
            error = "Treść komentarza nie może być pusta"

        if error is None:
            db = get_db()
            db.execute(insert_comment, (g.user["id"], img_id, body))
            db.commit()
            return redirect(request.url)
        flash(error)

    db = get_db()
    image_page_data = db.execute(select_single_image, (img_id, )).fetchone()
    comments = db.execute(select_comments_on_img, (img_id, )).fetchall()

    return render_template(
        "homepage/image_page.html", image=image_page_data, comments=comments
    )


def set_next_page(next_page_data: list[dict], page: int) -> int | None:
    """If is any data in next_page_data it increases page by one.
    If next_page_data is empty, returns None.

    Args:
        next_page_data: empty list or list containing db.Row object.
        page: an integer that will be increased by one if the conditions are met.

    Returns
        integer or none. If next_page_data is not empty,
        it increments the value of page by one."""
    if not next_page_data:
        return None
    else:
        return page + 1
