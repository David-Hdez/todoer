import functools
# flash: enviar mensajes a las plantillas
from flask import (
    Blueprint, flash, g, render_template, request, url_for, session, redirect
)
from werkzeug.security import check_password_hash, generate_password_hash
from todo.db import get_db

# Blueprint is a way to organize a group of related views and other code.
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None

        c.execute(
            "SELECT id FROM user WHERE username = %s", (username,)
        )

        if not username:
            error = 'Username is required.'
        if not password:
            error = 'Password is required.'
        elif c.fetchone() is not None:
            error = 'User {} is registered'.format(username)

        if error is None:
            c.execute(
                "INSERT INTO user (username, password) VALUES (%s, %s)",
                (username, generate_password_hash(password)),
            )
            db.commit()

            return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db, c = get_db()
        error = None
        c.execute(
            'SELECT * FROM user WHERE username = %s', (username,)
        )
        user = c.fetchone()

        if user is None:
            error = 'Incorrect username and/or password.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect username and/or password..'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('todo.index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        db, c = get_db()
        c.execute(
            'SELECT * FROM user WHERE id = %s', (user_id,)
        )
        # fetchone() return first element
        g.user = c.fetchone()


# Funcion decoradora
# Recibe como argumento una función
def login_required(view):
    """
    Protegiendo rutas
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            # Usuario no ha iniciado sesión
            redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
