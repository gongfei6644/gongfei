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
    ABY_URI_TEST = 'http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020'
    ABY_URI_TEST2 = 'http://H8V3J5567GO1TK6D:40EA701B8D9631D0@http-dyn.abuyun.com:9020'
    ABY_URI_LIST = "http://HFH42T02VGR3555D:46B87CE79849DE31@http-dyn.abuyun.com:9020"
    ABY_URI_DETAIL = "http://HN1I77A0285548DD:93993D807DC1F467@http-dyn.abuyun.com:9020"
    ABY_URI_MAP = {
        "房天下二手房": "http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020",
        "安居客二手房": "http://H8V3J5567GO1TK6D:40EA701B8D9631D0@http-dyn.abuyun.com:9020",
    }

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


class DevelopConfig(BaseConfig):
    """测试环境配置"""
    ENV = "dev"
    PROXY = "aby"
    ABY_URI_LIST = 'http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020'
    ABY_URI_DETAIL = 'http://HZ6G1XLV727H0R3D:B853A793BA6EF2D1@http-dyn.abuyun.com:9020'
    MONGO_URI = 'mongodb://admin:fxtxq1205@192.168.4.103:27017/'
    MONGO_DB = "DataCollecting"
    CONFIG_LOG_DIR = "/log/config/"
    LIST_LOG_DIR = "/home/xiquadmin/fxt_case_crawler/logs/lists/"
    DETAIL_LOG_DIR = "/home/xiquadmin/fxt_case_crawler/logs/details/"
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
    CONFIG_LOG_DIR = "/log/config/"
    LIST_LOG_DIR = "/usr/local/DataCollection/logs/lists/"
    DETAIL_LOG_DIR = "/usr/local/DataCollection/logs/details/"

    MQ_HOST = '192.168.4.100'
    MQ_PORT = 5672
    MQ_USER = "admin"
    MQ_PWD = "admin"


# 在此处切换环境
##########################
config = DevelopConfig
# config = ProduceConfig
##########################
