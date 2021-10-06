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
        'SELECT td.id, td.description, usr.username, td.completed, td.created_at FROM todo td JOIN user usr ON td.created_by = usr.id ORDER BY created_at DESC'
    )
    todos = c.fetchall()

    return render_template('todo/index.html', todos=todos)
