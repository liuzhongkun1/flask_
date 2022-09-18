#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "models.py"
__time__ = "2022/9/11 19:56"

from App.exts import db


class Group(db.Model):  # 创建一个群的表
    __tablename__ = "group"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=True)
    qqId = db.Column(db.String(20), nullable=False, unique=True, index=True)
    isDetect = db.Column(db.BOOLEAN, default=True)  # 是否开启
    auth = db.Column(db.SmallInteger, default=0)  # 在群里面的的地位，默认为群成员，1为管理员，2为群主

    def __init__(self, name, qqId):
        self.name = name
        self.qqId = qqId


class GroupAuthority(db.Model):  # 创建一个权限管理表
    __tablename__ = "groupAuth"
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    chat = db.Column(db.INTEGER, default=0, nullable=False)  # 是否开启智能聊天的功能
    welcome = db.Column(db.INTEGER, default=1, nullable=False)  # 是否开启新成员入群欢迎的功能
    banTalk = db.Column(db.INTEGER, default=0)  # 群禁言功能，以及消息撤回功能
    click = db.Column(db.INTEGER, default=1)  # 戳一戳功能，默认开启
    smallFunction = db.Column(db.INTEGER, default=1)  # 是否开启小功能，如疫情数据查询等
    dailyBrief = db.Column(db.INTEGER, default=0)  # 是否开启每日简报功能
    groupId = db.Column(db.INTEGER, db.ForeignKey("group.id", ondelete="CASCADE"), nullable=False)  # 外键约束，同时进行级联删除
    auth2group = db.relationship("Group", backref=db.backref("group2auth", uselist=False))  # 使用代理

    def __init__(self, is_privade=False, chat=None, welcome=None, bantalk=None, click=None, smallFunction=None,
                 dailyBrief=None):
        if is_privade:
            self.chat = chat
            self.welcome = welcome
            self.banTalk = bantalk
            self.click = click
            self.smallFunction = smallFunction
            self.dailyBrief = dailyBrief
