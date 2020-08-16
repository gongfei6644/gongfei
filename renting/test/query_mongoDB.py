import time

from utils.common_mongo import MongoOption
import datetime


def start_query():
    mongo_client = MongoOption()

    today = datetime.datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

    match_today_detail = {
        "$match": {'$and': [{'d_status': {"$exists": True}}, {'d_status': 1}, {'detail_time': {'$gt': today}}]}}
    match_today_crt = {"$match": {'crt_time': {'$gt': today}}}

    match_yesterday_detail = {"$match": {
        '$and': [{'d_status': {"$exists": True}}, {'d_status': 1}, {'detail_time': {'$gt': yesterday}},
                 {'detail_time': {'$lt': today}}]}}
    match_yesterday_crt = {"$match": {'$and': [{'crt_time': {'$gt': yesterday}}, {'crt_time': {'$lt': today}}]}}

    match_list = [match_today_detail, match_today_crt, match_yesterday_detail, match_yesterday_crt]

    group = {"$group": {"_id": {"data_source": "$data_source"}, "count": {"$sum": 1}}}

    for i in range(len(match_list)):
        t1 = time.time()
        lst = list(mongo_client.statistics_aggregate([match_list[i], group]))
        if i == 0:
            print('(%s)今天详情案例量：' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if i == 1:
            print('(%s)今天列表案例量：' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if i == 2:
            print('(%s)昨天详情案例量：' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if i == 3:
            print('(%s)昨天列表案例量：' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        count = 0
        for dic in lst:
            print(dic['_id']['data_source'], '：', dic['count'])
            count += dic['count']
        print('总量：', count)
        print('用时: %ds' % (time.time() - t1))
        print('====================================', '\n')


if __name__ == '__main__':
    print('开始查询...')
    start_query()
    print("查询完成")
