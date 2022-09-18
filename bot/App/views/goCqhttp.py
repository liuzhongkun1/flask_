# !/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "goCqhttp.py"
__time__ = "2022/9/11 19:57"

from flask_restful import Resource
from flask import request
import asyncio
from App.events.private import PriChatMes
from App.events.group import GroupChatMes
from App.events.groupAndPri import GroupAndPri
from flask import current_app
from App.models import Group
from App.events.groupAndPri import Command


class AcceptMes(Resource):

    def post(self):
        # 这里对消息进行分发，暂时先设置一个简单的分发
        _ = request.json
        if _.get("message_type") == "private":  # 说明有好友发送信息过来
            asyncio.run(PriChatMes.handle_private(_))  # 处理私聊的信息
        elif _.get("message_type") == "group" and "[CQ:at,qq=2786631176]" in _["raw_message"]:
            # 制作群聊消息
            db = current_app.config["db"]
            session = db.session
            group = session.query(Group).filter(db.and_(Group.qqId == _["group_id"], Group.isDetect)).first()
            if group and group.group2auth.chat:  # 如果允许聊天的话，就在群内开启聊天功能
                asyncio.run(GroupChatMes.handle_group(_))

        elif _.get("message_type") == "group":
            # 获取群命令
            db = current_app.config["db"]
            session = db.session
            group = session.query(Group).filter(db.and_(Group.qqId == _["group_id"], Group.isDetect)).first()
            if not group:
                return
            message = _.get("raw_message")
            if message.startswith("/"):
                asyncio.run(Command.command(_, "group", group.group2auth.smallFunction))

        elif _.get("notice_type") == "group_increase":
            # 有新成员加入
            db = current_app.config["db"]
            session = db.session
            group = session.query(Group).filter(db.and_(Group.qqId == _["group_id"], Group.isDetect)).first()
            if group and group.group2auth.welcome:  # 如果允许聊天的话，就在群内开启聊天功能
                asyncio.run(GroupChatMes.group_increase(_))  # 发送欢迎语

        elif _.get("sub_type") == "poke":
            # 如果事件类型为戳一戳
            asyncio.run(GroupAndPri.click_event(_))
