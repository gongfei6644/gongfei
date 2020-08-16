# -*- coding: utf-8 -*-


import logging
import traceback

from mongoengine import *
from pymongo.errors import BulkWriteError
from pymongo import InsertOne

from app.config import PAGE_SIZE
from app.date_util import *
from app.dbs.mongo_manager import *
from app.dbs.pymongo_manager import factory
from app.switch_table import *

mongo_mengine()
base_table = 'renting_std_case'


class StdCase(DynamicDocument):
    meta = {
        'db_alias': 'master',
        'collection': base_table,
        'strict': False
    }
    id = StringField(primary_key=True)
    case_id = StringField(required=True)
    case_type = StringField(required=True)
    city_id = IntField()
    city_name = StringField(required=True)
    area_id = IntField()
    area_name = StringField()

    project_name = StringField(required=True)
    build_type = StringField()
    build_date = StringField()
    house_type = StringField()
    house_structure = StringField()
    floor_no = IntField()
    total_floor_num = IntField()
    usable_area = DecimalField()   # 使用面积 留空
    orientation = StringField()
    unitprice = DecimalField(required=True)
    total_price = DecimalField(required=True)
    usage = StringField(required=True)
    decoration = StringField()
    supporting_facilities = StringField()
    case_happen_date = StringField()
    source_link = StringField()
    tel = StringField()
    data_source = StringField()
    currency = StringField(required=True)

    build_name = StringField()  # 空值
    house_name = StringField()  # 空值

    rental_method = StringField()  # 出租方式
    deposit_method = StringField()  # 押付方式
    build_area = DecimalField()
    new_ratio = StringField()  # 剩余年限 留空
    remaining_years = StringField()  # 成新率 留空
    remark = StringField()  # 备注 留空
    affiliated_house = StringField() # 附属房屋 留空

    md5_ = StringField(required=True)  # 签名，用于识别不同案例
    status = IntField()  # 案例状态，重复删除数据: 0, 合格数据: 1, 用途偏差数据: -1, 建筑类型偏差数据: -2, 按楼盘分偏差数据：-3
    std_remark = StringField()
    std_date = DateField()
    etl_date = DateField()  # 去重去偏差日期

    # 反调差标准价 反调差均价
    adjust_std_price = DecimalField()
    adjust_avg_price = DecimalField()

    def city(self, city):
        city = city.split(':')
        self.city_id = city[1]
        self.city_name = city[0]

    def area(self, area):
        area = area.split(':')
        self.area_id = area[1]
        self.area_name = area[0]

    def insert(self):
        self.case_date_ym = self.case_happen_date[0:7]
        p = [
            self.project_name, self.city_name, self.area_name, self.floor_no, self.total_floor_num,
            self.usage, self.build_area, self.unitprice, self.total_price, self.orientation,
            self.build_type, self.house_type,
        ]
        st = ''.join([str(v) for v in p if v])
        self.md5_ = md5(st.encode('utf-8')).hexdigest()
        self.std_date = datetime.now()
        # ret = self.save()
        op = InsertOne(self._data)
        return op

    def bulk_update(self, lst, city):
        ret = -1
        try:
            clt = factory.collection(table_name_by_city(base_table, city))
            ret = clt.bulk_write(lst, ordered=False)
        except BulkWriteError as e:
            logging.error('{} batch update failed, data is: {}, exception is: {}'
                          .format(datetime.now(), lst, traceback.format_exc()), e)
        except Exception as e:
            raise e
        return ret

    def del_dups(self, city, start_date, end_date):
        if not city:
            raise Exception('城市不存在')

        lst = self.get_dups(city, start_date, end_date)  # 分组后的数据列表
        del_list = []
        for case in lst:
            dups = case['dups']
            if dups and len(dups) > 1:
                del_list = del_list + dups[1:]
            if len(del_list) > 3000:
                self.multi_update_status(del_list, city)
                del_list = []
        if del_list:
            self.multi_update_status(del_list, city)

    def multi_update_status(self, del_list, city):
        def func():
            ret = StdCase.objects(id__in=del_list).update(set__status=0)
            print(ret)

        switch(func, StdCase, base_table, city)

    def get_dups(self, city, start_date, end_date):
        def func():
            pl = [
                {"$group": {"_id": {"md5_": "$md5_"}, "count": {"$sum": 1}, "dups": {"$addToSet": "$_id"}}},
                {"$match": {"count": {"$gt": 1}}}
            ]
            # ti = datetime.combine(datetime.now(), time.min).strftime('%Y-%m-%d %H:%M:%S')
            # d = datetime(int(datetime.now().year), int(datetime.now().month), 1)
            options = {'allowDiskUse': True}
            lst = list(StdCase.objects(case_happen_date__gte=ym(start_date), case_happen_date__lte=ym(end_date),
                                       status__ne=-99, city_name=city).aggregate(*pl, **options))
            return lst

        return switch(func, StdCase, base_table, city)

    def get_by_type(self, d_type, city, start_date, end_date):
        if not city:
            raise Exception('城市不存在')

        def func():
            if d_type == 'usage':
                pl = [
                    {"$group": {"_id": {"city": "$city_name",
                                        "project_name": "$project_name", "usage": "$usage"},
                                "t_price": {"$sum": "$total_price"}, "t_area": {"$sum": "$build_area"},
                                "ids": {"$addToSet": "$_id"}}}
                ]
            elif d_type == 'btype':
                pl = [
                    {"$group": {"_id": {"city": "$city_name",
                                        "project_name": "$project_name", "build_type": "$build_type"},
                                "t_price": {"$sum": "$total_price"}, "t_area": {"$sum": "$build_area"},
                                "ids": {"$addToSet": "$_id"}}}
                ]
            elif d_type == 'project':
                pl = [
                    {"$match": {"usage": {"$ne": "别墅"}}},
                    {"$group": {"_id": {"city": "$city_name", "project_name": "$project_name"},
                                "t_price": {"$sum": "$total_price"}, "t_area": {"$sum": "$build_area"},
                                "ids": {"$addToSet": "$_id"}}}
                ]
            # d = datetime(int(datetime.now().year), int(datetime.now().month), 1)
            options = {'allowDiskUse': True}
            lst = list(StdCase.objects(case_happen_date__gte=ym(start_date), case_happen_date__lte=ym(end_date),
                                       status__nin=[0, -1, -2, -3], city_name=city).aggregate(*pl, **options))
            return lst

        return switch(func, StdCase, base_table, city)

    def update_status_by_id(self, id, city, status, remark=None):
        def func():
            ret = StdCase.objects(id=id).update_one(set__status=status, set__std_remark=remark)

        switch(func, StdCase, base_table, city)

    def update_status(self, city, start_date, end_date):
        if not city:
            raise Exception('城市不存在')

        def func():
            ret = StdCase.objects(case_happen_date__gte=ym(start_date), case_happen_date__lte=ym(end_date),
                                  status__ne=None, city_name=city).update(set__status=None)
            return ret

        return switch(func, StdCase, base_table, city)

    def get_list(self, city, start_date, end_date, page_index, status=None):
        # last_ym = get_last_month_ym()
        # .order_by('case_happen_date')\
        if not city:
            raise Exception('城市不存在')

        def func():
            params = Q(case_happen_date__gte=ym(start_date)) & Q(case_happen_date__lte=ym(end_date))
            if status:
                params = params & Q(status__in=status)
            else:
                params = params & Q(status__ne=None)
            params = params & Q(city_name=city)
            lst = list(StdCase.objects(params).skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE))
            return lst

        return switch(func, StdCase, base_table, city)

    def get_deviation_cases(self, page_index):
        def func():
            lst = list(StdCase.objects(case_happen_date__ne=None, status__in=[0, -1, -2, -3])
                       .skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE))
            return lst

        return switch_for(func, StdCase, base_table)

    def get_by_case_ids(self, case_ids, city):
        if not city:
            raise Exception('城市不存在')

        # with switch_db(StdCase, 'slave'):
        def func():
            lst = list(StdCase.objects(case_id__in=case_ids))
            return lst

        return switch(func, StdCase, base_table, city)

    def get_by_id(self, _id, city):
        if not city:
            raise Exception('城市不存在')

        def func():
            case = StdCase.objects(id=_id).first()
            return case

        return switch(func, StdCase, base_table, city)

    def get_by_ids(self, ids, city):
        if not city:
            raise Exception('城市不存在')

        def func():
            cases = list(StdCase.objects(id__in=ids).fields(id=1, unitprice=1))
            return cases

        return switch(func, StdCase, base_table, city)

    # def select_distinct(self):
    #   pipleline = [
    #     {"$group": {"_id":
    #                   {
    #                     "project_name": '$project_name', "city_name": '$city_name', "area_name": '$area_name',
    #                     "floor_no": '$floor_no', "total_floor_num": '$total_floor_num', "usage": '$usage',
    #                     "house_area": '$house_area', "unitprice": '$unitprice', "total_price": '$total_price',
    #                     "orientation": '$orientation', "building_type": '$building_type', "house_type": '$house_type'
    #                   }
    #                 }
    #      }
    #   ]
    #   list = StdCase.objects.aggregate(*pipleline)
    #   list = StdCase.objects.distinct('md5_')
    #   return list
