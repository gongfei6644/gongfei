# -*- coding: utf-8 -*-

# @Desc    : 分表函数

import logging
import random
from hashlib import md5

from mongoengine.context_managers import switch_collection

from app.config import SPLIT_TABLE_NUM


# 遍历分表查找数据，直到查询出结果或者退出循环
# ret_bool: 返回类型是否为bool类型
def switch_for(func, cls, base_table, ret_bool=False):
    # f = random.choices([0, 1], [1, 1])[0]
    # rg = range(0, SPLIT_TABLE_NUM)
    # if f == 0:
    #     rg = range(SPLIT_TABLE_NUM - 1, -1, -1)
    # for i in rg:
    while True:
        i = random.randint(0, SPLIT_TABLE_NUM - 1)
        # i = random.choice([4,46])
        table = table_name(base_table, i)
        with switch_collection(cls, table):
            ret = func()
            if ret:
                logging.debug('table_name: {}'.format(table))
                return ret
    if ret_bool:
        return False
    return None


# 遍历分表统计数据
def switch_for_with_statistics(func, cls, base_table):
    lst = []
    for i in range(0, SPLIT_TABLE_NUM):
        table = table_name(base_table, i)
        with switch_collection(cls, table):
            ret = func()
            if ret:
                lst += ret
    return lst


# 切换到分表执行操作
def switch(func, cls, base_table, city):
    table = table_name_by_city(base_table, city)
    with switch_collection(cls, table):
        return func()


# 获取表名
def table_name(base_table, idx):
    table = base_table + '_{}'.format(str(idx))
    if idx < 10:
        table = base_table + '_0{}'.format(str(idx))
    return table


# 获取表名
def table_name_by_city(base_table, city):
    return table_name(base_table, table_idx(city))


# 获取城市对应的表索引
def table_idx(city):
    hash_code = int(md5(city.encode('UTF-8')).hexdigest(), 16)
    idx = hash_code % SPLIT_TABLE_NUM
    return idx


