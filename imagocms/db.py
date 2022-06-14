import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """Checks if a connection was created by checking if g.db was set. If connection exist, it is closed.

    Args:
        e: refers to the error object. None by default."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    """Initiates database and execute instructions from schema.sql file."""
    with app.app_context():
        db = get_db()
        with app.open_resource("schema.sql", mode="r") as f:
            db.executescript(f.read())


def add_demo_users_and_external_websites(app):
    """Function only for testing purpose. It's adding a demo users and external websites to download demo data."""
    with app.app_context():
        db = get_db()
        with app.open_resource("init_data.sql", mode="r") as file:
            db.executescript(file.read())


def init_app(app):
    """Register close_db, use init_db and prepare_images method."""
    app.teardown_appcontext(close_db)
    init_db(app)
    add_demo_users_and_external_websites(app)
