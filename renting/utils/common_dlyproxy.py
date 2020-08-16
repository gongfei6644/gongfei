import requests
import redis
from random import choice


def get_proxy_redis(logger=None):
    """
    代理云, 使用redis缓冲池
    :param logger:
    :return:
    """
    try:
        redis_db = redis.Redis(host='192.168.4.87', port=6379, password='123456')
        result = redis_db.hgetall('spider_proxies')
        if result:
            return choice(list(result.keys())).decode('utf-8')

        proxyusernm = "cabbagesmile"  # 代理帐号
        proxypasswd = "fxt168"  # 代理密码
        proxyaddr = 'http://cabbagesmile.v4.dailiyun.com/query.txt?key=NP6301C7B1&word=&count=1&rand=true&detail=false'
        res = requests.get(proxyaddr, timeout=15)
        proxy_str = res.text.replace('\r\n', '')
        proxyurl = "http://" + proxyusernm + ":" + proxypasswd + "@" + proxy_str
    except Exception as e:
        print(e)
    else:
    	return proxyurl


def get_proxy(logger=None):
    """
    直接返回代理云
    :param logger:
    :return:
    """
    try:
        proxyusernm = "cabbagesmile"  # 代理帐号
        proxypasswd = "fxt168"  # 代理密码
        proxyaddr = 'http://cabbagesmile.v4.dailiyun.com/query.txt?key=NP6301C7B1&word=&count=1&rand=true&detail=false'
        res = requests.get(proxyaddr, timeout=15)
        proxy_str = res.text.replace('\r\n', '')
        proxyurl = "http://" + proxyusernm + ":" + proxypasswd + "@" + proxy_str
    except Exception as e:
        print(e)
    else:
        return proxyurl






if __name__ == '__main__':

    proxy = get_proxy_redis()
    print(proxy)
