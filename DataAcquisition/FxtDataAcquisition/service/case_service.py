# -*- coding: utf-8 -*-
# @Time    : 2019-05-08 18:07
# @Author  : luomingming
# @Desc    :

import random
import threading
import logging

from bson import json_util
from pypinyin import lazy_pinyin

from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.service import distinct
from FxtDataAcquisition.utils.redis_client import rediz

logger = logging.getLogger(__name__)
finished = {}
lock = threading.Lock()
config_repo = ConfigRepo()


class CaseService:
    def __init__(self, case_repo):
        self.case_repo = case_repo

    def get_raw_case(self, source):
        lock.acquire()
        py = ''.join(str(i) for i in lazy_pinyin(source))
        key = 'crawl_' + py
        case = rediz.lpop(key)
        if not case and self.case_repo.exist(source, min_num=50):
            lst = self.get_case_lst(source, py)
            for cs in lst:
                rediz.lpush(key, json_util.dumps(cs))
            case = rediz.lpop(key)
        if case:
            case = json_util.loads(case, encoding='utf-8')
        else:
            case = {}
        lock.release()
        return case

    def get_case_lst(self, source, pinyin):
        cites = self.choice_cities(source, pinyin)
        lst = self.case_repo.find(source, cites)
        if not lst:
            # 将已爬取完的城市存到finished字典
            if pinyin not in finished.keys():
                finished[pinyin] = set(cites)
            else:
                finished.get(pinyin).add(cites[0])

            lst = self.get_case_lst(source, pinyin)
        return lst

    def choice_cities(self, source, pinyin):
        cities = config_repo.get_cities(source)
        cws = self.get_city_weights(cities, pinyin)
        cws_cities = cws[0]
        cws_weights = cws[1]
        if cities.__len__() != cws_cities.__len__():
            for city in cities:
                if city not in cws_cities:
                    cws_cities.append(city)
                    cws_weights.append(5)
        # 去除已经爬取完成的城市
        fcs = finished.get(pinyin, [])
        for fc in fcs:
            try:
                idx = cws_cities.index(fc)
                cws_cities.pop(idx)
                cws_weights.pop(idx)
            except Exception as e:
                logger.error(e)
        lst = None
        if cws_cities:
            lst = random.choices(cws_cities, cws_weights)
        return lst

    def get_city_weights(self, cities_in, pinyin):
        cities_str = "'" + "','".join(cities_in) + "'"
        cws = distinct.get_city_weights(cities_str, pinyin)
        cities = []
        weights = []
        if cws:
            sp = cws.split(":")
            cities = sp[0].split(',')
            ws = sp[1].split(',')
            for w in ws:
                weights.append(int(w))
        for c in cities_in:
            if c not in cities:
                cities.append(c)
                weights.append(5)
        return cities, weights
