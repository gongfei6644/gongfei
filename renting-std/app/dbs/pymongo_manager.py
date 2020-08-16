# -*- coding: utf-8 -*-


import pymongo

from app.config import DB_MONGO


class PyMongoFactory:
    def __init__(self):
        self.host = DB_MONGO['host']
        self.port = DB_MONGO['port']
        self.user = DB_MONGO['user']
        self.password = DB_MONGO['password']
        self.dbname = DB_MONGO['db']
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
