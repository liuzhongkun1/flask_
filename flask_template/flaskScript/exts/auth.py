from flask import request, session, redirect


class Auth:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.auto = self  # 将这个类的信息全部写入app里面
        self.app = app
        self.app.before_request(self.check_login)

    def check_login(self):
        usr = session.get("usr")
        print(usr)

    def login(self, data):
        """创建session"""
        session["usr"] = data

    def login_out(self):
        """用户登出"""
        del session["usr"]