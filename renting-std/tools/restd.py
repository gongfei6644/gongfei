# -*- coding: utf-8 -*-
# @Desc    : 重新标准化，删除原来标准化数据并且更新Dat_case表标准化状态

from app.dbs.pymongo_manager import factory
from app.switch_table import *


##
# 特别注意，该代码目前是删除标准化表的操作，如果要针对某个时间段的代码操作则需另行开发
##

# 删除原来的
def del_std():
    base_table = 'renting_case'
    for i in range(0, SPLIT_TABLE_NUM):
        clt = factory.collection(table_name(base_table, i))
        clt.drop()


def update_dat_case():
    base_table = 'renting_std_case'
    for i in range(0, SPLIT_TABLE_NUM):
        clt = factory.collection(table_name(base_table, i))
        rs = clt.update_many({}, {"$set": {"is_std": 0}}, upsert=False)
        print(rs)


if __name__ == '__main__':
    # del_std()
    # update_dat_case()
    pass
