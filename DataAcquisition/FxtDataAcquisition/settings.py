# -*- coding: utf-8 -*-

# Scrapy settings for FxtDataAcquisition project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'FxtDataAcquisition'

SPIDER_MODULES = ['FxtDataAcquisition.spiders']
NEWSPIDER_MODULE = 'FxtDataAcquisition.spiders'
COMMANDS_MODULE = 'FxtDataAcquisition.commands'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'FxtDataAcquisition (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 3

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 1
# RANDOMIZE_DOWNLOAD_DELAY = False
DOWNLOAD_TIMEOUT = 30
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Connection': 'keep-alive',
    'X-Requested-With': 'XMLHttpRequest',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'FxtDataAcquisition.middlewares.FxtdataacquisitionSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    'FxtDataAcquisition.middlewares.ProxySpiderMiddleware': 800,
    'FxtDataAcquisition.middlewares.ExceptionMiddleware': 600,
    'FxtDataAcquisition.middlewares.TooManyRequestsRetryMiddleware': 601,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
EXTENSIONS = {
    'scrapy.extensions.logstats.LogStats': 500,
    'scrapy.extensions.corestats.CoreStats': 501,
}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'FxtDataAcquisition.pipelines.CityPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 3
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

RETRY_ENABLED = True
RETRY_TIMES = 50
S29_RETRY_TIMES = 199
RETRY_DELAY = 3
RETRY_HTTP_CODES = [500, 502, 503, 504, 522, 524, 408, 429]

HTTPERROR_ALLOWED_CODES = [301, 302, 429, 503]

LOG_LEVEL = "DEBUG"
LOG_PATH = "/var/log/FxtDataAcquisition/"

# data collection type
DAQ_LIST = 'list'
DAQ_DETAIL = 'detail'

# 采集的网站
SITE_FANGTAN = '房探网'
SITE_HOUSE365 = '365淘房网'
SITE_ANJUKE_COMMUNITY = '安居客小区'
SITE_58_COMMUNITY = '58小区'
SITE_LIANJIA_COMMUNITY = '链家小区'
SITE_CITYHOUSE_COMMUNITY = '城市房产小区'
SITE_FANG_COMMUNITY = '房天下小区'
SITE_QFANG_COMMUNITY = 'Q房网小区'

# 详情爬取延后N秒
DETAIL_DELAY = 60 * 10

# 批量读写数
BATCH_WRITE_NUM = 20
BATCH_READ_NUM = 100

# 列表采集最大页数
CRAWL_MAX_PAGE = 40

# 分表数
SPLIT_TABLE_NUM = 50

# mongodb config
DB_MONGO = {
    'host': '192.168.4.103',
    'port': 27017,
    'user': 'admin',
    'password': 'fxtxq1205',
    'db': 'DataCollecting',
}

# mysql config
MYSQL = {
    'host': '192.168.2.60',
    'port': 3306,
    'user': 'luomm',
    'password': 'DJ360disoK',
    'db': 'das-job',
}
# page size
PAGE_SIZE = 1500

# redis config
# REDIS = {
#     'host': '192.168.1.85',
#     'port': 6379,
#     'password': '',
#     'db': 0
# }
REDIS = {
    'host': '192.168.0.56',
    'port': 6379,
    'password': '',
    'db': 0
}
# 缓存时间
CACHE_EX_TIME = 1800

EMAIL = {
    'host': 'smtp.mxhichina.com',
    'port': 465,
    'username': 'daq@fxtcn.com',
    'password': 'daq@fxt123',
    'receivers': 'luomm@fxtcn.com',
}

# statistics redis key
STATIS_LIST_KEY = "s_s_l"
STATIS_DETAIL_KEY = "s_s_d"
STATIS_LIST_INCR_KEY = "s_s_l_i"
STATIS_DETAIL_INCR_KEY = "s_s_d_i"

# MQ config
RABBIT_MQ = {
    'host': '192.168.2.34',
    'port': 5672,
    'user': 'admin',
    'password': '123456'
}

# crawler proxy
PROXY = {
    'provider': 'abuyun',
    'proxy_server': 'http://http-dyn.abuyun.com:9020',
    'user': 'HZ6G1XLV727H0R3D',
    'password': 'B853A793BA6EF2D1',
    'redis_key':  'spider_proxies',
}
# PROXY = {
#     'provider': 'dailiyun',
#     'proxy_server': '',
#     'user': 'cabbagesmile',
#     'password': 'fxt168',
#     'redis_key': 'spider_proxies',
# }

# 行政区缓存key
CITY_PRE = 'city_'
CITY_WEIGHTS = 'city_weights'

UA_LIST = [
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


# 环境
###################
ENV = 'dev'
# ENV = 'pro'
###################