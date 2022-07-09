# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "models.py"
__time__ = "2022/7/9 21:32"

from . import db


class Foo(db.Model):
    """
    模型，将映射到数据库表中
    """
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age

    __tablename__ = 'foo'
    # 主键ID
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 名字
    name = db.Column(db.String(100), nullable=False)
    # 年龄
    age = db.Column(db.INTEGER)
