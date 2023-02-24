from pony.orm import db_session, select
from flaskr.ponydb import db, User, Staff, Role

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('pages', __name__, url_prefix='')


@bp.route("/db_view", methods=["GET", "POST"])
@db_session
def db_view():
    user = User.get(id=session["user_id"])
    role = user.role.id
    if request.method == "POST":
        req_dict = request.form.to_dict()

        staff = Staff.get(id=req_dict["id"])

        print(req_dict)
        if staff is None:
            role = req_dict["role"]
            fname = req_dict["fname"]
            sname = req_dict["sname"]
            raddr = req_dict["raddr"]
            tnumber = req_dict["tnumber"]
            Staff(role=role, fname=fname, sname=sname, raddr=raddr, tnumber=tnumber)
        else:
            staff.set(**req_dict)

        return redirect( url_for("pages.db_view"))


    attributes, users = prepare_table_template(Staff)

    return render_template("db_view.html", attributes=attributes, users=users, role=role)


@db_session
def prepare_table_template(ponyEntity):
    attributes, users = [], []

    for a in ponyEntity._attrs_:
        attributes.append(a.name)

    attributes = attributes

    for i, u in enumerate(ponyEntity.select()):
        users.append([])
        dc = u.to_dict()
        for a in attributes:
            users[i].append(dc[a])
        users[i] = enumerate(users[i])

    return attributes, users


@bp.route("/")
def index():
    return render_template("wrapper.html")

