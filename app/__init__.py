from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

db = SQLAlchemy()
lm = LoginManager()
bootstrap = Bootstrap()
lm.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)
    
    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth)

    return app