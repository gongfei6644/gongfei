import time
from hashlib import md5
import pymongo
import pandas as pd
import datetime as dt
from dateutil.parser import parse

from utils.constants import SPLIT_TABLE_NUM


def std_describ(city=None, source=None):
    city = {"$ne": ''} if city is None else city
    source = {"$ne": ''} if source is None else source
    target_client = pymongo.MongoClient(host="192.168.4.89", port=27017)
    target_client.admin.authenticate("app_xiqu", "eQ5fy5tIKxBg9vp07E9q")
    target_database = target_client["DataCollecting"]
    origin_client = target_database["renting_case"]
    params = {
        "city": city,
        "detail_time": {"$gt": '2019-06-18 00:00:00', "$lt": '2019-06-19 00:00:00'},
        "data_source": source,
        "is_std": {"$exists": True}
    }
    params_false = {
        "city": {"$ne": ''},
        "detail_time": {"$gt": '2019-06-18 00:00:00', "$lt": '2019-06-19 00:00:00'},
        "data_source": source,
        "is_std": -1
    }
    print("{}开始查询, {}".format(source, dt.datetime.now()))
    print("查询参数{}".format(params))
    have_std = origin_client.find(params).count()
    std_false = origin_client.find(params_false).count()
    print("共标准化案例{}条, 失败{}条".format(have_std, std_false))
    print("完成查询, {}".format(dt.datetime.now()))

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

def save2csv(web='', city=''):
    """
    :param source:
    :return:
    """

    source = {"$ne":''} if not web else web
    if not city:
        city = {"$ne":''}
    target_client = pymongo.MongoClient(host="192.168.4.90", port=27017)
    target_client.admin.authenticate("app_xiqu", "eQ5fy5tIKxBg9vp07E9q")
    target_database = target_client["DataCollecting"]
    # table = "renting_case"
    # table = "renting_case_17"
    # city_list = ['深圳市',]
    city_list = ["平顶山市", "三门峡市", "漯河市", "信阳市", "鹤壁市", "开封市", "濮阳市", "商丘市", "济源市", "周口市",
                 "安阳市", "南阳市", "郑州市", "驻马店市", "许昌市", "洛阳市", "新乡市", "焦作市"]
    base_table = "renting_case"
    for city in city_list:
        table = table_name_by_city(base_table, city)
        origin_client = target_database[table]
        # for city in city_list:
        print("{}开始查询, {}".format(city, dt.datetime.now()))
        items = list(origin_client.find({
            "city": city,
            # "data_source": source,
            "d_status": 1,
            # 'case_happen_date': {"$gt": '2019-05-19', "$lt": '2019-06-19'}
        }))
        print("完成查询{}条数据, {}".format(len(items), dt.datetime.now()))
        df_s = pd.DataFrame()
        if items:
            # df = pd.DataFrame(columns=["_id","d_status", "title", "source_link", "list_page_url", "unit_price"])
            df = pd.DataFrame(items)
            # print(df.columns)
            df_s["*城市名称"] = df["city"]
            df_s["*楼盘名称"] = df["project_name"]
            df_s["行政区"] = df["area"]
            df_s["楼栋名称"] = df["build_name"]
            df_s["所在楼层"] = df["floor_no"]
            df_s["房号名称"] = df["house_name"]
            df_s["楼栋地上总层数"] = df["total_floor_num"]
            df_s["*案例日期"] = df["case_happen_date"]
            df_s["*案例用途"] = df["usage"]
            df_s["*建筑面积"] = df["build_area"]
            df_s["*案例单价"] = df["unitprice"]
            df_s["*案例总价"] = df["total_price"]
            df_s["*案例类型"] = df["case_type"]
            df_s["出租方式"] = df["rental_method"]
            df_s["押付方式"] = df["deposit_method"]
            df_s["朝向"] = df["orientation"]
            df_s["建筑类型"] = df["build_type"]
            df_s["户型"] = df["house_type"]
            df_s["户型结构"] = df["house_structure"]
            df_s["建筑年代"] = df["build_date"]
            df_s["装修"] = df["decoration"]
            df_s["使用面积"] = df["usable_area"]
            df_s["剩余年限"] = df["remaining_years"]
            df_s["成新率"] = df["new_ratio"]
            df_s["币种"] = df["currency"]
            df_s["附属房屋"] = df["affiliated_house"]
            df_s["配套"] = df["supporting_facilities"]
            df_s["案例来源"] = df["data_source"]
            df_s["来源链接"] = df["source_link"]
            df_s["来源电话"] = df["tel"]
            df_s["备注"] = df["remark"]


            print("start to save")
            filename = "{}{}_{}_{}.xlsx".format(table, web, city, dt.date.today())
            df_s.to_excel(filename, index=False, encoding='utf-8_sig')
            print("finished")



if __name__ == '__main__':
    # for web in {"安居客租房"}:
    #     save2csv(web)
    #     time.sleep(3)
    save2csv()
