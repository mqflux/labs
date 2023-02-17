import os

from flask import Flask
from flaskr.ponydb import db


# flask --app flaskr run --debug
# to start the server


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    db.bind(provider='mysql', host='localhost', user='root', passwd='admin', db='labs')
    db.generate_mapping(create_tables=True)

    from . import auth, pages
    app.register_blueprint(auth.bp)
    app.register_blueprint(pages.bp)

    return app
