#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "groupAndPri.py"
__time__ = "2022/9/11 20:08"

import re
from flask import current_app
from random import choice
from App.script import Super, Admin, Common, ConnectApi, Sender
from base64 import b64encode
from App.models import Group


class GroupAndPri:
    @staticmethod
    async def click_event(resp):
        uid = resp["user_id"]
        tid = resp["target_id"]
        if str(tid) != "3500515050" and str(tid) != "2786631176":  # 如果不是这两个账号的戳一戳，则不管
            return
        try:
            gid = resp["group_id"]
            db = current_app.config["db"]
            session = db.session
            group = session.query(Group).filter(db.and_(Group.qqId == gid, Group.isDetect)).first()
        except KeyError as e:
            gid = None
            group = None

        # 处理戳一戳的消息
        info = choice(current_app.config.get("CLICK_MES"))  # 获取戳一戳的信息
        try:
            info = info % uid
        except Exception as e:
            if gid:  # 说明其为群戳戳
                info = f"[CQ:at,qq={uid}]" + info
        if gid is None:
            await Sender.send(uid, info, "private")
        elif gid and group.group2auth.click:  # 如果允许聊天的话，就在群内开启聊天功能
            await Sender.send(gid, info, "group")


class Command:
    @staticmethod
    async def super_command(uid, message):  # 处理开发者的命令
        com_1 = re.findall(r"/admin:(.*)", message.split()[0])[0]
        try:
            com_2 = message.split()[1]  # qq群号
        except Exception as e:
            com_2 = None
        if com_1 == "add" and com_2.isdecimal():  # 这说明其为添加qq群
            com_3 = message.split()[2]  # qq昵称
            ret = await Super.add(com_2, b64encode(com_3.encode()))
            if ret["status"] == 200:
                await Sender.send(uid, f"{com_2}添加成功，该群名为{com_3}", "private")
            else:
                await Sender.send(uid, ret["error"], "private")
        elif com_1 == "get" and com_2.isdecimal():
            ret = await Admin.get(com_2)
            await Sender.send(uid, ret, ty="private")
        elif com_1 == "close" and com_2.isdecimal():
            ret = await Super.close(com_2)
            await Sender.send(uid, ret, ty="private")
        elif com_1 == "delete" and com_2.isdecimal():
            ret = await Super.delete(com_2)
            await Sender.send(uid, ret, ty="private")
        elif com_1 == "changeAuth" and com_2.isdecimal():
            data = list(message.split()[2])
            ret = await Admin.changeAuth(com_2, data, "private")
            await Sender.send(uid, ret, "private")
        elif com_1 == "show":
            ret = await Super.show()
            await Sender.send(uid, ret, "private")
        else:
            ret = await ConnectApi.get_help()
            await Sender.send(uid, ret, "private")

    @staticmethod
    async def com_command(id, message, ty, resp):  # 处理一般的命令
        uid = resp["sender"]["user_id"]
        base = "[CQ:at,qq=" + str(uid) + "]" if ty == 'group' else ""
        command = re.findall(r"/(.*)", message.split()[0])[0]  # 先获取一个类似函数的命令，作为启动
        if command == "bing":
            msg = await ConnectApi.get_bing()
            await Sender.send(id, msg, ty)
        elif command == "天气":
            if len(message.split()) != 2:
                await Sender.send(id, "输入格式错误，请根据帮助文档输入！", ty)
                return
            city = message.split()[1]
            msg = await ConnectApi.weather(city)
            await Sender.send(id, msg, ty)
        elif command == "send":
            if len(message.split()) < 2:
                await Sender.send(id, "输入格式错误，请根据帮助文档输入！", ty)
                return
            content = "\n".join(message.split()[1:]) + f"\n——{uid}"
            await Sender.send(current_app.config["ADMIN"], content, "private")
            await Sender.send(id, base + "收到，谢谢您的建议！[CQ:face,id=63][CQ:face,id=63][CQ:face,id=63]", ty)
        elif command == "随机图片":
            msg = await ConnectApi.random_img()
            await Sender.send(id, msg, ty)
        elif command == "二次元":
            msg = await ConnectApi.erciyuan()
            await Sender.send(id, msg, ty)
        elif command == "随机一言":
            msg = await ConnectApi.random_quote()
            await Sender.send(id, msg, ty)
        elif command == "段子":
            msg = await ConnectApi.random_word()
            await Sender.send(id, msg, ty)
        elif command == "历史":
            msg = await ConnectApi.history()
            await Sender.send(id, msg, ty)
        elif command == "诗词":
            msg = await ConnectApi.poem()
            await Sender.send(id, msg, ty)
        elif command == "短视频":
            if len(message.split()) != 2:
                await Sender.send(id, "输入格式错误，请根据帮助文档输入！", ty)
                return
            url = message.split()[1]
            msg = await ConnectApi.video_parser(url, ty)
            await Sender.send(id, base + msg, ty)
        elif command == "人生语录":
            msg = await ConnectApi.quote()
            await Sender.send(id, msg, ty)
        elif command == "疫情":
            try:
                city = message.split()[1]
            except Exception as e:
                await Sender.send(id, "输入格式错误，请按照帮助文档输入！", ty)
                return
            msg = await ConnectApi.epidemic(city)
            await Sender.send(id, msg, ty)
        elif command == "农历":
            msg = await ConnectApi.cale()
            await Sender.send(id, msg, ty)
        elif command == "简报":  # 获取每日简报
            msg = await ConnectApi.brief()
            await Sender.send(id, msg, ty)
        else:
            msg = await ConnectApi.get_help()
            await Sender.send(id, msg, ty)

    @staticmethod
    async def admin_command(uid, gid, message):  # 群管理员命令
        com_1 = re.findall(r"/admin:(.*)", message.split()[0])[0]
        if com_1 == "get":
            ret = await Admin.get(gid)
            await Sender.send(gid, ret, ty="group")
        elif com_1 == "change":
            try:
                data = list(message.split()[1])
                ret = await Admin.changeAuth(gid, data, "group")
            except Exception as e:
                ret = "格式错误，请查看帮助文档"
            await Sender.send(gid, ret % uid, "group")
        else:
            ret = await ConnectApi.get_help()
            await Sender.send(gid, ret, "group")

    @staticmethod
    async def command(resp, ty, isornot=None):  # 对命令进行分类
        """
        对所有命令进行处理
        :param resp: post的数据
        :param ty: 消息来自哪里
        :param isornot: 当为群消息时，要传入是否支持拓展功能
        :return:
        """
        uid = resp["sender"]["user_id"]  # 获取发信息的好友qq号
        message = resp["raw_message"]  # 获取发送过来的消息
        if ty == "group":
            gid = resp["group_id"]  # 获取群号
        else:
            gid = None
        if message.startswith("/admin:"):
            """管理系统的命令"""
            if str(uid) in current_app.config["SUPER_USER"] and ty == "private":
                await Command.super_command(uid, message)
            elif ty == "group" and resp["sender"]["role"] in ["owner", "admin"]:
                # 说明这个是群管理员的修改
                await Command.admin_command(uid, gid, message)
            else:
                await Sender.send(uid if ty == "private" else gid, "权限不足！", ty)
        else:
            if isornot or ty == "private":  # 查看是否开启这个功能
                """管理拓展功能的命令"""
                await Command.com_command(uid if gid is None else gid, message, ty, resp)
            else:
                await Sender.send(resp["group_id"], "本群没有开启拓展功能哦！请联系管理员开启这个功能！", "group")
