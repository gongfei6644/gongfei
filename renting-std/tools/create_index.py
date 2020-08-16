# -*- coding: utf-8 -*-
# @Desc    : 创建索引
import time

from app.dbs.pymongo_manager import factory
from app.switch_table import *


# 为renting_case表添加索引
def add_idx_case():
    base_table = 'renting_case'
    for i in range(0, SPLIT_TABLE_NUM):
        clt = factory.collection(table_name(base_table, i))
        try:
            clt.create_index([('city', 1), ('d_status', 1), ('detail_time', 1), ('is_std', 1), ('case_happen_date', 1),
                              ('std_date', 1), ('data_source', 1), ('project_name', 1), ('build_area', 1),
                              ('unitprice', 1),('total_price', 1), ('crt_time', 1)],
                             background=True, name='idx_01')
        except:
            pass


# 为std_case表添加索引
def add_idx_std():
    base_table = 'renting_std_case'
    for i in range(0, SPLIT_TABLE_NUM):
        print(i)
        clt = factory.collection(table_name(base_table, i))
        clt.create_index([('case_happen_date', 1), ('status', 1), ('city_name', 1), ('area_name', 1),
                          ('project_name', 1), ('usage', 1), ('build_type', 1), ('data_source', 1)],
                         background=True, name='idx_01')
        clt.create_index([('case_id', 1), ('md5_', 1)], background=True, name='idx_02')


if __name__ == '__main__':
    # add_idx_case()
    add_idx_std()
    pass
