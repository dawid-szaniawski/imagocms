from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app

from imagocms.db import get_db
from imagocms.auth import login_required

from imagocms.utilities.file_operations import allowed_file, upload_image

bp = Blueprint('create', __name__, url_prefix='/create')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['image']
        error = None
        allowed_extensions = current_app.config['ALLOWED_EXTENSIONS']

        if not title:
            error = 'Tytuł jest wymagany.'
        elif len(title) > 80:
            error = 'Tytuł może mieć maksymalnie 80 znaków.'
        elif not file or file.filename == '':
            error = 'Proszę załączyć plik'
        elif not allowed_file(allowed_extensions, file):
            error = 'Nieprawidłowe rozszerzenie pliku.'
        elif description == '':
            description = None

        if error is None:
            db = get_db()
            filename = upload_image(current_app.config['UPLOAD_FOLDER'], file)
            db.execute(
                'INSERT INTO images (title, author_id, description, filename)'
                ' VALUES (?, ?, ?, ?)',
                (title, g.user['id'], description, filename)
            )
            db.commit()
            return redirect(url_for('homepage.index'))

        flash(error)
    return render_template('homepage/create.html')


@bp.errorhandler(413)
def request_entity_too_large(error):
    flash('Maksymalna wielkość pliku to 2MB')
    return redirect(request.url)
