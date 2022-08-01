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
from werkzeug.exceptions import abort

from imagocms.db import get_db

bp = Blueprint("homepage", __name__)


@bp.route("/")
@bp.route("/<int:page>")
def index(page: int = 1):
    """Route for the home page. It can take optional argument.
    Shows the newest post with its title, description, image, and the number of comments.

    Args:
        page = int. On one page we show 10 post."""
    db = get_db()

    to_execute_command = """
    SELECT i.id, i.title, i.description, i.img_src, i.filename, i.created, u.username, COUNT(c.id) AS comments
    FROM images i
    LEFT JOIN user u ON i.author_id = u.id
    LEFT JOIN comments c ON i.id = c.image_id
    GROUP BY i.id
    ORDER BY i.created DESC
    LIMIT 11 OFFSET ?"""
    to_execute_variables = ((page * 10) - 10,)

    images_data = db.execute(to_execute_command, to_execute_variables).fetchall()
    images = images_data[:10]

    if not images and page != 1:
        abort(404)

    return render_template(
        "homepage/index.html",
        images=images,
        page=page,
        next_page=set_next_page(images_data[10:], page),
    )


@bp.route("/author:<author_name>")
@bp.route("/author:<author_name>/<int:page>")
def author_index(page: int = 1, author_name: str = None):
    """Route for the author page. It can take two optional arguments.
    Shows the newest author post with its title, description, image, and the number of comments.

    Args:
        page = int. On one page we show 10 post.
        author_name = str. Show only post from that author."""
    db = get_db()

    to_execute_command = """
    SELECT i.id, i.title, i.description, i.img_src, i.filename, i.created, u.username, COUNT(c.id) AS comments
    FROM images i
    LEFT JOIN user u ON i.author_id = u.id
    LEFT JOIN comments c ON i.id = c.image_id
    WHERE u.username = ?
    GROUP BY i.id
    ORDER BY i.created DESC
    LIMIT 11 OFFSET ?"""
    to_execute_variables = (
        author_name,
        (page * 10) - 10,
    )

    images_data = db.execute(to_execute_command, to_execute_variables).fetchall()
    images = images_data[:10]

    if not images and page != 1:
        abort(404)

    return render_template(
        "homepage/author_index.html",
        images=images,
        page=page,
        next_page=set_next_page(images_data[10:], page),
        author=author_name,
    )


@bp.route("/img/<int:img_id>", methods=("GET", "POST"))
def image_page(img_id: int):
    """Route for single post page. It takes one argument and shows the post and all the comments related to the post.

    Args:
        img_id: int. Unique ID number from the database."""
    if request.method == "POST":
        body = request.form["comment"]
        error = None

        if not body:
            error = "Treść komentarza nie może być pusta"

        if error is None:
            db = get_db()
            db.execute(
                "INSERT INTO comments (author_id, image_id, body) VALUES (?, ?, ?)",
                (g.user["id"], img_id, body),
            )
            db.commit()
            return redirect(request.url)
        flash(error)

    image_page_data = (
        get_db()
        .execute(
            """
    SELECT i.title, i.description, i.img_src, i.filename, i.created AS img_created, img_u.username AS img_author,
    c.body, c.created AS c_created, u.username AS c_author, counter.c_count
    FROM images i
    LEFT JOIN user img_u ON i.author_id = img_u.id
    LEFT JOIN comments c ON i.id = c.image_id
    LEFT JOIN user u ON c.author_id = u.id
    CROSS JOIN (SELECT COUNT(*) AS c_count FROM comments c2 WHERE c2.image_id = ?) counter
    WHERE i.id = ? ORDER BY c_created DESC""",
            (img_id, img_id),
        )
        .fetchall()
    )

    return render_template("homepage/image_page.html", image_page_data=image_page_data)


def set_next_page(next_page_data: list, page: int) -> int | None:
    """If is any data in next_page_data it increases page by one. If next_page_data is empty, returns None."""
    if not next_page_data:
        return None
    else:
        return page + 1
