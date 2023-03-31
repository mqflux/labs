import requests
import xml.etree.ElementTree as et
import json
import datetime

from pony.orm import db_session, select
from flaskr.ponydb import *

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

bp = Blueprint('pages', __name__, url_prefix='')


payment_type_enum = {
    0: "Cash",
    1: "Online",
    2: "Credit",
    3: "Barter",
    4: "Offset",
}

def db_view_redirect():
    return render_template("clients.html")


def db_view_staff():
    user = User.get(id=session["user_id"])
    role = user.role.id

    print(request.args.get("name"))

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

        return redirect(url_for("pages.table_view"))

    attributes, users = prepare_table_template(Staff)

    return render_template("db_view.html", attributes=attributes, users=users, role=role, db_name="Staff")


def db_view_client():
    pass


def db_view_item():
    pass


def db_view_order():
    pass


db_view_callbacks = {
    "Staff": db_view_staff,
    "User": db_view_redirect,
    "Role": db_view_redirect,
    "Client": db_view_client,
    "Item": db_view_item,
    "Order": db_view_order,
    "None": db_view_redirect,
}


@bp.route("/db_view", methods=["GET", "POST"])
@db_session
def table_view():
    db_name = request.args.get("name", type=str, default="None")
    user = User.get(id=session["user_id"])
    role = user.role.id

    if db_name not in db_enumerate:
        return db_view_redirect()

    attributes, data = prepare_table_template(db_enumerate[db_name])
    data = [enumerate(item) for item in data]

    if request.method == "POST":
        return db_view_callbacks[db_name]()

    if db_name == "Order":

        _, client_data = prepare_table_template(db_enumerate["Client"])

        return render_template("db_view.html", attributes=attributes, users=data, role=role, db_name=db_name,
                               clients=client_data)

    if db_name == "Client":
        return client_view(role, db_name)

    return render_template("db_view.html", attributes=attributes, users=data, role=role, db_name=db_name)


@db_session
def client_view(role, db_name):
    attributes, data = prepare_table_template(db_enumerate[db_name])

    attributes.append("total_spent")

    for client in data:
        db_client = Client.get(name=client[1])
        total_spent = 0

        db_orders = Order.select(client=db_client)

        for order in db_orders:
            print(order, [i for i in Ordered.select(order=order)])
            total_spent = sum([e.item.cost * e.amount for e in Ordered.select(order=order)])

        client.append(total_spent)

    print(attributes, data)

    data = [enumerate(item) for item in data]

    return render_template("db_view.html", attributes=attributes, users=data, role=role, db_name=db_name)


@db_session
def prepare_table_template(ponyEntity):
    attributes, content, raw_ent = [], [], ponyEntity.select()

    for a in ponyEntity._attrs_:
        attributes.append(a.name)

    #  fix empty attribute
    for i, u in enumerate(raw_ent):

        content.append([])
        dc = u.to_dict()
        for a in attributes:
            if a not in dc:
                attributes.pop(attributes.index(a))
                continue
            content[i].append(dc[a])

    return attributes, content


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


def parse_xml(xml_file, char_code):
    parsed, attrs = [], []
    tree = et.parse(xml_file)
    root = tree.getroot()

    for elem in tree.find('./Valute'):
        attrs.append(elem.tag)

    i = 0
    for elem in root:
        if char_code is not None and elem.find("CharCode").text.lower() != char_code.lower():
            continue
        parsed.append([])

        for attr in attrs:
            parsed[i].append(elem.find(attr).text)

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


@bp.route("/js_db_data/<db_name>", methods=["GET"])
def js_get(db_name):
    attr, data = prepare_table_template(db_enumerate[db_name])
    modified = []

    for i in range(len(data)):
        modified.append({})
        for j in range(len(attr)):
            modified[i][attr[j]] = data[i][j]

    return json.dumps(modified)


@bp.route("/js_create_order", methods=["POST"])
@db_session
def js_post():
    js_data = json.loads(request.form["javascript_data"])
    print(js_data)
    db_client = Client.get(name=js_data["client"])
    db_order = Order(client=db_client, date=datetime.now(), paytype=js_data["payment"])
    resolve_payment(js_data, db_order, db_client)

    return redirect("/index")


def resolve_payment(js_data, order, client):
    if js_data["payment"] == "Cash":
        for item in js_data["items"]:
            amount = int(item["amount"])
            db_item = Item.get(name=item["name"])
            db_item.stock -= amount
            Ordered(item=db_item, amount=amount, order=order)
    elif js_data["payment"] == "Online":
        for item in js_data["items"]:
            amount = int(item["amount"])
            db_item = Item.get(name=item["name"])
            db_item.stock -= amount
            Ordered(item=db_item, amount=amount, order=order)
            client.money -= amount * db_item.cost
    elif js_data["payment"] == "Credit":
        for item in js_data["items"]:
            amount = int(item["amount"])
            db_item = Item.get(name=item["name"])
            db_item.stock -= amount
            Ordered(item=db_item, amount=amount, order=order)
            client.credit += amount * db_item.cost
