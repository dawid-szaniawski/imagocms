import datetime
import functools
import os

from flask import Blueprint, request, current_app
import jwt
from werkzeug.security import check_password_hash

from imagocms.db import get_db
from imagocms.sql_queries import (
    select_user_by_id_name_email,
    select_all_user_data_by_name,
    select_images_by_author_id,
    select_last_img_scr_from_author,
    insert_image,
    do_nothing_on_conflict
)
from imagocms.file_operations import is_valid_image, change_file_name


bp = Blueprint("api", __name__, url_prefix="/api")


def api_login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

            try:
                decoded = jwt.decode(
                    jwt=token,
                    key=current_app.config["SECRET_KEY"],
                    algorithms=["HS256"]
                )
            except (
                jwt.exceptions.InvalidSignatureError, jwt.ExpiredSignatureError
            ):
                return "", 401

            if all((
                    "sub" in decoded, "name" in decoded, "email" in decoded
            )):
                user = get_db().execute(
                    select_user_by_id_name_email,
                    (decoded["sub"], decoded["name"], decoded["email"])
                ).fetchone()

                if user and user["username"] == decoded["name"]:
                    return view(**kwargs)
        return "", 401

    return wrapped_view


@bp.route("/login", methods=("POST", ))
def login_via_api():
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    db = get_db()
    user = db.execute(select_all_user_data_by_name, (username, )).fetchone()

    if user is None:
        return {"error": "User does not exist"}, 401

    if check_password_hash(
            user["password"], password
    ) and user["email"] == email:
        token = jwt.encode(
            payload={
                "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
                "iat": datetime.datetime.utcnow(),
                "sub": user["id"],
                "name": username,
                "email": email
            },
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )
        return {"__token__": token}, 200

    return {"error": "Incorrect credentials"}, 401


@bp.route("/images", methods=("GET", "POST"))
@api_login_required
def user_images():
    user_id = jwt.decode(
        jwt=request.headers["Authorization"].split(" ")[1],
        key=current_app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )["sub"]
    db = get_db()

    if request.method == "POST":
        title = request.json.get("title")
        description = request.json.get("description")
        img_src = request.json.get("img_src")
        source = request.json.get("source")
        accepted = request.json.get("accepted", False)
        try:
            db.execute(
                do_nothing_on_conflict(insert_image),
                (user_id, title, description, None, img_src, source, accepted)
            )
        except db.IntegrityError:
            db.cancel()
            return "", 406
        db.commit()
        return "", 201

    limit = request.args.get("limit", 5)
    offset = request.args.get("offset", 0)
    images = db.execute(
        select_images_by_author_id, (user_id, limit, offset)
    ).fetchall()
    return images, 200


@bp.route("/images_src")
@api_login_required
def images_sources():
    user_id = jwt.decode(
        jwt=request.headers["Authorization"].split(" ")[1],
        key=current_app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )["sub"]
    db = get_db()
    limit = request.args.get("limit", 5)
    images = db.execute(
        select_last_img_scr_from_author, (user_id, limit)
    ).fetchall()
    return [img["img_src"] for img in images], 200


@bp.route("/image_upload", methods=("POST", ))
@api_login_required
def upload_image():
    user_data = jwt.decode(
        jwt=request.headers["Authorization"].split(" ")[1],
        key=current_app.config["SECRET_KEY"],
        algorithms=["HS256"]
    )["sub"]
    if all((
        user_data["sub"] == 1,
        request.files, "title" in request.headers,
        "author_id" in request.headers
    )):
        image = request.files["image"]

        if is_valid_image(
            allowed_extensions=current_app.config["ALLOWED_EXTENSIONS"],
            file=image.stream,
            filename=image.filename
        ):
            image.stream.seek(0)
            filename = change_file_name(image.filename)
            image.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
            image.close()

            db = get_db()
            db.execute(
                insert_image,
                (user_data["sub"], request.headers["title"], None, filename, None, True)
            )
            db.commit()
            return "", 201

        return "", 415

    return "", 404
