import redis
from setting import REDIS

pool = redis.ConnectionPool(host=REDIS['host'], port=REDIS['port'], db=REDIS['db'],
                            password=REDIS['password'], decode_responses=True, max_connections=10000)
conn = redis.Redis(connection_pool=pool)