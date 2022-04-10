import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """
    Checks if a connection was created by checking if g.db was set. If connection exist, it is closed.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """
    Command line command that calls the init_db function, with is cleaning existing data, creating new tables, then
    show a success message.
    """
    init_db()
    click.echo('Initialized the database.')


def create_superuser(admin_login, admin_password):
    admin_login, admin_password = admin_login, admin_password

    db = get_db()
    db.execute(
        "INSERT INTO user (username, password, superuser) VALUES (?, ?, ?)",
        (admin_login, generate_password_hash(admin_password), 1),
    )
    db.commit()


@click.command('create-superuser')
@with_appcontext
def create_superuser_command():
    login = click.prompt('Enter a administrator login', type=str)
    password = click.prompt('Enter a administrator password', type=str, hide_input=True)

    create_superuser(login, password)

    click.echo('Created superuser.')


def init_app(app):
    """
    Register close_db, init_db and create_superuser functions.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_superuser_command)
