#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "exts.py"
__time__ = "2022/9/11 23:39"

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()  # 操作数据库


def init_exts(app):
    db.init_app(app)
    Migrate().init_app(app, db)  # 使用app初始化Migrate
    app.config["db"] = db
