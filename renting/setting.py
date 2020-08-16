# coding: utf-8

"""
配置环境的模块
在最下地方进行切换
"""


class BaseConfig:
    """
    通用配置
    """
    # HZ6G1XLV727H0R3D
    # B853A793BA6EF2D1
    # 通行证书：H8V3J5567GO1TK6D
    # 通行密钥：40EA701B8D9631D0
    ABY_URI = 'http://H1Q1590G07Z0DK3D:09514962B740DB46@http-dyn.abuyun.com:9020' # 租金专用代理
    # ABY_URI = 'http://H8623AGQRD4331CD:2BB8BAE2D12F22D1@http-dyn.abuyun.com:9020' # 测试  安居客+开发代理

    MYSQL_INFO = {
        'host': '192.168.4.99',
        'port': 3306,
        'database': 'das_job_prod',
        'user': 'root',
        'password': 'Admin_123',
        'charset': 'utf8'}
    AGENT_LIST = [
            "Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1",
            "Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;TheWorld)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
            "Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)",
            "Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)"]

EMAIL = {
    'host': 'smtp.mxhichina.com',
    'port': 465,
    'username': 'daq@fxtcn.com',
    'password': 'daq@fxt123',
    'receivers': 'gongf@fxtcn.com,yuanhl@fxtcn.com,caiqs@fxtcn.com',
}
REDIS = {
    # 'host': '192.168.4.26',
    'host': '192.168.4.102',
    'port': 6379,
    # 'password': '',
    'password': 123456,
    'db': 3,
}


class DevelopConfig(BaseConfig):
    """测试环境配置"""
    ENV = "dev"
    PROXY = "aby"
    MONGO_URI = 'mongodb://admin:fxtxq1205@192.168.4.103:27017/'
    MONGO_DB = "DataCollecting"
    CONFIG_LOG_DIR = "/home/xiquadmin/fxt_renting/logs/log/config/"
    LIST_LOG_DIR = "/home/xiquadmin/fxt_renting/logs/lists/"
    DETAIL_LOG_DIR = "/home/xiquadmin/fxt_renting/logs/details/"
    # MQ_HOST = '192.168.4.99'
    MQ_HOST = '192.168.4.100'  # for test
    MQ_PORT = 5672
    MQ_USER = "admin"
    MQ_PWD = "admin"


class ProduceConfig(BaseConfig):
    """生产环境配置"""
    ENV = "pro"
    PROXY = "aby"
    MONGO_URI = 'mongodb://app_xiqu:eQ5fy5tIKxBg9vp07E9q@192.168.4.90:27017/'

    MONGO_DB = "DataCollecting"
    CONFIG_LOG_DIR = "/usr/projects/logs/fxt_renting/config/"
    LIST_LOG_DIR = "/usr/projects/logs/fxt_renting/list/"
    DETAIL_LOG_DIR = "/usr/projects/logs/fxt_renting/detail/"

    MQ_HOST = '192.168.4.100'
    MQ_PORT = 5672
    MQ_USER = "admin"
    MQ_PWD = "admin"


# 在此处切换环境
##########################
config = DevelopConfig
# config = ProduceConfig
##########################
