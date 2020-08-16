# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:32
# @Author  : luomingming
# @Desc    :


import random

from FxtDataAcquisition.repository.base_repo import BaseRepo
from FxtDataAcquisition.utils.dbs.pymongo_manager import factory


class ConfigRepo(BaseRepo):
    def __init__(self):
        self.clt = factory.collection('config')

    def get_all_urls(self, source):
        ret = list(self.clt.find({'source': source}, {'sub_area_url': 1, '_id': 0}))
        if ret:
            random.shuffle(ret)
        lst = []
        for r in ret:
            lst.append(r['sub_area_url'])
        return lst

    def get_detail(self, source, url):
        params = {'sub_area_url': url}
        if source:
            params = {'source': source, 'sub_area_url': url}
        ret = self.clt.find_one(params, {'sub_area_url': 0, '_id': 0})
        return ret

    def delete(self, source, city):
        ret = self.clt.delete_many({'source': source, 'city': city})
        return ret

    def get_cities(self, source):
        ret = list(self.clt.find({'source': source}, {'city': 1, '_id': 0}).distinct('city'))
        if ret:
            ret.sort()
        return ret

    def exist(self, source, sub_area, min_num=0):
        num = self.clt.find(
            {'source': source, 'sub_area': sub_area}
        ).count()
        if num > min_num:
            return True
        return False
