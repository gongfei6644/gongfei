import datetime
import time, sys
from pymongo import UpdateOne
from utils.common_mongo import MongoOption
from utils.common_tools import table_name_by_city
from utils.constants import STOP_TIME


def partition_table():
    """
    分表
    :return:
    """
    while True:
        delete_historical_data()

        update_list = []
        items = list(mongo_client.m_select({'$and': [{'d_status': {'$exists': True}}, {'d_status': 1},
                                                     {'partition_table_status': {'$exists': False}}]},
                                           'renting_case').limit(1000))
        for item in items:
            base_table = 'renting_case'
            city = item['city']
            table_name = table_name_by_city(base_table, city)
            print('table_name:', table_name)
            result = mongo_client.s_insert(item, table_name)
            print(result)
            # if result:
            dic = item
            dic["partition_table_status"] = 1
            update_list.append(UpdateOne({'_id': dic['_id']}, {'$set': dic}))
        if update_list:
            mongo_client.m_update(update_list, 'renting_case')
            time.sleep(0.0001)
        print('已分表数据：', len(update_list))
        process_cur_time = time.time()
        if int(process_cur_time) - int(process_start_time) >= STOP_TIME:
            print('分表进程已运行23个小时，退出程序')
            sys.exit()
        if len(update_list) < 200:
            print('数据量少，睡眠5分钟...')
            time.sleep(300)
        print('......')
        time.sleep(10)


def delete_historical_data():
    """
    删除5天前的列表数据和一个月前的已分表的详情数据
    :return:
    """
    global flag, date_time
    if flag:
        print('正在删除5天前的列表数据和一个月前的已分表的详情数据...')
        day_5_ago = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%Y-%m-%d')
        day_31_ago = (datetime.datetime.now() - datetime.timedelta(days=31)).strftime('%Y-%m-%d')
        print(day_5_ago, day_31_ago)

        result = mongo_client.m_delete({'$and': [{'d_status': {'$exists': False}}, {'crt_time': {'$lt': day_5_ago}}]},
                                       'renting_case')
        print(result)

        result = mongo_client.m_delete(
            {'$and': [{'d_status': 1}, {'partition_table_status': 1}, {'crt_time': {'$lt': day_31_ago}}]},
            'renting_case')
        print(result)
        print('删除完成')
    else:
        print(datetime.datetime.now())
    if date_time == datetime.datetime.now().strftime('%Y-%m-%d'):
        flag = False
    else:
        date_time = datetime.datetime.now().strftime('%Y-%m-%d')
        flag = True
    # time.sleep(1)


if __name__ == '__main__':
    date_time = datetime.datetime.now().strftime('%Y-%m-%d')
    print(date_time)
    flag = True
    mongo_client = MongoOption()
    process_start_time = time.time()
    partition_table()
