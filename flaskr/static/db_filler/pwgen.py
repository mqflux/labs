import names
from flaskr.ponydb import db, db_session, Staff, User, Role, Client, Item
from werkzeug.security import check_password_hash, generate_password_hash
from random import randint

db.bind(provider='mysql', host='localhost', user='root', passwd='admin', db='labs')
db.generate_mapping(create_tables=True)

lss = ["Admin", "Deputy", "Secretary", "Guest"]


@db_session
def create_roles():
    for ls in lss:
        Role(name=ls)


@db_session
def create_users():
    for role in Role.select():
        User(login=role.name.lower(), pwhash=generate_password_hash(role.name.lower()), role=role)


@db_session
def create_clients(n):
    for i in range(n):
        Client(name=names.get_first_name(), money=randint(85, 100) * 1000, credit=0, limit=50000)


@db_session
def create_items():
    items = {
        "Sofa": randint(1, 5) * 1000,
        "Bed": randint(1, 10) * 1000,
        "Cabinet": randint(1, 3) * 1000,
        "Chair": randint(1, 2) * 1000,
        "Clock": randint(1, 5) * 100,
        "Desk": randint(5, 10) * 1000,
        "Table": randint(1, 5) * 1000,
        "Couch": randint(1, 5) * 1000,
        "TV": randint(5, 10) * 1000,
        "Shelf": randint(1, 7) * 100,
    }
    for item in items:
        Item(name=item, stock=randint(100, 500), cost=items[item])


if __name__ == "__main__":
    #create_roles()
    #create_users()
    #create_clients(5)
    create_items()
    pass
