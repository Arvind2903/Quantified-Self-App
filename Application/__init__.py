from flask import Flask
from .views import *
from .auth import *
from os import path
from .config import LocalDevelopmentConfig
from flask_login import LoginManager
from .database import db

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    if not path.exists('Application/' + DB_NAME):
        db.create_all(app=app)
