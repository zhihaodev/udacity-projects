from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    from .main import main
    app.register_blueprint(main)

    return app