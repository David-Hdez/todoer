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


@bp.route('/create', methods=['GET', 'POST'])
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


def get_todo(id):
    db, c = get_db()
    c.execute(
        'SELECT td.id, td.description, td.completed, td.created_by, td.created_at, usr.username '
        'FROM todo td JOIN user usr ON td.created_by = usr.id WHERE usr.id = %s',
        (id,)
    )

    todo = c.fetchone()

    if todo is None:
        abort(404, "Todo con identificador {0} no existe".format(id))

    return todo


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    todo = get_todo(id)

    if request.method == 'POST':
        description = request.form['description']
        # checkbox from form
        completed = True if request.form.get('completed') == 'on' else False
        error = None

        if not description:
            error = 'Description is required.'

        if error is not None:
            flash(error)
        else:
            db, c = get_db()
            c.execute(
                'UPDATE todo SET description = %s, completed = %s '
                'WHERE id = %s',
                (description, completed, id)
            )
            db.commit()

            return redirect(url_for('todo.index'))

    return render_template('todo/update.html', todo=todo)


@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete():
    return 'deleted'
