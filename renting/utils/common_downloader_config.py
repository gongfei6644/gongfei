import requests
import random
import time
from requests.exceptions import ProxyError
from setting import config
from utils.constants import RETRY_TIMES_MAP



def get_by_abucloud(source,self_logger,url, headers=None, encoding="utf-8"):
    '''
    :param url: 爬取的url ，为空则默认类中的url
    :param headers: 请求头，为空则默认类中的 headers
    :param encoding: 页面编码，默认utf-8
    :return: content 有3种状态: 正常网页数据的str / "404" / "retry"
    '''
    self_logger.info("进入下载:{}".format(url))
    self_headers = {'User-Agent': random.choice(config.AGENT_LIST)}
    self_proxy = config.ABY_URI
    if headers:
        self_headers.update(headers)
    content = ""
    for i in range(300):
        try:
            response = requests.get(url, headers=self_headers, proxies={
                "http": self_proxy, "https": self_proxy}, timeout=30, verify=False)
            self_logger.info("第{}次重试,code:{}".format(i, response.status_code))
            self_logger.info("\n访问链接 {}\n返回链接 {}".format(url, response.url))
            if response.status_code == 200 and "verify" not in response.url:
                content = response.content.decode(encoding, "ignore")
                break
            elif response.status_code == 404 or "/404." in response.url:
                content = "404"
                break
            else:
                content = "retry"
                # self_logger.info("{}进入retry, code:{}".format(url, response.status_code))
        except ProxyError as e:
            # 未获取到隧道资源,返回重试标识
            content = "retry"
            self_logger.info("第{}次重试,代理异常: {}".format(i, e))
        except Exception as ex:
            content = "retry"
            self_logger.error("第{}次重试,出现异常,错误信息：{}".format(i, ex))
    else:
        self_logger.info("连续{}次请求失败{}".format(RETRY_TIMES_MAP[source], url))
    time.sleep(0.5)
    return content