import sqlite3
import click
import os
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


def create_folders():
    try:
        os.mkdir(current_app.instance_path)
    except OSError:
        pass


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('prepare-app')
@with_appcontext
def prepare_app_command():
    create_folders()
    init_db()
    click.echo('Done.')


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
    app.cli.add_command(prepare_app_command)
    app.cli.add_command(create_superuser_command)
