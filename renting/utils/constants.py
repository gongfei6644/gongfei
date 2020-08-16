﻿# coding: utf-8

"""
用于定义常量的模块
"""
import re

WEBSITE_PAGESIZE = {"房天下租房": {'first_tier_cities': 80, "generic_city": 50},
                    "赶集网租房": {'first_tier_cities': 50, "generic_city": 30},
                    "58同城租房": {'first_tier_cities': 50, "generic_city": 30},
                    "安居客租房": {'first_tier_cities': 50, "generic_city": 30},
                    "链家租房": {'first_tier_cities': 50, "generic_city": 30},
                    "城市房产租房": {'first_tier_cities': 50, "generic_city": 30},
                    "中原地产租房": {'first_tier_cities': 50, "generic_city": 30},
                    "中国房产超市租房": {'first_tier_cities': 50, "generic_city": 30},
                    "Q房网租房": {'first_tier_cities': 50, "generic_city": 30},
                    "房途网租房": {'first_tier_cities': 50, "generic_city": 30},
                    "房探网租房": {'first_tier_cities': 40, "generic_city": 40},
                    "我爱我家租房": {'first_tier_cities': 50, "generic_city": 30},
                    "诸葛找房租房": {'first_tier_cities': 50, "generic_city": 30},
                    }

SLEEP_MAP = {  # 单位: s
    "安居客租房": 5,
    "房天下租房": 5,
    "赶集网租房": 1,
    "链家租房": 1
}

LOG_EXPIRED = 3  # 单位: d

EXIT_MAP = {  # 单位: d
    "北京市": 23 * 60 * 60,
    "上海市": 23 * 60 * 60,
    "广州市": 23 * 60 * 60,
    "深圳市": 23 * 60 * 60,
}

RETRY_TIMES = 50
RETRY_TIMES_MAP = {  # 重试次数, 单位: s
    "安居客租房": 50,
    "房天下租房": 50,
    "城市房产租房": 50,
    "诸葛找房租房": 50,
    "58同城租房": 50,
    "赶集网租房": 30,
    "链家租房": 50,
    "中国房产超市租房": 50,
    "中原地产租房": 80,
}

WAIT_TIME_MAP = {  # 存储数据后的等待时间
    "安居客租房": 5,
    "房天下租房": 5,
    "城市房产租房": 5,
    "诸葛找房租房": 5,
    "58同城租房": 3,
    "赶集网租房": 3,
    "链家租房": 1,
    "中国房产超市租房": 1,
    "中原地产租房": 1
}

WARNING_TIME = 1 * 60 * 60  # 预警消息的时间间隔

STOP_TIME = 23 * 60 * 60  # 主动中止线程的时间

CONTAINER_SIZE = 4000  # 缓存队列大小

MIN_PERSISTENCE = 100  # 最小持久化量

INTERVAL = 15

INTERVAL_MAP = {
"58同城租房": 15,
"安居客租房": 15,
"房天下租房": 15,
"城市房产租房": 15,
"链家租房": 15,
}

PATTTERN_MAP = {
    "blank": re.compile(r'\s', re.S),
    "house_type": re.compile(r'\d+室\d*厅?', re.S),
    "zhuge_floor": re.compile(r'[/\\(]共?(\d+)层', re.S),  # 低层/6层  或者 低楼层(共10层)
    "floor": re.compile(r'([高中低底]+层)[/\\(]共?(\d+)层', re.S),
    "font": re.compile(r"charset=utf-8;base64,(.*?)'\)", re.S),
    "float": re.compile(r'[\d\\.]+')}

SPLIT_TABLE_NUM = 50

LIST_SIZE = 1500  # 每个列表最多存储的案例数

CITIES = ["郑州市", "开封市", "洛阳市", "平顶山市", "焦作市", "鹤壁市", "新乡市 ", "安阳市", "濮阳市", "许昌市", "漯河市",
    "三门峡市", "南阳市", "商丘市", "信阳市", "周口市", "驻马店市", "济源市"]