from flask import Flask
import os


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'imago.sqlite'),
        UPLOAD_FOLDER=os.path.join(app.static_folder, 'images'),
        MAX_CONTENT_LENGTH=2*1000*1000,
        ALLOWED_EXTENSIONS={'png', 'jpg', 'jpeg', 'gif'}
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    from imagocms import db, auth, panel, homepage
    db.init_app(app)
    app.register_blueprint(auth.bp)
    app.register_blueprint(panel.bp)
    app.register_blueprint(homepage.bp)
    app.add_url_rule('/', endpoint='index')

    return app
