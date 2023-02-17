import functools

import flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='')


@bp.route("/auth", methods=('GET', 'POST'))
def auth():
    print(flask.url_for("static", filename="auth.css"))
    return render_template("auth.html")
