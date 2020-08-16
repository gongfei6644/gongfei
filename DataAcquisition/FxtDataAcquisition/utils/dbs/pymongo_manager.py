# -*- coding: utf-8 -*-
# @Time    : 2019-02-27 16:29
# @Author  : luomingming

import pymongo
from FxtDataAcquisition import settings


class PyMongoFactory:
    def __init__(self):
        db = settings.DB_MONGO
        self.host = db.get('host')
        self.port = db.get('port')
        self.user = db.get('user')
        self.password = db.get('password')
        self.dbname = db.get('db')
        self.client = None

    def client_fac(self):
        if not self.client:
            self.client = pymongo.MongoClient(self.host, self.port, minPoolSize=10)
            if self.user:
                self.client.admin.authenticate(self.user, self.password)

    def db(self):
        if not self.client:
            self.client_fac()
        return self.client[self.dbname]

    def collection(self, clt):
        db = self.db()
        return db[clt]


factory = PyMongoFactory()
