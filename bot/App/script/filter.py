#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "filter.py"
__time__ = "2022/9/11 11:02"

import re


class Filter:
    @staticmethod
    def sensitive_filter(message):
        message = message.replace("{br}", "\n").replace("菲菲", "小透明")  # 进行替换
        if "爸爸" in message:
            return "获取回答失败，请换一个问题！"
        # 进行表情的过滤
        ids = re.findall(r"{face:(?P<ID>\d+)}", message)
        for i in ids:
            message = message.replace("{face:%s}" % i, f"[CQ:face,id={i}]")
        return message



