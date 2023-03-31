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
    role = Required('Role')


class Role(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    users = Set(User)


class Client(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Optional(str)
    money = Optional(float)
    limit = Optional(float)  # Credit limit
    credit = Optional(float)  # Current client's credit
    comment = Optional(LongStr)
    orders = Set('Order')


class Item(db.Entity):
    id = PrimaryKey(int, auto=True)
    stock = Optional(int)
    name = Required(str, unique=True)
    cost = Optional(float)
    ordereds = Set('Ordered')


class Order(db.Entity):
    id = PrimaryKey(int, auto=True)
    date = Optional(datetime)
    client = Required(Client)
    paytype = Optional(str)
    ordereds = Set('Ordered')


class Ordered(db.Entity):
    id = PrimaryKey(int, auto=True)
    amount = Optional(int)
    item = Required(Item)
    order = Required(Order)


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
    "Order": Order,
    "Ordered": Ordered
}