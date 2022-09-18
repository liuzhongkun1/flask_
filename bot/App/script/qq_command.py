#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "qq_command.py"
__time__ = "2022/9/11 23:17"

from flask import current_app
from App.models import Group, GroupAuthority
from base64 import b64decode


class Super:
    @staticmethod
    async def add(gid, nick):
        session = current_app.config["db"].session
        data = session.query(Group).filter_by(qqId=gid).first()
        if data is None:
            g = Group(nick, gid)
            g.group2auth = GroupAuthority()
            session.add(g)
            session.commit()  # 提交事务
            return {
                "status": 200
            }
        data.isDetect = True
        data.name = nick
        session.commit()
        return {
            "status": 300,
            "error": "该群号已存在！",
        }

    @staticmethod
    async def close(gid):
        db = current_app.config["db"]
        session = db.session
        group = session.query(Group).filter(db.and_(Group.qqId == gid, Group.isDetect)).first()
        if group:
            group.isDetect = False
            session.commit()
        return "该群关闭成功"

    @staticmethod
    async def delete(gid):
        db = current_app.config["db"]
        session = db.session
        group = session.query(Group).filter(Group.qqId == gid).first()
        if group:
            session.delete(group.group2auth)
            session.delete(group)
            session.commit()
        return "该群已从数据库中删除"

    @staticmethod
    async def show():
        session = current_app.config["db"].session
        data = [f"|{b64decode(i.name).decode()} :: {i.qqId} :: {'yes' if i.isDetect else 'no'} |" for i in
                session.query(Group).all()]
        return "\n".join(data)


class Admin:
    @staticmethod
    async def changeAuth(gid, data, ty):
        db = current_app.config["db"]
        session = db.session
        try:
            for i in data:
                if int(i) not in [0, 1] or len(data) != 6:
                    raise ValueError
            data = (int(i) for i in data)
            group = session.query(Group).filter(db.and_(Group.qqId == gid, Group.isDetect)).first()
            if group:
                session.delete(group.group2auth)
                group.group2auth = GroupAuthority(True, *data)
                session.commit()
                _ = await Admin.get(gid)
                ret = f"[CQ:at,qq=%d]设置成功，设置后的权限为：\n{_}" if ty == "group" else f"设置成功，设置后的权限为：\n{_}"
            else:
                ret = "该群不支持机器人"
        except Exception as e:
            ret = "[CQ:at,qq=%d]设置失败，请查看帮助文档！" if ty == "group" else "设置失败，请查看帮助文档！"
        return ret

    @staticmethod
    async def get(gid):
        db = current_app.config["db"]
        session = db.session
        data = session.query(Group).filter(db.and_(Group.qqId == gid, Group.isDetect)).first()
        if data is None:
            return "在该群不支持，请与开发者联系！"
        name = b64decode(data.name).decode()  # qq群名称
        chat = "1. 已开启聊天功能" if data.group2auth.chat else "1. 未开启聊天功能"  # 有没有开启智能聊天的功能
        welcome = "2. 已开启入群欢迎功能" if data.group2auth.welcome else "2. 未开启入群欢迎功能"  # 是否开启入群欢迎的功能
        banTalk = "3. 已开启管理群功能" if data.group2auth.banTalk else "3. 未开启管理群功能"  # 是否开启管理员的功能
        click = "4. 已开启戳一戳功能" if data.group2auth.click else "4. 未开启戳一戳功能"  # 戳一戳功能
        smallFunction = "5. 已开启拓展功能" if data.group2auth.smallFunction else "5. 未开启拓展功能"  # 是否开启小功能
        dailyBrief = "6. 已开启定时发消息功能" if data.group2auth.dailyBrief else "6. 未开启定时发消息功能"  # 是否开启每日自动播报的功能
        return f"{name}\n{chat}\n{welcome}\n{banTalk}\n{click}\n{smallFunction}\n{dailyBrief}\n"


class Common:
    pass
