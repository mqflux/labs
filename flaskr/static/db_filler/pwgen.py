from flaskr.ponydb import db, db_session, Staff, User, Role
from werkzeug.security import check_password_hash, generate_password_hash

db.bind(provider='mysql', host='localhost', user='root', passwd='admin', db='labs')
db.generate_mapping(create_tables=True)

lss = ["Admin", "Deputy", "Secretary", "Guest"]

with db_session:
    for ls in lss:
        Role(name=ls)