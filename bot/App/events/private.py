#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "private.py.py"
__time__ = "2022/9/9 22:04"

from App.script import AIResp, Sender
from App.script import Filter
from App.events.groupAndPri import Command


class PriChatMes:
    @staticmethod
    async def handle_private(resp):  # 处理私聊信息
        uid = resp["sender"]["user_id"]  # 获取发信息的好友qq号
        message = resp["raw_message"]  # 获取发送过来的消息
        if message:  # 简单的判断，只是判断其是否为空
            if message.startswith("/"):
                """如果是发过来的命令信息"""
                await Command.command(resp, "private")
                return
            _ = await AIResp.get_resp(message)
            ret = _.get("content", "获取回复失败")
            await Sender.send(uid, Filter.sensitive_filter(ret), "private")



