from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bootstrap import Bootstrap

from flaskext.uploads import configure_uploads, UploadSet, IMAGES


from sqlalchemy import event
from .listeners import receive_before_delete


db = SQLAlchemy()
lm = LoginManager()
bootstrap = Bootstrap()
lm.login_view = 'auth.login'

images = UploadSet('images', IMAGES)


from .models import Item


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    bootstrap.init_app(app)
    db.init_app(app)
    lm.init_app(app)

    configure_uploads(app, images)

    event.listen(Item, 'before_delete', receive_before_delete)

    from .main import main
    app.register_blueprint(main)
    from .auth import auth
    app.register_blueprint(auth)

    return app
