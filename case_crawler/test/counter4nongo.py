import datetime
import datetime as dt
import time

from utils.common_mongo import MongoOption
from utils.common_tools import timeit
from utils.switch_table import table_name_by_city

db = MongoOption()

SPLIT_TABLE_NUM = 50
base_table = "Dat_case"

# @timeit
def case_counter(source="", d_status=0, city="", ref=0, start_time='', end_time=''):
    """
    昨天的列表统计
    根据起止时间网站城市查已完成详情的数量
    """
    num = 0
    if not ref and not start_time:
        start_time = dt.datetime.combine(dt.datetime.now(), dt.time.min).strftime('%Y-%m-%d %H:%M:%S')
    if not ref and not end_time:
        end_time = dt.datetime.combine(dt.datetime.now(), dt.time.max).strftime('%Y-%m-%d %H:%M:%S')
    if not source:
        source = {"$ne": ""}
    if not city:
        city = {"$ne": ""}
    if d_status == 0:
        d_status = {"$ne": ''}
        detail_time = {"$ne": ""}
    if ref:
        start_time = (dt.datetime.combine(
            dt.datetime.now(), dt.time.min)-dt.timedelta(days=ref)).strftime('%Y-%m-%d %H:%M:%S')
        end_time = (dt.datetime.combine(
            dt.datetime.now(), dt.time.max)-dt.timedelta(days=ref)).strftime('%Y-%m-%d %H:%M:%S')

    params = {
        "city": city,
        "d_status": d_status,
        "detail_time": {"$ne": ''},
        "data_source": source,
        "crt_time": {"$gt": start_time, "$lt": end_time}
    }
    print(params)
    if city:
        table = table_name_by_city(city)
        print("table", table)
        num = db.m_select(params, table).count()
    else:
        for i in range(0, SPLIT_TABLE_NUM):
            table = "{}_{}".format(base_table, str(i).rjust(2, "0"))

            r = db.m_select(params, table).count()
            num += r
    print(num)
    if isinstance(source, str):
        if d_status == 1:
            print("{} 详情完成: {}w".format(source, round(num / 10000, 3)))
        else:
            print("{} 列表完成: {}w".format(source, round(num / 10000, 3)))
    else:
        if d_status == 1:
            print("{} 详情完成: {}w".format("所有网站", round(num / 10000, 3)))
        else:
            print("{} 列表完成: {}w".format("所有网站", round(num / 10000, 3)))


# {
#     "city" : 1,
#     "d_status" : 1,
#     "detail_time" : 1,
#     "is_std" : 1,
#     "case_happen_date" : 1,
#     "std_date" : 1,
#     "data_source" : 1,
#     "project_name" : 1,
#     "house_area" : 1,
#     "unitprice" : 1,
#     "crt_time" : 1
# }

if __name__ == '__main__':
    sources = ["安居客二手房", "房天下二手房", "城市房产二手房", "诸葛找房二手房", "58同城二手房", "赶集网二手房",
               "中国房产超市二手房", "链家二手房", "中原地产二手房"]
    print("统计时间:{}".format(datetime.datetime.now()))
    print("今日完成情况统计: ")
    case_counter("房天下二手房", 1, "上海市")
    print("\n")
    print("昨日完成情况统计: ")
    # for city in ["南京市", "杭州市", "温州市", "厦门市", "苏州市", "上海市"]:
    #     case_counter("中国房产超市二手房", 0, city, 1)
    case_counter("房天下二手房", 1, "北京市", 1)





