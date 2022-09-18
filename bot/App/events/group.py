#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "group.py"
__time__ = "2022/9/10 11:49"

from App.script import AIResp, Sender, Filter
from flask import current_app


class GroupChatMes:
    @staticmethod
    async def handle_group(resp):
        message = resp["raw_message"].replace("[CQ:at,qq=2786631176]", "")  # 获取发送过来的消息
        gid = resp["group_id"]  # 获取发送消息的群号
        # 处理群聊信息
        if message.strip() == "":
            await Sender.send(gid, "艾特我干啥？又不发消息，一巴掌呼死你！[CQ:face,id=86][CQ:face,id=12]", "group")
        else:
            _ = await AIResp.get_resp(message)
            ret = _.get("content", "获取回复失败")
            await Sender.send(gid, Filter.sensitive_filter(ret), "group")

    @staticmethod
    async def group_increase(resp):
        uid = resp["user_id"]  # 获取加入者的qq
        gid = resp["group_id"]  # 获取群号
        # 处理有新成员加入的情况
        welcome_group = current_app.config.get("WELCOME_MES")
        msg = welcome_group.get(str(gid),
                                welcome_group["default"]) % uid  # welcome_group的键是qq群号，值是欢迎语
        await Sender.send(gid, msg, "group")  # 发送信息
