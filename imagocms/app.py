import os

from flask import Flask

from imagocms import db, auth, homepage, add_image, api


def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY"),
        DB_NAME=os.environ.get("DB_NAME"),
        DB_USER=os.environ.get("DB_USER"),
        DB_HOST=os.environ.get("DB_HOST"),
        DB_PORT=os.environ.get("DB_PORT"),
        DB_PASSWORD=os.environ.get("DB_PASSWORD"),
        UPLOAD_FOLDER=os.path.join(app.static_folder, "images"),
        MAX_CONTENT_LENGTH=3 * 1000 * 1000,
        ALLOWED_EXTENSIONS={"PNG", "JPG", "JPEG", "GIF", "WEBP"},
    )

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(add_image.bp)
    app.register_blueprint(homepage.bp)
    app.register_blueprint(api.bp)
    app.add_url_rule("/", endpoint="index")

    return app
