from pony.orm import db_session
from flaskr.ponydb import db, User, Staff

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('pages', __name__, url_prefix='')


@bp.route("/db_view", methods=["GET", "POST"])
def db_view():

    return render_template("db_view.html")


@bp.route("/")
def index():
    return render_template("wrapper.html")

