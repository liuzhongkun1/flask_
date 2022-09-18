#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "__init__.py.py"
__time__ = "2022/9/11 14:25"

from flask import Flask
from App.settings import envs
from App.views import init_app
from App.exts import init_exts


# from App.models import *  # 注意，这里需要导入啊，不然无法创建对应的表，同时，到后面运行时，需要把这行注释调，不然无法运行

def create_app(env):
    app = Flask(__name__)
    app.config.from_object(envs.get(env))
    init_exts(app)
    init_app(app)  # 将路由传入app中
    return app
