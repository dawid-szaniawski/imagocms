import os
import threading

from flask import Flask

from imagocms import db, auth, homepage, add_image
from imagocms.demo_data_maker import ExternalWebsitesSynchronizer


def prepare_demo_data(app):
    with app.app_context():
        synchronizer = ExternalWebsitesSynchronizer(app.config["UPLOAD_FOLDER"])
        synchronizer.prepare_images_from_external_websites()


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

    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    threading.Thread(target=prepare_demo_data, args=[app]).start()

    app.register_blueprint(auth.bp)
    app.register_blueprint(add_image.bp)
    app.register_blueprint(homepage.bp)
    app.add_url_rule("/", endpoint="index")

    return app
