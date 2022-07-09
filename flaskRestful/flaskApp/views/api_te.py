# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "api_te.py"
__time__ = "2022/7/9 21:52"

from flask import request, jsonify
from .test import te
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flaskApp import db
from flaskApp.models import Foo
from flaskApp.tools import HttpCode

api = Api(te)


def restful_result(code, message, data):
    return jsonify({"code": code, "message": message, "data": data or {}})


def success(message="", data=None):
    """
    正确返回
    :return:
    """
    return restful_result(code=HttpCode.ok, message=message, data=data)


class FooListApi(Resource):
    # 定义要返回的字段
    resource_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'age': fields.String
    }

    # 装饰器，定义返回数据
    @marshal_with(resource_fields)
    def get(self):
        """
        返回所有记录
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='args', help='必须输入姓名')  # 注意，如果添加了parser参数解析，则，返回数据需要是JSON数据
        arg = parser.parse_args()
        print(arg)
        # http://127.0.0.1:5000/api/v1/foo?name=1&a=2  终端输出: {'name': '1'}

        # 查询数据库
        foos = db.session.query(Foo).all()
        return {
            "data": foos,
            "status": HttpCode.ok
        }

    def post(self):
        """
        创建一条记录
        :return:
        """
        # 参数
        params = request.get_json()
        name = params.get("name")
        age = params.get("age")
        # 构建一个模型
        foo = Foo(name=name, age=age)

        # 加入到数据库
        db.session.add(foo)
        db.session.commit()

        return success("新增一条记录成功！")


# 所有记录
api.add_resource(FooListApi, '/api/v1/foo', endpoint="operateData")  # 返回数据
