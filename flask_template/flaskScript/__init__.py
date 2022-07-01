from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .exts.auth import Auth

at = Auth()

db = SQLAlchemy()

from .views.account import ac
from .views.home import hm




def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("settings.py")

    app.register_blueprint(ac)
    app.register_blueprint(hm)
    db.init_app(app)
    at.init_app(app)
    return app
