from urllib import request
import time
import re
import random
import pymysql

class MaoyanSpider(object):
    def __init__(self):
        self.url = 'https://maoyan.com/board/4?offset={}'
        self.headers = {
            'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'
        }
        # 添加计数变量
        self.page = 1
        # 创建2个对象(mysql)
        self.db = pymysql.connect(
            'localhost','root','123456','maoyandb',
            charset='utf8'
        )
        self.cursor = self.db.cursor()


    def get_page(self,url):
        req = request.Request(
            url,
            headers=self.headers
        )
        res = request.urlopen(req)
        html = res.read().decode('utf-8')
        # 直接调用解析函数
        self.parse_page(html)

    def parse_page(self,html):
        pattren = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?star">(.*?)</p>.*?releasetime">(.*?)</p>',re.S)
        film_list = pattren.findall(html)
        # film_list: [('霸王别姬','张国荣','1993'),(),()]
        self.write_mysql(film_list)


    def write_mysql(self,film_list):
        ins = 'insert into filmset values(%s,%s,%s)'
        data_list = []
        for film in film_list:
            L = [
                film[0].strip(),
                film[1].strip(),
                film[2].strip()[5:15]
            ]
            data_list.append(L)
        # 执行数据库插入语句
        # data_list: [[],[],[],[]]
        self.cursor.executemany(ins,data_list)
        self.db.commit()


    def main(self):
        for offset in range(0,31,10):
            url = self.url.format(str(offset))

            self.get_page(url)
            print('第%d页完成' % self.page)
            self.page += 1
            time.sleep(random.randint(1,3))
        # 等所有页的数据爬完后再关闭
        self.cursor.close()
        self.db.close()

if __name__ == '__main__':
    spider = MaoyanSpider()
    spider.main()















