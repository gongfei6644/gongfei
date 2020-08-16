# -*- coding: utf-8 -*-

import redis
from FxtDataAcquisition.settings import *


pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], password=REDIS['password'],
                            decode_responses=True, max_connections=20)
rediz = redis.Redis(connection_pool=pool)


