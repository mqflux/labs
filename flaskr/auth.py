import functools
from pony.orm import db_session
from flaskr.ponydb import db, User, Staff, create_account

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='')


@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        print(request.form.to_dict())
        username = request.form['username']
        password = request.form['password']
        error = None

        with db_session:
            entity = User.get(login=username)

        if entity is None:
            error = 'Incorrect username.'
        elif not check_password_hash(entity.pwhash, password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session["user_id"] = entity.id
            print(url_for("pages.db_view"))
            return redirect(url_for("pages.db_view"))

        flash(error)

    return render_template("login.html")


@bp.route("/register", methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        print(request.form.to_dict())
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                with db_session:
                    User(login=username, pwhash=generate_password_hash(password))
            except Exception:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

    return render_template("register.html")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with db_session:
            g.user = User.get(id=user_id)


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('hello'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
