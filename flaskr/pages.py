import requests
import xml.etree.ElementTree as et
import os
import datetime

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


@bp.route("/currencies", methods=("GET", "POST"))
def currencies():
    table_head = ["Num code", "Char code", "Unit", "Currency", "Rate"]
    date = datetime.date.today()
    char_code = None
    str_date = f"{(date.day - 1):02d}/{date.month:02d}/{date.year}"

    print(str_date)

    url = f"https://cbr.ru/scripts/XML_daily_eng.asp?date_req={str_date}"

    if request.method == "POST":
        print(request.form.to_dict())
        char_code = request.form["char_code"]
        if len(char_code) == 0:
            char_code = None

    if load_currency_info(url):
        parsed = parse_xml(f"./flaskr{url_for('static', filename='currency_info.xml')}", char_code)
    else:
        return redirect(url_for("bp.index"))

    return render_template("currencies.html", attributes=table_head, currencies=parsed, date=str_date)


@bp.route("/clients", methods=("GET", "POST"))
def client_search():
    pass


@bp.route("/items", methods=("GET", "POST"))
def item_stock():
    pass


@bp.route("/createorder", methods=("GET", "POST"))
def new_order():
    pass


def parse_xml(xml_file, char_code):
    parsed, attrs = [], []
    tree = et.parse(xml_file)
    root = tree.getroot()

    for elem in tree.find('./Valute'):
        attrs.append(elem.tag)

    print(attrs)

    i = 0
    for elem in root:
        if char_code is not None and elem.find("CharCode").text.lower() != char_code.lower():
            continue
        parsed.append([])

        for attr in attrs:
            parsed[i].append(elem.find(attr).text)
        print(parsed[i])

        i += 1

    return parsed


def load_currency_info(url):
    success = True

    response = requests.get(url)
    if response.status_code == 200:
        content = response.content
    else:
        return False

    with open(f"./flaskr{url_for('static', filename='currency_info.xml')}", 'wb+') as file:
        file.write(content)

    return success
