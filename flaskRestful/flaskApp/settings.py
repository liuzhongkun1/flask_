# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "settings.py"
__time__ = "2022/7/9 19:40"


class Basic():
    """编写配置文件"""
    DEBUG = True
    # 连接数据的URI
    DB_URI = "sqlite:///app.db"
    SQLALCHEMY_DATABASE_URI = DB_URI  # 使用sqlachemy

    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SWAGGER_TITLE = "API"
    SWAGGER_DESC = "API接口"
    # 地址，必须带上端口号
    SWAGGER_HOST = "localhost:5000"


class Product():
    pass
