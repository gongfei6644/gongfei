# -*- coding: utf-8 -*-

from app.config import *
from app.redis_util import conn
from ..dbs.mysql_manager import mysql

sql = """
SELECT * from (
	SELECT type,subtype,subtype_name,'' net_name
	FROM `sys_code`
	union all
	SELECT type,sys_id subtype,sys_name subtype_name,net_name
	FROM `sys_comparision` where type not in(1,2)
)t WHERE type={}
"""


def get_code(code_type):
    key = '{}{}'.format(CODE_PRE, code_type)
    _codes = conn.hgetall(key)
    if not _codes:
        ret = mysql.query(sql.format(code_type))
        for code in ret:
            net_name = code[3]
            if not net_name:
                net_name = code[2]
            value = code[1]
            if net_name:
                value = '{}:{}'.format(code[1], code[2])
            conn.pipeline().hset(key, net_name, value).expire(key, CACHE_EX_TIME).execute()
        _codes = conn.hgetall(key)
    return _codes
