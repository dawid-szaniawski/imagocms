import os
import threading

from imagocms import db, auth, homepage, add_image

from flask import Flask


def prepare_app_requirements(app):
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(add_image.bp)
    app.register_blueprint(homepage.bp)
    app.add_url_rule("/", endpoint="index")


def prepare_demo_data(app):
    from imagocms.demo_data_maker import prepare_images_from_external_websites
    from time import sleep

    while True:
        with app.app_context():
            prepare_images_from_external_websites(app.config["UPLOAD_FOLDER"])
        sleep(1620)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY="dev",
            DATABASE=os.path.join(app.instance_path, "imago.sqlite"),
            UPLOAD_FOLDER=os.path.join(app.static_folder, "images"),
            MAX_CONTENT_LENGTH=2 * 1000 * 1000,
            ALLOWED_EXTENSIONS={"PNG", "JPG", "JPEG", "GIF", "WEBP"},
        )
    else:
        app.config.from_mapping(test_config)

    threading.Thread(target=prepare_demo_data, args=[app]).start()
    threading.Thread(target=prepare_app_requirements, args=[app]).start()

    return app
