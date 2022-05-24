import sqlite3
from flask import current_app, g
from webscraper import start_sync


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


def prepare_images(app):
    """Method to start WebScraper, a tool that prepares demo data.
    It starts only when there is no data in images table."""
    with app.app_context():
        db = get_db()
        with app.open_resource("init_data.sql", mode="r") as file:
            db.executescript(file.read())
        db = get_db()
        test = db.execute("SELECT id FROM images").fetchone()

        if not test:
            websites_data = db.execute(
                "SELECT website_user_id, website_url, image_class, pagination_class FROM ext_websites"
            ).fetchall()
            sync_data = start_sync(websites_data)
            for i in sync_data:
                db.execute(
                    "INSERT INTO images (author_id, filename, title, accepted) VALUES (?, ?, ?, 1)",
                    (i[0], i[1], i[2]),
                )
                db.commit()


def init_app(app):
    """Register close_db, use init_db and prepare_images method."""
    app.teardown_appcontext(close_db)
    init_db(app)
    prepare_images(app)
