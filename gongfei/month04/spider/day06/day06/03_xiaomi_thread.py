import requests
import json
from threading import Thread
from queue import Queue
import time

class XiaomiSpider(object):
    def __init__(self):
        self.url = 'http://app.mi.com/categotyAllListApi?page={}&categoryId=2&pageSize=30'
        self.headers = {'User-Agent':'Mozilla/5.0'}
        # 创建队列
        self.q = Queue()
        self.i = 0

    # URL入队列
    def url_in(self):
        for page in range(67):
            url = self.url.format(str(page))
            # 入队列
            self.q.put(url)

    # 线程事件函数:获取队列中URL,发请求解析处理数据
    def get_data(self):
        while True:
            # 获取URL
            if not self.q.empty():
                url = self.q.get()
                html = requests.get(
                    url,
                    headers=self.headers
                ).text
                html = json.loads(html)
                # html: 字典
                for app in html['data']:
                    # 应用名称
                    app_name = app['displayName']
                    # 应用链接
                    app_link = 'http://app.mi.com/details?id=' + app['packageName']
                    d = {
                        '应用名称':app_name,
                        '应用链接':app_link
                    }
                    print(d)
                    self.i += 1
            else:
                break

    def main(self):
        # 入队列
        self.url_in()
        # 空列表
        t_list = []
        # 创建多个线程并启动线程
        for i in range(10):
            t = Thread(target=self.get_data)
            t_list.append(t)
            t.start()
        # 回收线程
        for i in t_list:
            i.join()
        print(self.i)

if __name__ == '__main__':
    start = time.time()
    spider = XiaomiSpider()
    spider.main()
    end = time.time()
    print('执行时间:%.2f' % (end-start))











