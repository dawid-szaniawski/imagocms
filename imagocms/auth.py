import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from imagocms.db import get_db

from imagocms.utilities.string_operations import check_correctness_of_the_data


bp = Blueprint('auth', __name__, url_prefix='/login')


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        if not check_correctness_of_the_data(username, password):
            error = 'Wprowadzone dane są nieprawidłowe.'

        if error is None:
            db = get_db()
            user = db.execute(
                'SELECT id, password FROM user WHERE username = ?', (username,)
            ).fetchone()
            if check_password_hash(user['password'], password):
                session.clear()
                session['user_id'] = user['id']
                return redirect(url_for('index'))
            else:
                error = 'Nieprawidłowe hasło'

        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not check_correctness_of_the_data(username, password, email):
            error = 'Wprowadzone dane są nieprawidłowe.'
        elif email == '':
            email = None

        if error is None:
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, password, email) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), email),
                )
                db.commit()
            except db.IntegrityError:
                error = 'Użytkownik o takim loginie lub adresie mailowym już istnieje!'
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view


def moderator_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['superuser'] == 1 or g.user['moderator'] == 1:
            return view(**kwargs)
        session.clear()
        return redirect(url_for('auth.login'))
    return wrapped_view


def superuser_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None or g.user['superuser'] != 1:
            session.clear()
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view
