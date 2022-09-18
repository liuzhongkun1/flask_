#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "requests_tools.py"
__time__ = "2022/9/11 11:00"

import httpx, re
from fake_useragent import UserAgent
from flask import current_app
from random import choice
from aiohttp import ClientSession


class AIResp:
    @staticmethod
    async def get_resp(message):  # 对接口发送请求，获取响应数据
        async with httpx.AsyncClient() as client:
            params = {
                "key": "free",
                "appid": 0,
                "msg": message,
            }
            resp = await client.get("http://api.qingyunke.com/api.php", params=params)
            data = resp.json()
            return data


class ConnectApi:
    """连接接口，创建拓展功能"""

    @staticmethod
    async def get_bing():
        """
        获取bing的每日一图
        :return:
        """
        return "[CQ:image,file=https://www.yuanxiapi.cn/api/bing/,cache=0]"

    @staticmethod
    async def random_img():
        """随机图片获取"""
        return "[CQ:image,file=https://www.yuanxiapi.cn/api/img/,cache=0]"

    @staticmethod
    async def weather(city):
        """天气数据获取"""
        async with httpx.AsyncClient(headers={
            "user-agent": UserAgent().random,
        }) as client:
            resp = await client.get("https://api.wpbom.com/api/weather.php?city=%s" % city)
            data = resp.json()
            try:
                if data["status"] == 1000:
                    # 获取成功
                    city = data["data"]["city"]
                    wea = data["data"]["forecast"][0]
                    high = re.findall(r".*?(?P<tem>\d.*)", wea["high"])[0]
                    low = re.findall(r".*?(?P<tem>\d.*)", wea["low"])[0]
                    type_ = wea["type"]
                    ganmao = data["data"]["ganmao"]
                    ret = f"{city}今日天气{type_}：\n{low}~{high}\n温馨提示：{ganmao}"
                else:
                    raise ValueError
            except Exception as e:
                # 接口获取失败
                ret = f"{city}天气数据获取失败！"
            return ret

    @staticmethod
    async def erciyuan():
        """二次元图片获取"""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get(choice(current_app.config["ACGIMG"]))
            url = resp.url
        return f"[CQ:image,file={url},cache=0]"

    @staticmethod
    async def random_quote():
        """随机一言获取"""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get("https://api.sunweihu.com/api/yan/api.php?charset=utf-8&encode=json")
            if resp.is_success:
                ret = resp.json()["text"]
            else:
                ret = "获取失败！接口出现问题！"
            return ret

    @staticmethod
    async def random_word():
        """段子获取"""
        async with httpx.AsyncClient(follow_redirects=True) as client:
            resp = await client.get("https://yuanxiapi.cn/api/Aword/")
            if resp.is_success:
                ret = resp.json()["duanju"]
            else:
                ret = "获取失败！"
            return ret

    @staticmethod
    async def history():
        """历史的今天的数据获取"""
        async with ClientSession() as session:
            resp = await session.get("https://yuanxiapi.cn/api/history/?format=json")
            r = await resp.json()
        if r.get("code", '300') == '200':
            day = r["day"]
            content = "\n".join([f"{i + 1}. " + k for i, k in enumerate(r["content"])])
            ret = f"{day}\n\n{content}"
        else:
            ret = "获取接口数据失败！"
        return ret

    @staticmethod
    async def video_parser(url, ty):
        # 视频解析接口
        async with httpx.AsyncClient() as client:
            resp = await client.get("https://www.yuanxiapi.cn/api/video/?url=" + url)
            data = resp.json()
            if data["code"] == 200:
                # 说明视频数据获取成功
                video = data["video"]
                title = data["desc"]
                source = data["name"]
                cover = data["cover"]
                msg = f"视频解析完成\n\n视频来源: {source}\n视频标题: {title}\n下载链接: {video}"
                msg += f"\n[CQ:image,file={cover},type=show,id=40004]" if ty == "private" else ""
            else:
                msg = f"视频解析失败，请输入正确的url."
            return msg

    @staticmethod
    async def poem():
        # 获取随机一句诗接口
        async with httpx.AsyncClient() as client:
            ret = await client.get("https://v2.jinrishici.com/token")
            data = ret.json()
            if data.get("status") == "success":
                token = data["data"]
            else:
                return "获取失败，请重新尝试！"
            headers = {
                "X-User-Token": token
            }
            ret = await client.get("https://v2.jinrishici.com/sentence", headers=headers)
            data = ret.json()
            if data.get("status") == "success":
                content = data["data"]["content"]
                return content
            else:
                return "获取失败，请重新尝试！"

    @staticmethod
    async def quote():
        # 获取人生语录接口
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get("http://api.zhaoge.fun/api/rshy.php")
                sten = resp.text.split()[2]
                return sten
            except Exception as e:
                return "获取失败，请重新尝试"

    @staticmethod
    async def epidemic(city):
        # 获取疫情数据接口
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"http://api.zhaoge.fun/api/yq.php?msg={city}")
            ret = resp.text.split()
            return "\n".join(ret[2: 8])

    @staticmethod
    async def cale():
        # 获取日历接口
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://api.zhaoge.fun/api/nl.php")
            ret = resp.text.split("━━━━━━━━━")
            return ret[1].strip()

    @staticmethod
    async def get_help():
        # 获取帮助文档
        return "[CQ:image,file=file:///root/bot/code/App/static/总帮助文档.jpg,cache=0]"

    @staticmethod
    async def brief():
        # 获取每日简报
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://bjb.yunwj.top/php/tp/lj.php")
            url = re.findall('"tp":"(?P<url>.*?)"', resp.text)[0]
            return f"[CQ:image,file={url},cache=0]"


class Sender:
    @staticmethod
    async def send(id, message, ty):
        """
        用于发送消息的函数
        :param id: qq号，或者qq群号
        :param message: 发送的消息
        :param ty: 传入的
        :return: None
        """
        async with httpx.AsyncClient(base_url="http://127.0.0.1:5700") as client:
            # 如果发送的为私聊消息
            params = {
                "message_type": ty,
                "group_id" if ty == "group" else "user_id": id,
                "message": message,
            }
            await client.get("/send_msg", params=params)
