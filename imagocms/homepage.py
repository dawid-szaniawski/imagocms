from flask import Blueprint, flash, g, redirect, render_template, request, url_for, current_app
from werkzeug.exceptions import abort

from imagocms.db import get_db
from imagocms.auth import login_required

from imagocms.utilities.file_operations import allowed_file, upload_image

bp = Blueprint('homepage', __name__)


@bp.route('/')
@bp.route('/page:<int:page>')
@bp.route('/author:<author_name>')
@bp.route('/author:<author_name>/page:<int:page>')
def index(page=1, author_name=None):
    def split_list(object_to_split):
        return object_to_split[:10], object_to_split[10:]

    db = get_db()

    if author_name:
        to_execute_command = """
        SELECT i.id, i.title, i.description, i.img_src, i.filename, i.created, u.username, COUNT(c.id) AS comments
        FROM images i LEFT JOIN user u ON i.author_id = u.id LEFT JOIN comments c ON i.id = c.image_id
        GROUP BY i.id
        WHERE u.username = ?
        ORDER BY i.created DESC
        LIMIT 11 OFFSET ?"""
        to_execute_variables = (author_name, (page * 10) - 10,)
    else:
        to_execute_command = """
        SELECT i.id, i.title, i.description, i.img_src, i.filename, i.created, u.username, COUNT(c.id) AS comments
        FROM images i LEFT JOIN user u ON i.author_id = u.id LEFT JOIN comments c ON i.id = c.image_id
        GROUP BY i.id
        ORDER BY i.created DESC
        LIMIT 11 OFFSET ?"""
        to_execute_variables = ((page * 10) - 10,)

    images_data, next_page_data = split_list(db.execute(to_execute_command, to_execute_variables).fetchall())

    if not images_data and page != 1:
        abort(404)

    if not next_page_data:
        next_page = None
    else:
        next_page = page+1

    return render_template('homepage/index.html', images=images_data, page=page, next_page=next_page, author=author_name)


@bp.route('/img/<int:img_id>', methods=('GET', 'POST'))
def image_page(img_id):
    def get_image_and_comments(image_id):
        return get_db().execute("""
        SELECT i.title, i.description, i.img_src, i.filename, i.created AS img_created, img_u.username AS img_author,
        c.body, c.created AS c_created, u.username AS c_author
        FROM images i
        LEFT JOIN user img_u ON i.author_id = img_u.id
        LEFT JOIN comments c ON i.id = c.image_id
        LEFT JOIN user u ON c.author_id = u.id
        WHERE i.id = ? ORDER BY c_created DESC""", (image_id,)).fetchall()

    if request.method == 'POST':
        body = request.form['comment']
        error = None

        if not body:
            error = 'Treść komentarza nie może być pusta'

        if error is None:
            db = get_db()
            db.execute("""
            INSERT INTO comments (author_id, image_id, body)
            VALUES (?, ?, ?)""", (g.user['id'], img_id, body))
            db.commit()
            return redirect(request.url)
        flash(error)

    return render_template('homepage/image_page.html', image_page_data=get_image_and_comments(img_id))


@bp.route('/create', methods=('GET', 'POST'))
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
