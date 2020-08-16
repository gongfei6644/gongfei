# -*- coding: utf-8 -*-


from mongoengine import connect

from app.config import DB_MONGO, DB_MONGO_SLAVE


def mongo_mengine():
    master = connect(
        DB_MONGO['db'],
        host=DB_MONGO['host'],
        port=DB_MONGO['port'],
        alias='master',
        # 在这里添加认证无效，暂未知什么原因
        # username=user,
        # password=password,
        # authentication_source='admin'
    )
    if DB_MONGO['user'] and DB_MONGO['password']:
        master.admin.authenticate(DB_MONGO['user'], DB_MONGO['password'])

    slave = connect(
        DB_MONGO_SLAVE['db'],
        host=DB_MONGO_SLAVE['host'],
        port=DB_MONGO_SLAVE['port'],
        alias='slave',
    )
    if DB_MONGO_SLAVE['user'] and DB_MONGO_SLAVE['password']:
        slave.admin.authenticate(DB_MONGO_SLAVE['user'], DB_MONGO_SLAVE['password'])
