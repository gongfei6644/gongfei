# -*- coding: utf-8 -*-
# @Time    : 2019-04-18 15:47
# @Author  : luomingming
# @Desc    :


import pika
from FxtDataAcquisition.settings import *


class RabbitmqClient:

    def conn(self):
        user_pwd = pika.PlainCredentials(RABBIT_MQ['user'], RABBIT_MQ['password'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBIT_MQ['host'], port=RABBIT_MQ['port'],
                                      credentials=user_pwd))
        return connection

    def send_msg(self, queue, exchange, routing_key, msg):
        conn = self.conn()
        try:
            channel = conn.channel()
            channel.queue_declare(queue=queue, durable=True)
            channel.basic_publish(exchange=exchange,
                                  routing_key=routing_key,
                                  body=msg,
                                  properties=pika.BasicProperties(delivery_mode=2))  # make message persistent
        finally:
            conn.close()


mq = RabbitmqClient()

