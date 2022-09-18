#!/usr/bin/python3
# -*- coding: UTF-8 -*-
__author__ = "A.L.Kun"
__file__ = "settings.py"
__time__ = "2022/9/11 19:17"


class Config:
    """基础的配置字"""
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1:3306/bot?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    SUPER_USER = ["3500515050", ]  # 超级用户
    ADMIN = 3500515050  # 开发者


class Url:
    ACGIMG = [
        # 二次元图片链接
        "https://api.ghser.com/random/api.php",
        "https://www.dmoe.cc/random.php",
        "https://api.mtyqx.cn/api/random.php",
        "https://api.ixiaowai.cn/api/api.php",
        "https://service-5z0sdahv-1306777571.sh.apigw.tencentcs.com/release/",
        "https://api.vvhan.com/api/acgimg",
        "https://api.imacroc.cn/acg/",
        'https://tuapi.eees.cc/api.php?category=dongman&type=302',
    ]


class Help:
    """简陋的帮助文档"""
    ADMIN_HELP = """开发者命令提示：
1. 添加群:\n/admin:add QQ群号 QQ群名
2. 关闭功能:\n/admin:close QQ群号
3. 删除功能:\n/admin:delete  QQ群号
4. 查找功能:\n/admin:get QQ群号
5. 获取所有群:\n/admin:show
6. 修改权限命令:\n/admin:changeAuth QQ群号 |聊天功能|入群欢迎|管理群|戳一戳|拓展功能|定时功能|(比如110011)\n
如果还是有问题，请与开发人员联系哦！"""
    GROUP_ADMIN = """[CQ:at,qq=%d]命令提示：
1. 查看群权限:\n/admin:get
2. 修改群权限：\n/admin:change |聊天功能|入群欢迎|管理群|戳一戳|拓展功能|定时功能|(比如/admin:change 110011)\n
如果还是有问题，请与开发人员联系哦！"""
    COM_HELP = """所有功能：
1. 必应每日图片:\n/bing
2. 随机图片获取:\n/随机图片
3. 天气获取:\n/天气 城市
4. 建议:\n/send 内容
5. 二次元图片:\n/二次元 
6. 随机一言:\n/随机一言
7. 段子:\n/段子
8. 历史的今天:\n/历史
9. 无水印短视频解析:\n/短视频 链接
10. 随机诗词:\n/诗词
11. 人生语录:\n/人生语录
12. 疫情查询:\n/疫情 城市名
13. 农历:\n/农历"""


class Mes(Help):
    WELCOME_MES = {  # 新成员进入回复信息
        "873260268": f"[CQ:at,qq=%d] 欢迎大佬加入这个大家庭哦！希望在这个群里面，可以获得提升哦！[CQ:face,id={63}][CQ:face,id={63}]",
        "698292693": f"[CQ:at,qq=%d] 欢迎加入这个大家庭哦！在这个大家庭，你肯定可以有所收获的！[CQ:face,id={63}][CQ:face,id={63}][CQ:face,id={63}]",
        "662444335": f"[CQ:at,qq=%d] 欢迎加入田径队招新群！",
        "default": f"[CQ:at,qq=%d] 欢迎加入这个大家庭，来了就别想走哦！[CQ:face,id={43}][CQ:face,id={43}][CQ:face,id={43}]",
    }
    CLICK_MES = [  # 戳一戳的回复信息
        "？有事吗？没事我走了！[CQ:face,id=125]，goodbye",
        "睡觉去，困死了！",
        "戳我干啥！本人在叙利亚做兼职呢？没事别烦我！",
        "你好呀！我在躺平呢！请问有啥事呀？",
        "hello",
        "[CQ:poke,qq=%d]",
        "(－ｏ⌒) ☆",
    ]


class ProductConfig(Config, Mes, Url):
    """生产环境配置"""
    pass


class DevelopConfig(Config, Mes, Url):
    """开发环境配置"""
    DEBUG = True


envs = {
    "product": ProductConfig,
    "develop": DevelopConfig
}
