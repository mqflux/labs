from werkzeug.security import generate_password_hash
from datetime import datetime
from pony.orm import *


db = Database()


class Staff(db.Entity):
    id = PrimaryKey(int, auto=True)
    role = Required(str)  # Role in the company
    fname = Required(str)  # First name
    sname = Required(str)  # Surname
    raddr = Optional(str)  # Residential address
    tnumber = Optional(str)  # Telephone number of user


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    login = Required(str, unique=True)
    pwhash = Required(str, unique=True)
    roleID = Optional(str)
    role = Required('Role')


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    users = Set(User)


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    money = Optional(float)
    limit = Optional(float)  # Credit limit
    credit = Optional(float)  # Current client's credit
    comment = Optional(LongStr)
    orders = Set('Order')


class Item(db.Entity):
    id = PrimaryKey(int, auto=True)
    stock = Optional(int)
    name = Optional(str)
    cost = Optional(float)
    orders = Set('Order')


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Optional(int)
    date = Optional(datetime)
    item = Required(Item)
    client = Required(Client)
    paytype = Optional(str)


@db_session
def create_account(login, password, bound_staff_id=None):

    hashed = generate_password_hash(password)

    if bound_staff_id is None:
        User(login=login, pwhash=hashed)
    else:
        User(login=login, pwhash=hashed, staffID=bound_staff_id)


db_enumerate = {
    "Staff": Staff,
    "User": User,
    "Role": Role,
    "Client": Client,
    "Item": Item,
    "Order": Order
}