# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:32
# @Author  : luomingming
# @Desc    :

import logging

from FxtDataAcquisition.repository.base_repo import BaseRepo
from FxtDataAcquisition.settings import PAGE_SIZE
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory

logger = logging.getLogger(__name__)


class ProjectInfoRepo(BaseRepo):
    def __init__(self):
        self.clt = factory.collection('dat_project_info')

    def find(self, source, cities=None):
        if cities:
            params = {'data_source': source, 'city': {'$in': cities}, 'd_status': {'$in': [None, -1]}}
        else:
            params = {'data_source': source, 'd_status': {'$in': [None, -1]}}
        lst = list(self.clt.find(params, {'city': 1, 'data_source': 1, 'source_link': 1}).limit(PAGE_SIZE))
        return lst

    def find_all(self, cities, start_date, end_date, source=None, page_index=1):
        params = {'data_source': {'$ne': None}, 'city': {'$in': cities}, 'd_status': 1,
                  'detail_time': {'$gte': start_date, '$lte': end_date}}
        if not cities:
            params['city'] = {'$ne': None}
        if source:
            params['data_source'] = source
        lst = list(self.clt.find(params).skip((page_index - 1) * PAGE_SIZE).limit(PAGE_SIZE))
        return lst

    def find_by_url(self, url):
        case = self.clt.find_one({'source_link': url})
        return case

    # 获取未爬取完成的城市列表
    def un_finish_cities(self, source):
        cities = self.clt.find(
            {'data_source': source, 'city': {'$ne': None}, 'd_status': {'$in': [None, -1]}},
            {'city': 1, '_id': 0}
        ).distinct('city')
        return cities

    def exist(self, source, min_num=0):
        num = self.clt.find(
            {'data_source': source, 'city': {'$ne': None}, 'd_status': {'$in': [None, -1]}}
        ).count()
        if num > min_num:
            return True
        return False

    def update_status(self, _id, status=0, remark=None, url=None):
        condition = {'_id': _id}
        if url:
            condition = {'source_link': url}
        ret = self.clt.update(condition, {'$set': {'d_status': status, 'remark': remark}})
        return ret
