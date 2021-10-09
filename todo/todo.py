from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from todo.auth import login_required
from todo.db import get_db

bp = Blueprint('todo', __name__)


@bp.route('/')
@login_required
def index():
    """
    Show all Todos that belongs to the user
    """
    db, c = get_db()
    c.execute(
        'SELECT td.id, td.description, usr.username, td.completed, td.created_at '
        'FROM todo td JOIN user usr ON td.created_by = usr.id '
        'ORDER BY created_at DESC'
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        description = request.form['description']
        error = None

        if description is None:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'INSERT INTO todo (description, completed, created_by) '
                'VALUES (%s, %s, %s)',
                (description, False, g.user['id'])
            )
            db.commit()

            return redirect(url_for('todo.index'))

    return render_template('todo/create.html')


@bp.route('/update', methods=('GET', 'POST'))
@login_required
def update():
    return 'updating'
