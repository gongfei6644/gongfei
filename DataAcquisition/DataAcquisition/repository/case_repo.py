# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:32
# @Author  : luomingming
# @Desc    :

import logging
import traceback
from datetime import datetime

from pymongo.errors import BulkWriteError

from FxtDataAcquisition.settings import PAGE_SIZE
from FxtDataAcquisition.utils.switch_table import *
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory

logger = logging.getLogger(__name__)
base_table = 'Dat_case'


class CaseRepo:

    def batch_update(self, city, lst):
        if not city:
            raise Exception('城市不存在')
        ret = -1
        try:
            clt = self.get_clt(city)
            ret = clt.bulk_write(lst, ordered=False, bypass_document_validation=True)
        except BulkWriteError as e:
            logger.error('{} batch update failed, data is: {}, exception is: {}'
                         .format(datetime.now(), lst, traceback.format_exc()), e)
        except Exception as e:
            raise e
        return ret

    def find(self, source, cities):
        if not cities:
            raise Exception('城市不存在')
        # if cities:
        #     params = {'data_source': source, 'city': {'$in': cities}, 'd_status': {'$in': [None, -1]}}
        # else:
        #     params = {'data_source': source, 'd_status': {'$in': [None, -1]}}
        lst = []
        for city in cities:
            clt = self.get_clt(city)
            params = {'data_source': source, 'city': city, 'd_status': {'$in': [None, -1]}}
            lst += list(clt.find(params, {'city': 1, 'data_source': 1, 'source_link': 1}).limit(PAGE_SIZE))
        return lst

    def exist(self, source, min_num=0):
        def func(table):
            clt = factory.collection(table)
            num = clt.find(
                {'data_source': source, 'city': {'$ne': None}, 'd_status': {'$in': [None, -1]}}
            ).count()
            if num > min_num:
                return True
            return False

        return switch_for(func, base_table, ret_bool=True)

    def update_status(self, _id, city, status=0, remark=None, url=None):
        if not city:
            raise Exception('城市不存在')
        condition = {'_id': _id}
        if url:
            condition = {'source_link': url}
        clt = self.get_clt(city)
        ret = clt.update(condition, {'$set': {'d_status': status, 'remark': remark}})
        return ret

    def get_clt(self, city):
        clt = factory.collection(table_name_by_city(base_table, city))
        return clt
