from pony.orm import *
from werkzeug.security import generate_password_hash


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
    staffID = Optional(str)  # ID of staff which uses this account


@db_session
def create_account(login, password, bound_staff_id=None):

    hashed = generate_password_hash(password)

    if bound_staff_id is None:
        User(login=login, pwhash=hashed)
    else:
        User(login=login, pwhash=hashed, staffID=bound_staff_id)
