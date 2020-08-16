# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from bson import json_util

from FxtDataAcquisition.repository.config_repo import ConfigRepo
from FxtDataAcquisition.utils.redis_client import rediz

logger = logging.getLogger(__name__)


class CityPipeline(object):
    def __init__(self):
        self.config_repo = ConfigRepo()

    def process_item(self, item, spider):
        config = dict(item)
        ret = self.config_repo.insert(config)
        return item

    def close_spider(self, spider):
        print('---------spider close----------')


class CasePipeline(object):

    def __init__(self):
        self.batch_list = []
        self.batch_detail = []

    def process_item(self, item, spider):
        case = dict(item)
        if spider.name.__contains__('detail'):
            key = 'update_detail'
            # ret = case_repo.update(case)
        else:
            key = 'insert_list'
            # try:
            #     ret = case_repo.insert(case)
            # except Exception as e:
            #     pass
        rediz.sadd(key, json_util.dumps(case))
        # if spider.name == 'fangtan_detail':
        #     op = UpdateOne({'_id': case['_id']}, {'$set': case}, upsert=False)
        #     self.batch_detail.append(op)
        #     if len(self.batch_detail) == BATCH_WRITE_NUM:
        #         ret = case_repo.batch_update(self.batch_detail)
        #         del self.batch_detail[:]
        # else:
        #     op = InsertOne(case)
        #     self.batch_list.append(op)
        #     if len(self.batch_list) == BATCH_WRITE_NUM:
        #         ret = case_repo.batch_update(self.batch_list)
        #         del self.batch_list[:]
        return item

    def close_spider(self, spider):
        # if len(self.batch_list) != 0:
        #     ret = case_repo.batch_update(self.batch_list)
        #     del self.batch_list[:]
        #
        # if len(self.batch_detail) != 0:
        #     ret = case_repo.batch_update(self.batch_detail)
        #     del self.batch_detail[:]
        logger.info('---------spider close----------')


class ProjectInfoPipeline(object):

    def process_item(self, item, spider):
        case = dict(item)
        if spider.name.__contains__('detail'):
            key = 'update_detail_community'
        else:
            key = 'insert_list_community'
        r = rediz.sadd(key, json_util.dumps(case))
        return item

    def close_spider(self, spider):
        logger.info('---------spider close----------')
