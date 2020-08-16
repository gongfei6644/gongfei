# -*- coding: utf-8 -*-


import logging
import traceback
import random
from datetime import timedelta

from mongoengine import *
from pymongo.errors import BulkWriteError
from mongoengine.context_managers import switch_db

from app.config import PAGE_SIZE
from app.date_util import *
from app.switch_table import *
from app.dbs.mongo_manager import *
from app.dbs.pymongo_manager import factory

mongo_mengine()
base_table = 'renting_case'


class Case(DynamicDocument):
    meta = {
        'db_alias': 'master',
        'collection': base_table,
        'strict': False
    }
    id = StringField(db_field='_id', max_length=32, primary_key=True)
    city = StringField()
    area = StringField()
    project_name = StringField()
    build_date = StringField()
    build_type = StringField()
    house_type = StringField()
    house_structure = StringField()
    floor_no = StringField()
    total_floor_num = StringField()
    usable_area = StringField()
    orientation = StringField()
    unitprice = StringField()
    total_price = StringField()
    usage = StringField()
    decoration = StringField()
    supporting_facilities = StringField()
    case_happen_date = StringField()
    source_link = StringField()
    tel = StringField()
    data_source = StringField()

    rental_method = StringField()
    build_area = StringField()
    deposit_method = StringField()

    case_type = StringField()
    currency = StringField()

    build_name = StringField()
    house_name = StringField()
    new_ratio = StringField()
    remaining_years = StringField()
    affiliated_house = StringField()
    remark = StringField()

    sub_area = StringField()
    title = StringField()
    address = StringField()
    detail_time = StringField()
    crt_time = StringField()
    d_status = IntField()

    is_std = IntField()  # 标准化状态：-1失败，1成功
    std_remark = StringField()
    std_date = DateField()

    def find(self):
        def func():
            params = Q(city__nin=[None, '', '周边', '其它']) & Q(d_status=1) & Q(is_std__nin=[-1, 1]) & Q(
                case_happen_date__nin=[None, ''])
            lst = list(Case.objects(params).limit(PAGE_SIZE))
            if lst:
                if len(lst) >= 500:
                    return lst
                # if len(lst) > 100:
                #     f = random.choices([0, 1], [1, 2])[0]
                else:
                    f = random.choices([0, 1], [1, 25])[0]
                if f == 0:
                    return lst
                else:
                    return []
            return lst
        return switch_for(func, Case, base_table)

    def find_total_floor(self,city,area,project_name):
        def func():
            params = Q(city=city) & Q(area=area) & Q(project_name=project_name) & Q(
                total_floor_num__exists=True)
            lst = list(Case.objects(params))
            lst = [case.total_floor_num for case in lst]
            return lst

        return switch(func, Case, base_table,city)


    def update_std_status(self, case, status, std_remark=None):
        if not case.city:
            raise Exception('案例[{}]城市不存在'.format(case.id))

        def func():
            ret = Case.objects(id=case.id).update_one(
                set__is_std=status, set__std_remark=std_remark, set__std_date=datetime.now())
            return ret
        return switch(func, Case, base_table, case.city)

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

    def statis(self, s_type,l_time,n_time):
        # with switch_db(Case, 'slave'):
        def func():
            params = Q(d_status=1) & Q(detail_time__gt=l_time) & Q(detail_time__lt=n_time)
            pl = [
                {"$project": {
                    "city": 1,
                    "data_source": 1,
                    "time": {"$substr": ["$detail_time", 0, 10]}
                }},
                {"$group": {"_id": {"city": "$city", "data_source": "$data_source",
                                    "time": "$time"},
                            "count": {"$sum": 1}}}
            ]
            if 'proj_name_count' in s_type:
                params = params & Q(project_name__nin=[None, ''])
            elif 'std_count' in s_type:
                params = params & Q(is_std=1)
            elif 'totalprice_count' in s_type:
                params = params & Q(total_price__nin=[None, '', 0])
            options = {'allowDiskUse': True}
            lst = list(Case.objects(params).aggregate(*pl, **options))
            return lst

        return switch_for_with_statistics(func, Case, base_table)

    def statis_std(self):
        # with switch_db(Case, 'slave'):
        def func():
            now = datetime.now()
            d = now - timedelta(days=1)
            pl = [
                {"$project": {
                    "city": 1,
                    "data_source": 1,
                    "time": {"$substr": ["$std_date", 0, 10]}
                }},
                {"$group": {"_id": {"city": "$city", "data_source": "$data_source",
                                    "time": "$time"},
                            "count": {"$sum": 1}}}
            ]
            options = {'allowDiskUse': True}
            lst = list(Case.objects(city__ne='', is_std=1, std_date__gte=d.strftime('%Y-%m-%d'),
                                    data_source__ne='').aggregate(*pl, **options))
            return lst

        return switch_for_with_statistics(func, Case, base_table)

    def get_std_err_cases(self, city, page_index, start_date, end_date):
        if not city:
            raise Exception('城市不存在')

        # with switch_db(Case, 'slave'):
        def func():
            lst = list(Case.objects(city=city, is_std=-1, std_date__gte=start_date, std_date__lte=end_date,
                                    data_source__ne='')
                       .skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE))
            return lst

        return switch(func, Case, base_table, city)

    # 获取已经过标准化处理的案例，包含标准化成功和失败的
    # 注：由于列表和详情采集速度的差异，导致不同时刻导出同样案例时间段的结果会有差异；
    # 因为详情采集很可能在这一段时间间隔里采集到这个案例时间段的案例，因此需加上标准化的时间，使得平台导出的数据与此处导出数据尽量一致
    def get_std_cases(self, city, page_index, start_date, end_date, std_date=None, data_source=None):
        if not city:
            raise Exception('城市不存在')

        # with switch_db(Case, 'slave'):
        def func():
            params = Q(city=city) & Q(d_status=1) & Q(is_std__ne=None) & \
                     Q(case_happen_date__gte=ym(start_date)) & Q(case_happen_date__lte=ym(end_date))
            if std_date:
                params = params & Q(std_date__lte=std_date)
            if data_source:
                params = params & Q(data_source__in=data_source)
            lst = list(Case.objects(params).skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE))
            return lst

        return switch(func, Case, base_table, city)
