# -*- coding: utf-8 -*-

import redis

from app.config import REDIS

pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'],
                            password=REDIS['password'], decode_responses=True, max_connections=5)
conn = redis.Redis(connection_pool=pool)
