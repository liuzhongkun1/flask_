#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "app.py"
__time__ = "2022/9/11 19:17"

from App import create_app
from flask_script import Manager

app = create_app("develop")
manage = Manager(app)

if __name__ == '__main__':
    manage.run()
