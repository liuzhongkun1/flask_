# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "test.py"
__time__ = "2022/7/9 21:23"

from flask import Blueprint, url_for, redirect
from flaskApp.models import Foo
from flaskApp import db

te = Blueprint("te", __name__)

from . import api_te


@te.route("/index")
def index():
    """则，这里只要关注返回页面的请求，返回数据交给restful去处理"""
    return redirect(url_for("te.operateData"))  # 这里就只是进行一个简单的模拟，进行重定向访问，实际开发中可以使用Ajax异步请求


@te.route("/add")
def search():
    """这里为了方便，我们使用add路由来添加数据"""
    db.session.add(Foo(1, "李华", 23))
    db.session.commit()
    db.session.remove()
    return "success"
