#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "__init__.py.py"
__time__ = "2022/9/11 19:30"

from App.views.goCqhttp import AcceptMes
from flask_restful import Api


def init_app(app):
    api = Api(app)
    api.add_resource(AcceptMes, "/", endpoint="index")
