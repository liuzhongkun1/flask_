# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "__init__.py"
__time__ = "2022/7/9 21:20"

from flask import Flask
from . import settings
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .views.test import te


def create_app():
    app = Flask(__name__)
    app.register_blueprint(te)
    app.config.from_object(settings.Basic)
    db.init_app(app)
    return app
