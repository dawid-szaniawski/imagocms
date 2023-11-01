from flask import g, current_app
import psycopg
from psycopg.rows import dict_row


def get_db():
    if "db" not in g:
        g.db = psycopg.connect(
            dbname=current_app.config["DB_NAME"],
            user=current_app.config["DB_USER"],
            host=current_app.config["DB_HOST"],
            port=current_app.config["DB_PORT"],
            password=current_app.config["DB_PASSWORD"],
            row_factory=dict_row
        )
    return g.db


def close_db(e=None):
    """Checks if a connection was created by checking if g.db was set.
    If connection exist, it is closed.

    Args:
        e: refers to the error object. None by default."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db(app):
    """Initiates database and execute instructions from schema.sql file."""
    with app.app_context():
        db = get_db()
        with app.open_resource("postgresql.sql", mode="r") as file:
            db.execute(file.read())
            db.commit()


def init_app(app):
    """Register close_db, use init_db and prepare_images method."""
    app.teardown_appcontext(close_db)
    init_db(app)
