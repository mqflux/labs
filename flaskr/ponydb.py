from pony.orm import *

db = Database()
db.bind(provider='mysql', host='localhost', user='root', passwd='admin', db='labs')


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


db.generate_mapping(create_tables=True)