# -*- coding: utf-8 -*-
# @Time    : 2019-06-18 5:40 PM
# @Author  : luomingming
# @Desc    : 分表函数

from hashlib import md5

from FxtDataAcquisition.settings import SPLIT_TABLE_NUM


# 遍历分表查找数据，直到查询出结果或者退出循环
# ret_bool: 返回类型是否为bool类型
def switch_for(func, base_table, ret_bool=False):
    for i in range(0, SPLIT_TABLE_NUM):
        table = table_name(base_table, i)
        ret = func(table)
        if ret:
            return ret
    if ret_bool:
        return False
    return None


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


if __name__ == '__main__':
    # print(int(md5('南宁市'.encode('UTF-8')).hexdigest(), 16))
    print(table_idx('广州市'))
    print(table_idx('上海市'))
    print(table_idx('北京市'))
    print(table_idx('深圳市'))
