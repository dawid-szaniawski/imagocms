import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from imagocms.db import get_db


bp = Blueprint('auth', __name__, url_prefix='/login')


@bp.route('/', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            print('no name')
            error = 'Nieprawidłowa nazwa użytkownika'
        elif not check_password_hash(user['password'], password):
            print('no pass')
            error = 'Nieprawidłowe hasło'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None

        if not username:
            error = 'Nazwa użytkownika jest wymagana.'
        elif not password:
            error = 'Musisz podać hasło.'
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
