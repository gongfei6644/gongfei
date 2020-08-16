# -*- coding: utf-8 -*-
# @Time    : 2019-04-17 11:32
# @Author  : luomingming
# @Desc    :

import logging
import traceback
from datetime import datetime

from pymongo.errors import BulkWriteError

logger = logging.getLogger(__name__)


class BaseRepo:
    def __init__(self, clt):
        self.clt = clt

    def insert(self, item):
        ret = self.clt.insert(item, {'ordered': True})
        return ret

    def update_by_id(self, item):
        ret = self.clt.update({'_id': item['_id']}, {'$set': item}, upsert=True, multi=True)
        return ret

    def batch_update(self, lst):
        ret = -1
        try:
            ret = self.clt.bulk_write(lst, ordered=False, bypass_document_validation=True)
        except BulkWriteError as e:
            logger.error('{} batch update failed, data is: {}, exception is: {}'
                         .format(datetime.now(), lst, traceback.format_exc()), e)
        except Exception as e:
            raise e
        return ret
