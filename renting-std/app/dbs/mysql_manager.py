# -*- coding: utf-8 -*-


from mysql.connector import Error
from mysql.connector import pooling

from app.config import MYSQL


class MysqlManager:

    def __init__(self):
        self.pool = pooling.MySQLConnectionPool(pool_size=5, pool_reset_session=True,
                                                host=MYSQL['host'], port=MYSQL['port'], database=MYSQL['db'],
                                                user=MYSQL['user'], password=MYSQL['password'])
        self.conn_obj = None
        self.cursor = None

    def conn(self):
        self.conn_obj = self.pool.get_connection()

        self.cursor = self.conn_obj.cursor()
        if not self.cursor:
            raise (NameError, "连接数据库失败")
        else:
            return self.cursor

    def query(self, sql):
        try:
            cursor = self.conn()
            cursor.execute(sql)
            res = cursor.fetchall()
        finally:
            self.close()
        return res

    def query_(self, sql):
        try:
            cursor = self.conn()
            cursor.execute(sql)
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        finally:
            self.close()

    def update(self, sql):
        try:
            cursor = self.conn()
            cursor.execute(sql)
            self.conn_obj.commit()
        except Error as e:
            self.rollback()
        finally:
            self.close()

    def commit(self):
        self.conn_obj.commit()

    def rollback(self):
        self.conn_obj.rollback()

    def close(self):
        if self.conn_obj.is_connected():
            self.cursor.close()
            self.conn_obj.close()
            # print('Mysql connection is closed')


mysql = MysqlManager()
