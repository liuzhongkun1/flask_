# ！/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "app.py"
__time__ = "2022/7/9 21:21"
from flaskApp import create_app, db
from flask_script import Manager
from flask_migrate import Migrate

app = create_app()
manage = Manager(app)
Migrate(app, db)

if __name__ == '__main__':
    manage.run()
