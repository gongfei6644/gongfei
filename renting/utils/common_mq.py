# coding=utf-8
import pika
import json
import datetime

from setting import config


def send_mq_msg(messagetype, collecttype, cityname, website, params):
    '''
    发送rabbitmq 消息
    :param messagetype: 消息类型   (增量：increase  总量：total)
    :param collecttype: 采集类型   (列表：list   详情：details   )
    :param cityname: 城市
    :param website: 网站
    :param params: 案例总量和预警字段数量
    :return:
    '''
    #rabbitmq 设置
    user_pwd = pika.PlainCredentials(config.MQ_USER, config.MQ_PWD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=config.MQ_HOST, port=config.MQ_PORT, credentials=user_pwd))
    channel = connection.channel()

    channel.queue_declare(queue='daq-state-report-queue', durable=True)
    #消息体

    crt_time= str(datetime.datetime.now()) #当前消息时间
    if messagetype == "total":
        # 案例总量
        case_count = params.get("case_count", 0)

        # 缺失楼盘名量
        projectname_count = params.get("lsprojectname_count", 0)
        # 缺失单价量
        unitprice_count = params.get("lsunitprice_count", 0)
        # 建筑面积量
        buildarea_count = params.get("lsbuildarea_count", 0)

    else:
        # 案例增量
        case_count = params.get("add_case_count", 0)

        #缺失楼盘名增量
        projectname_count = params.get("add_lsprojectname_count", 0)
        #缺失单价增量
        unitprice_count = params.get("add_lsunitprice_count", 0)
        #建筑面积增量
        buildarea_count = params.get("add_lsbuildarea_count", 0)

    message = json.dumps(
        {"messagetype": messagetype, 'collecttype': collecttype,
         "cityname": cityname, "website": website,"crt_time":crt_time,
         "case_count": case_count,"projectname_count":projectname_count,
         "unitprice_count":unitprice_count,"buildarea_count":buildarea_count
         }
        )

    channel.basic_publish(exchange='daq-info',
                          routing_key='state-report',
                          body=message,
                          properties=pika.BasicProperties(
                              delivery_mode=2,  # make message persistent
                          ))

    connection.close()




