from flask import Blueprint, flash, g, render_template, request
from imagocms.db import get_db
from imagocms.auth import login_required, moderator_required, superuser_required

bp = Blueprint('panel', __name__, url_prefix='/panel')


@bp.route('/', methods=('GET', 'POST'))
@login_required
def mod_panel():
    return render_template('panel/mod_panel.html')


@bp.route('/admin', methods=('GET', 'POST'))
@superuser_required
def admin_panel():
    return render_template('panel/admin_panel.html')
